import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from webapp.models import Profile, Post
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# Create your views here.
def about(request):
    return render(request, "about.html")


def home(request):
    if 'post' in request.GET:
        query = request.GET['post']
        if query=="all":
            allPosts = reversed(Post.objects.all())
            activeFilter = "All Posts"
        elif query=="today":
            allPosts = reversed(Post.objects.filter(date_created__gt=datetime.date.today()))
            activeFilter = "Today's Posts"
        elif query=="week":
            allPosts = reversed(Post.objects.filter(date_created__gt=datetime.date.today()-datetime.timedelta(days=7)))
            activeFilter = "This week"
        else:
            allPosts = reversed(Post.objects.filter(date_created__gt=datetime.date.today()-datetime.timedelta(days=30)))
            activeFilter = "This month"
    else:
        allPosts = reversed(Post.objects.all())
        activeFilter = "All Posts"
    allUsers = Profile.objects.all()
    context = {'posts':allPosts, 'informants':allUsers, 'activeFilter':activeFilter}
    return render(request, "home.html", context)



def profile(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    allPosts = reversed(Post.objects.filter(user=user))
    allUsers = Profile.objects.all()
    context = {'posts': allPosts, 'informant':profile, 'informants':allUsers}
    return render(request, "profile.html", context)


@login_required(login_url='/login/')
def add_post(request):
    if request.method == 'POST':
        postTitle = request.POST.get('postTitle')
        postContent = request.POST.get('postContent')
        postImage = request.FILES.get('postImage')
        postLink = request.POST.get('postLink')
        try:
            Post.objects.create(
                title=postTitle,
                image=postImage,
                content=postContent,
                usefulLink=postLink,
                user=request.user
            )
            messages.success(request, "Post added successfully!")
            return redirect('add_post')
        except:
            messages.error(request, "Unable to add new post!")
            return redirect('/profile/'+str(request.user.id))
    profile = Profile.objects.get(user=request.user)
    context = {'informant':profile}
    return render(request, "add_post.html", context)


@login_required(login_url='/login/')
def edit_post(request, id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=request.POST.get('postId'))
            post.title = request.POST.get('postTitle')
            post.content = request.POST.get('postContent')
            post.usefulLink = request.POST.get('postLink')
            if request.POST.get('clearImage')=="True":
                post.image = None
            if request.FILES.get('postImage'):
                post.image = request.FILES.get('postImage')
            post.save()
            messages.success(request, "Post edited successfully!")
            return redirect('/profile/'+str(request.user.id))
        except:
            messages.error(request, "Unable to edit post!")
            return redirect('/profile/'+str(request.user.id))
    post = Post.objects.get(id=id)
    if post.user!=request.user:
        messages.error(request, "Unauthorized access!")
        return redirect('/profile/'+str(request.user.id))
    else:
        profile = Profile.objects.get(user=request.user)
        context = {'informant':profile, 'post':post}
        return render(request, "edit_post.html", context)


@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == "POST":
        try:
            user = request.user
            user.username = request.POST.get('username')
            user.email = request.POST.get('emailAddress')
            profile = Profile.objects.get(user=request.user)
            profile.fullName = request.POST.get('fullName')
            profile.bio = request.POST.get('bio')
            profile.linkInBio = request.POST.get('linkInBio')
            if request.POST.get('clearImage')=="True":
                profile.logo = None
            if request.FILES.get('profilePhoto'):
                profile.logo = request.FILES.get('profilePhoto')
            user.save()
            profile.save()
            messages.success(request, "Profile edited successfully!")
            return redirect('/profile/'+str(request.user.id))
        except:
            messages.error(request, "Unable to edit profile!")
            return redirect('/profile/'+str(request.user.id))
    profile = Profile.objects.get(user=request.user)
    context = {'profile':profile}
    return render(request, "edit_profile.html", context)


@login_required(login_url='/login/')
def change_password(request):
    if request.method == "POST":
        user = request.user
        currentPassword = request.POST.get('currentPassword').strip()
        newPassword = request.POST.get('newPassword').strip()
        confirmNewPassword = request.POST.get('confirmNewPassword').strip()
        if user.check_password(currentPassword):
            if (newPassword == confirmNewPassword):
                user.password = make_password(newPassword)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully!")
                return redirect('change_password')
            else:
                messages.error(request, "New passwords did not match!")
                return redirect('change_password')
        else:
            messages.error(request, "Current password did not match!")
            return redirect('change_password')
    profile = Profile.objects.get(user=request.user)
    context = {'profile':profile}
    return render(request, "change_password.html", context)