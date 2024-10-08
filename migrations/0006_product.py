# Generated by Django 5.0.6 on 2024-09-02 15:45

import bboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0005_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название продукта')),
                ('description', models.TextField(verbose_name='Описание продукта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена продукта')),
                ('image', models.ImageField(upload_to=bboard.models.get_timetap_path, verbose_name='Изображение продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['name'],
            },
        ),
    ]
