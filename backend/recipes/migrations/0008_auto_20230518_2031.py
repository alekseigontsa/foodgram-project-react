# Generated by Django 2.2.16 on 2023-05-18 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20230518_2027'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_favorite',
        ),
        migrations.RemoveConstraint(
            model_name='favorite',
            name='user_favorite_diferent',
        ),
    ]
