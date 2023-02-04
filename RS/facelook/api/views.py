from django.http import JsonResponse
from ..models import Post, Like, Fallowing, User, Topic
from .serializers import Topics_serialized, Post_serialized, User_serialized
from rest_framework.decorators import api_view
from rest_framework.response import Response




@api_view(['GET'])
def set_value_post(request, id, action):
    post = Post.objects.get(id = id)
    user = request.user
    if action == 'like':
        if post and user:            
            like = Like.objects.filter(post = post, user = user).first()
            if like:
                if like.value == True:
                    like.delete()
                    return JsonResponse({'message': 'Deleted Successfully'}, safe=False)
                else:
                    like.value = True
                    like.save()
                    return JsonResponse({'message': 'Liked Successfully'}, safe=False)
            else:
                like = Like.objects.create(post = post, user = request.user)
                return JsonResponse({'message': 'Like created Successfully'}, safe=False)
        else:
            return JsonResponse({'message': 'Post or User not found'}, safe=False)
    elif action == 'dislike':
        if post and user:            
            like = Like.objects.filter(post = post, user = user).first()
            if like:
                if like.value == True:
                    like.delete()
                    like = Like.objects.create(post = post, user = request.user, value = False)
                    return JsonResponse({'message': 'Disliked Successfully'}, safe=False)
                else:
                    like.delete()
                    return JsonResponse({'message': 'Undisliked Successfully'}, safe=False)
            else:
                like = Like.objects.create(post = post, user = request.user, value = False)
        else:
            return JsonResponse({'message': 'Post or User not found'}, safe=False)
    return JsonResponse({'message': 'Undefined path'}, safe=False)


@api_view(['GET'])
def get_nb_likes(request, id):
    post = Post.objects.get(id = id)
    if post:
        likes = Like.objects.filter(post = post, value = True).count()
        dislikes = Like.objects.filter(post = post, value = False).count()
        return JsonResponse({'likes': likes, 'dislikes' : dislikes}, safe=True)
    else:
        return JsonResponse({'message': 'Post not found'}, safe=False)


@api_view(['GET'])
def get_value_follow(request, id):
    user = request.user
    if user == User.objects.get(id = id):
        return JsonResponse({'message': 'You can not follow yourself'}, safe=False)
    if user:
        followings = Fallowing.objects.filter(fallower = User.objects.get(id=id), user = request.user).first()
        if followings:
            return JsonResponse({'anser' : True}, safe=True)
        else:
            return JsonResponse({'anser' : False}, safe=True)
    else:
        return JsonResponse({'message': 'User not found'}, safe=False)



@api_view(['GET'])
def set_value_follow(request, id):
    me = request.user
    user = None
    try : user = User.objects.get(id = id)
    except : return JsonResponse({'message': 'User not found'}, safe=False)
    if me and user:
        if me == user:
            return JsonResponse({'message': 'You can not follow yourself'}, safe=False)
        else:
            fowl = Fallowing.objects.filter(user = me, fallower = user)
            if fowl:
                fowl.delete()
                return JsonResponse({'message': 'Unfollowed Successfully'}, safe=False)
            else:
                fowl = Fallowing.objects.create(user = me, fallower = user)
                return JsonResponse({'message': 'Followed Successfully'}, safe=False)
    else:
        return JsonResponse({'message': 'User not found'}, safe=False)

@api_view(['GET'])
def get_nb_like_dislike(request, id):
    post = Post.objects.get(id = id)
    if post:
        likes = Like.objects.filter(post = post)
        nb_like = likes.filter(value = True).count()
        nb_dislike = likes.filter(value = False).count()
        return JsonResponse({'nb_like': nb_like, 'nb_dislike': nb_dislike}, safe=False)
    else:
        return JsonResponse({'message': "hello"}, safe=False)


@api_view(['GET'])
def get_all_topics(request):
    topics = Topic.objects.all()
    serialized = Topics_serialized(topics, many=True)
    return Response(serialized.data)
    


@api_view(['GET'])
def get_topic(request, id):
    topic = Topic.objects.get(id = id)
    serialized = Topics_serialized(topic, many=False)
    return Response(serialized.data)

# route to create a new post
@api_view(['POST'])
def create_post(request):
    data = request.data
    post = Post.objects.create(
        user = request.user,
        topic = Topic.objects.get(id = data['topic']),
        title = data['title'],
        body = data['body'],
        image = data['image'],
    )
    serialized = Post_serialized(post, many=False)
    return Response(serialized.data)



@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    for user in users:
        user.password = ''
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

    serialized = User_serialized(users, many=True)
    return Response(serialized.data)

@api_view(['GET'])
def get_users_custom(request):
    data = list()
    users = User.objects.all()
    for user in users:
        user_info = dict()
        user_info['id'] = user.id
        user_info['username'] = user.username
        user_info['email'] = user.email
        user_info['first_name'] = user.first_name
        user_info['last_name'] = user.last_name
        user_info['nb_topics'] = Topic.objects.filter(creator=user).all().count()
        user_info['nb_posts'] = Post.objects.filter(creator=user).all().count()
        user_info['nb_followers'] = Fallowing.objects.filter(fallower=user).all().count()
        user_info['nb_following'] = Fallowing.objects.filter(user=user).all().count()
        user_info['i_follow'] = Fallowing.objects.filter(
            fallower=User.objects.get(id=user.id), user=request.user).exists()
        data.append(user_info)
    return JsonResponse(data, safe=False)