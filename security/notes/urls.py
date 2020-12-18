from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:note_id>/', views.note, name='note'),
  path('add/', views.add, name='add'),
  path('user/<int:user_id>/account/', views.user, name='user_info'),
  path('search/', views.search, name='search'),
  path('logout/', views.logout_view, name='logout')
]