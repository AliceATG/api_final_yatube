from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post, Follow
from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import ValidationError
from .serializers import (
    CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer)

# Сообщение об ошибке при попытке изменить чужой контент.
PERM_DENIED_MSG = 'Изменение чужого контента запрещено!'


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Post.
    Позволяет аутентифицированным пользователям создавать,
    изменять и удалять посты.
    Неаутентифицированные пользователи могут только просматривать.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Сохранение нового поста с автором текущим пользователем.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Изменение доступно только автору поста.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(PERM_DENIED_MSG)
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        """
        Удаление доступно только автору поста.
        """
        if instance.author != self.request.user:
            raise PermissionDenied(PERM_DENIED_MSG)
        super().perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Comment.
    Позволяет аутентифицированным пользователям создавать, изменять
    и удалять комментарии.
    Неаутентифицированные пользователи могут только просматривать.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Получение комментариев для указанного поста.
        """
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        """
        Сохранение нового комментария с автором и постом.
        """
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """
        Изменение доступно только автору комментария.
        """
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(PERM_DENIED_MSG)
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        """
        Удаление доступно только автору комментария.
        """
        if serializer.author != self.request.user:
            raise PermissionDenied(PERM_DENIED_MSG)
        super(CommentViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet для модели Group.
    Позволяет всем пользователям просматривать группы.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]


class FollowViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin,
                    viewsets.mixins.CreateModelMixin):
    """
    ViewSet для модели Follow.
    Позволяет аутентифицированным пользователям подписываться на других
    пользователей
    и просматривать свои подписки.
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    queryset = Follow.objects.all()

    def get_queryset(self):
        """
        Получение подписок текущего пользователя.
        """
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """
        Создание новой подписки с проверкой на уникальность и самоподписку.
        """
        user = self.request.user
        following = serializer.validated_data['following']
        if user == following:
            raise ValidationError("Вы не можете подписаться на самого себя.")
        if Follow.objects.filter(user=user, following=following).exists():
            raise ValidationError("Вы уже подписаны на этого пользователя.")
        serializer.save(user=user)
