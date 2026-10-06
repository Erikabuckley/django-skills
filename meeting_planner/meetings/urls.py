from django.urls import path

from meetings import views

#urls for the meetings page
urlpatterns = [
    path('<int:id>', views.detail, name='detail'),
    path('rooms', views.rooms_list, name='rooms') 
]