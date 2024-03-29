# Generated by Django 2.2.16 on 2023-05-27 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230522_2058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddConstraint(
            model_name='recipeingredientamount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredientt'),
        ),
    ]
