from django.urls import path

from . import views

urlpatterns = [
    path('recurso_list/', views.recurso_list, name='recurso_list'),
    path('recurso_get/<int:id>', views.recurso_get, name='recurso_get'),
    path('recurso_put/', views.recurso_put, name='recurso_put'),
    path('recurso_post/', views.recurso_post, name='recurso_post'),
    path('fase_byid/<int:id>', views.fase_byid, name='fase_byid'),
]
