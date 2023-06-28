import json
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Comment


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({
                "message": "Login successful."
            }, status=200)
        else:

            return JsonResponse({
                "error": "Invalid username and/or password."
            }, status=400)
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        username = data.get("username")  # username name bio url pass conf_pass
        email = data.get("email")
        bio = data.get("bio")
        url = data.get("url")
        password = data.get("password")
        confirmation = data.get("confirmation")

        # Ensure password matches confirmation
        if password != confirmation:
            return JsonResponse({
                "error": "passwords_mismatch"
            }, status=400)

        # Ensure username is not taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "error": "username_taken"
            }, status=400)

        # Ensure email is not taken
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "error": "email_taken"
            }, status=400)

        # Ensure password is at least 5 characters and no more than 16 characters.
        if len(password) < 5 or len(password) > 16:
            return JsonResponse({
                "error": "password_length"
            }, status=400)

        # Ensure username is between 5 and 25 characters.
        if len(username) < 5 or len(username) > 25:
            return JsonResponse({
                "error": "username_length"
            }, status=400)

        # Ensure email is valid.
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return JsonResponse({
                "error": "email_invalid"
            }, status=400)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, name=name, bio=bio, url=url)
            user.save()
        except IntegrityError:
            return JsonResponse({
                "error": "email_username_taken"
            }, status=400)
        login(request, user)
        return JsonResponse({
            "message": "koker"
        }, status=201)
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
@csrf_exempt
def create(request):
    # Creating a new post
    if request.method == "POST":
        body = request.POST.get("text")
        if body == "":
            return JsonResponse({
                "error": "Content is required."
            }, status=400)
        new_post = Post(user=request.user, body=body)
        new_post.save()
        return JsonResponse({
            "message": "Post created successfully."
        }, status=201)
    elif request.method == "PUT":
        data = json.loads(request.body)
        body = data.get("text")
        post_id = data.get("id")
        # Getting user id from the post
        post_k = Post.objects.filter(id=post_id).first()
        post_user_id = post_k.user.id
        # Checking if the user is the owner of the post
        if post_user_id != request.user.id:
            return JsonResponse({
                "error": "You are not the owner of this post."
            }, status=403)
        else:
            if body == "":
                return JsonResponse({
                    "error": "Content is required."
                }, status=400)
            post_upd = Post.objects.filter(id=post_id, user=request.user).first()
            if not post_upd:
                return JsonResponse({
                    "error": "Post not found."
                }, status=404)
            post_upd.body = body
            post_upd.save()
            return JsonResponse({
                "message": "Post updated successfully."
            }, status=201)


def not_found(request, exception=None):
    if request.method == "GET":
        try:
            error = request.GET.get("error")
        except Exception as e:
            try:
                error = exception.args[0]
            except Exception as e:
                error = "(404) Page not found."
        context = {"error": error}
        # return render(request, '404.html', status=404)
        return render(request, "network/index.html", context)


def posts_wo_pg(request, type_p):
    if request.method == "GET":
        if type_p == "all" or type_p == "following" or type_p == "saved":
            return redirect(reverse("posts", args=[type_p, 1]))
        else:
            return redirect(reverse("404") + "?error=This page doesn't exist")


def posts_all(request):
    if request.method == "GET":
        return redirect(reverse("posts", args=["all", 1]))


def posts(request, type_p, page_id):
    if request.method == "GET":

        if type_p == "all":
            data = Post.objects.all()
        elif type_p == "following":
            if request.user.is_authenticated:
                data = Post.objects.filter(user__in=request.user.following.all())
            else:
                return redirect(reverse("404") + "?error=This page doesn't exist")
        elif type_p == "saved":
            if request.user.is_authenticated:
                user_obj = User.objects.filter(id=request.user.id).first()
                data = Post.objects.filter(id__in=user_obj.saved_posts.all())
            else:
                return redirect(reverse("404") + "?error=This page doesn't exist")
        else:
            return redirect(reverse("404") + "?error=This page doesn't exist")
        data = data.order_by("-timestamp").all()
        paginator = Paginator(data, 10)
        if paginator.num_pages < page_id:
            return redirect(reverse("404") + "?error=This page doesn't exist")

        return render(request, "network/index.html")


