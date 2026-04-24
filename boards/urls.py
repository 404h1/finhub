from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('',                                  views.board_home,  name='home'),
    path('<str:asset_id>/',                   views.board_list,  name='list'),
    path('<str:asset_id>/create/',            views.post_create, name='create'),
    path('<str:asset_id>/<int:pk>/',          views.post_detail, name='detail'),
    path('<str:asset_id>/<int:pk>/edit/',     views.post_edit,   name='edit'),
    path('<str:asset_id>/<int:pk>/delete/',   views.post_delete, name='delete'),
]
