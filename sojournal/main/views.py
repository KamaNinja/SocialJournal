from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView
from .forms import PostForm, CommentForm
from .models import Post, Comment


class HomePage(ListView):
    template_name = 'main/index.html'
    model = User
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        data = self.request.GET.get('search')
        print(data)

        return context


class RegisterUser(CreateView):
    template_name = 'main/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    template_name = 'main/register.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('home')


@login_required()
def logout_user(request):
    logout(request)
    return redirect('login')


class AddPost(CreateView):
    template_name = 'main/add_post.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return redirect(reverse('post', kwargs={'pk': post.pk}))


class PostPage(DetailView, CreateView):
    template_name = 'main/post.html'
    model = Post
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        comment.post = post
        comment.save()
        return redirect(reverse('post', kwargs={'pk': post.pk}))


class ProfilePage(ListView):
    template_name = 'main/profile.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return Post.objects.filter(user=user)
