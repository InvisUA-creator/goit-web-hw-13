from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from django.contrib import messages
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import threading
from .scrapping import QuotesSpider

from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag

is_spider_running = False


def main(request, page=1):
    quotes = Quote.objects.all()
    top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by("-num_quotes")[
        :10
    ]
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "quotes/index.html",
        context={"quotes": quotes_on_page, "top_tags": top_tags},
    )


def author_detail(request, author_id):
    author = get_object_or_404(Author, fullname=author_id)
    return render(request, "quotes/author_detail.html", {"author": author})


@login_required
def author_add(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="/")
        else:
            return render(request, "quotes/author_add.html", {"form": form})
    return render(request, "quotes/author_add.html", {"form": AuthorForm()})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="/")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def quotes_by_tag(request, tag_name, page=1):
    top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by("-num_quotes")[
        :10
    ]
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag)
    per_page = 5
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "quotes/quotes_by_tag.html",
        {"quotes": quotes_on_page, "tag": tag, "top_tags": top_tags},
    )


def run_spider(request):
    global is_spider_running
    is_spider_running = True

    def start_crawler():
        process = CrawlerProcess(get_project_settings())
        process.crawl(QuotesSpider)
        process.start()
        global is_spider_running
        is_spider_running = False

    thread = threading.Thread(target=start_crawler)
    thread.start()
    messages.success(request, "Scrapy spider started successfully.")
    return redirect(to="/")


def check_spider_status(request):
    global is_spider_running
    return JsonResponse({"is_spider_running": is_spider_running})


def home(request):
    global is_spider_running
    return render(request, "quotes/base.html", {"is_spider_running": is_spider_running})
