
from django.urls import path, include 
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.register ,name='signup'),
    path('login/', views.register ,name='login'),
    path('logout/', views.logout_user ,name='logout'),
    
]
htmx_urlpatterns = [
    path('add-review/', views.add_review, name='add_review'),
    ]

urlpatterns += htmx_urlpatterns