from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.conf import settings
from catalog.forms import ProductForm
from catalog.models import Product, Category
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from catalog.services.product_services import get_products_by_category
from django.views.generic import ListView
from django.views.decorators.http import require_POST


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = cache.get('product_list')
        if not products:
            products = Product.objects.filter(is_available=True, status='published').order_by('-updated_at')
            cache.set('product_list', products, 60 * 15)  # кеш на 15 минут
        return products


class ContactsView(TemplateView):
    template_name = 'contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        messages.success(request, 'Ваше сообщение успешно отправлено! Спасибо за обращение.')
        return self.render_to_response({'form_submitted': True})


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60 * 15) if settings.CACHE_ENABLED else lambda x: x)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        action = self.request.POST.get('action')
        if action == 'publish':
            form.instance.status = 'published'
        else:
            form.instance.status = 'draft'
        response = super().form_valid(form)
        cache.delete('product_list')
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

    def handle_no_permission(self):
        return HttpResponseForbidden("Вы не являетесь владельцем этого продукта.")

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'publish':
            form.instance.status = 'published'
        else:
            form.instance.status = 'draft'
        response = super().form_valid(form)
        cache.delete('product_list')
        return response


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('drafts_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.can_unpublish_product')

    def handle_no_permission(self):
        return HttpResponseForbidden("У вас нет прав для удаления этого продукта.")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.delete('product_list')
        return response


class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'products_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return get_products_by_category(self.category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['category'] = Category.objects.get(id=category_id)
        return context

class DraftProductsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Product
    template_name = 'drafts_list.html'
    context_object_name = 'products'

    def test_func(self):
        user = self.request.user
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def get_queryset(self):
        return Product.objects.filter(status='draft').order_by('-updated_at')

@login_required
@permission_required('catalog.can_unpublish_product')
@require_POST
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'draft'
    product.save()
    cache.delete('product_list')
    messages.success(request, f'Продукт «{product.name}» переведен в черновики.')
    return redirect('drafts_list')

@login_required
@permission_required('catalog.can_unpublish_product')
@require_POST
def publish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'published'
    product.save()
    cache.delete('product_list')
    messages.success(request, f'Продукт «{product.name}» успешно опубликован.')
    return redirect('drafts_list')

@login_required
@permission_required('catalog.can_unpublish_product')
@require_POST
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_name = product.name
    product.delete()
    cache.delete('product_list')
    messages.success(request, f'Продукт «{product_name}» удалён.')
    return redirect('drafts_list')

@login_required
def delete_product_from_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.owner and not request.user.has_perm('catalog.can_unpublish_product'):
        return HttpResponseForbidden("У вас нет прав на удаление этого продукта.")

    product_name = product.name
    product.delete()
    cache.delete('product_list')
    messages.success(request, f'Продукт «{product_name}» удалён.')
    return redirect('home')
