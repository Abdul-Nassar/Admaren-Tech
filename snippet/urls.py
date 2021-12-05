'''
	URLs against Snippets
'''
from django.urls import (path, include)
from .views import *

urlpatterns = [
	path('snippet/', SnippetListCreateView.as_view(), name='snippet'),
	path('snippet/<int:pk>',
		SnippetRetrieveUpdateDestroyView.as_view(), name='snippet'),
	path('snippet-delete/',
		SnippetDeleteView.as_view(), name='snippet-delete'),
	path('tags/', TagListView.as_view(), name='tags'),
	path('tag-detail/', TagDetailView.as_view(), name='tag_-detail')
]