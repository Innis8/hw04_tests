# Generated by Django 2.2.16 on 2022-03-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20220307_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='mage',
            field=models.ImageField(blank=True, upload_to='posts/', verbose_name='Картинка'),
        ),
    ]