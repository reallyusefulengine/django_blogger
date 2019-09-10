from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Post, Comment
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView,
UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.models import Profile
from users.managers import ProfileManager


# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'about'})

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class FollowsListView(LoginRequiredMixin, ListView):
    # Follow.follow_data = [[],[]]
    model = Profile
    template_name = 'blog/follows.html' # <app>/<model>_<viewtype>.html

    def get_queryset(self):
        follow_data = Profile.objects.get_users_follows(self.request.user)
        return follow_data


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['following_me'] = Profile.objects.get_users_following_me(self.request.user)
        return context


class UserFollowView(View):
    # def get_queryset(self):
    #     is_following = Profile.objects.is_following(self.kwargs.get('username'), self.request.user)
    #     return is_following

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_following'] = Profile.objects.is_following(self.kwargs.get('username'), self.request.user)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["is_following"] = context.pop("object_list")
    #     return context

    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(Profile, user__username=username)
        if request.user.is_authenticated:
            user_profile, created = Profile.objects.get_or_create(user=request.user)
            if toggle_user in user_profile.follows.all():
                user_profile.follows.remove(toggle_user)
            else:
                user_profile.follows.add(toggle_user)

        return redirect("user-posts", username=username)
