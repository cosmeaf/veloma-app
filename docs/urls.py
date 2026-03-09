from django.urls import path
from . import views


urlpatterns = [
    path("", views.docs_index, name="docs_index"),
    path("<str:module>/<str:page>/", views.docs_page, name="docs_page"),

]