from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea
from django import forms
from django.urls import re_path as url
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from . import data_format, contract_engine
from slugify import slugify
import os
from django.urls import reverse

admin.site.site_header = 'Панель администрирования туристической компании ООО "Вояж"'
admin.site.site_title = 'Вояж'
admin.site.index_title = 'Администрирование'

class RoutePointForm(forms.ModelForm):
    class Meta:
        model = RoutePoint
        help_texts = {'hotel': 'Введите название или адрес',
                      'town': 'Введите город'}
        exclude = ()


class RoutePointInline(admin.TabularInline):
    model = RoutePoint
    form = RoutePointForm

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    autocomplete_fields = ['hotel', ]
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    model = Hotel

    list_display = ['name', 'type', 'address', ]
    search_fields = ['name', 'address', ]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/hotel_masking.js',)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    model = Worker

    search_fields = ['lastName', 'firstName', 'patronymic', ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client

    fieldsets = (
        ('Общие данные', {
            'fields': (('lastName', 'firstName', 'patronymic', ), ('born', ), )
        }),
        ('Документ, удостоверяющий личность', {
            'fields': (('document', ), ('serial', 'number', ), ('date', 'region'), )
        }),
        ('Другое', {
            'fields': (('picture', 'image_tag', ), ('passport', ), )
        }),
    )
    readonly_fields = ('image_tag',)
    search_fields = ['lastName', 'firstName', 'patronymic', ]

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/client_masking.js',)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    model = Route

    list_display = ['routeName', 'country', 'get_towns', 'worker', 'amount', 'route_actions', ]

    inlines = [RoutePointInline, ]
    autocomplete_fields = ['worker', 'clients']

    class Media:
        js = ('//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
              'js/jquery.maskedinput.js',
              'js/jquery.maskedinput.min.js',
              'js/route.js',)

    def route_actions(self, obj):
        html = ''
        clients = []
        for item in Client.objects.filter(route__id=obj.pk):
            temp = {}
            temp['id'] = item.id
            temp['name'] = item.__str__()
            clients.append(temp)
        for item in clients:
            id = item['id']
            name = item['name']
            template = f'<a class="button" href="contract/{obj.pk}/{id}">{name}</a> ' + '<p></p>'
            html = html + template
        return format_html(html[:-7])

    route_actions.short_description = 'Договор оказания услуг'
    route_actions.allow_tags = True


    def get_urls(self):
        urls = super(RouteAdmin, self).get_urls()
        custom_urls = [
            url(
                r'^contract/(?P<route>[0-9])/(?P<client>[0-9])$',
                self.admin_site.admin_view(self.save_check),
                name='save_check',
            ),
        ]
        return custom_urls + urls


    def save_check(self, request, route, client,  *args, **kwargs):
        data = data_format.get_order_data(route, client)
        path = contract_engine.contract_generate(data)
        print(path)
        temp = slugify(path.split('/')[2], save_order=True, separator='.')
        if os.path.exists(path):
            with open(path, 'rb') as fh:
                response = HttpResponse(fh.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'inline; filename=' + temp
                return response
        # return HttpResponseRedirect("../../")