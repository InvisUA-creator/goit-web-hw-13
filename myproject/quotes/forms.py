from django.forms import (
    ModelForm,
    CharField,
    TextInput,
    Select,
    Textarea,
    CheckboxSelectMultiple,
    ModelMultipleChoiceField,
)
from .models import Author, Quote, Tag


class AuthorForm(ModelForm):
    fullname = CharField(max_length=50, required=True, widget=TextInput())
    born_date = CharField(max_length=50, widget=TextInput())
    born_location = CharField(max_length=150, widget=TextInput())
    description = Textarea(attrs={"class": "form-control", "style": "width: 100%;"})

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ["name"]


class QuoteForm(ModelForm):
    existing_tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,
        label="Existing Tags",
    )
    new_tags = CharField(
        required=False,
        label="New Tags (comma-separated)",
        widget=TextInput(attrs={"placeholder": "e.g., motivation, life, wisdom"}),
    )

    class Meta:
        model = Quote
        fields = ["quote", "author"]
        widgets = {
            "quote": Textarea(attrs={"class": "form-control", "style": "width: 100%;"}),
            "author": Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].queryset = Author.objects.all()
        self.fields["author"].label_from_instance = lambda obj: obj.fullname

    def save(self, commit=True):
        quote = super().save(commit=False)
        if commit:
            quote.save()
        existing_tags = self.cleaned_data["existing_tags"]
        for tag in existing_tags:
            quote.tags.add(tag)
        new_tags = self.cleaned_data["new_tags"]
        if new_tags:
            new_tags_list = [tag.strip() for tag in new_tags.split(",") if tag.strip()]
            for tag_name in new_tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                quote.tags.add(tag)
        return quote
