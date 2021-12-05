# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import (
    login as auth_login,
    authenticate
)
from rest_framework.generics import(
    ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *

def get_tokens_for_user(user):
    '''
        Function to get JWT tokens (access & refresh).
    '''
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

class LoginView(ObtainAuthToken):
    '''
        View for login a user, returns JWT tokens (access & refresh), username and id of the user if login is success
    '''

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user:
            data = {
                "non_field_errors": [
                "Unable to log in with provided credentials."
            ]}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        tokens = get_tokens_for_user(user)
        auth_login(request, user)
        data = {
            'username': user.username,
            'user_id': user.id
        }
        response_data = {
            'status': 'success',
            'tokens': tokens,
            'data': data
        }
        return Response(response_data)


class SnippetListCreateView(ListCreateAPIView):
    '''
        View to create & list snippets
    '''
    permission_classes = (IsAuthenticated,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_data = {
            'status': 'success',
            'total_snippets': queryset.count(), # Finds total number of snippets added
            'snippets': SnippetSerializer(queryset, many=True,
                context={'request': request}).data
        }
        return Response(response_data)

    def create(self, request, *args, **kwargs):
        snippet_data = request.data.copy()
        tag_title = snippet_data.pop('tag_title')
        # Returns snippet object as new one if tag with given title not exists otherwise returns existing one
        tag_obj, created = Tag.objects.update_or_create(title=tag_title)
        snippet_data['tag'] = tag_obj.id
        snippet_data['created_by'] = request.user.id
        serializer = self.get_serializer(data=snippet_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED,
            data={"status": "success", "id": serializer.instance.id}
        )


class SnippetRetrieveUpdateDestroyView(RetrieveUpdateAPIView):
    '''
        View to get Snippet details against a snippet id
    '''
    permission_classes = (IsAuthenticated,)
    queryset = Snippet.objects.all()
    serializer_class = SnippetDetailSerializer


class SnippetDeleteView(APIView):
    '''
        View to delete snippets of given array of ids
    '''
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        Snippet.objects.filter(
            pk__in=request.data['delete_snippets']).delete()
        queryset = Snippet.objects.all()
        return Response(SnippetSerializer(queryset, many=True).data)


class TagListView(ListAPIView):
    '''
        View to list Tag detials
    '''
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailView(APIView):
    '''
        View to get Snippets under a Tag
    '''
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        tag_id = request.query_params['tag_id']
        queryset = Snippet.objects.filter(tag__id=tag_id)
        return Response(SnippetSerializer(queryset, many=True).data)
