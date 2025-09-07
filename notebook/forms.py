import datetime

from django import forms

from .models import Notebook, NotebookRecord
from .mixins import FormControlMixin
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.shortcuts import redirect, get_object_or_404, render

class NotebookCreateForm(FormControlMixin, forms.ModelForm):
    """
    Форма создания блокнота
    """
    class Meta:
        model = Notebook
        fields = ['title',]


class NotebookRecordCreateForm(FormControlMixin, forms.ModelForm):
    """
    Форма создания записи в блокноте

    добавить поля ссылки на блокнот-владелец и шаблон страницы
    """
    notebook = forms.ModelChoiceField(queryset=Notebook.objects.all(), empty_label=None)
    title = forms.CharField(required=False)


    class Meta:
        model = NotebookRecord
        fields = '__all__'
        widgets = {
            'created_at': DateTimePickerInput(),
        }

    """
    добавить конструктор для заполнения полей по умолчанию
    """
    def __init__(self, *args, **kwargs):
        print(f"args: {args}")
        notebook_id = kwargs.pop('pk', None)
        if not notebook_id:
            if args:
                notebook_id = args[0].get('notebook', None)
        page_number = kwargs.pop('number', None)
        print(f"notepad_id: {notebook_id}")
        notebook = get_object_or_404(Notebook, pk=notebook_id)
        super(NotebookRecordCreateForm, self).__init__(*args, **kwargs)

        # print(f"kwargs: {kwargs}")
        self.fields["notebook"].queryset = Notebook.objects.filter(owner=notebook.owner)
        self.fields['number'].initial = page_number
        self.fields['created_at'].initial = datetime.datetime.now()
        self.fields['notebook'].initial = notebook
