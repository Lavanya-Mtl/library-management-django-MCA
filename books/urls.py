from django.urls import path

from .views import *
app_name='books'
urlpatterns = [
    path("", books_home,name='index'),
    path("add",add_book, name="add_book"),
    path('edit/<int:id>',edit_book,name="edit_book"),
    path('delete/<int:id>',delete_book,name="delete_book"),
    path('view/<int:id>',view_book,name="view_book"),
    path('booktomember/<int:id>',booktomember,name="book_to_member")
]

