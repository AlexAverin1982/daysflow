from django.urls import path
from . import views
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("new_notebook/", views.NotebookCreateView.as_view(), name="new_notebook"),
    # path("errors/", views.ErrorsView.as_view(), name="errors"),
    path("notebook/<int:pk>/", views.RecordsListView.as_view(), name="notebook_records"),
    path("notebook_details/<int:pk>/", views.NotebookDetailsView.as_view(), name="notebook_details"),
    path("edit_notebook_title/<int:pk>/", views.NotebookTitleView.as_view(), name="edit_notebook_title"),
    path("new_record/<int:pk>/", views.RecordCreateView.as_view(), name="new_record"),
    path("record/<int:pk>/", views.RecordDetailsView.as_view(), name="record_details"),
    path("error/<int:pk>/", views.ErrorView.as_view(), name="error"),
    # path("new_record_text/<int:pk>/", views.RecordTextCreateView.as_view(), name="new_record_text"),
]
