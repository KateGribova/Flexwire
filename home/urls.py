from django.urls import path

import home.views

app_name = 'home'

urlpatterns = [
    path(
        '',
        home.views.Landing.as_view(),
        name='landing',
    ),
]
