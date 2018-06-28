from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^list_books$', views.list_books),    
    url(r'^new_book$', views.new_book),    
    url(r'^add_book$', views.add_book),    
    url(r'^view_book/(?P<id>\d+)$', views.view_book),    
    url(r'^view_user/(?P<id>\d+)$', views.view_user),  
    url(r'^add_review$', views.add_review),
    url(r'^delete_review/(?P<id>\d+)$', views.delete_review),  
    
]