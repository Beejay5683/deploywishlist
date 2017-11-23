from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^dashboard$', views.dashboard),
  url(r'^iteminfo$', views.iteminfo),
  url(r'^add$', views.add),
  url(r'^remove$', views.remove),
  url(r'^delete$', views.delete),
  url(r'^additem$', views.additem),
  url(r'^create$', views.create),
  url(r'^logout$', views.logout),
 
]