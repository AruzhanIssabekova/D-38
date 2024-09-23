from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from precise_bbcode.fields import BBCodeTextField
from datetime import datetime
from os.path import splitext
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField, ThumbnailerFileField

class MyModel(models.Model):
    image = ThumbnailerImageField(upload_to='uploads/')

class Thumbnails(models.Model):
    image = ThumbnailerImageField(upload_to='images/')
    file = ThumbnailerFileField(upload_to='files/')

def get_timetap_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название продукта')
    description = models.TextField(verbose_name='Описание продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продукта')
    image = models.ImageField(verbose_name='Изображение продукта', upload_to=get_timetap_path)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']


# def validate_even(val):
#     if val % 2 != 0:
#         raise ValidationError('Число %(value)s нечетно', code='Error price', params={'value': val})
    

# class MinMaxValueVallidator:
#     def __init__(self, min_value, max_value):
#         self.min_value = 5
#         self.max_value = 20

#     def __call__(self, val):
#         if val < self.min_value or val > self.max_value:
#             raise ValidationError(
#                 'Введенное значение далжно находиться в дипазоне от %(min)s до %(max)s',
#                 code='out_of_range',
#                 params={'min': self.min_value, 'max': self.max_value}
#             )

class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Spare(models.Model):
    name = models.CharField(max_length=30)

class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare)
    notes = GenericRelation('Note')

class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return self.annotate(cnt=models.Count('bb')).order_by('-cnt')

class RubricManager(models.Manager):
    def get_queryset(self):
        return RubricQuerySet(self.model, using=self._db)
    
    def order_by_bb_count(self):
        return self.get_queryset().order_by_bb_count()

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True)
    objects = models.Manager()
    bbs = RubricManager()
    # bbs = RubricManager()

    def get_absolute_url(self):
        return "/bboard/%s/" % self.pk

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['order','name']



class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('price')

class Bb(models.Model):
    def clean(self):
        errors ={}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите правильное значение')
        if errors:
            errors[NON_FIELD_ERRORS] = ValidationError('Ошибка в модели')

    objects = models.Manager()
    by_price = BbManager()

    class Kinds(models.TextChoices):
        BUY = 'b', "Куплю"
        SELL = 's', "Продам"
        EXCHANGE = 'c', "Обменяю"
        RENT = 'r'

    kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.SELL)
    rubric = models.ForeignKey(Rubric, null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(verbose_name='Опубликованно')
    content2 = BBCodeTextField(null=True, blank=True, verbose_name='Описание c помощью BBcode')

    def title_and_price(self):
        if self.price:
            return '%s (%.2f)' % (self.title, self.price)
        else:
            return self.title

    title_and_price.short_description = 'Название и цена'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['rubric']
        # order_with_respect_to = 'rubric'


class Measure(models.Model):
    class Measurements(float, models.Choices):
        METERS = 1.0, 'Метры'
        FEET = 0.3048, 'Футы'
        YARDS = 0.9144, 'Ярда'

    measurement = models.FloatField(choices=Measurements.choices)



class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')


class Message(models.Model):
    content = models.TextField()

class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, parent_link=True)

class RevRubric(Rubric):
    class Meta:
        proxy =True
        ordering = ['-name']

def get_timetap_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])

class Img(models.Model):
    img = models.ImageField(verbose_name='Изображение', upload_to=get_timetap_path)
    desc = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'