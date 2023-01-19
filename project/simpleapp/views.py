from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView
)
from .models import Product, Post, CategoryN
from datetime import datetime
from django.http import HttpResponse
from .filters import ProductFilter, PostFilter
from .forms import ProductForm, NewsForm
from django.shortcuts import redirect, get_object_or_404, render


def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')

    try:
        result = int(number) * int(multiplier)
        html = f"<html><body>{number}*{multiplier}={result}</body></html>"
    except (ValueError, TypeError):
        html = f"<html><body>Invalid input.</body></html>"

    return HttpResponse(html)


class ProductsList(ListView):
    model = Product
    ordering = 'name'
    # queryset = Product.objects.filter(
    #    price__lt= 300
    # ).order_by('name')
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = 'Распродажа в среду'
        context['filterset'] = self.filterset
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'id'


class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    raise_exception = True
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма.
    template_name = 'product_edit.html'


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.add_product',)
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


class PostsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearch(ListView):
    model = Post
    ordering = 'title'
    # queryset = Product.objects.filter(
    #    price__lt= 300
    # ).order_by('name')
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_product',)
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.add_product',)
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.add_product',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryList(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(CategoryN, id=self.kwargs)
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super.get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = CategoryN.objects.get(id=pk)
    category.subsribers.add(user)
    message = "Вы успешно подписались"
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
