from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Group, Post
from django.urls import reverse
from datetime import datetime
from time import sleep

User = get_user_model()


class PostViewTest(TestCase):
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

        for i in range(1, 14):
            cls.post = Post.objects.create(
                author=cls.author,
                pub_date=datetime.now(),
                text=(
                    f'Тестовый пост номер {i}: '
                    'Европейский союз был создан Маастрихтским договором 1992 '
                    'года, вступившим в силу 1 ноября 1993 года, на основе '
                    'Европейского экономического сообщества и нацелен на '
                    'региональную интеграцию. ЕС — международное образование, '
                    'сочетающее признаки международной организации '
                    '(межгосударственности) и государства '
                    '(надгосударственности), однако юридически он не является '
                    'ни тем, ни другим. С помощью стандартизированной системы '
                    'законов, действующих во всех странах союза, был создан '
                    'общий рынок, гарантирующий свободное передвижение '
                    '(движение) людей, товаров.'
                ),
                group=cls.group
            )
            sleep(0.1)

    def test_first_page_contains_ten_records(self):
        """
        Тест пагинатора 1: количество постов на первой странице равно 10.
        """
        response = self.authorized_author.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        """
        Тест пагинатора 2: на второй странице должно быть 4 поста.
        """
        response = self.authorized_author.get(
            reverse('posts:index') + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)
