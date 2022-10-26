from datetime import timedelta
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from .models import *
import numpy as np

# Create your views here.

now = datetime.now().strftime("%Y-%m-%d %H:M")
today = datetime.today()
long_ago = today + timedelta(days = -30)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'user/moderator/post_form.html'

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
    return render(request, 'blog/about.html', {'title': 'About'})

def trendingpostfunction():
    rdata = Post.objects.filter(date__gte=long_ago)
    likerate = []
    dislikerate = []
    viewrate = []
    for i in rdata:
        lr = i.post_like.count() + 1
        vr = i.post_views + 1
        lr = lr / vr
        likerate.append(lr)
        dr = i.post_dislike.count() + 1
        dr = dr / vr
        dislikerate.append(dr)
        u = User.objects.count()
        vrt = vr / u
        viewrate.append(vrt)
    lr1 = np.array(likerate)
    dr1 = np.array(dislikerate)
    vr1 = np.array(viewrate)
    lr = lr1.round(2)
    dr = dr1.round(2)
    vr = vr1.round(2)
    results = []
    for i in lr, dr, vr:
        a = (lr - dr) + vr
        a = a * 50
    rdata = Post.objects.filter(date__gte=long_ago)
    trendingdata = a
    j = 0
    trendingdict = {}
    for i in rdata:
        trendingdict[i.id] = trendingdata[j]
        j += 1
    trend = {k: v for k, v in sorted(trendingdict.items(), key=lambda item: item[1], reverse=True)}
    print('latest trending -->', trend)
    trendlist = []
    for k in trend.keys():
        trendlist.append(k)
    #print('trendlist --', trendlist)
    return trendlist

