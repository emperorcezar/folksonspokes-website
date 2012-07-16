from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

# Patch the admin
from directupload.widgets import DirectUploadClearableFileInput
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
FORMFIELD_FOR_DBFIELD_DEFAULTS[models.FileField] = {'widget': DirectUploadClearableFileInput}

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^directupload/', include('directupload.urls')),
    url(r'^', include('cms.urls')),
)


urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns