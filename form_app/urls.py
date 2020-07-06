from django.conf.urls.static import static
from django.conf.urls import url, include
from form_app import views
from form_project import settings

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
        [
              url(r'^admin_view/(?P<id>[A-Za-z_0-9\-]+)', views.admin_view, name='admin_view'),
              url(r'^admin_view/', views.admin_view, name='admin_view'),
              url(r'^form_details/', views.form_details, name='form_details'),
              url(r'^user_form/', views.user_form, name='user_form'),
              url(r'^signup/', views.signup, name='signup'),
              url(r'^signin/', views.signin, name='signin'),
              url(r'^', views.signin),
        ]

# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)