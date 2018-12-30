from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^events/$',views.get_events,name='register'),
    url(r'^events/sports/$',views.sports, name='sports'),
    url(r'^events/technical/$',views.technical, name='technical'),
    url(r'^events/cultural/$',views.cultural, name='cultural'),
    url(r'^events/(?P<category>\w+)/(?P<subcategory>\w+)$',views.specificEventView, name='events'),
    url(r'^signin/', views.login1, name='login'),
    url(r'^signup/', views.register, name='register'),
    url(r'^gallery/$', views.gallery,name='gallery'),
    url(r'^partners/$', views.partners, name='partners'),
    url(r'^team/$', views.team, name='team'),
    url(r'^transport/$', views.transport, name='transport'),
    url(r'^accommodation/$', views.accomodation, name='accomodation'),
    url(r'^events/register/$',views.event_register, name='event_register'),
    url(r'^accommodation/register/$', views.accom_register, name='accom_register'),
    url(r'^events/register2/$',views.event_register2, name='event_register2'),
    url(r'^accommodation/register2/$',views.accom_register2, name='accom_register2'),
    url(r'^events/(?P<category>\w+)/$', views.specificEventView, name='specificView'),
    url(r'^pronights/', views.pronights, name='pronights'),
    url(r'^forgotPassMail/', views.forgotmail, name='forgotmail'),
    url(r'^forgotPassword/(?P<hashkey>\w+)', views.forgot, name='forgot'),
    url(r'^clubdashboard/', views.clubdashboard, name='clubdashboard'),
    url(r'^updateremarks/', views.updateremarks, name='updateremarks'),
    url(r'^me/', views.profile, name='profile'),
    url(r'^18/$', views.eighteen, name='eighteen'),
    url(r'^18/Breeze_2018_Brochure.pdf/', views.pdf_redirect, name='pdf_redirect'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
]
