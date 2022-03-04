from posts.forms import PostForm
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

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
        cls.post = Post.objects.create(
            author=cls.author,
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
        print(cls.post.id)
        print(cls.post.group)
        print(cls.post.text)

        cls.form = PostForm()

    def test_create_post_form(self):
        """
        Валидная форма создает пост
        """
        post_count = Post.objects.count()
        form_data = {
            'text': self.post.text,
            'group': self.group.id,
        }
        response = self.authorized_author.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(
            response, reverse(
                'posts:profile',
                kwargs={'username': self.author}
            )
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), post_count+1)
        # Проверяем, что создался ли пост с заданным содержанием
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
                group=self.group.id
            ).exists()
        )
        # Проверяемм, что ничего не упало и страница отдаёт код 200
        self.assertEqual(response.status_code, 200)

    def test_edit_post_form(self):
        """
        Валидная форма редактирует пост
        """
        form_data = {
            'text': self.post.text,
            'group': self.group.id,
        }
        response = self.authorized_author.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            ),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            ),
        )
