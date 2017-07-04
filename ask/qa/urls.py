from django.conf.urls import url

from django.contrib import admin
from qa.views import *
admin.autodiscover()

urlpatterns = [
               url(r'^question/(?P<qa_id>\d+)/', question, name='question'),
               url(r'^popular/', popular, name='popular'),
               url(r'^ask/', ask, name='ask'),
               url(r'^$', main, name='main'),
               url(r'^login/', my_login, name='login'),
               url(r'^signup/', signup, name='signup'), ]
