from django.urls import path, include
from . import views as item_views

urlpatterns = [
    path('items/', item_views.items, name='items'),
    path('item/', item_views.add, name='add_item'),
    path('summary/', item_views.summary, name='summary'),
    path('item/<int:pk>/', item_views.update, name='update_item'),
    path('item/<int:pk>/', item_views.delete, name='delete_item'),
]