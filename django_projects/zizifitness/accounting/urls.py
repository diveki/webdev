from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.index, name='accounting'), 
    path('categorytype/create/', views.CategoryTypeCreate.as_view(), name='categorytype_create'), 
    path('categorytype/list/', views.CategoryTypeListView.as_view(), name='categorytype_list'),
    path('categorytype/<int:pk>/update', views.CategoryTypeUpdate.as_view(), name='categorytype_update'),
    path('categorytype/<int:pk>/delete/', views.CategoryTypeDelete.as_view(), name='categorytype_delete'),

    
]
