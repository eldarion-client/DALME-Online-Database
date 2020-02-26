from django.urls import path

from . import views

app_name = 'dalme_public'
urlpatterns = [
    path('sources/', views.SourceList.as_view(), name='source_list'),
    path('sources/<uuid:pk>/', views.SourceDetail.as_view(), name='source_detail'),
]
