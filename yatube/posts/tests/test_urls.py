from http import HTTPStatus
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Group, Post
# from django.core.cache import cache

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='user')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.author = User.objects.create_user(username='author')
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.author)

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост',
        )

    def test_existing_pages(self):
        """URL-адреса доступны всем пользователям и возвращают статус код 200
        (по иному HTTPStatus.OK)
        """
        addresses = {
            HTTPStatus.OK: '/',
            HTTPStatus.OK: '/group/test-slug/',
            HTTPStatus.OK: '/profile/user/',
            HTTPStatus.OK: f'/posts/{PostURLTest.post.id}/',
        }
        for url, address in addresses.items():
            with self.subTest(address=address):
                response = (
                    self.guest_client.get(address)
                    and self.authorized_client.get(address)
                )
                self.assertEqual(response.status_code, url)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон и доступен всем."""
        # cache.clear()
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test-slug/',
            'posts/profile.html': '/profile/user/',
            'posts/post_detail.html': f'/posts/{PostURLTest.post.id}/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = (
                    self.guest_client.get(address)
                    and self.authorized_client.get(address)
                )
                self.assertTemplateUsed(response, template)

    def test_authorized_urls_uses_correct_template(self):
        """URL-адрес /create/ использует соответствующий шаблон и доступен
        только авторизованным.
        """
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_author_urls_uses_correct_template(self):
        """URL-адрес posts/<post_id>/edit/ использует соответствующий шаблон и
        доступен только автору поста. Если вписать в response просто
        авторизованного юзера authorized_client - тест ожидаемо не пройдет.
        """
        response = self.authorized_author.get(
            f'/posts/{PostURLTest.post.id}/edit/'
        )
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_author_urls_access_to_edit(self):
        """URL-адрес posts/<post_id>/edit/ доступен только автору поста."""
        response = self.authorized_author.get(
            f'/posts/{PostURLTest.post.id}/edit/'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page_must_return_404(self):
        """Запрос к несуществующей странице должен вернуть ошибку 404
        (по иному HTTPStatus.NOT_FOUND)
        """
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
