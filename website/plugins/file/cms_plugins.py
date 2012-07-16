from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from models import File
from django.conf import settings
from django import forms

from directupload.widgets import DirectUploadFileInput

class FileForm(forms.ModelForm):
    file = forms.FileField(widget = DirectUploadFileInput)
    class Meta:
        model = File



class FilePlugin(CMSPluginBase):
    model = File
    name = _("File")
    render_template = "cms/plugins/file.html"
    text_enabled = True

    class Media:
        js = ("directupload/js/vendor/jquery.ui.widget.js",
              "directupload/js/jquery.fileupload.js",
              "directupload/js/jquery.iframe-transport.js",
              "directupload/widget.js",
        )
    
    def render(self, context, instance, placeholder):  
        context.update({
            'object':instance, 
            'placeholder':placeholder
        })    
        return context

    def icon_src(self, instance):
        file_icon = instance.get_icon_url()
        if file_icon: return file_icon
        return settings.STATIC_URL + u"cms/images/plugins/file.png"
    
plugin_pool.register_plugin(FilePlugin)
