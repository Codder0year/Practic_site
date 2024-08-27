from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version
from catalog.services import get_cached_versions_for_product


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'object_list'


def contacts(request):
    context = {
        'title': 'Контакты',
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}, phone: {phone}, message: {message}')
    return render(request, 'catalog/contacts.html', context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['versions'] = get_cached_versions_for_product(self.object)
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = self.request.user
        product = form.save(commit=False)  # Не сохраняем сразу в базу
        product.owner = user  # Присваиваем владельца
        product.save()  # Теперь сохраняем продукт с владельцем
        return super().form_valid(form) # Возвращаем форму


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        self.object = form.save()  # Сохраняем основной объект

        if formset.is_valid():
            formset.instance = self.object  # Устанавливаем связь с основной моделью
            formset.save()
            return super().form_valid(form)
        else:
            # Если формсет не валиден, возвращаем ту же страницу с ошибками
            return self.render_to_response(self.get_context_data(form=form))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        elif (
            user.has_perm('catalog.can_unpublish_product') and
            user.has_perm('catalog.can_edit_any_product') and
            user.has_perm('catalog.can_change_category')
        ):
            return ProductModeratorForm
        else:
            raise PermissionDenied