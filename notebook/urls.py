from django.urls import path
from . import views

urlpatterns = [
    path("new_notebook/", views.ClientCreateView.as_view(), name="new_notebook"),
    # path("new_notebook/", views.ClientCreateView.as_view(), name="pages"),
]
