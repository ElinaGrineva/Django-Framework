import random

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


# Create your views here.
def index(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.filter(
            Q(category__name='дом') | Q(category__name='офис')
        )
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context)


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]
    Product.objects.all()[3:5]


def get_same_products(hot_product):
    products_list = Product.objects.all().filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return products_list


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            "title": 'Продукты',
            'category': category_item,
            'products': products_paginator
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'links_menu': links_menu,
        "title": 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': links_menu
    }

    return render(request, 'mainapp/product.html', context)
