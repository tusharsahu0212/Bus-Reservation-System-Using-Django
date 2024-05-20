from django.urls import path
from bus import views
from home import views as home_views
urlpatterns = [
    path('find', views.find, name='find'),
    path('book', views.book, name='book'),
    path('myBookings', views.myBookings, name='myBookings'),
    path('cancel', views.cancel, name='cancel'),
    path('logout', home_views.logout, name='logout')
]