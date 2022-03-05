from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post
from http import HTTPStatus
from django.contrib.auth import get_user_model

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.author)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    def test_create_post_form(self):
        """
        Валидная форма создает пост
        """
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': self.group.id,
        }
        response = self.authorized_author.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse(
                'posts:profile',
                kwargs={'username': self.author}
            )
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост',
                group=self.group.id
            ).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_post_form(self):
        """
        Валидная форма редактирует пост
        """
        self.post = Post.objects.create(
            author=self.author,
            text='Тестовый пост 2',
            group=self.group
        )
        form_data = {
            'text': self.post.text,
            'group': self.group.id,
        }
        response = self.authorized_author.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': '1'}
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': '1'}
            ),
        )
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост 2',
                group=self.group.id
            ).exists()
        )
