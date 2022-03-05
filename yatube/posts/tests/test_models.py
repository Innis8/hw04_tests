from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост длиной больше 15 символов',
        )

    def test_post_models_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        expected_value = post.text[:15]
        self.assertEqual(expected_value, str(post))

    def test_verbose_name_post_model(self):
        """Проверяем, что verbose_name в полях - ожидаемый"""
        post = PostModelTest.post
        verbose_field = {
            'text': 'Текст поста',
            'pub_date': 'Время создания',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected_value in verbose_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name,
                    expected_value
                )

    def test_help_text_post_model(self):
        """Проверяем, что help_text в полях - ожидаемый"""
        post = PostModelTest.post
        help_field = {
            'text': 'Текст нового или редактируемого поста',
            'pub_date': 'Время создание поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой относится пост. Необязательно.'
        }
        for value, expected_value in help_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text,
                    expected_value
                )


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    def test_group_models_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = GroupModelTest.group
        expected_value = group.title
        self.assertEqual(expected_value, str(group))

    def test_verbose_name_group_model(self):
        """Проверяем, что verbose_name в полях - ожидаемый"""
        group = GroupModelTest.group
        verbose_field = {
            'title': 'Группа',
            'slug': 'Читабельная slug-ссылка',
            'description': 'Описание группы',
        }
        for value, expected_value in verbose_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name,
                    expected_value
                )

    def test_help_text_group_model(self):
        """Проверяем, что help_text в полях - ожидаемый"""
        group = GroupModelTest.group
        help_field = {
            'title': 'Название группы',
            'slug': (
                'Может состоять из символов латиницы, '
                'цифр, нижнего подчеркивания и дефиса '
            ),
            'description': 'Расскажите, о чём эта группа',
        }
        for value, expected_value in help_field.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text,
                    expected_value
                )
