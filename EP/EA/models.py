from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
import re
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=False, verbose_name='Фамилия')
    username = models.CharField(max_length=150, unique=True, blank=False, verbose_name='Логин')
    email = models.EmailField(unique=True, blank=False, verbose_name='Электронная почта')
    middle_name = models.CharField(max_length=150, blank=False, verbose_name='Отчество')
    password1 = models.CharField(max_length=128, blank=False, null=True, verbose_name='Пароль')
    password2 = models.CharField(max_length=128, blank=False, null=True, verbose_name='Повтор пароля')
    consent = models.BooleanField(default=False, verbose_name='Я соглашаюсь на обработку моих персональных данных')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='groups_set',  # Измените имя здесь
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Измените имя здесь
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def clean(self):
        super().clean()
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.last_name):
            raise ValidationError('Фамилия должна содержать только кириллические буквы, пробелы и дефисы.')
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.first_name):
            raise ValidationError('Имя должно содержать только кириллические буквы, пробелы и дефисы.')
        if self.middle_name and not re.match(r'^[А-Яа-яЁёs-]*$', self.middle_name):
            raise ValidationError('Отчество должно содержать только кириллические буквы, пробелы и дефисы.')
        if not self.consent:
            raise ValidationError('Необходимо согласие на обработку персональных данных.')


from django.db import models
from datetime import date
class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name



from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    biography = models.TextField(max_length=2000, help_text="Enter a brief biography of the author", blank=True)
    works = models.TextField(max_length=2000, help_text="List of works by the author", blank=True)
    notable_achievements = models.TextField(max_length=2000, help_text="Significant achievements of the author", blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
class Book(models.Model):
    TITLE_CHOICES = [
        ('fiction', 'Художественное произведение'),
        ('textbook', 'Учебник'),
    ]
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    publication_year = models.IntegerField(blank=True, null=True, help_text="Enter the year of publication (1000-9999)", validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    category = models.CharField(blank=True, null=True, max_length=100, help_text="Enter the category of the book")
    publisher = models.CharField(blank=True, null=True, max_length=100, help_text="Enter the publisher of the book")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, help_text="Upload the cover image of the book")
    text_file = models.FileField(upload_to='books/', blank=True, null=True, help_text="Upload the text file of the book")
    title_type = models.CharField(blank=True, null=True, max_length=20)

    class Meta:
        unique_together = (('title', 'author', 'publication_year', 'publisher'),)  # Уникальность по указанным полям

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class Edition(models.Model):
    book = models.ForeignKey(Book, related_name='editions', on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    year = models.IntegerField()

    class Meta:
        unique_together = ('book', 'publisher', 'year')

    def __str__(self):
        return f"{self.book.title} - {self.publisher.name} ({self.year})"


import uuid # Required for unique book instances
class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)


    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id,self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False