from django.conf.urls import url

import eventex.subscriptions.views

urlpatterns = [
    url(r'^$', eventex.subscriptions.views.new, name='new'),
    url(r'^/(\d+)/$', eventex.subscriptions.views.detail, name='detail'),
]
