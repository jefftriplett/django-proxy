from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from .managers import ProxyManager


class ProxyBase(models.Model):
    """
    Represents the proxy objects. Retains the name, description, and any tags
    related to the associated object.

    A good use, I've found, for this type of object is aggregate view of all
    content types in an RSS feed (post, links, tweets, etc.).

    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    #denormalized fields
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now)

    #audit fields
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_on = timezone.now()
        super(ProxyBase, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Proxy(ProxyBase):
    """The default proxy model."""

    objects = ProxyManager()

    class Meta:
        verbose_name = 'proxy'
        verbose_name_plural = 'proxies'

    def __str__(self):
        return self.title
