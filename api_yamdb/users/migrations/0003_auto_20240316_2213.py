# Generated by Django 3.2 on 2024-03-16 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_newuser_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newuser',
            options={'verbose_name': 'пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='newuser',
            name='bio',
            field=models.TextField(blank=True, max_length=20, verbose_name='Биография'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='email',
            field=models.EmailField(max_length=256, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('admin', 'Администратор'), ('moderator', 'Модератор')], default='user', max_length=20, verbose_name='Роль'),
        ),
    ]
