from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from media.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import datetime
import json
from django.core import serializers
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.



def index(request):
    # VALIDATE USER AUTHENTICATION
    if not request.user.is_authenticated:
        return render(request, "media/login.html")
    
    # all posts
    all_posts = reversed(Posts.objects.all())

    #ALL LIKES 
    allLikes = Likes.objects.all()

    # ALL USERS
    filterd_names = []
    all_users = User.objects.all()
    all_users_filterd = Follow.objects.filter(userf=request.user)
    for names in all_users_filterd:
        filterd_names.append(names.user.username)
    print(filterd_names)
    
    
    for post in Posts.objects.all():
        print(post.liked_users.all())

    return render(
        request, "media/index.html", {"allposts": all_posts, "id": request.user, "allLikes": allLikes, "users": all_users, "filtered_names": filterd_names}
    )


def new_user(request):
    user = User.objects.get(username=request.user.username)
    if request.user.is_authenticated and user.times_loggin_in == 1:
        if request.method == 'POST':
            img_url = request.POST['profile_img_url']
            username = request.POST['new_username']
            first_name = request.POST['new_first_name']
            last_name = request.POST['new_last_name']
            bio = request.POST['bio']
            print(img_url)
            # CHECKING IF USER CHANGED THERE NAMES

            if username != user.username:
                user.username = username
            if first_name != user.first_name:
                user.first_name = first_name
            if last_name != user.last_name:
                user.last_name = last_name

            user.profile_image = img_url
            user.bio = bio
            user.save()
            return HttpResponseRedirect(reverse("profile", args=(user.username, )))

        else:
            return render(request, "media/newuser.html", {
                "user": user
            })
    else:
        return HttpResponseRedirect(reverse("index"))
def user_profile(request, username):
    # get the user of that page
    id = User.objects.get(username=username)
    
    # get the users posts
    posts = Posts.objects.filter(username=id.username)
    
    # Check if the current user is following the user of the page
    check_if_following = Follow.objects.filter(user=id, userf=request.user)
    is_following = False
    if len(check_if_following) > 0:
        is_following = True
        
        
    # Check how many followers the user of the page has
    followers_count = Follow.objects.filter(user=id)
    
    
    # Check how many people the user of the page is following
    following_count = Follow.objects.filter(userf=id)
    
    
    return render(request, "media/profile.html", {
        "id": id, 
        "allposts": posts,
        "isFollowing": is_following,
        "followers_count": len(followers_count),
        'following_count': len(following_count)
        })


def register(request):
    # Check For Request method
    if request.method == "POST":
        # Post Data
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        # VALIDATION

        # Check for empty boxes
        if (
            len(first_name) == 0
            or len(last_name) == 0
            or len(email) == 0
            or len(username) == 0
            or len(password) == 0
            or len(password2) == 0
        ):
            return render(
                request,
                "media/register.html",
                {"message": "All Fields Must Not Be blank"},
            )

            # Check if the passwords match
        if password != password2:
            return render(
                request, "media/register.html", {"message": "Password Does Not Match"}
            )

            # Check if email is valid
        if not "@" in email:
            return render(request, "media/register.html", {"message": "Invalid Email"})

            # Check if password is strong
        if not len(password) > 4:
            return render(
                request, "media/register.html", {"message": "Password is weak"}
            )

            # Check if username exists
        try:
            check = User.objects.get(username=username)
            if len(check.username) > 0:
                return render(
                    request,
                    "media/register.html",
                    {"message": "Username already exists"},
                )
            else:
                pass
        except ObjectDoesNotExist as e:
            pass

        # ADD DATA TO DATABASE

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.save()
        return HttpResponseRedirect(reverse("login"))

    else:
        return render(request, "media/register.html")


def login_user(request):
    # Check for request method
    if request.method == "POST":
        # POSTING Username and password
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Authenticating the current user
        user = authenticate(request, username=username, password=password)
        
        # Validating User authentication
        if user is not None:
            login(request, user)
            newUser = User.objects.get(username=username)
            newUser.times_loggin_in +=1
            newUser.save()
            if newUser.times_loggin_in == 1:
                return HttpResponseRedirect(reverse("newuser"))
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "media/login.html", {"message": "Invalid Username or Password"}
            )
            
            
    return render(request, "media/login.html")


def logout_user(request):
    # Logging out the user
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def new_posts(request):
    # UNFINISHED 
    if request.method == "POST":
        post = request.POST["post"]

        new_post = Posts(
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            username=request.user.username,
            post=post,
            date=datetime.datetime.now(),
        )

        new_post.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "media/newpost.html")



