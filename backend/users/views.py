from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.paginations import AvailablePagination
from recipes.models import Subscribe
from .models import User
from api.serializers import SubscribeSerializer
from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):
    """Позволяет просматривать собственные данные пользователя."""
    pagination_class = AvailablePagination

    @action(['get'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(
        detail=False,
        url_path='subscriptions',
        methods=['GET'],
        permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        cur_page = self.paginate_queryset(queryset)
        if queryset.exists():
            serializer = SubscribeSerializer(
                cur_page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response(
            'errors: Нет подписок.', status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=True,
        url_path='subscribe',
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if Subscribe.objects.filter(user=user,
                                        author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя!'},
                    status=status.HTTP_400_BAD_REQUEST)
            if user == author:
                return Response(
                    {'errors': 'Подписка на самого себя невозможна.'},
                    status=status.HTTP_400_BAD_REQUEST)
            author = Subscribe.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(
                author, context={'request': request})
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED) 
        if not Subscribe.objects.filter(user=user,
                                        author=author).exists():
            return Response({'errors': 'Вы не подписаны!'},
                            status=status.HTTP_404_NOT_FOUND)
        Subscribe.objects.get(user=user,
                              author=author).delete()
        return Response('Вы отписались от автора',
                        status=status.HTTP_204_NO_CONTENT)
