from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Группа',
        help_text='Название группы'
    )
    slug = models.SlugField(
        max_length=50, unique=True,
        verbose_name='Читабельная slug-ссылка',
        help_text='Может состоять из символов латиницы, '
        'цифр, нижнего подчеркивания и дефиса '
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Расскажите, о чём эта группа'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Текст нового или редактируемого поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
        help_text='Время создание поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой относится пост. Необязательно.'
    )

    class Meta:
        ordering = ('-pub_date',)
        # ordering = ('pk',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]