# API'S
@login_required
@csrf_exempt
def post_api(request):
    # Checking for request method
    if request.method == "POST":
        # Loading the data that came from javascript
        data = json.loads(request.body)
        
        # Creating a new Obect of Posts class and saving it
        new_post = Posts(
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            username=request.user.username,
            date=datetime.datetime.now(),
            post=data["Post"],
        )
        new_post.save()
        
        
        # Returning A Json response to the front end
        return JsonResponse(203, safe=False)
    # JsonResponse(json.dumps("hi"))


@csrf_exempt
def get_api(request):
    # Get all posts 
    all_posts = Posts.objects.all()
    
    # Convert data into json
    serialized_data = serializers.serialize(
        "json", all_posts, fields=["first_name", "last_name", "username", "post"]
    )
    # Return success response to the front end
    return JsonResponse(serialized_data, safe=False, status=200)


@csrf_exempt
def current_user(request):
    # Returning the current user
    return JsonResponse(data=request.user.username, status=200, safe=False)


@csrf_exempt
def follow(request):
    # Loading the data sent from javascript
    data = json.loads(request.body)

    # Getting the current user
    userf = User.objects.get(username=data["current_user"])
    print(data['user_being_followed'])
    # Getting the user of that page
    user = User.objects.get(username=data["user_being_followed"])
    
    # Checking weather to follow or unfollow the user
    if data['follow_id'] == '1':
         # Creating a new follow object and saving it
        new_follower = Follow(user=user, userf=userf)
        new_follower.save()
        
        # Returning a successfull json response to the front end
        return JsonResponse(data="Followed user", status=200, safe=False)
    else:
        remove_follow = Follow.objects.get(user=user, userf=userf)
        remove_follow.delete()
    
        # Returning a successfull json response 
        return JsonResponse(data='Unfollowed user', status=200, safe=False)

@csrf_exempt
def like_post(request):
    # Check for request method
    if request.method =='POST':
        # load the json data from javascript
        data = json.loads(request.body)
        
        # Finding the post 
        find_post = Posts.objects.get(id=data['id'])
        
    
        # CHECKING IF THE USER LIKED OR UNLIKED
        if request.user in find_post.liked_users.all():
            
            find_post.liked_users.remove(request.user)
            return HttpResponse(status=201)
        else:
            if request.user in find_post.disliked_users.all():
                find_post.disliked_users.remove(request.user)
            # Adding a new like object and saving it
            new_like = Likes(user=request.user, post=find_post)
            new_like.save()
        
            find_post.liked_users.add(request.user)
            # Returning a successull response
            return HttpResponse(status=200)
   
@csrf_exempt 
def like_count(request, id):
    # Getting the post from the database
    posting = Posts.objects.get(id=id)
    
    # Getting the likes by filtering with post
    all_likes = len(posting.liked_users.all())
    
    # getting the count and returning a successfull response
    return JsonResponse(status=200, data=json.dumps({"count": str(all_likes)}), safe=False)

@csrf_exempt
def dislike_post(request):
    # Check for request method
    if request.method =='POST':
        # load the json data from javascript
        data = json.loads(request.body)
        
        # Finding the post 
        find_post = Posts.objects.get(id=data['id'])
        
    
        # CHECKING IF THE USER LIKED OR UNLIKED
        if request.user in find_post.disliked_users.all():
            
            find_post.disliked_users.remove(request.user)
            return HttpResponse(status=201)
        
        else:
            if request.user in find_post.liked_users.all():
                find_post.liked_users.remove(request.user)
            # Adding a new like object and saving it
            new_dislike = Likes(user=request.user, post=find_post)
            new_dislike.save()
        
            find_post.disliked_users.add(request.user)
            # Returning a successull response
            return HttpResponse(status=200)

@csrf_exempt
def dislike_count(request, id):
    # Getting the post from the database
    posting = Posts.objects.get(id=id)
    
    # Getting the likes by filtering with post
    all_dislikes = len(posting.disliked_users.all())
    
    # getting the count and returning a successfull response
    return JsonResponse(status=200, data=json.dumps({"count": str(all_dislikes)}), safe=False)

@csrf_exempt
def get_user(request):
    user = User.objects.get(username=request.user.username)
    
    return JsonResponse(data=user.serialize(), safe=False, status=200)

@csrf_exempt
def comment(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        posting = Posts.objects.get(id=id)
        new_comment = Comment(user=request.user, comment=data['comment'], post=posting)
        new_comment.save()
    
        return HttpResponse(status=200)
    else:
        json_comments = []
        posting = Posts.objects.get(id=id)
        all_comments = Comment.objects.filter(post=posting)
        
        for comment in all_comments:
            json_comments.append({
                "comment":comment.comment,
                "user": comment.user.username,
                "post": comment.post.post
            })
            

        return JsonResponse(status=200, data=json_comments, safe=False)
    