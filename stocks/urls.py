from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('',              views.stocks_index,   name='index'),
    path('<str:symbol>/', views.stock_analysis, name='analysis'),
]
