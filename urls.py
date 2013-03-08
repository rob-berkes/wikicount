from django.conf.urls.defaults import patterns, include, url
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
     url(r'^$','polls.views.trending', name='home'),
     url(r'^listLast.htm$','polls.views.listLastHour'),
     url(r'^index.htm$','polls.views.trending'),
     url(r'^search.htm$','polls.views.searchForm'),
     url(r'^search-results/$','polls.views.searchResults'),
     url(r'^debug.rob$','polls.views.debug'),
     url(r'^blog.htm$','polls.views.blog'),
     url(r'^trending.htm$', 'polls.views.top3hr'),
     url(r'^cold.htm$', 'polls.views.cold'),
#     url(r'^top.htm$', 'polls.views.top3hr'),
     url(r'^debuts.htm$','polls.views.debuts'),
     url(r'^random.htm$','polls.views.randPage'),
     url(r'^archives/(\d{4})/(\d{1,2})/index.htm$','polls.views.dailypage'),
     url(r'^archives.htm$','polls.views.dailypage'),
     url(r'^listtop/(\d{4})/(\d{1,2})/index.htm$','polls.views.dailypage'),
     url(r'^archives/(\d{4})/(\d{1,2})/(\d{1,2})/index.htm$','polls.views.listtop'),
     url(r'^infoview/(\w+)$','polls.views.infoview'),
#     url(r'^hourly/(\w+)$','polls.views.hourly'),
     url(r'^debug.htm$','polls.views.category_trending'),
     url(r'^cat_top.htm$','polls.views.category_trending'),
     url(r'^files.htm$','polls.views.file_trending'),
     url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':'/tmp/django/wikicount/static/',}),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
#     url(r'^admin/', include(admin.site.urls)),
) +static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
