from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

POPULAR = [
    {'symbol':'AAPL','name':'Apple','flag':'🇺🇸'},
    {'symbol':'NVDA','name':'NVIDIA','flag':'🇺🇸'},
    {'symbol':'TSLA','name':'Tesla','flag':'🇺🇸'},
    {'symbol':'005930.KS','name':'삼성전자','flag':'🇰🇷'},
    {'symbol':'BTC-USD','name':'Bitcoin','flag':'₿'},
]

def index(request):
    return render(request, 'index.html', {'popular_stocks': POPULAR})

def handler404(request, exception):
    return render(request, '404.html', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('stocks/', include('stocks.urls')),
    path('boards/', include('boards.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handler404
