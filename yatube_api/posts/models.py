from django.contrib.auth import get_user_model
from django.db import models

# Получаем модель пользователя
User = get_user_model()


class Group(models.Model):
    """
    Модель для группы постов.
    Поля:
    - title: Заголовок группы (строка с максимальной длиной 200 символов).
    - slug: Уникальный идентификатор группы в URL (строка).
    - description: Описание группы (текст).
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Модель для постов.
    Поля:
    - text: Текст поста (текст).
    - pub_date: Дата публикации (дата и время, автоматически добавляется при
      создании).
    - author: Автор поста (связь с моделью User, при удалении автора все его
    посты удаляются).
    - image: Изображение, прикрепленное к посту (необязательное поле).
    - group: Группа, к которой относится пост (связь с моделью Group,
    необязательное поле, при удалении группы пост остается).
    """
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель для комментариев к постам.
    Поля:
    - author: Автор комментария (связь с моделью User, при удалении автора
      комментарии удаляются).
    - post: Пост, к которому относится комментарий (связь с моделью Post,
      при удалении поста комментарии удаляются).
    - text: Текст комментария (текст).
    - created: Дата создания комментария (дата и время, автоматически
      добавляется при создании).
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    """
    Модель для подписок пользователей друг на друга.
    Поля:
    - user: Пользователь, который подписывается (связь с моделью User).
    - following: Пользователь, на которого подписываются.

    Ограничения:
    - Уникальность пары (user, following) для предотвращения дублирования.
    - Пользователь не может подписаться сам на себя.
    """
    user = models.ForeignKey(User, related_name='follower',
                             on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following',
                                  on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'following')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
