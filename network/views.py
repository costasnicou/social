from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm,EditPostForm
from .models import User,Post,Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def like(request,postid):
    post = Post.objects.get(pk=postid)
    user = request.user
    
    if request.user.is_authenticated:

        # Return email contents
        if request.method == "GET":
            
            
            post.likes.add(request.user) 
            post.save()
           
            if request.user in post.likes.all():
                post.liked = True
                total_likes = post.likes.all().count()      
         
                return JsonResponse({"liked":post.liked,"total_likes":total_likes})
        # elif request.method == "PUT":
        #     data = json.loads(request.body)
   
    return JsonResponse({"message": "Like added!"})

@csrf_exempt
def save_edited_post(request,postid):
    # all_posts = Post.objects.all().order_by('-creation_date')
    post = Post.objects.get(id=postid)
    if request.method == "POST":
        if f'save-edited-post-{post.id}' in request.POST:
            post.editpostform=EditPostForm(request.POST)
            if post.editpostform.is_valid():
                valid_post_data = post.editpostform.cleaned_data
                post.content = post.editpostform.cleaned_data["content"]
                post.creation_date = post.creation_date
                post.user = request.user
                post.save()   
                return JsonResponse({
                    "status": "success",
                    "content": post.content,
                    "post_id": post.id,
                    "post_date":  post.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "post_user": post.user.username,
                })

def unlike(request,postid):
    post = Post.objects.get(pk=postid)
    user = request.user
    
    if request.user.is_authenticated:

        # Return email contents
        if request.method == "GET":
            
            
            post.likes.remove(request.user) 
            
            # if not post.likes.filter(request.user):
            # print(f"like status, {post.liked}")
            if request.user not in post.likes.all():
                post.liked = False   
                total_likes = post.likes.all().count()      
                return JsonResponse({"liked":post.liked,"total_likes":total_likes})
        # elif request.method == "PUT":
        #     data = json.loads(request.body)
   
    return JsonResponse({"message": "Like removed!"})


def index(request):
    postform = PostForm()     
    all_posts = Post.objects.all().order_by('-creation_date')
    editpostform = EditPostForm()
    for post in all_posts:
        post.editpostform = EditPostForm(initial={"content":post.content})

    already_liked = False
    paginator = Paginator(all_posts, 10) # Show 10 per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    if request.method=="POST":
        if "add_new_post" in request.POST:
            postform=PostForm(request.POST)
            if postform.is_valid():
                valid_post_data = postform.cleaned_data
                newpost = Post(user=request.user,content=valid_post_data["content"])
                newpost.save()
                return HttpResponseRedirect(reverse("index"))      

    for post in page_obj:
        
        if request.user in post.likes.all():
            post.liked = True
        else:
            # print(f"User has not liked the post {post.id}")
            post.liked = False


    return render(request, "network/index.html",{
        "all_posts":all_posts,
        "postform":postform,
        "page_obj":page_obj,
        "editpostform":editpostform,
    })


def profile(request,profile_user):
    username= User.objects.get(username=profile_user)
    postform = PostForm()     
    if not Profile.objects.filter(user=username).exists():
        new_profile = Profile(user=username)
        new_profile.save()
   
    user_posts = Post.objects.filter(user=username).order_by('-creation_date')
    editpostform = EditPostForm()
    for post in user_posts:
        post.editpostform = EditPostForm(initial={"content":post.content})
    profile = Profile.objects.get(user=username)
    follows = profile.following.count()
    followers = username.followers.all().count()
    paginator = Paginator(user_posts, 10) # Show 10 per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    for user_post in page_obj:
        if request.user in user_post.likes.all():
            user_post.liked = True
        else:
            # print(f"User has not liked the post {post.id}")
            user_post.liked = False
    
    if request.method == "POST":
        if "follow-btn" in request.POST:
            if not Profile.objects.filter(user=request.user).exists():
                new_follower_profile = Profile(user=request.user)
                new_follower_profile.save()
                
            thefollower = User.objects.get(username=request.user)
            followerprofile = Profile.objects.get(user=thefollower)
            followerprofile.following.add(username)
                       

        if "unfollow-btn" in request.POST:
            thefollower = User.objects.get(username=request.user)
            followerprofile = Profile.objects.get(user=thefollower)
            followerprofile.following.remove(username)
        
        if "add_new_post" in request.POST:
            postform=PostForm(request.POST)
            if postform.is_valid():
                valid_post_data = postform.cleaned_data
                newpost = Post(user=request.user,content=valid_post_data["content"])
                newpost.save()
                
         
          
        return HttpResponseRedirect(reverse('profile',args={profile_user:username}))
            

    hasfollower = False
    profileowner = False

    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).exists():
            followerprofile = Profile.objects.get(user=request.user)
            hasfollower = followerprofile.following.filter(id=username.id).exists()

        if request.user.username == profile_user:
            profileowner = True
        
    
    return render(request,"network/profile.html",{
        "profile_user":profile_user,
        "profile":profile,
        "followers":followers,
        "follows":follows,
        "hasfollower":hasfollower,
        "user_posts":user_posts,
        "profileowner":profileowner,
        "postform":postform,
        "page_obj":page_obj,
    })
    
@login_required
def following(request):
    current_user = request.user 
    if not Profile.objects.filter(user=current_user).exists():
        new_profile = Profile(user=current_user)
        new_profile.save()
    profile = Profile.objects.get(user=current_user)
    following_profiles = profile.following.all()
    profile_posts = None
    all_posts=[]
    for following_profile in following_profiles:
        profile_posts_list = Post.objects.filter(user=following_profile)   
        for profile_post in profile_posts_list:
            all_posts.append(profile_post)

    all_posts.sort(key=lambda post: post.creation_date, reverse=True)
    paginator = Paginator(all_posts, 10) # Show 10 per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for user_post in page_obj:
        if request.user in user_post.likes.all():
            user_post.liked = True
        else:
            user_post.liked = False
    return render(request, "network/following.html",{
       "all_posts":all_posts,
       "page_obj":page_obj,
         
    })