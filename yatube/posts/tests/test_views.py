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

        # Не совсем понял, куда перенести данный цикл создания постов.
        # Проверка пагинатора находится не отдельном файле, а
        # тут же, чуть ниже, в виде двух тестовых функций. К тому же,
        # данный цикл используется в функции
        # test_index_page_show_correct_context
        # для проверки содержимого выбранного поста на главной странице
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
        # В models указана сортировка постов по убывающей дате. Значит, нулевой
        # индекс (выбранный пост) - это последний созданный пост, в данном
        # случае 13-й. функция print() используется для того, чтобы тест
        # затрачивал некоторое время на печатание каждого поста. Иначе,
        # без print(), без вывода на экран, тестовые посты создаются слишком
        # быстро, практически в одну и ту же миллисекунду, и не могут быть
        # правильно отсортированы по времени создания. В случае надобности,
        # метод сортировки можно менять в models. Остальные дебажные посты,
        # печатающие id, группу и тд, удалил.
            print(cls.post.text)

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

    def test_index_page_show_correct_context(self):
        """
        Содержимое поста на главной странице должно соответствовать ожиданиям
        """
        # В models указана сортировка постов по убывающей дате. Значит, нулевой
        # индекс (выбранный пост) - это последний созданный пост, в данном
        # случае 13-й. функция print() используется для того, чтобы тест
        # затрачивал некоторое время на печатание каждого поста. Иначе,
        # без print(), без вывода на экран, тестовые посты создаются слишком
        # быстро, практически в одну и ту же миллисекунду, и не могут быть
        # правильно отсортированы по времени создания. В случае надобности,
        # метод сортировки можно менять в models
        response = self.authorized_author.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author
        post_text_0 = first_object.text
        post_group_0 = first_object.group
        self.assertEqual(post_author_0, self.author)
        self.assertEqual(
            post_text_0,
            'Тестовый пост номер 13: '
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
        self.assertEqual(post_group_0, self.group)

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
        post_author_0 = first_object.author
        post_text_0 = first_object.text
        post_group_0 = first_object.group
        # Ломал голову, не мог догадаться, как их вынесты отдельно, чтоб
        # можно было тестовыми функциями к этим проверкам обращаться.
        self.assertEqual(post_author_0, self.author)
        self.assertEqual(
            post_text_0,
            'Тестовый пост номер 13: '
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
        self.assertEqual(post_group_0, self.group)

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
        post_author_0 = first_object.author
        post_text_0 = first_object.text
        post_group_0 = first_object.group
        post_id_0 = first_object.id
        self.assertEqual(post_author_0, self.author)
        self.assertEqual(
            post_text_0,
            'Тестовый пост номер 13: '
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
        self.assertEqual(post_group_0, self.group)
        self.assertEqual(post_id_0, 13)

    def test_post_appears_on_index_page(self):
        """
        Тест того, что пост с данным содержанием и с принадлежность к данной
        группе был успешно создан.
        """
        self.assertTrue(
            Post.objects.filter(
                text=(
                    'Тестовый пост номер 13: '
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
                    'Тестовый пост номер 13: '
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
