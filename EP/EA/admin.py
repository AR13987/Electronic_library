from django.contrib import admin
# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language, Edition, Publisher

class BookInline(admin.TabularInline):
    model = Book
    extra = 0
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Edition)
admin.site.register(Publisher)

class EditionInline(admin.TabularInline):
    model = Edition
    extra = 1

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    inlines = [EditionInline]

    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'title_type') and obj.title_type == 'textbook':
            # Убеждаемся, что у учебника только одно переиздание
            if obj.editions.count() > 1:
                raise ValueError("Учебник может иметь только одно переиздание.")
        super().save_model(request, obj, form, change)

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )