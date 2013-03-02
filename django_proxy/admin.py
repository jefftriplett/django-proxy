from django.contrib import admin

from .models import Proxy


class ProxyAdmin(admin.ModelAdmin):
    """Represents proxy model in the admin."""
    search_fields = ('title',)
    list_filter = ('content_type',)
    list_display = ('title', 'object_id', 'description', 'tags', 'content_type',)


admin.site.register(Proxy, ProxyAdmin)
