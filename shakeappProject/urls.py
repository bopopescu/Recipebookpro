from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import settings

urlpatterns = patterns('shakeapp.views',
    # Examples:
    # url(r'^$', 'shakeappProject.views.home', name='home'),
    # url(r'^shakeappProject/', include('shakeappProject.foo.urls')),
    url(r'shakeapp/$', 'index'),
    url(r'shakeapp/(?P<recipe_id>\d+)/','detail'),
    url(r'shakeapp/random/', 'random'),
    url(r'shakeapp/like/', 'like'),
    url(r'shakeapp/add/', 'add'),
    url(r'shakeapp/delete/$', 'delete'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    url(r'^$', 'django.contrib.auth.views.login' ),
    url(r'shakeapp/logout', 'django.contrib.auth.views.logout'),
)