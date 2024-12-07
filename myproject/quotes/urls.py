from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("add-author/", views.author_add, name="author_add"),
    path("add-quote/", views.add_quote, name="add_quote"),
    path('tag/<str:tag_name>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('tag/<str:tag_name>/<int:page>/', views.quotes_by_tag, name='quotes_by_tag'),
    path("quotes/<author_id>/", views.author_detail, name="author_detail"),
    path("run_spider/", views.run_spider, name="run_spider"),
    path("check_spider_status/", views.check_spider_status, name="check_spider_status")
]