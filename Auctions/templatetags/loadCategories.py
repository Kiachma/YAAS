__author__ = 'eaura'

from django import template
register = template.Library()
from Auctions.models import  Category

@register.inclusion_tag('auctions/categories.html')
def getCategories():
    category_list = Category.objects.order_by('name')
    return {'category_list': category_list}