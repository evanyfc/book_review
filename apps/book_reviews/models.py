# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_and_reg.models import User
from django.db import models

# Create your models here.
class ReviewManager(models.Manager):
    def createBookandReview(self, form_data, user_id):
        errors = []
        title = form_data['title'].title()
        preset = form_data['preset']
        author = form_data['author'].title()
        review = form_data['review']
        rating = form_data['rating']
        if not title or title.isspace():
            errors.append("Please enter the book title!")
        elif Book.objects.filter(title__iexact=title).exists():
            errors.append("Book already exists!")
        if(not preset and not author) or (preset and author):
            errors.append("Please enter a new author or choose from the list!")
        elif author:
            if Author.objects.filter(name__iexact=author).exists():
                errors.append("This author already exists, please choose from the list!")
            else:
                curr_author = author
        else:
            curr_author = preset
        if not review or review.isspace():
            errors.append("Please enter the book review!")
        if not rating:
            errors.append("Please input rating from 1 to 5!")

        if errors:
            return (False, errors)

        user = User.objects.get(id=user_id)
        book_author = Author.objects.create(name = curr_author)
        book = Book.objects.create(title = title, author = book_author)
        new_review = self.create(content = review, user = user, book = book, rating = rating)
        return (True, book.id)

    def createReview(self, form_data, book_id, user_id):
        errors = []
        review = form_data['review']
        rating = form_data['rating']
        if not review or review.isspace():
            errors.append("Please enter the book review!")
        if not rating:
            errors.append("Please input rating from 1 to 5!")
        if errors:
            return (False, errors)

        user = User.objects.get(id = user_id)
        book = Book.objects.get(id = book_id)
        new_review = self.create(content = review, user = user, book = book, rating = rating)
        return (True, book.id)

    def deleteReview(self, review_id):
        errors = []
        review = self.get(id = review_id)
        book_id = review.book.id
        review.delete()
        return (True, book_id)

class Author(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=55)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()
