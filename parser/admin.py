from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from parser import models
from parser.models import Product


@admin.register(models.Parsing)
class ParsingAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_field', 'products')
    list_display_links = None

    @staticmethod
    def get_link_to_obj(obj):
        url = reverse('admin:parser_product_change', args=(obj.id,))
        link = format_html('{}: <a href="{}">{}</a>', obj.id, url, obj)
        return link

    def products(self, obj):
        products = obj.products.filter(parser=obj)
        links = ""
        for product in products:
            url = reverse("admin:parser_product_change",
                          args=(product.id,))
            link = format_html('{}:<a href="{}">{}</a>', product.id, url,
                               product)
            links += link + "<br>"
        return format_html(links)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'clear_price', 'href', 'parsers')
    list_display_links = ('short_title',)
    list_filter = ('parser', 'parser__date_field')

    def short_title(self, obj):
        title = obj.title
        return title[:70] + '...' if len(title) > 70 else title

    def parsers(self, obj):
        parser = obj.parser_id
        url = reverse('admin:parser_parsing_changelist',)
        return format_html('<a href="{}">{}</a>', url, parser)

    def clear_price(self, obj):
        return str(obj.price) + '₽'

    def href(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}...</a>', obj.link, obj.link[:70]
        )

    short_title.shorted_description = 'Title'
    parsers.shorted_description = 'Parser'
    clear_price.shorted_description = 'Price'
    href.shorted_description = 'Link'

