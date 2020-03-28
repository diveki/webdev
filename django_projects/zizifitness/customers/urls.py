from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.CustomersAllListView.as_view(), name='customers-list'),
    path('<slug:slug>/add_input/', views.physical_appearance_updateview, name='input-measurements'),
    # path('<slug:slug>/', views.PersonDetailView.as_view(), name='person-detail'),
    path('<slug:slug>/', views.person_detail_view, name='person-detail'),
    # path('<slug:slug>/graph', views.PersonDetailView.as_view(), name='person-detail-graph'),
    
]


