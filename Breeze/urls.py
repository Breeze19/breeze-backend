from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^19/$', views.nineteen, name='nineteen'),
    url(r'^events/$',views.get_events,name='register'),
    url(r'^events/sports/$',views.sports, name='sports'),
    url(r'^events/technical/$',views.technical, name='technical'),
    url(r'^events/cultural/$',views.cultural, name='cultural'),
    url(r'^events/(?P<category>\w+)/(?P<subcategory>\w+)$',views.specificEventView, name='events'),
    url(r'^signin/', views.signin, name='register'),
    url(r'^signup/', views.register, name='register'),
    url(r'^login/$',views.login1,name='login'),
    url(r'^createaccount/$',views.createaccount,name='createaccount'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^gallery/$', views.gallery,name='gallery'),
    url(r'^sponsors/$',views.sponsors,name='sponsors'),
    url(r'^team/$', views.team, name='team'),
    url(r'^events/register/$',views.event_register2, name='event_register2'),
    url(r'^accomodation/$', views.accomodation, name='accomodation_brochure'),
    url(r'^19/accomodation/$', views.accomodation_brochure, name='accomodation_brochure'),
    url(r'^19/sportshandbook/$',views.sports_handbook,name='sports_handbook'),
    url(r'^19/transport/$',views.transport,name='transport_handbook'),
    url(r'^forgotpassmail',views.forgotpassmail,name='forgotpassmail'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^partners/$', views.partners, name='partners'),
    url(r'^accommodation/register/$',views.accom_register, name='accom_register'),
    url(r'^pronights/', views.pronights, name='pronights'),
    url(r'^forgotpass/', views.forgotmail, name='forgotmail'),
    url(r'^forgotPassword/(?P<hashkey>\w+)', views.forgot, name='forgot'),
    url(r'^id/$',views.id,name='id'),
    url(r'^genid/$',views.gen_id,name='gen_id'),
    url(r'^clubdashboard/', views.clubdashboard, name='clubdashboard'),
    url(r'^updateremarks/', views.updateremarks, name='updateremarks'),
    url(r'^viewcsv/(?P<key>\w+)$',views.get_reg_csv,name='get_reg_csv'),
    url(r'^viewreg/(?P<key>\w+)/$',views.view_reg,name="view_reg"),
    url(r'^viewreg/(?P<key>\w+)/(?P<clubname>\w+)$',views.view_reg_club,name="view_reg_club")
]
