from django.urls import path, include
from . import views as item_views

urlpatterns = [
    path('items', item_views.items),
    path("item", item_views.add),
    path('summary', item_views.summary)
]