@login_required
def profile_own(request):
    if request.method == "GET":
        return redirect(reverse("profile", args=[request.user.id, 1]))


@login_required
def profile_wo_pg(request, user_id):
    if request.method == "GET":
        # get requested user obj
        user_id = User.objects.filter(id=user_id).first()
        if user_id:
            return redirect(reverse("profile", args=[user_id.id, 1]))
        else:
            return redirect(reverse("404") + "?error=User not found")


@login_required
def profile(request, user_id, page_id):
    if request.method == "GET":
        user_id = User.objects.filter(id=user_id).first()
        data = Post.objects.filter(user=user_id)
        data = data.order_by("-timestamp").all()
        paginator = Paginator(data, 10)

        # Get the page object for the current page number

        print(paginator.num_pages)
        if not user_id:
            return redirect(reverse("404") + "?error=User not found")
        if paginator.num_pages < page_id:
            return redirect(reverse("404") + "?error=This page doesn't exist")

        return render(request, "network/index.html")


@login_required
def followers(request):
    if request.method == "GET":
        return render(request, "network/index.html")


@csrf_exempt
def post(request):
    if request.method == "GET":
        # Get the current page number from the request query parameters
        page_number = request.GET.get('page')
        r_type = request.GET.get('type')
        # Define the number of items per page
        items_per_page = 10
        data = None
        if r_type == "all":
            # Get all posts
            data = Post.objects.all()
            data = data.order_by("-timestamp").all()
        elif r_type == "following":
            data = Post.objects.filter(user__in=request.user.following.all())
            data = data.order_by("-timestamp").all()
        elif r_type == "user":
            user_id = request.GET.get('user')
            data = Post.objects.filter(user=user_id)
            data = data.order_by("-timestamp").all()
        elif r_type == "saved":
            user_obj = User.objects.filter(id=request.user.id).first()
            data = Post.objects.filter(id__in=user_obj.saved_posts.all())
            # data = user_obj.saved_posts.all()
            data = data.order_by("-timestamp").all()
        else:
            return redirect(reverse("404") + "?error=Invalid request")
        # Initialize the paginator
        paginator = Paginator(data, items_per_page)
        # Get the page object for the current page number
        page_obj = paginator.get_page(page_number)
        post_dicts = []
        if r_type == "all":
            if request.user.is_authenticated:
                post_dicts = [post_t.serialize(user=request.user) for post_t in page_obj]
            else:
                post_dicts = [post_t.serialize() for post_t in page_obj]
        else:
            if request.user.is_authenticated:

                post_dicts = [post_t.serialize(user=request.user) for post_t in page_obj]
            else:
                return redirect(reverse("404") + "?error=Log in to see this page")
        # Build the JSON response
        response_data = {
            'results': post_dicts,
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'type': r_type
        }
        # Return the JSON response
        return JsonResponse(response_data)
    elif request.method == "PUT":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            post_id = data.get("post_id")
            method = data.get("method")
            action = data.get("action")
            post_data = Post.objects.get(id=post_id)
            user_data = request.user.id
            user_data = User.objects.get(id=user_data)
            if method == "like":
                if action == "add":
                    post_data.likes.add(user_data)
                    print(f"{user_data} liked {post_data}")
                    return JsonResponse({
                        "message": "Post liked successfully."
                    }, status=201)
                elif action == "remove":
                    post_data.likes.remove(user_data)
                    print(f"{user_data} unliked {post_data}")
                    return JsonResponse({
                        "message": "Post unliked successfully."
                    }, status=201)
                else:
                    return JsonResponse({
                        "error": "Invalid request."
                    }, status=400)
            elif method == "bookmark":
                if action == "add":
                    user_data.saved_posts.add(post_data)
                    print(f"{user_data} bookmarked {post_data}")
                    return JsonResponse({
                        "message": "Post bookmarked successfully."
                    }, status=201)
                elif action == "remove":
                    user_data.saved_posts.remove(post_data)
                    print(f"{user_data} unbookmarked {post_data}")
                    return JsonResponse({
                        "message": "Post unbookmarked successfully."
                    }, status=201)
                else:
                    return redirect(reverse("404") + "?error=Invalid request")
            elif method == "comment":
                body = data.get("text")
                if body == "":
                    return JsonResponse({
                        "error": "Content is required."
                    }, status=400)
                else:
                    comment = Comment.objects.create(body=body)
                    comment.user.set([user_data])
                    comment.post.set([post_data])
                    post_data.comments.add(comment)
                    print(comment)
                    comment.save()
                    return JsonResponse({
                        "message": "Comment added successfully."
                    }, status=201)
            else:
                return redirect(reverse("404") + "?error=Invalid request")
        else:
            return JsonResponse({
                "error": "Login required."
            }, status=400)


