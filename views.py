from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect, Http404, StreamingHttpResponse, FileResponse, HttpResponseForbidden
from .models import Bb, Rubric, Comment, Img 
from django.template import loader
from .forms import BbForm, RegisterUserForm, SearchForm, ImgForm, ImgNonModel
from django.urls import reverse_lazy, reverse
from django.template.loader import get_template, render_to_string
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView, DayArchiveView, DateDetailView, WeekArchiveView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.forms.models import BaseModelFormSet
from django.core.exceptions import ValidationError
from precise_bbcode.bbcode import get_parser
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
import os
from django.conf import settings

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('document')
        if uploaded_file:
            file_path = os.path.join(settings.MEDIA_ROOT, 'files', uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        return render(request, 'upload.html', {'message': 'File uploaded successfully!'})

    return render(request, 'upload.html')


def display_files(request):
    files_dir = os.path.join(settings.MEDIA_ROOT, 'files')
    file_list = []

    if os.path.exists(files_dir):
        for file_name in os.listdir(files_dir):
            file_path = os.path.join('files', file_name)
            file_list.append({
                'name': file_name,
                'url': os.path.join(settings.MEDIA_URL, file_path),
            })

    context = {
        'files': file_list,
    }
    return render(request, 'display.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'bboard/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'bboard/product_list.html', {'products': products})



def get_comments(request):
    comments = Comment.objects.all().values('id', 'text', 'created_at')
    return JsonResponse(list(comments), safe=False)

def get_comment_by_id(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return JsonResponse({'id': comment.id, 'text': comment.text, 'created_at': comment.created_at})

def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'status': 'success'})
    except Comment.DoesNotExist:
        return HttpResponseNotFound({'status': 'comment not found'})


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    # bbf = BbForm(initial={'price': 1000.0})
    success_url = '/bboard/detail/{rubric_id}'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['rubrics'] = Rubric.objects.all()
    #     return context
    
    

class UserCreateView(CreateView):
    template_name = 'bboard/createuser.html'
    form_class = RegisterUserForm
    # success_url = '/bboard/'

def redirect_to_index(request):
    return HttpResponseRedirect(reverse('bboard:index'))
    # return HttpResponsePermanentRedirect('https://www.instagram.com/')

def fetch_data():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def split_data(data, page_size):
    pages = []
    for i in range(0, len(data), page_size):
        pages.append(data[i:i + page_size])
    return pages



# def index(request):
#     data = fetch_data()
#     page_size = 10
#     pages = split_data(data, page_size)

#     page_num = int(request.GET.get('page', 1)) - 1
#     if page_num < 0 or page_num >= len(pages):
#         page_num = 0

#     context = {
#         'bbs': pages[page_num],
#         'page_num': page_num + 1,
#         'total_pages': len(pages),
#     }
#     return render(request, 'bboard/index.html', context)


def index(request):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    url1 = reverse('bboard:index')
    # print(request.headers['Content-Language'])
    context = {'bbs': page.object_list, 'rubrics': rubrics, 'url1': url1, 'page': page}
    return render(request, 'bboard/index.html', context)

    # date = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10000.0}
    # return JsonResponse(date, json_dumps_params={'ensure_ascii': False})

def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    url = reverse('bboard:by_rubric', args=(rubric_id,))

    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric, 'url': url}
    return render(request, 'bboard/by_rubric.html', context)

def redirect_to_rubric(request, rubric_id):
    return redirect('bboard:by_rubric', rubric_id=rubric_id)

# @require_http_methods(['GET', 'POST'])
def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)
    
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def detail(request, bb_id):

    # parser = get_parser()
    # bb = Bb.objects.get(pk=bb_id)
    # parsed_content = parser.render(bb.content)
    # context = {'bb': bb, 'parsed_content': parsed_content}
    try:
        bb = get_object_or_404(Bb, pk=bb_id)
        return HttpResponse(f'Название: {bb.title}, Описание: {bb.content}, Дата публикации: {bb.published}')
    except Bb.DoesNotExist:
        return HttpResponseNotFound(('<h1>Такого объявления не существует</h1>'))
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.all()
        return context


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    # initial = {'price': 0.0}

    bbf = BbForm(initial={'price': 1000.0})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object
    
    def get_success_url(self):
        return reverse('bboard:by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context



class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['url1'] = reverse_lazy('bboard:index')
        return context
    


class BbMonthArchiveView(DayArchiveView):
    model = Bb
    date_field = 'published'
    month_format = "%m"
    template_name = 'bboard/bb_archive_month.html'


class BbRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('bboard:detail', kwargs={'pk': self.kwargs['pk']})


class BbByRubricView(SingleObjectMixin ,ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'   

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_rubric'] = self.object
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = context['object_list']
        return context
    
    def get_queryset(self):
        return self.object.bb_set.all()
    



def edit(request, pk):
    bb = Bb.objects.get(pk=pk)
    if request.method == 'POST':
        bbf = BbForm(request.POST, instance=bb)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/bb_form.html', context)
    else:
        bbf = BbForm(instance=bb)
        context = {'form': bbf}
        return render(request, 'bboard/bb_form.html', context)
        

class RubricBaseFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        names = [form.cleaned_data['name'] for form in self.forms if 'name' in form.cleaned_data]

        if ('Недвижимость' not in names) or ('Еда' not in names) or ('Транспорт' not in names):
            raise ValidationError('Добавьте рубрики Недвижимость, Еда, Транспорт')



def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_delete=True, can_order=True, formset=RubricBaseFormSet)

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.save()
        return redirect('bboard:index')
    else:
        formset = RubricFormSet(queryset=Rubric.objects.all())

    return render(request, 'bboard/rubric.html', {'formset': formset})



def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()
            return redirect('bboard:index')
    else:
        formset = BbsFormSet(instance=rubric)

    return render(request, 'bboard/bbs.html', {'formset': formset, 'current_rubric': rubric})




def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            bbs = Bb.objects.filter(title__icontains=keyword, rubric_id=rubric_id) 
            context = {'bbs': bbs}
            return render(request, 'bboard/search_results.html', context)
    else:
        sf = SearchForm()
    
    context = {'form': sf}
    return render(request, 'bboard/search.html', context)



def formset_processing(request):
    FS = formset_factory(SearchForm, extra=3, can_delete=True, can_order=True)

    if request.method == 'POST':
        formset = FS(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    keyword = form.cleaned_data['keyword']
                    rubric_id = form.cleaned_data['rubric'].pk
                    order = form.clraned_data['ORDER']
            return  render(request, 'bboard/process_result.html')
    else:
        formset = FS()
    context = {'formset': formset}
    return render(request, 'bboard/process_formset.html', context)


def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('bboard:index')
    else:
        form = ImgForm()
    context = {'form': form}
    return render(request, 'bboard/add.html', context)


def addNonModelForm(request):
    if request.method == 'POST':
        form = ImgNonModel(request.POST, request.FILES)
        if form.is_valid():
            desc = form.cleaned_data['desc']
            for img_file in request.FILES.getlist('imgs'):
                img_instance = Img(img=img_file, desc=desc)
                img_instance.save()
            return redirect('bboard:index')
    else:
        form = ImgNonModel()
    context = {'form': form}
    return render(request, 'bboard/addNon.html', context)


def image_list(request):
    images = Img.objects.all()
    return render(request, 'bboard/image_list.html', {'images': images})


def delete_image(request, img_id):
    if request.method == 'POST':
        img = get_object_or_404(Img, pk=img_id)
        img.delete()
        return redirect('bboard:image_list')
    return HttpResponseForbidden("Неверный метод запроса.")