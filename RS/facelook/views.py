from multiprocessing import context
import re
from turtle import pos
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import User, Post, Topic, Like, Fallowing
from .forms import NewUserForm, TopicForm, PostForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password

##############################################
"""
Pour l'instant, on va vérifier si l'utilisateur est connecté via une variable globale
Mais apres on va utiliser la session et ((django.login))
"""
##############################################
from django.contrib.auth import get_user_model
User = get_user_model()


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
                return render(request=request, template_name="login.html", context={"login_form": form, 'error__' : 'Email ou mot de passe incorrect'})
        else:
            messages.error(request, "Invalid username or password.")
            return render(request=request, template_name="login.html", context={"login_form": form, 'error__' : 'Email ou mot de passe incorrect'})
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def registe(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
        return render(request=request, template_name="register.html", context={"register_form": form, 'error__':f'{form.errors}'})    
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if not request.user.is_authenticated:
        if q != '':
            posts = Post.objects.filter(Q(text__icontains=q) | Q(topic__title__icontains=q) | Q(topic__text__icontains=q) | Q(topic__creator__username__icontains=q))
            topics = Topic.objects.filter(Q(title__icontains=q) | Q(text__icontains=q) | Q(text__icontains=q) | Q(creator__username__icontains=q))
            users = User.objects.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
            for user in users:
                nb_topics = Topic.objects.filter(creator=user).all().count()
                nb_posts = Post.objects.filter(creator=user).all().count()
                nb_followers = Fallowing.objects.filter(fallower=user).all().count()
                nb_following = Fallowing.objects.filter(user=user).all().count()
                user.nb_topics = nb_topics
                user.nb_posts = nb_posts
                user.nb_followers = nb_followers
                user.nb_following = nb_following
                user.i_follow = Fallowing.objects.filter(
                    fallower=User.objects.get(id=user.id), user=request.user).exists()
            for post in posts:
                like_counter = 0
                dislike_counter = 0
                for like in Like.objects.filter(post=post):
                    if like.value == True:
                        like_counter += 1
                        if like.user == request.user:
                            post.liked = True
                    else:
                        dislike_counter += 1
                        if like.user == request.user:
                            post.disliked = True
                post.like_counter = like_counter
                post.dislike_counter = dislike_counter
            return render(request, 'index.html', {'posts': posts, 'topics': topics, 'users': users, 'followers': Fallowing.objects.all(), 'search' : q})
        else:
            users = User.objects.all()
            topics = Topic.objects.all()
            posts = Post.objects.all()


            for user in users:
                nb_topics = Topic.objects.filter(creator=user).all().count()
                nb_posts = Post.objects.filter(creator=user).all().count()
                nb_followers = Fallowing.objects.filter(fallower=user).all().count()
                nb_following = Fallowing.objects.filter(user=user).all().count()
                user.nb_topics = nb_topics
                user.nb_posts = nb_posts
                user.nb_followers = nb_followers
                user.nb_following = nb_following
                user.i_follow = False
            for post in posts:
                like_counter = 0
                dislike_counter = 0
                for like in Like.objects.filter(post=post):
                    if like.value == True:
                        like_counter += 1
                        if like.user == request.user:
                            post.liked = True
                    else:
                        dislike_counter += 1
                        if like.user == request.user:
                            post.disliked = True
                post.like_counter = like_counter
                post.dislike_counter = dislike_counter
            return render(request, 'index.html', {'posts': posts, 'topics': topics, 'users': users})
    followers = Fallowing.objects.filter(user=request.user)
    
    posts = Post.objects.filter(
        Q(creator=request.user) | Q(topic__title__icontains=q)).order_by('-date')
    if q == '':
        posts = Post.objects.filter(
            creator__in=followers.values_list('fallower', flat=True))
        posts |= (Post.objects.filter(creator=request.user))
        if posts.count() < 5:
            posts |= (Post.objects.all().order_by('-date')[:5])
        if followers.count() == 0:
            posts = Post.objects.all()
    else:
        posts = Post.objects.filter(
            Q(creator=request.user) | Q(text__icontains=q) | Q(topic__title__icontains=q)).order_by('-date')
        if posts.count() < 5:
            posts |= (Post.objects.all().order_by('-date')[:5])
        if followers.count() == 0:
            posts = Post.objects.all()
    res = dict()
    res['topics'] = Topic.objects.filter(Q(title__icontains=q) | Q(text__icontains=q) | Q(text__icontains=q) | Q(creator__username__icontains=q) | Q(creator__first_name__icontains=q) | Q(creator__last_name__icontains=q))
    res['posts'] = posts
    res['followers'] = followers
    res['users'] = User.objects.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
    res['search'] = q
    for user in res['users']:
        nb_topics = Topic.objects.filter(creator=user).all().count()
        nb_posts = Post.objects.filter(creator=user).all().count()
        nb_followers = Fallowing.objects.filter(fallower=user).all().count()
        nb_following = Fallowing.objects.filter(user=user).all().count()
        user.nb_topics = nb_topics
        user.nb_posts = nb_posts
        user.nb_followers = nb_followers
        user.nb_following = nb_following
        user.i_follow = Fallowing.objects.filter(
            fallower=User.objects.get(id=user.id), user=request.user).exists()
    res['form'] = PostForm()
    for post in res['posts']:
        like_counter = 0
        dislike_counter = 0
        for like in Like.objects.filter(post=post):
            if like.value == True:
                like_counter += 1
                if like.user == request.user:
                    post.liked = True
            else:
                dislike_counter += 1
                if like.user == request.user:
                    post.disliked = True
        post.like_counter = like_counter
        post.dislike_counter = dislike_counter
    return render(request, 'index.html', res)


def profile(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return redirect('page_404')
    res = dict()
    res['user'] = user
    res['posts'] = Post.objects.filter(creator=user).all()
    res['topics'] = Topic.objects.filter(creator=user).all()
    res['followers'] = Fallowing.objects.filter(fallower=user).all()
    res['following'] = Fallowing.objects.filter(user=user).all()
    res['is_following'] = False

    if request.user.is_authenticated:
        res['is_following'] = Fallowing.objects.filter(
            user=request.user, fallower=user).exists()
    return render(request, 'profile.html', res)


def topic(request, id):
    res = dict()
    try:
        topic = Topic.objects.get(id=id)
    except:
        return redirect('page_404')
    res['topic'] = topic
    res['posts'] = Post.objects.filter(topic=topic)
    for post in res['posts']:
        like_counter = 0
        dislike_counter = 0
        for like in Like.objects.filter(post=post):
            if like.value == True:
                like_counter += 1
                if like.user == request.user:
                    post.liked = True
            else:
                dislike_counter += 1
                if like.user == request.user:
                    post.disliked = True
        post.like_counter = like_counter
        post.dislike_counter = dislike_counter


    return render(request, 'topic.html', res)


def topics(request):
    res = dict()
    res['topics'] = Topic.objects.all()
    if not res['topics']:
        return redirect('page_404')

    return render(request, 'topics.html', res)


def posts(request, id):
    res = dict()
    res['post'] = Post.objects.filter(id=id).first()
    if not res['post']:
        return redirect('page_404')

    like_counter = 0
    dislike_counter = 0
    for like in Like.objects.filter(post=res['post']):
        if like.value == True:
            like_counter += 1
            if like.user == request.user:
                res['post'].liked = True
        else:
            dislike_counter += 1
            if like.user == request.user:
                res['post'].disliked = True
    res['post'].like_counter = like_counter
    res['post'].dislike_counter = dislike_counter
    return render(request, 'posts.html', res)


@login_required(login_url='/login')
def add_post(request):
    form = PostForm(request.POST or None)
    topics = Topic.objects.all()
    if form.is_valid():
        post = form.save(commit=False)
        post.creator = request.user
        form.save()
        return redirect('index')
    return render(request, 'add_post.html', {'form': form, 'topics': topics, 'new': True})


@login_required(login_url='/login')
def edit_post(request, id):
    post = Post.objects.get(id=id)
    if not post:
        return redirect('page_404')
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.objects.filter(id=id)
            post.update(
                text=form.cleaned_data['text'],
                topic=form.cleaned_data['topic'])
            return redirect('posts', id=id)
    return render(request, 'add_post.html', {'form': form, 'new': False, 'post': post})


@login_required(login_url='/login')
def add_topic(request):
    form = TopicForm(request.POST or None)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.creator = request.user
        form.save()
        return redirect('topic', id=topic.id)
    return render(request, 'add_topic.html', {'form': form, 'new': True})


@login_required(login_url='/login')
def edit_topic(request, id):
    try:
        topic = Topic.objects.get(id=id)
        if topic.creator != request.user:
            return redirect('page_404')

    except:
        return redirect('page_404')
    form = TopicForm(instance=topic)
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            topic.title=form.cleaned_data['title']
            topic.text=form.cleaned_data['text']
            topic.save()
            return redirect('topic', id=id)
    return render(request, 'edit_topic.html', {'form': form, 'object':topic})

@login_required(login_url='/login')
def edit_post(request, id):
    try:
        post = Post.objects.get(id=id)
        if post.creator != request.user:
            return redirect('page_404')
    except:
        return redirect('page_404')
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post.text=form.cleaned_data['text']
            post.topic=form.cleaned_data['topic']
            post.save()
            return redirect('posts', id=id)
    return render(request, 'edit_post.html', {'form': form, 'object':post})


@login_required(login_url='/login')
def edit_profile(request):
    form = NewUserForm()
    if request.method == "POST":
        user = User.objects.filter(id=request.user.id)
        if not check_password(request.POST.get('password'), request.user.password):
            return render(request, 'edit_profile.html', {'form': form, 'error': "Informations incorrectes!"})

        if User.objects.filter(email=request.POST.get('email')).first() and request.POST.get('email') != request.user.email:
            return render(request, 'edit_profile.html', {'form': form, 'error': "Email existe déjà!"})
        if User.objects.filter(username=request.POST.get('username')).first() and request.POST.get('username') != request.user.username:
            return render(request, 'edit_profile.html', {'form': form, 'error': "Pseudo exite déjà!"})
        user.update(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
            bio=request.POST.get('bio'),
            email=request.POST.get('email'))

        return redirect('profile', id=request.user.id)
    return render(request, 'edit_profile.html', {'form': form})


@login_required(login_url='/login')
def password_edit(request):
    if request.method == "POST":
        user = User.objects.filter(id=request.user.id)
        if not check_password(request.POST.get('password0'), request.user.password):
            return render(request, 'edit_password.html', {'error': "Le mot de passe n\'est pas correct" })
        if request.POST.get('password1') != request.POST.get('password2'):
            return render(request, 'edit_password.html', {'error': "Mots de passe ne correspondent pas!"})
        try:
            make_password(request.POST.get('password1'))
        except:
            return render(request, 'edit_password.html', {'error': "Le mot de passe ne respecte pas les conseils"})
        user.update(password=make_password(request.POST.get('password1')))
        return redirect('profile', id=request.user.id)
    return render(request, 'edit_password.html', {})


def posts_for_user(request, id):
    res = dict()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    try:
        res['user'] = User.objects.get(id=id)
    except:
        return redirect('page_404')
    
    if q != '':
        res['posts'] = Post.objects.filter(creator=res['user']).filter(
            Q(text__icontains=q) |
            Q(date__icontains=q) |
            Q(topic__title__icontains=q) |
            Q(topic__text__icontains=q)
        )
    else: 
        res['posts'] = Post.objects.filter(creator=User.objects.get(id=id))
    for post in res['posts']:
        like_counter = 0
        dislike_counter = 0
        for like in Like.objects.filter(post=post):
            if like.value == True:
                like_counter += 1
                if like.user == request.user:
                    post.liked = True
            else:
                dislike_counter += 1
                if like.user == request.user:
                    post.disliked = True
        post.like_counter = like_counter
        post.dislike_counter = dislike_counter
    return render(request, 'posts_for_user.html', res)


def topics_for_user(request, id):
    res = dict()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    try:
        res['user'] = User.objects.get(id=id)
    except:
        return redirect('page_404')
    if q !='':
        res['topics'] = Topic.objects.filter(creator=res['user']).filter(
            Q(title__icontains=q) |
            Q(text__icontains=q) |
            Q(date__icontains=q))
    else:
        res['topics'] = Topic.objects.filter(creator=res['user'])
    
    return render(request, 'topics_for_user.html', res)


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('login_user')


def __zone__de__debug(mes):
    print('\n'*5)
    print(mes)
    print('\n'*5)


def page_404(request):
    return render(request, '404.html', {})


@login_required(login_url='/login')
def delete(request, id, type_of_object):
    if type_of_object == "post":
        post = Post.objects.filter(id=id)
        if not post:
            return redirect('page_404')
        post.delete()
        return redirect('index')
    elif type_of_object == "topic":
        topic = Topic.objects.filter(id=id)
        if not topic:
            return redirect('page_404')
        topic.delete()
        return redirect('index')
    else:
        return redirect('page_404')


@login_required(login_url='/login')
def follow_or_unfollow(request, id):
    user = User.objects.get(id=id)
    if not user:
        return redirect('page_404')
    following = Fallowing.objects.filter(
        user=request.user).filter(fallower=user)
    if following:
        following.delete()
        return redirect('profile', id=id)
    else:
        fallowing = Fallowing(user=request.user, fallower=user)
        fallowing.save()
        return redirect('profile', id=id)


def users_list(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = []

    if q != '':
        users = User.objects.filter(Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(email__icontains=q) |
        Q(bio__icontains=q))
    else:
        users = User.objects.all()

    
    for user in users:
        nb_topics = Topic.objects.filter(creator=user).all().count()
        nb_posts = Post.objects.filter(creator=user).all().count()
        nb_followers = Fallowing.objects.filter(fallower=user).all().count()
        nb_following = Fallowing.objects.filter(user=user).all().count()
        user.nb_topics = nb_topics
        user.nb_posts = nb_posts
        user.nb_followers = nb_followers
        user.nb_following = nb_following
        user.i_follow = Fallowing.objects.filter(
            fallower=User.objects.get(id=user.id), user=request.user).exists()
    return render(request, 'users_list.html', {'users': users})
