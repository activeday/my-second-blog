from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from mysite.core import views as core_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^apartments/$', core_views.list_view, name='apartments'),
    url(r'^(?P<pk>[0-9]+)/$', core_views.DetailsView.as_view(), name='detail'),
    url(r'^$', core_views.home, name='home'),
    url(r'^baze_test/$', core_views.baze_test, name='baze_test'),
 
    #authentication views 
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^accounts/', include('allauth.urls')),
    #disabled views 
    #url(r'^apartments/$', core_views.apartments_page, name='apartments'),
    #url(r'^apartments/$', core_views.apartments_page.as_view()),
    #url(r'^apartmentdetail/(?P<id>\d+)/', core_views.apartment_detail, name="apartmentdetail"),
 #url(r'^apartments/$', core_views.IndexView.as_view(), name='apartments'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
