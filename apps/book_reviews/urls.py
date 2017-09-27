from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add$', add, name='add'),
    url(r'^create$', create, name='create'),
    url(r'^reviews/add/(?P<book_id>\d+)$', add_review, name='add_review'),
    url(r'^reviews/delete/(?P<review_id>\d+)$', delete_review, name='delete_review'),
    url(r'^(?P<book_id>\d+)$', show_book, name='show_book'),
    url(r'^users/(?P<user_id>\d+)$', show_user, name='show_user'),
]
