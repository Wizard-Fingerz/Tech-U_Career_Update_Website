from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from passlib.hash import pbkdf2_sha256
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from blog.models import *
from .forms import *
from user.models import *
from user.resources import ProgrammeResources
from tablib import Dataset
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

import requests
from django.conf import settings
from isodate import parse_duration
# messages.debug, messages.success, messages.info, messages.warning, messages.error
# Create your views here.




def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name: str = 'blog/home.html'
    
    def get_context_data(self):
        context = super(PostListView, self).get_context_data()
        context['posts'] = Post.objects.all()
        context['departments'] = Department.objects.all()
        context['header_posts'] = Post.objects.all().order_by('-id')[:3]
        context['first_posts'] = Post.objects.all()[:2]
        context['latest_posts'] = Post.objects.all().order_by('-id')[:3]
        context['latest_posts_2'] = Post.objects.all()[:3]
        context['footer_recent_posts'] = Post.objects.all().order_by('-id')[:5]
        
        # Faculty One
        context['faculty_1'] = Faculty.objects.get(id = 1)
        context['faculty_1_posts'] = Post.objects.all().filter(faculty_id = 1).order_by('-id')[:6]
        context['faculty_1_departmental_posts'] = Post.objects.get(department_id = 1)
        context['Mathematics_and_Computational_Sciences'] = Post.objects.all().filter(department_id = 2)[:1]
        context['Physical_Sciences'] = Post.objects.all().filter(department_id = 3)[:1]
        
        # Faculty Two
        context['faculty_2'] = Faculty.objects.get(id = 2)
        context['faculty_2_posts'] = Post.objects.all().filter(faculty_id = 2).order_by('-id')[:6]
        context['faculty_2_posts_2'] = Post.objects.all().filter(faculty_id = 2).order_by('id')[:2]
        context['faculty_2_posts_3'] = Post.objects.all().filter(faculty_id = 2).order_by('id')[:7:5]
        context['faculty_2_departmental_posts'] = Post.objects.filter(department_id = 4)
        context['Engineering_and_Biomedical_Engineering'] = Post.objects.all().filter(department_id = 5)[:6]
        
        
        # Faculty Three
        context['faculty_3'] = Faculty.objects.get(id = 3)
        context['faculty_3_posts'] = Post.objects.all().filter(faculty_id = 3).order_by('-id')[:6]
        context['faculty_3_posts_2'] = Post.objects.all().filter(faculty_id = 3).order_by('id')[4:2]
        context['faculty_3_posts_3'] = Post.objects.all().filter(faculty_id = 3).order_by('id')[:6]
        context['faculty_3_departmental_posts'] = Post.objects.get(department_id = 9)
        context['Property_planning_survey'] = Post.objects.all().filter(department_id = 8)[:2]
        return context



def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('/admin')
            elif user.is_student and user.is_moderator:
                return redirect('moderator')
            else:
                return redirect('student')
        else:
            messages.info(request, "Invalid Username or password")
            return redirect('login')
    return render(request, 'users/login.html')


def logoutView(request):
    logout(request)
    return redirect('blog-home')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save() ###add user to database
            messages.success(request, f'Account was created successfully!')
            return redirect('login')
		
    else:
        messages.error(request, 'Registration Fail, try again later')
        form = UserRegistrationForm()
    return render(request,'users/register.html', {'form' : form})


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('login')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/profile.html', context)




# student view
def student(request):
    return render(request, 'users/students/home.html')


class StudentPostListView(ListView):
    model = Post
    template_name = 'users/students/home.html'

    def get_context_data(self):
        context = super(StudentPostListView, self).get_context_data()
        context['User_posts'] = Post.objects.all()
        context['top_video'] = Video.objects.all()
        context['latest_posts'] = Post.objects.all().order_by('-id')[:6]
        context['footer_recent_posts'] = Post.objects.all().order_by('-id')[:5]
        context['departments'] = Department.objects.all()
        context['header_posts'] = Post.objects.all().order_by('-id')[:3]
        context['first_posts'] = Post.objects.all()[:2]
        return context


@login_required(login_url='login')
def student_video_index(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }
        
        
        r = requests.get(search_url, params=search_params)
        
        results = r.json()['items']
        
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        
        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
        
        video_params = {
            'part': 'snippet, contentDetails',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'id': ','.join(video_ids),
            'maxResults': 9,
        }
        
        
        r = requests.get(video_url, params = video_params)
        results = r.json()['items']
        
       
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
                }
            videos.append(video_data)
            
    context = {
        'videos': videos
    }
    
    return render(request, 'users/students/video/index.html', context)



# moderator view
def moderator(request):
    return render(request, 'users/moderator/moderator_home.html')

class ModeratorPostListView(ListView):
    model = Post
    template_name = 'users/moderator/moderator_home.html'

    def get_context_data(self):
        context = super(StudentPostListView, self).get_context_data()
        context['User_posts'] = Post.objects.all()
        context['top_video'] = Video.objects.all()
        context['latest_posts'] = Post.objects.all().order_by('-id')[:6]
        context['footer_recent_posts'] = Post.objects.all().order_by('-id')[:5]
        context['departments'] = Department.objects.all()
        context['header_posts'] = Post.objects.all().order_by('-id')[:3]
        context['first_posts'] = Post.objects.all()[:2]
        return context

@login_required(login_url='login')
def moderator_video_index(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }
        
        
        r = requests.get(search_url, params=search_params)
        
        results = r.json()['items']
        
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        
        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
        
        video_params = {
            'part': 'snippet, contentDetails',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'id': ','.join(video_ids),
            'maxResults': 9,
        }
        
        
        r = requests.get(video_url, params = video_params)
        results = r.json()['items']
        
       
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
                }
            videos.append(video_data)
            
    context = {
        'videos': videos
    }
    
    return render(request, 'users/moderators/video/index.html', context)


@login_required(login_url='login')
def simple_upload(request):
    if request.method == 'POST':
        programme_resources = ProgrammeResources
        dataset = Dataset()
        new_programme = request.FILES['myfile']
        
        if not new_programme.name.endswith('csv'):
            messages.info(request, 'Wrong Format')
            return render(request, 'upload.html')
        
        imported_data = dataset.load(new_programme.read().decode(), format='csv')
        
        for data in imported_data:
            value = Programme(
                data[0],
                data[1],
                data[2]
            )
            value.save()
    return  render(request, 'upload.html')
            



