# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
# from posts.models import Group, Post
# from django.urls import reverse
# from datetime import datetime

# User = get_user_model()


# class PaginatorViewsTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.author = User.objects.create_user(username='author')
#         cls.authorized_author = Client()
#         cls.authorized_author.force_login(cls.author)

#         cls.group = Group.objects.create(
#             title='Тестовая группа',
#             slug='test-slug',
#             description='Тестовое описание',
#         )

#     for i in range(1, 14):
#         cls.post = Post.objects.create(
#             author=cls.author,
#             pub_date=datetime.now(),
#             text=(f'Тестовый пост номер {i}: '
#             'Европейский союз был создан Маастрихтским договором 1992 '
#             'года, вступившим в силу 1 ноября 1993 года, на основе '
#             'Европейского экономического сообщества и нацелен на '
#             'региональную интеграцию. ЕС — международное образование, '
#             'сочетающее признаки международной организации '
#             '(межгосударственности) и государства (надгосударственности), '
#             'однако юридически он не является ни тем, ни другим. С помощью'
#             ' стандартизированной системы законов, действующих во всех '
#             'странах союза, был создан общий рынок, гарантирующий '
#             'свободное передвижение (движение) людей, товаров.'
#             ),
#             group=cls.group
#         )
#         print(cls.post.text)
#         print(cls.post.pub_date)


#     def test_first_page_contains_ten_records(self):
#         response = self.authorized_author.get(reverse('posts:index'))
#         # Проверка: количество постов на первой странице равно 10.
#         self.assertEqual(len(response.context['page_obj']), 10)

#     def test_second_page_contains_three_records(self):
#         # Проверка: на второй странице должно быть три поста.
#         response = self.authorized_author.get(
#             reverse('posts:index') + '?page=2'
#         )
#         self.assertEqual(len(response.context['page_obj']), 3)

#     def test_index_page_show_correct_context(self):
#         """
#         Содержимое поста на главной странице должно соответствовать ожиданиям
#         """
#     # В models указана сортировка постов по убывающей дате. Значит, нулевой
#     # индекс - это последний созданный пост, в данном случае 13-й.
#     # функция print() используется для того, чтобы тест затрачивал
#     # некоторое время на печатание каждого поста. Иначе, без print()
#     # тестовые маленькие тесты создаются слишком быстро, практически в одну
#     # миллисекунду, и не могут быть правильно отсортированы.
#     # В случае надобности, метод сортировки можно менять в models
#         response = self.authorized_author.get(reverse('posts:index'))
#         first_object = response.context['page_obj'][0]
#         post_author_0 = first_object.author
#         post_text_0 = first_object.text
#         post_group_0 = first_object.group
#         self.assertEqual(post_author_0, self.author)
#         # print(self.author)
#         self.assertEqual(
#             post_text_0,
#             'Тестовый пост номер 13: '
#             'Европейский союз был создан Маастрихтским договором 1992 '
#             'года, вступившим в силу 1 ноября 1993 года, на основе '
#             'Европейского экономического сообщества и нацелен на '
#             'региональную интеграцию. ЕС — международное образование, '
#             'сочетающее признаки международной организации '
#             '(межгосударственности) и государства (надгосударственности), '
#             'однако юридически он не является ни тем, ни другим. С помощью'
#             ' стандартизированной системы законов, действующих во всех '
#             'странах союза, был создан общий рынок, гарантирующий '
#             'свободное передвижение (движение) людей, товаров.'
#         )
#         self.assertEqual(post_group_0, self.group)

#     def test_group_page_show_correct_context(self):
#         """
#         Содержимое поста на странице группы должно соответствовать ожиданиям.
#         """

#         response = self.authorized_author.get(reverse(
#             'posts:group_posts',
#             kwargs={'slug':'test-slug'}
#             )
#         )
#         first_object = response.context['page_obj'][0]
#         post_author_0 = first_object.author
#         post_text_0 = first_object.text
#         post_group_0 = first_object.group
#         self.assertEqual(post_author_0, self.author)
#         # print(self.author)
#         self.assertEqual(
#             post_text_0,
#             'Тестовый пост номер 13: '
#             'Европейский союз был создан Маастрихтским договором 1992 '
#             'года, вступившим в силу 1 ноября 1993 года, на основе '
#             'Европейского экономического сообщества и нацелен на '
#             'региональную интеграцию. ЕС — международное образование, '
#             'сочетающее признаки международной организации '
#             '(межгосударственности) и государства (надгосударственности), '
#             'однако юридически он не является ни тем, ни другим. С помощью'
#             ' стандартизированной системы законов, действующих во всех '
#             'странах союза, был создан общий рынок, гарантирующий '
#             'свободное передвижение (движение) людей, товаров.'
#         )
#         self.assertEqual(post_group_0, self.group)

#     def test_profile_page_show_correct_context(self):
#     """
#     Содержимое поста на странице профиля должно соответствовать ожиданиям.
#     """

#         response = self.authorized_author.get(reverse(
#             'posts:profile',
#             kwargs={'username':self.author}
#             )
#         )
#         first_object = response.context['page_obj'][0]
#         post_author_0 = first_object.author
#         post_text_0 = first_object.text
#         post_group_0 = first_object.group
#         self.assertEqual(post_author_0, self.author)
#         # print(self.author)
#         self.assertEqual(
#             post_text_0,
#             'Тестовый пост номер 13: '
#             'Европейский союз был создан Маастрихтским договором 1992 '
#             'года, вступившим в силу 1 ноября 1993 года, на основе '
#             'Европейского экономического сообщества и нацелен на '
#             'региональную интеграцию. ЕС — международное образование, '
#             'сочетающее признаки международной организации '
#             '(межгосударственности) и государства (надгосударственности), '
#             'однако юридически он не является ни тем, ни другим. С помощью'
#             ' стандартизированной системы законов, действующих во всех '
#             'странах союза, был создан общий рынок, гарантирующий '
#             'свободное передвижение (движение) людей, товаров.'
#         )
#         self.assertEqual(post_group_0, self.group)
