from django.urls import path
from . import views


urlpatterns = [
    path('my-reservations/', views.ReservationViewSet.as_view({'get': 'list'}), name='my-reservations'),
    path('create/', views.ReservationViewSet.as_view({'post': 'create'}), name='reservation-create'),
    path('<pk>', views.ReservationViewSet.as_view({'get': 'retrieve'}), name='reservation-retrieve'),
    path('update/<pk>', views.ReservationViewSet.as_view({'put': 'update'}), name='reservation-update'),
    path('delete/<pk>', views.ReservationViewSet.as_view({'delete': 'destroy'}), name='reservation-delete'),

    path('all-reservations/<pk>', views.RetrieveReservationListForRoomViewSet.as_view({'get': 'retrieve'}), name='all-reservations'),
]

