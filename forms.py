from django.forms import ModelForm, modelform_factory, DecimalField, IntegerField, formset_factory
from django import forms
from django.forms.widgets import Select
from .models import Bb, Rubric, Img
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']


# BbForm = modelform_factory(Bb,
#                            fields=('title', 'content', 'price', 'rubric'),
#                            labels={'title': 'Название товара'},
#                            help_texts={'rubric': 'Не забудь выбрать!'},
#                            field_classes={'price': IntegerField},
#                            widgets={'rubric': Select(attrs={'size': 8})})


# class BbForm(ModelForm):
#     class Meta:
#         model = Bb
#         fields = ('title', 'content', 'price', 'rubric')
#         labels={'title': 'Название товара'}
#         help_texts={'rubric': 'Не забудь выбрать!'}
#         field_classes={'price': IntegerField}
#         widgets={'rubric': Select(attrs={'size': 8})}



class BbForm(forms.ModelForm):
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание', widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    label='Рубрики', help_text='Не забудь выбрать!',
                                    widget=forms.widgets.Select(attrs={'size': 8}))
    published = forms.DateField(widget=forms.widgets.SelectDateWidget(empty_label=('Выберите год', 'Выберите месяц', 'Выберите число')))

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric', 'published')
        labels = {'title': 'Название товара'}

    def clean_title(self):
        val = self.cleaned_data.get('title')
        if val == "Прошлогодний снег":
            raise ValidationError('К продаже не допускается')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data['content']:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.cleaned_data['price'] < 0:
            errors['price'] = ValidationError('Укажите неотрицательное значение цены')
        if errors:
            raise ValidationError(errors)



class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль повторно')

    captcha = CaptchaField(label = 'Введите текст с картинки', error_messages={'invalid': 'Неправельный текст'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')



    
class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label='Искомое слово')
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label='Рубрика')



class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изображение', validators=[validators.FileExtensionValidator(
        allowed_extensions= ('gif', 'jpg', 'png'))],
        error_messages={
            'invalid_extension': 'Этот формат не поддерживается'})
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImgNonModel(forms.Form):
    imgs = MultipleFileField(label='Выберете файлы', required=False)
    desc = forms.CharField(label='Описание', widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'