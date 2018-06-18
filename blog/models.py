from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(_('Nazwa'), max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = _('Kategoria')
        verbose_name_plural = _('Kategorie')

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while self.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(_('Nazwa'), max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tagi')

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while self.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Szkic')),
        ('published', _('Opublikowano')),
    )

    title = models.CharField(_('Tytuł'), max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    categories = models.ManyToManyField(Category, 'posts', verbose_name=_('Kategorie'))
    tags = models.ManyToManyField(Tag, 'posts', verbose_name=_('Tago'))
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE, verbose_name=_('Autor'))
    body = RichTextField()
    publish = models.DateTimeField(_('Opublikowano'), default=timezone.now)
    created = models.DateTimeField(_('Utworzono'), auto_now_add=True)
    updated = models.DateTimeField(_('Zaktualizowano'), auto_now=True)
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name = _('Wpis')
        verbose_name_plural = _('Wpisy')
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
