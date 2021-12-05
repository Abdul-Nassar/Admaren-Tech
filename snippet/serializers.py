from rest_framework import serializers, fields
from rest_framework.reverse import reverse
from rest_framework.serializers import (
    ModelSerializer
)
from .models import *

class SnippetSerializer(ModelSerializer):
    '''
        Serializer to get Snippet details of snippet & also user to create new snippet
    '''
    tag_title = serializers.CharField(source='tag.title', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.first_name', read_only=True)
    detail_url = serializers.SerializerMethodField(read_only=True)

    def get_detail_url(self, instance):
        url = self.context['request'].build_absolute_uri() + str(instance.id)
        return url
    
    class Meta:
        model = Snippet
        fields = '__all__'
    

class SnippetDetailSerializer(ModelSerializer):
    '''
        Serializer to get details of a Snippet
    '''
    tag_title = serializers.CharField(source='tag.title', read_only=True)

    class Meta:
        model = Snippet
        fields = ['title', 'tag_title', 'created_on', 'updated_on']


class TagSerializer(ModelSerializer):
    '''
        Serializer to get details of a tag
    '''

    class Meta:
        model = Tag
        fields = '__all__'
