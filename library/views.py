from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Book, BorrowBook
from django.utils import timezone
from datetime import timedelta
from datetime import date
from django.contrib import messages
from django.db.models import Sum
# ✅ Show All Books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})
from django.db.models import Q
from .models import Book

def book_list(request):
    query = request.GET.get('q')
    status = request.GET.get('status')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) 
            
        )

    if status == 'available':
        books = books.filter(available_copies__gt=0)
    elif status == 'unavailable':
        books = books.filter(available_copies=0)

    return render(request, 'library/book_list.html', {'books': books})

#index
def home(request):
    return render(request,'library/home.html',)


# ✅ Borrow Book (only if copies are available)
@login_required
def borrow_book(request, pk):
    # Retrieve the book to be borrowed
    book = get_object_or_404(Book, pk=pk)

    # Check if the user has already borrowed this book and hasn't returned it
    existing_borrow = BorrowBook.objects.filter(user=request.user, book=book, is_returned=False).exists()

    if existing_borrow:
        # If the user already borrowed this book and hasn't returned it, show an error message
        messages.error(request, "You can't borrow the same book until you return the first one!")
        return redirect('borrowed_books')  # Redirect to the borrowed books page

    # Proceed with borrowing the book if it's available
    if book.available_copies > 0:
        if request.method == 'POST':
            # Set the borrow date to today's date
            borrow_date = timezone.now().date()

            # Set the return date to one week later
            return_date = borrow_date + timedelta(weeks=1)

            # Create the BorrowBook instance with the calculated dates
            BorrowBook.objects.create(
                user=request.user,
                book=book,
                borrow_date=borrow_date,
                return_date=return_date
            )

            # Update the book's available copies
            book.available_copies -= 1
            book.save()

            # Success message
            messages.success(request, f"You have successfully borrowed the book '{book.title}'. The return date is {return_date}.")

            # Info message (reminder to return the book)
            messages.info(request, "Please make sure to return the book on time.")

            # Redirect to a view that lists the borrowed books
            return redirect('borrowed_books')

        # If the request method is GET, calculate the dates and pass them to the template
        else:
            borrow_date = timezone.now().date()
            return_date = borrow_date + timedelta(weeks=1)

            return render(request, 'library/borrow_book.html', {
                'book': book,
                'borrow_date': borrow_date,
                'return_date': return_date
            })

    else:
        # If no copies are available, render the no copies available template
        messages.warning(request, f"The book '{book.title}' is currently out of stock.")
        return render(request, 'library/no_copies_available.html', {'book': book})

# # ✅ Show Borrowed Books for Logged-in User
def borrowed_books(request, user_id=None):
    # If user_id is provided, it means it's the admin viewing another user's borrowed books
    if user_id:
        # Fetch the user whose borrowed books we want to show (admin view)
        viewing_user = get_object_or_404(User, id=user_id)
        borrowed_books = BorrowBook.objects.filter(user=viewing_user)
    else:
        # If no user_id is provided, it's the logged-in user viewing their own borrowed books
        viewing_user = request.user
        borrowed_books = BorrowBook.objects.filter(user=viewing_user)

    return render(request, 'library/borrowed_books.html', {
        'borrowed_books': borrowed_books,
        'viewing_user': viewing_user,  # Pass the viewing_user for template logic
    })


def user_borrowed_books(request, user_id):
    user = get_object_or_404(User, id=user_id)
    borrowed_books = BorrowBook.objects.filter(user=user)
    return render(request, 'library/user_borrowed_books.html', {
        'user': user,
        'borrowed_books': borrowed_books
    })


@login_required
def borrowed_books(request):
    # Get all borrowed books for the logged-in user
    user_borrowed = BorrowBook.objects.filter(user=request.user)

    return render(request, 'library/borrowed_books.html', {
        'borrowed_books': user_borrowed,
        'viewing_user': request.user,  # Pass this for template use
    })

# ✅ Return Book
@login_required
def return_book(request, pk):
    # Retrieve the borrow record for the logged-in user and the given book ID (pk)
    borrow_record = get_object_or_404(BorrowBook, pk=pk, user=request.user)

    # Check if the book hasn't already been returned
    if not borrow_record.is_returned:
        # Get today's date to mark it as the actual return date
        today = date.today()
        borrow_record.actual_return_date = today  # Save the actual return date
        borrow_record.is_returned = True  # Mark the book as returned
        borrow_record.save()  # Save changes to the borrow record

        # Update the available copies of the book
        book = borrow_record.book
        book.available_copies += 1  # Increase available copies since the book is returned
        book.save()  # Save the updated book record

        # ✅ Add success message
        messages.success(request, f"You have successfully returned the book: '{book.title}'.")

    # Redirect to the user's borrowed books page after the update
    return redirect('borrowed_books')

# ✅ Mixin to Restrict Access to Staff
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# ✅ Staff Can Add Book
class BookCreateView(StaffRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'published_date', 'total_copies']
    template_name = 'library/add_book.html'
    success_url = reverse_lazy('book_list')
    def form_valid(self, form):
        # Set available_copies equal to total_copies
        form.instance.available_copies = form.instance.total_copies
        return super().form_valid(form)


# ✅ Staff Can Edit Book
class BookUpdateView(StaffRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'published_date', 'available_copies']
    template_name = 'library/edit_book.html'
    success_url = reverse_lazy('book_list')


# ✅ Staff Can Delete Book
class BookDeleteView(StaffRequiredMixin, DeleteView):
    model = Book
    template_name = 'library/delete_book.html'
    success_url = reverse_lazy('book_list')

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.filter(is_staff=False).count()
    users_with_borrows = User.objects.filter(borrowbook__isnull=False).distinct()
    total_copies = Book.objects.aggregate(total=Sum('total_copies'))['total'] or 0
    available_copies = Book.objects.aggregate(total=Sum('available_copies'))['total'] or 0
    total_borrowed = BorrowBook.objects.filter(is_returned=False).count()

    context = {
        'total_users': total_users,
        'total_copies': total_copies,
        'available_copies': available_copies,
        'total_borrowed': total_borrowed,
        'users_with_borrows':users_with_borrows,
    }

    return render(request, 'library/admin_dashboard.html', context)