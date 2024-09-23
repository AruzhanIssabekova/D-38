from django.urls import path, re_path
from .views import (index, by_rubric, BbCreateView, get_comments, get_comment_by_id, 
                    delete_comment, add_and_save, redirect_to_index, detail, redirect_to_rubric, 
                    BbByRubricView, BbDetailView, BbAddView, BbEditView, BbDeleteView, BbIndexView, BbMonthArchiveView,
                    BbDetailView, BbRedirectView, UserCreateView, edit, rubrics, bbs, search, formset_processing, add, addNonModelForm, image_list, delete_image)
from .models import Bb
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = 'bboard'



urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.display_files, name='display_files'),
    path('add-product/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='product_list'),
    path('comments/', get_comments, name='get_comments'),
    path('comments/<int:comment_id>/', get_comment_by_id, name='get_comment_by_id'),
    path('comments/delete/<int:comment_id>/', delete_comment, name='delete_comment'),

    # path('add-and-save/', add_and_save, name='add_and_save'),
    # path('add/', BbCreateView.as_view(), name='add'),
    # path('add/', BbCreateView.as_view(), name='add'),
    path('add/', add, name='add'),
    path('addNonModelForm/', addNonModelForm, name='addNonModelForm'),
    path('images/', image_list, name='image_list'),
    path('images/delete/<int:img_id>/', delete_image, name='delete_image'),
    path('rubrics/', rubrics, name='rubrics'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('edit_bb/<int:pk>/', edit, name='edit_bb'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    path('<int:year>/<int:month>/<int:day>/', BbMonthArchiveView.as_view(), name='month_archive'),


    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('bbs/<int:rubric_id>/', bbs , name='bbs'),
    path('<int:rubric_id>/', BbByRubricView.as_view() , name='by_rubric'),
    path('', index, name='index'),
    # path('', BbIndexView.as_view(), name='index'),
    path('redirect/', redirect_to_index, name='redirect_to_index'),
    # path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'), 
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    # path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbDetailView.as_view(), name='detail'),
    # path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbRedirectView.as_view(), name='old_detail'),
    path('redirect/<int:rubric_id>/', redirect_to_rubric, name='redirect_to_rubric'),

    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('account/password_change/', PasswordChangeView.as_view(template_name='registration/change_password.html', success_url='bboard:password_change_done'), name='password_change'),
    path('account/password_change/done', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('account/password_reset/', PasswordResetView.as_view(template_name='registration/reset_password.html', 
                                                              subject_template_name='registration/reset_subject.txt', email_template_name='registration/reset_email.txt'), 
                                                              name='password_reset'),
    path('account/password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/reset_password_done.html'), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/reset_password_confirm.html'), name='password_reset_confirm'),
    path('account/reset/done/', PasswordResetCompleteView.as_view(template_name='registration/reset_password_complete.html'), name='password_reset_complete'),



    path('search/', search, name='search'),
    path('formset_processing/', formset_processing, name='formset_processing'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

