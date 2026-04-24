from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',           views.login_view,     name='login'),
    path('logout/',          views.logout_view,    name='logout'),
    path('signup/',          views.signup_view,    name='signup'),
    path('',                 views.user_list,      name='user_list'),
    path('profile/',         views.profile,        name='profile'),
    path('profile/edit/',    views.profile_edit,   name='profile_edit'),
    path('password/',        views.password_change,name='password_change'),
    path('<str:username>/',  views.user_detail,    name='user_detail'),
]
