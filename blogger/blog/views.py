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

# class Follow(LoginRequiredMixin, CreateView):
#     model = Post
#     context_object_name = 'posts'
#     who_is_following_who = [[],[]]
#
#
#     def follow(self):
#         theUser = Profile.objects.filter(user_id__exact=self.request.user.id)
#         add_to_following = who_is_following_who[0].append(post.author.username)
#         print(who_is_following_who)
#
#
#     def post(self, request, *args, **kwargs):
#         # form.instance.author = self.request.user
#         # form = self.form_class(request.POST)
#         # form.follow()
#         # if form.is_valid():
#         #     return super().form_valid(form)
#         # return render(request, self.blog_home, {'form': form})
#         if request.method=='POST':
#             follow_form = FollowForm(request.POST, instance=request.user)
#             if follow_form.is_valid():
#                 self.follow(request)
#                 follow_form.save()
#                 messages.success(request, f'Now following the user')
#                 return redirect('profile')
#         else:
#             follow_form = FollowForm(instance=request.user)
#
#         context= {
#             'follow_form': follow_form,
#         }
#
#         return render(request, 'users/profile.html', context)
#
#     def get_queryset(self):
#         theUser = Profile.objects.filter(user_id__exact=self.request.user.id)
#         i_follow = theUser[0].follows.all()
#         following_me = theUser[0].followed_by.all()
#         who_is_following_who[0].append(i_follow)
#         who_is_following_who[1].append(following_me)
#
#         return who_is_following_who

class FollowsListView(LoginRequiredMixin, ListView):
    # Follow.follow_data = [[],[]]
    model = Profile
    template_name = 'blog/follows.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'follow_data'
    paginate_by = 6
    #
    def get_queryset(self):
        follow_data = [[],[]]
        theUser = Profile.objects.filter(user_id__exact=self.request.user.id)
        theFollowers = theUser[0].follows.all()
        followers = theUser[0].followed_by.all()
        follow_data[0].append(theFollowers)
        follow_data[1].append(followers)

        print(f'I follow: {follow_data[0]}')
        print(f'{follow_data[1]} follows me')

        return follow_data

class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(Profile, user__username=username)
        if request.user.is_authenticated:
            user_profile, created = Profile.objects.get_or_create(user=request.user)
            print(f'user profile is: {user_profile}')
            print(f'toggle user: {toggle_user}')
            if toggle_user in user_profile.follows.all():
                user_profile.follows.remove(toggle_user)
            else:
                print(user_profile)
                user_profile.follows.add(toggle_user)

        return redirect("user-posts", username=username)
