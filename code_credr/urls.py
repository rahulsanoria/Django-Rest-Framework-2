from django.conf.urls import url
from code_credr import views
# from django.contrib.auth import views as auth_views

# from code_credr.core import views as core_views

urlpatterns = [

    url(r'^invoices/$', views.InvoiceList.as_view()),
    url(r'^invoices/(?P<pk>[0-9]+)/$', views.InvoiceDetail.as_view()),
]