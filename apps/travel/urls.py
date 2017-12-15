from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_user', views.register_user),
    url(r'^login_user', views.login_user),
    url(r'^logout', views.logout),
    url(r'^travels/add$', views.add),
    url(r'^add_trip', views.add_trip),
    url(r'^travels$', views.travels),
]
