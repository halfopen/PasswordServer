from django.conf.urls import patterns, include, url
from Password.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Password.views.index', name='home'),
    # url(r'^Server/', include('Server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'get/', get_password),

    url(r'save/', save_password),

    url(r'query_website/', query_website),
)
