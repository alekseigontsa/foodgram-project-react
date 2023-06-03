# Generated by Django 2.2.16 on 2023-06-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230527_2111'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipeingredientamount',
            name='unique_ingredientt',
        ),
        migrations.AddConstraint(
            model_name='recipeingredientamount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient'),
        ),
    ]
