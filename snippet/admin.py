# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('title',)

admin.site.register(Tag, TagAdmin)

class SnippetAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'tag', 'created_on', 'updated_on', 'created_by'
    )
    search_fields = ('title', 'tag__title')
    list_filter = ('tag__title', 'created_by')

admin.site.register(Snippet, SnippetAdmin)