@csrf_exempt
@login_required
def user(request):
    if request.method == "GET":
        if request.GET.get("profile"):
            user_id = request.GET.get('profile')
            curr_user = User.objects.get(id=user_id)
            from_user = request.user.id
            same = False

            following = curr_user.following.all()
            followers = curr_user.followers.all()
            following_count = following.count()
            followers_count = followers.count()
            is_followed = False
            for follower in followers:
                if follower.id == from_user:
                    is_followed = True
            if int(user_id) == int(from_user):
                is_followed = True
                same = True

            # Getting number of user posts
            posts_user = Post.objects.filter(user=curr_user)
            posts_count = posts_user.count()

            return JsonResponse({
                "id": curr_user.id,
                "username": curr_user.username,
                "same": same,
                "name": curr_user.name,
                "bio": curr_user.bio,
                "url": curr_user.url,
                "following": [curr_user.id for curr_user in following],
                "followers": [curr_user.id for curr_user in followers],
                "following_count": following_count,
                "followers_count": followers_count,
                "is_following": is_followed,
                "posts_count": posts_count
            }, status=200)

        elif request.GET.get("followers"):
            user_id = request.GET.get('followers')
            curr_user = User.objects.get(id=user_id)
            followers = curr_user.followers.all()
            from_user = request.user.id
            follower_list = []
            for follower in followers:
                follower_data = {
                    "id": follower.id,
                    "username": follower.username,
                    "name": follower.name,
                    "url": follower.url
                }
                if follower.followers.filter(id=from_user).exists():
                    follower_data["is_followed"] = True
                elif follower.id == from_user:
                    follower_data["is_followed"] = True
                else:
                    follower_data["is_followed"] = False
                follower_list.append(follower_data)
            return JsonResponse({
                "follow": follower_list
            }, status=200)
        elif request.GET.get("following"):
            user_id = request.GET.get('following')
            curr_user = User.objects.get(id=user_id)
            followers = curr_user.following.all()
            from_user = request.user.id
            follower_list = []
            for follower in followers:
                follower_data = {
                    "id": follower.id,
                    "username": follower.username,
                    "name": follower.name,
                    "url": follower.url
                }
                if follower.followers.filter(id=from_user).exists():
                    follower_data["is_followed"] = True
                elif follower.id == from_user:
                    follower_data["is_followed"] = True
                else:
                    follower_data["is_followed"] = False
                follower_list.append(follower_data)
            return JsonResponse({
                "follow": follower_list
            }, status=200)
        else:
            return redirect(reverse("404") + "?error=invalid request")
    elif request.method == "PUT":
        data = json.loads(request.body)
        method = data.get("method")
        request_id = data.get("id")
        user_id = request_id
        curr_user = request.user.id  # 2
        current_user_obj = User.objects.get(id=curr_user)
        user_to_f_uf = User.objects.get(id=user_id)
        if method == "follow":
            user_to_f_uf.followers.add(current_user_obj)
            current_user_obj.following.add(user_to_f_uf)
            return JsonResponse({
                "message": "User followed successfully."
            }, status=201)
        elif method == "unfollow":
            user_to_f_uf.followers.remove(current_user_obj)
            current_user_obj.following.remove(user_to_f_uf)
            return JsonResponse({
                "message": "User unfollowed successfully."
            }, status=201)
        else:
            return redirect(reverse("404") + "?error=Invalid request")
