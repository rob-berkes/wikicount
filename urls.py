from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from polls.models import hits
admin.autodiscover()

post_list=ListView.as_view(model=hits)
post_detail=DetailView.as_view(model=hits)


urlpatterns = patterns('',
    # Examples:
     url(r'^$','polls.views.indexLang', name='home'),
     url(r'^topics.htm$','polls.views.indexTopix'),
     url(r'^spam/(.*)/(.*)/(.*)','polls.views.spam'),
     url(r'^index.htm$','polls.views.indexLang'),
     url(r'^([A-Za-z]{2})/index.htm$','polls.views.indexLang'),
     url(r'^m/([A-Za-z.]{2})/index.htm$','polls.views.mobileIndexLang'),
     url(r'^m/([A-Za-z.]{4,6})/index.htm$','polls.views.mobileIndexLang'),
     url(r'^m/(commons).m/index.htm$','polls.views.mobileIndexLang'),
     url(r'^m/index.html$','polls.views.MobileLanguageList'),
     url(r'^m/index.htm$','polls.views.MobileLanguageList'),
     url(r'^([A-Za-z]{2})/archives.htm$','polls.views.dailypageI18'),
     url(r'^([A-Za-z]{2})/archives/(\d{4})/(\d{1,2})/index.htm$','polls.views.dailypageI18'),
     url(r'^([A-Za-z]{2})/listtop/(\d{4})/(\d{1,2})/index.htm$','polls.views.dailypageI18'),
     url(r'^(commons).m/index.htm$','polls.views.indexLang'),
     url(r'^([A-Za-z]{2})','polls.views.indexLang'),
     url(r'^m/([A-Za-z]{2})/(\w+)$','polls.views.Mobile_Hourly'),
     url(r'^(simple)/index.htm$','polls.views.indexLang'),
     url(r'^([A-Za-z.]{4,6})/index.htm$','polls.views.indexLang'),
     url(r'^search.htm$','polls.views.searchForm'),
     url(r'^search-results/$','polls.views.searchResults'),
     url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/ubuntu/wikicount/urls/static/',}),
     url(r'^([A-Za-z]{2})/static/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/ubuntu/wikicount/urls/static/',}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
#     url(r'^admin/', include(admin.site.urls)),
) +static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
