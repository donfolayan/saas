from django.urls import path
from . import views

urlpatterns = [
    path('<username>/', views.profile_detail_view),
    path('', views.profile_list_view),
]