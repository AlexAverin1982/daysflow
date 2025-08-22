from django import forms

from .models import Notebook
from .mixins import FormControlMixin
# from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class NotebookCreateForm(FormControlMixin, forms.ModelForm):
    """
    Форма добавления блокнота
    """
    class Meta:
        model = Notebook
        fields = ['title', ]
