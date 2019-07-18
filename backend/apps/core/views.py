from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.models import User, Post
from .serializers import UserSerializer, RegistrationSerializer, PostSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user).data
    }


class RegistrationViewSet(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class PostEndpoint(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        post_id = kwargs['pk']

        try:
            user = User.objects.get(id=data.get('user_id'))
            current_post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            return JsonResponse({"ok": False, "message": "User or post with provided id does not exist. "}, status=500)
        except Exception as e:
            return JsonResponse({"ok": False, "message": f"There was an exception: {e}"}, status=500)

        all_likes = current_post.user_likes.all()

        if user in all_likes:
            current_post.user_likes.remove(user)
            message = 'Post unliked'
        else:
            current_post.user_likes.add(user)
            message = 'Post liked'

        return JsonResponse({"ok": True, "message": message}, status=200)

    def destroy(self, request, *args, **kwargs):
        data = request.data
        post_id = kwargs['pk']

        try:
            user = User.objects.get(id=data.get('user_id'))
            current_post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            return JsonResponse({"ok": False, "message": "User or post with provided id does not exist. "}, status=500)
        except Exception as e:
            return JsonResponse({"ok": False, "message": f"There was an exception: {e}"}, status=500)

        if current_post.creator == user:
            current_post.delete()
            return JsonResponse({"ok": True, "message": 'Post removed'}, status=200)

        return JsonResponse({"ok": False, "message": "You can't remove this post"}, status=403)
