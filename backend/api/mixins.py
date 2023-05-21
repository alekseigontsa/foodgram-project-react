from rest_framework import mixins
from rest_framework import viewsets


class CreateDestroyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):

    pass
