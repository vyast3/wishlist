from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^main$',views.index),
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    url(r'^wish_items/create/(?P<id>\d+)$',views.add_show),
    url(r'^show_dashboard$',views.show_dashboard),
    url(r'^create_list$',views.create_list),
    url(r'^show_product/(?P<id>\d+)$',views.show_product),
    url(r'^add_list/(?P<id>\d+)$',views.add_list),
    url(r'^remove/(?P<id>\d+)/(?P<product_id>\d+)$',views.remove)

]

