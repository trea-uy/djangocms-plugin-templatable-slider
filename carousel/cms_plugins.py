# coding: utf-8
import re
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import *
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.forms import ModelForm, ValidationError


class CarouselForm(ModelForm):
    class Meta:
        model = Carousel

    def clean_domid(self):
        data = self.cleaned_data['domid']
        if not re.match(r'^[a-zA-Z_]\w*$', data):
            raise ValidationError(
                _("The name must be a single word beginning with a letter"))
        return data


class CarouselItemInline(admin.TabularInline):
    model = CarouselItem


class CarouselPlugin(CMSPluginBase):
    model = Carousel
    form = CarouselForm
    name = _("Carousel")    

    inlines = [
        CarouselItemInline,
        ]

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context

class TemplateCarouselPlugin(CarouselPlugin):
    model = TemplateCarousel
    name = _("Carousel")    
    render_template = TEMPLATES[0][0]
    text_enabled = True

    def render(self, context, instance, placeholder):
        if instance and instance.template:
            self.render_template = instance.template
        
        context['instance'] = instance
        context['placeholder'] = placeholder
        return context

plugin_pool.register_plugin(TemplateCarouselPlugin)
