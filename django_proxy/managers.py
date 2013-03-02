from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils import timezone


class ProxyQuerySet(QuerySet):

    def private(self):
        return self.exclude(pub_date__isnull=True)

    def published(self):
        return self.filter(pub_date__lte=timezone.now())


class ProxyManager(Manager):
    """Retrieve all published objects."""

    def get_query_set(self):
        return ProxyQuerySet(self.model, using=self._db)

    def private(self):
        return self.get_query_set().private()

    def published(self):
        return self.get_query_set().published()
