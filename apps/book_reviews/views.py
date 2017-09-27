# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import Author, Book, Review
from ..login_and_reg.views import print_errors
from ..login_and_reg.models import User
# Create your views here.

def check_session(request):
    return 'user' in request.session

def index(request):
    if not check_session(request):
        return redirect(reverse('users:index'))
    id = request.session['user']['id']
    reviews = Review.objects.order_by('-id')[:3]
    book_id = []
    for review in reviews:
        book_id.append(review.book.id)
    books = Book.objects.exclude(id__in=book_id).order_by('-id')
    context = {
        'reviews': reviews,
        'books': books,
    }
    return render(request, 'book_reviews/index.html', context)

def add(request):
    if not check_session(request):
        return redirect(reverse('users:index'))
    authors = Author.objects.order_by('name')
    return render(request, 'book_reviews/new.html', {'authors': authors})

def create(request):
    if not check_session(request):
        return redirect(reverse('users:index'))
    id = request.session['user']['id']
    result = Review.objects.createBookandReview(request.POST, id)
    if result[0]:
        book_id = result[1]
        return redirect(reverse('books:show_book', kwargs={'book_id' : book_id}))
    print_errors(request, result[1])
    return redirect('books:add')


def show_book(request, book_id):
    if not check_session(request):
        return redirect(reverse('users:index'))
    book = Book.objects.get(id = book_id)
    reviews = Review.objects.filter(book = book).order_by('-id')
    context = {
        'book': book,
        'reviews': reviews,
    }
    return render(request, 'book_reviews/show.html', context)

def add_review(request, book_id):
    if not check_session(request):
        return redirect(reverse('users:index'))
    id = request.session['user']['id']
    result = Review.objects.createReview(request.POST, book_id, id)
    if result[0]:
        book_id = result[1]
        return redirect(reverse('books:show_book', kwargs={'book_id' : book_id}))
    print_errors(request, result[1])
    return redirect('books:show')

def delete_review(request, review_id):
    if not check_session(request):
        return redirect(reverse('users:index'))

    result = Review.objects.deleteReview(review_id)
    if result[0]:
        book_id = result[1]
        return redirect(reverse('books:show_book', kwargs={'book_id' : book_id}))
    print_errors(request, result[1])
    return redirect(reverse('books:show_book'))

def show_user(request, user_id):
    if not check_session(request):
        return redirect(reverse('users:index'))

    user = User.objects.get(id = user_id)
    reviews = Review.objects.filter(user = user)
    count = len(reviews)
    context = {
        'user': user,
        'reviews': reviews,
        'count': count,
    }
    return render(request, 'book_reviews/user.html', context)
