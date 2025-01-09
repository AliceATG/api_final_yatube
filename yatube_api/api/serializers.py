from django.contrib.auth import get_user_model
from posts.models import Group, Post, Comment, Follow
from rest_framework import serializers

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Group.
    Определяет, какие поля модели Group будут сериализованы и доступны.
    """
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    Позволяет сериализовать и десериализовать данные постов,
    включая только для чтения поле author, которое отображает username.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    Включает поля author и post только для чтения, отображая username автора
    и первичный ключ поста, соответственно.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Follow.
    Позволяет сериализовать данные подписок, с полями user и following,
    где user отображает текущего пользователя,
    а following выбирается из всех пользователей.
    """
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        """
        Валидация данных: предотвращает подписку на самого себя.
        """
        request_user = self.context['request'].user
        if data['following'] == request_user:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя.")
        return data
