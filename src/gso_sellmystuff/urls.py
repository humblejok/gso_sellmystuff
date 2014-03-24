from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^accounts/', include('allauth.urls')),
    url(r'^index.html$', 'sellmystuff.views.index', name='index.html'),
    url(r'^account_view.html$', 'sellmystuff.views.account_view', name='account_view.html'),
    url(r'^account_edition.html$', 'sellmystuff.views.account_edition', name='account_edition.html'),
    url(r'^account_management.html$', 'sellmystuff.views.account_management', name='account_management.html'),
    url(r'^advertisement_creation.html$', 'sellmystuff.views.advertisement_creation', name='advertisement_creation.html'),
    
    # url(r'^gso_sellmystuff/', include('gso_sellmystuff.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
