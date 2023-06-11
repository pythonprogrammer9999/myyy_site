from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView

from .forms import SearchForm
from .models import Section, Product


def index(request):
    result = prerender(request)
    if result:
        return result
    sections = Section.objects.all().order_by('title')
    products = Product.objects.all().order_by(get_order_by_products(request))[:8]
    context = {'products': products}
    return render(
        request,
        'index.html',
        context=context
    )


def prerender(request):
    if request.GET.get('add_cart'):
        product_id = request.GET.get('add_cart')
        get_object_or_404(Product, pk=product_id)
        cart_info = request.session.get('cart_info', {})
        count = cart_info.get(product_id, 0)
        count += 1
        cart_info.update({product_id: count})
        request.session['cart_info'] = cart_info
        print(cart_info)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def get_order_by_products(request):
    order_by = ''
    if request.GET.__contains__('sort') and request.GET.__contains__('up'):
        sort = request.GET['sort']
        up = request.GET['up']
        if sort == 'price' or sort == 'title':
            if up == '0':
                order_by = '-'
            order_by += sort
    if not order_by:
        order_by = '-date'
    return order_by


def delivery(request):
    return render(
        request,
        'delivery.html',
    )


def contacts(request):
    return render(request, 'contacts.html')


def section(request, id):
    result = prerender(request)
    if result:
        return result
    obj = get_object_or_404(Section, pk=id)
    products = Product.objects.filter(section__exact=obj).order_by(get_order_by_products(request))
    context = {'section': obj, 'products': products}
    return render(
        request,
        'section.html',
        context=context
    )


class ProductDetailView(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        result = prerender(request)
        if result:
            return result
        return super(ProductDetailView, self).get(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects. \
                                  filter(section__exact=self.get_object().section). \
                                  exclude(id=self.get_object().id).order_by('?')[:5]
        return context


def handler404(request, exception):
    return render(request, '404.html', status=404)


def search(request):
    result = prerender(request)
    if result:
        return result
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.cleaned_data['q']
        products = Product.objects.filter(
            Q(title__icontains=q) | Q(country__icontains=q) |
            Q(director__icontains=q) |
            Q(cast__icontains=q) | Q(description__icontains=q)
        )
        context = {'products': products, 'q': q}
        return render(
            request,
            'search.html',
            context=context
        )





def cart(request):
    update_cart_info(request)
    cart_info = request.session.get('cart_info')
    products = []
    if cart_info:
        for product_id in cart_info:
            product = get_object_or_404(Product, pk=product_id)
            product.count = cart_info[product_id]
            products.append(product)
    context = {
        'products': products,
        'discount': request.session.get('discount', '')
    }
    return render(
        request,
        'cart.html',
        context=context
    )

def update_cart_info(request):
    if request.POST:
        cart_info = {}
        for param in request.POST:
            value = request.POST.get(param)
            print(param, value)
