from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.RoomCreateUpdateDestroyViewSet.as_view({'post': 'create'}), name='room-create'),
    path('update/<pk>/', views.RoomCreateUpdateDestroyViewSet.as_view({'put': 'update'}), name='room-update'),
    path('delete/<pk>/', views.RoomCreateUpdateDestroyViewSet.as_view({'delete': 'destroy'}), name='room-delete'),

    path('list/', views.RoomOnlyReadViewSet.as_view({'get': 'list'}), name='room-list'),
    path('retrieve/<pk>', views.RoomOnlyReadViewSet.as_view({'get': 'retrieve'}), name='retrieve-room'),
]