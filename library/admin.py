# from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from django.contrib.auth.models import User
# from django.urls import reverse
# from django.utils.html import format_html
# from .models import User as CustomUser  # Your custom User model

# # Unregister the default User admin
# admin.site.unregister(User)

# # Now register the custom UserAdmin for your User model
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'borrowed_books_link')  # Add a link for borrowed books

#     def borrowed_books_link(self, obj):
#         url = reverse('view_borrowed_books', args=[obj.id])
#         return format_html('<a href="{}">View Borrowed Books</a>', url)

#     borrowed_books_link.short_description = 'Borrowed Books'

# # Register your custom User model with the custom admin
# admin.site.register(CustomUser, UserAdmin)
