
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
urlpatterns = [
    path('', include('basics.urls')),
    path('admin/', admin.site.urls),
    # url('api/', include('basics.urls'))
]
