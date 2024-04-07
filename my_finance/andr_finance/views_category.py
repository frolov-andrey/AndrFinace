from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import CategoryForm
from .models import Category
from .views import icon_default, get_images, images_path


class CategoryView(LoginRequiredMixin, ListView):
    template_name = 'andr_finance/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['select_menu'] = 'categories'
        context['icon_default'] = icon_default

        return context


class CategoryAdd(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'andr_finance/category_add.html'
    success_url = reverse_lazy('andr_finance:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        images = get_images(images_path)
        context['images'] = images
        context['icon_default'] = icon_default
        context['images_path'] = images_path
        context['image_default_folder'] = 'default'
        context['image_default_file'] = 'default_icon.png'

        return context

    def form_valid(self, form):
        category = form.save(commit=False)
        category.icon_folder = form.data['icon_folder']
        category.icon_file = form.data['icon_file']

        return super().form_valid(form)


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'andr_finance/category_edit.html'
    success_url = reverse_lazy('andr_finance:categories')

    title_page = 'Редактирование категории'

    def get_object(self, queryset=None):
        category = super().get_object(queryset)
        if category.user != self.request.user:
            raise Http404("Категория не существует или у вас нет разрешения на доступ к ней")
        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        images = get_images(images_path, self.object)

        context['select_menu'] = 'categories',
        context['images'] = images
        context['images_path'] = images_path
        context['image_default_folder'] = 'default'
        context['image_default_file'] = 'default_icon.png'
        context['icon_file'] = self.object.icon_file
        context['icon_folder'] = self.object.icon_folder

        return context

    def form_valid(self, form):
        category = form.save(commit=False)
        category.icon_folder = form.data['icon_folder']
        category.icon_file = form.data['icon_file']

        return super().form_valid(form)


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy("andr_finance:categories")

    def get_object(self, queryset=None):
        category = super().get_object(queryset)
        if category.user != self.request.user:
            raise Http404("Категория не существует или у вас нет разрешения на доступ к ней")
        return category
