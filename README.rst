django-proxy
============

.. image:: jefftriplett/django-proxy.png?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/pydanny/staticserve


Introduction
------------

A reusable Django application to create a proxy object for your models.
Intended to aggregate various content types into a model for reuse.

What django-proxy provides is an aggregation of different content types by
denormalizing fields on various models into one database table (using signals
to update/delete changes to those denormalized fields). This concept was
initially used on my old blog (howiworkdaily.com) and a hacked version in the
TWiD (thisweekindjango) "everything" feed. I like to say this is a poor man's
`django-tumbleweed <http://github.com/mcroydon/django-tumbleweed>`_, which
defines itself as "A framework for creating tumblelog views of Django models
indexed by Haystack" to provide similar functionality. What I like about
django-proxy is that the denormalized data is available in the database and
the relationship to the source object is available via Generic Relation,
if needed.

Current implementation example:

::

        from django.db import models
        from django.db.models import signals
        from django_proxy.signals import proxy_save, proxy_delete
        ...

        class Post(models.Model):
            STATUS_CHOICES = (
                (1, _('Draft')),
                (2, _('Public')),
            )

            title = models.CharField(max_length=150)
            body = models.TextField()
            tag_data = TagField()
            status = models.IntegerField(_('status'), choices=STATUS_CHOICES,
                                        default=2)

            class ProxyMeta:
                title = 'title'
                description = 'body'
                tags = 'tag_data'
                active = {'status': 2}


        signals.post_save.connect(proxy_save, Post, True)
        signals.post_delete.connect(proxy_delete, Post)


Dependencies
------------

Nothing external. No contrib apps. Just Django proper.


TODO
----

-  Decouple further via signals possibly, removing ProxyMeta from the
   design


Examples
~~~~~~~~

To see this project in use, take a peek at
`Django-Mingus <http://github.com/montylounge/django-mingus>`__ and how
combined with django-basic-apps it leverages the solution.
