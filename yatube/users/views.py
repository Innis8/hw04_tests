# from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.forms import CreationForm
# from users.forms import ContactForm
from django.shortcuts import redirect
# from users.models import Contact


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'

# def only_user_view(request):
#     if not request.user.is_authenticated:
#         # Если пользователь не авторизован -
#         # отправляем его на страницу логина.
#         return redirect('/auth/login/')
#     # Если пользователь авторизован — здесь выполняется полезный код функции.


def authorized_only(func):
    # Функция-обёртка в декораторе может быть названа как угодно
    def check_user(request, *args, **kwargs):
        # В любую view-функции первым аргументом передаётся объект request,
        # в котором есть булева переменная is_authenticated,
        # определяющая, авторизован ли пользователь.
        if request.user.is_authenticated:
            # Возвращает view-функцию, если пользователь авторизован.
            return func(request, *args, **kwargs)
        # Если пользователь не авторизован — отправим его на страницу логина.
        return redirect('/auth/login/')
    return check_user


# Декорируем view-функцию
@authorized_only
def some_view(request):
    return 'Доступно только авторизованным!'

# def user_contact(request):
#     # Проверяем, получен POST-запрос или какой-то другой:
#     if request.method == 'POST':
#         # Создаём объект формы класса ContactForm
#         # и передаём в него полученные данные
#         form = ContactForm(request.POST)

#         # Если все данные формы валидны -
#         # работаем с "очищенными данными" формы
#         if form.is_valid():
#             # Берём валидированные данные формы из словаря form.cleaned_data
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['body']
#             # При необходимости обрабатываем данные
#             # ...
#             # сохраняем объект в базу
#             form.save()

#             # Функция redirect перенаправляет пользователя
#             # на другую страницу сайта, чтобы защититься
#             # от повторного заполнения формы
#             return redirect('/thank-you/')

#         # Если условие if form.is_valid() ложно и
#         # данные не прошли валидацию -
#         # передадим полученный объект в шаблон,
#         # чтобы показать пользователю информацию об ошибке

#         # Заодно заполним все поля формы данными, прошедшими валидацию,
#         # чтобы не заставлять пользователя вносить их повторно
#         return render(request, 'contact.html', {'form': form})

#     # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
#     # пусть пользователь напишет что-нибудь
#     form = ContactForm()
#     return render(request, 'contact.html', {'form': form})
