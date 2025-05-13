
from django.urls import path
from .views import *

urlpatterns = [
    path('',home),
    path('book_list', book_list, name='book_list'),
    path('add/', BookCreateView.as_view(), name='add_book'),
    path('edit/<int:pk>/', BookUpdateView.as_view(), name='edit_book'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='delete_book'),
    path('borrow/<int:pk>/', borrow_book, name='borrow_book'),
    path('borrowed/', borrowed_books, name='borrowed_books'),
    path('return/<int:pk>/', return_book, name='return_book'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user_borrowed_books/<int:user_id>/',user_borrowed_books, name='user_borrowed_books'),
    

]

