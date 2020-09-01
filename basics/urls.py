from django.urls import path
from rest_framework import routers
from .api import HistoryDataViewSet, UpdatedDataViewSet, DataViewSet
from . import views
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register('api/data', DataViewSet, 'HistoryData')
router.register('api/recentdata',DataViewSet, 'RecentData')
router.register('api/historydata', HistoryDataViewSet, 'HistoryData')
# router.register(('', views.index, name='index')
urlpatterns= [path('updatedData/', views.check_if_update_present),
path('data/<stock_name>/',csrf_exempt( views.check_recent_record.as_view())),
path('historicalData/<stock_name>/',csrf_exempt( views.check_historical_record.as_view())),
path('', views.index, name='index'),
# path('getRecentInfo', views.check_recent_record)
]

    

urlpatterns += router.urls