# Generated by Django 4.2.11 on 2024-10-19 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default='2024-10-16 18:07:49.51184+00'),
            preserve_default=False,
        ),
    ]