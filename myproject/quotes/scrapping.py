import os
import django

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

from .models import Author, Quote, Tag

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()


class QuoteItem(Item):
    quote = Field()
    author = Field()
    tags = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class DataPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            author, created = Author.objects.get_or_create(
                fullname=adapter.get("fullname"),
                defaults={
                    "born_date": adapter.get("born_date", ""),
                    "born_location": adapter.get("born_location", ""),
                    "description": adapter.get("description", ""),
                },
            )
        elif "quote" in adapter.keys():
            author = Author.objects.get(fullname=adapter.get("author"))
            quote, created = Quote.objects.get_or_create(
                quote=adapter.get("quote"), author=author
            )
            tags = adapter.get("tags", [])
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)
        return item


class QuotesSpider(scrapy.Spider):
    name = "get_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {DataPipeline: 300}}

    def parse(self, response, **kwargs):

        for q in response.xpath("/html//div[@class='quote']"):
            quote = q.xpath("span[@class='text']/text()").get().strip()
            author = q.xpath("span/small[@class='author']/text()").get().strip()
            tags = q.xpath("div[@class='tags']/a/text()").extract()

            yield QuoteItem(quote=quote, author=author, tags=tags)
            yield response.follow(
                url=self.start_urls[0] + q.xpath("span/a/@href").get(),
                callback=self.parse_author,
            )

        next_link = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    @classmethod
    def parse_author(cls, response, **kwargs):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("h3[@class='author-title']/text()").get().strip()
        born_date = (
            content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        )
        born_location = (
            content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        )
        description = (
            content.xpath("div[@class='author-description']/text()").get().strip()
        )
        yield AuthorItem(
            fullname=fullname,
            born_date=born_date,
            born_location=born_location,
            description=description,
        )


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
