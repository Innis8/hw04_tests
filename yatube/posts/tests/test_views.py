from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Group, Post
from django.urls import reverse
from datetime import datetime

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

        cls.group_without_needed_post = Group.objects.create(
            title='Группа без нужного поста',
            slug='group-without-needed-post',
            description='Описание группы без нужного поста',
        )

        cls.post = Post.objects.create(
            author=cls.author,
            pub_date=datetime.now(),
            text=(
                'Тестовый пост: '
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

    def test_namespace_uses_correct_template(self):
        """namespace:name использует соответствующий шаблон"""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_posts',
                kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.author}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_author.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_post(self, first_object):
        self.assertEqual(first_object.author, self.author)
        self.assertEqual(
            first_object.text,
            'Тестовый пост: '
            'Европейский союз был создан Маастрихтским договором 1992 '
            'года, вступившим в силу 1 ноября 1993 года, на основе '
            'Европейского экономического сообщества и нацелен на '
            'региональную интеграцию. ЕС — международное образование, '
            'сочетающее признаки международной организации '
            '(межгосударственности) и государства (надгосударственности), '
            'однако юридически он не является ни тем, ни другим. С помощью'
            ' стандартизированной системы законов, действующих во всех '
            'странах союза, был создан общий рынок, гарантирующий '
            'свободное передвижение (движение) людей, товаров.'
        )
        self.assertEqual(first_object.group, self.group)

    def test_index_page_show_correct_context(self):
        """
        Содержимое поста на главной странице должно соответствовать ожиданиям
        """
        response = self.authorized_author.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        self.check_post(first_object)

    def test_group_page_show_correct_context(self):
        """
        Содержимое поста на странице группы должно соответствовать ожиданиям.
        """
        response = self.authorized_author.get(reverse(
            'posts:group_posts',
            kwargs={'slug': 'test-slug'}
        )
        )
        first_object = response.context['page_obj'][0]
        self.check_post(first_object)

    def test_profile_page_show_correct_context(self):
        """
        Содержимое поста на странице профиля должно соответствовать ожиданиям.
        """
        response = self.authorized_author.get(reverse(
            'posts:profile',
            kwargs={'username': self.author}
        )
        )
        first_object = response.context['page_obj'][0]
        self.check_post(first_object)

    def test_post_appears_on_index_page(self):
        """
        Тест того, что пост с данным содержанием и с принадлежность к данной
        группе был успешно создан.
        """
        self.assertTrue(
            Post.objects.filter(
                text=(
                    'Тестовый пост: '
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
                group=self.group
            ).exists()
        )

    def test_post_not_in_another_group(self):
        """
        Пост не попал в группу, для которой не был предназначен, то есть,
        он там отсутствует.
        """
        self.assertFalse(
            Post.objects.filter(
                text=(
                    'Тестовый пост номер: '
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
                group=self.group_without_needed_post
            ).exists()
        )
