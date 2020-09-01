from basics.models import All_Records_Table, Recently_Updated_Records, Historical_stock_prices
from rest_framework import viewsets, permissions
from .serializers import HistoryDataSerializer, UpdatedDataSerializer, DataSerializer

class HistoryDataViewSet(viewsets.ModelViewSet):
    queryset = Historical_stock_prices.objects.all()
    permissions_classes =[
            permissions.AllowAny
        ]
    serializer_class = HistoryDataSerializer

class UpdatedDataViewSet(viewsets.ModelViewSet):
    queryset = Recently_Updated_Records.objects.all()
    permissions_classes =[
            permissions.AllowAny
        ]
    serializer_class = DataSerializer

class DataViewSet(viewsets.ModelViewSet):
    queryset = All_Records_Table.objects.all()
    permissions_classes =[
            permissions.AllowAny
        ]
    serializer_class = DataSerializer