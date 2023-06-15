from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import RetrieveAPIView

from .models import Hall
from .serializers import HallDetailSerializer, HallListSerializer, HallPriceSerializer


class HallViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = Hall.objects.all()
    lookup_field = 'name'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HallDetailSerializer
        if self.action == 'list':
            return HallListSerializer
        return HallDetailSerializer
    

class HallPriceAPIView(RetrieveAPIView):
    queryset = Hall.objects.all()
    serializer_class = HallPriceSerializer
    lookup_field = 'name'