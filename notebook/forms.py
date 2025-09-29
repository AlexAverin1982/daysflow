import datetime

from django import forms

from .models import Notebook, Record, ErrorMessage, RecordDisplaySettings
from .mixins import FormControlMixin
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.shortcuts import redirect, get_object_or_404, render


class NotebookCreateForm(FormControlMixin, forms.ModelForm):
    """
    Форма создания блокнота
    """

    class Meta:
        model = Notebook
        fields = ['title', ]

    def __init__(self, *args, **kwargs):
        """
        конструктор формы, инициализация полей
        """
        # instance = kwargs.get('instance')
        # if instance is not None:
        #     if hasattr(instance, 'owner'):
        #         self.user = instance.owner
        #         print(f"instance.owner self.user: {self.user}")
        # else:
        #     self.user = kwargs.pop('user', None)
        #     print(f"self.user from kwargs: {self.user}")
        # self.request = kwargs.pop("request")

        self.request = kwargs.pop("request", None)  # store value of request
        # print(f"self.request in __init__(): {self.request}")
        # print(f"self.request.user in __init__(): {self.request.user}")
        # print(f" __init__() args: {args}")
        # print(f" __init__() kwargs: {kwargs}")
        super().__init__(*args, **kwargs)
        self.user = None

        if args:
            self.user = args[0].get('owner')

        print(f" __init__() self.user: {self.user}")

    def clean(self):
        """
        проверка данных в форме на корректность
        """
        cleaned_data = super().clean()
        # print('0' * 100)
        # print(f"self.user in clean(): {self.user}")
        """
        проверяем существование блокнота с таким же заголовком
        """
        print(f"cleaned_data: {cleaned_data}")
        new_title = cleaned_data.get('title')
        if new_title:
            titles = Notebook.objects.filter(owner=self.user).values_list('title', flat=True)
            # print(f"titles: {titles}")
            if new_title in titles:
                self._errors["send_stop"] = ErrorMessage.objects.get(id=101)
                raise forms.ValidationError(self._errors["send_stop"])
                # self.add_error('send_stop', 'Время завершения рассылки не указано')

        else:
            count = Notebook.objects.filter(owner=self.request.user).count()
            cleaned_data['title'] = f'Блокнот {count + 1}'
        return cleaned_data


class NotebookTitleForm(FormControlMixin, forms.ModelForm):
    """
    Форма редактирования названия блокнота
    """

    class Meta:
        model = Notebook
        fields = ['title', ]

    def clean(self):
        """
        проверка данных в форме на корректность
        """
        cleaned_data = super().clean()
        user = self.instance.owner
        # print(f"self.instance.owner: {self.instance.owner}")
        """
        проверяем существование блокнота с таким же заголовком
        """
        # print(f"cleaned_data: {cleaned_data}")
        new_title = cleaned_data.get('title')
        if new_title:
            titles = Notebook.objects.filter(owner=user).values_list('title', flat=True)
            # print(f"titles: {titles}")
            if new_title in titles:
                self._errors["send_stop"] = ErrorMessage.objects.get(id=101)
                raise forms.ValidationError(self._errors["send_stop"])

        else:
            count = Notebook.objects.filter(owner=user).count()
            cleaned_data['title'] = f'Блокнот {count + 1}'
        return cleaned_data

    def __init__(self, *args, **kwargs):
        """
        конструктор формы, инициализация полей
        """
        self.request = kwargs.pop("request", None)  # store value of request
        super().__init__(*args, **kwargs)
        if args:
            self.user = args[0].get('owner')


class RecordCreateForm(FormControlMixin, forms.ModelForm):
    """
    Форма создания записи в блокноте

    добавить поля ссылки на шаблон страницы
    """
    notebook = forms.ModelChoiceField(queryset=Notebook.objects.all(), empty_label=None)
    title = forms.CharField(required=False)

    class Meta:
        model = Record
        # fields = '__all__'
        fields = ['title', 'created_at', 'text',  ]
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
        super(RecordCreateForm, self).__init__(*args, **kwargs)

        # print(f"kwargs: {kwargs}")
        self.fields["notebook"].queryset = Notebook.objects.filter(owner=notebook.owner)
        # self.fields['number'].initial = page_number
        self.fields['created_at'].initial = datetime.datetime.now()
        self.fields['notebook'].initial = notebook


class RecordDetailsForm(FormControlMixin, forms.ModelForm):
    number = forms.NumberInput()
    created_at = forms.DateTimeInput()
    title = forms.CharField()
    notebook = forms.ModelMultipleChoiceField(queryset=Notebook.objects.all())
    text = forms.Textarea()


    class Meta:
        model = Record
        fields = ['created_at', 'number', 'title', 'text', ]

        widgets = {
            'created_at': DateTimePickerInput(),
            'number': forms.NumberInput(),
            'text': forms.Textarea(),
        }



        # widgets = {
        #     'send_start': DateTimePickerInput(),
        #     'send_stop': DateTimePickerInput(),
        #     'scheduler_enabled': forms.CheckboxInput(attrs={'class': 'custom-checkbox-class'}),
        #     'scheduler_days_interval': forms.NumberInput(),
        #     'scheduler_hours_interval': forms.NumberInput(),
        #     'scheduler_minutes_interval': forms.NumberInput(),
        #     'scheduler_seconds_interval': forms.NumberInput(),
        # }

    def __init__(self, *args, **kwargs):
        super(RecordDetailsForm, self).__init__(*args, **kwargs)
        # instance = getattr(self, 'instance', None)
        instance = kwargs.get('instance')
        # if instance and instance.pk:
        print(f"instance: {instance}")
        # if instance:
        #     print(f"instance.send_start: {instance.send_start}")
        #     self.fields['send_start'].initial = instance.send_start
        # self.fields['send_start'].widget.attrs['readonly'] = True
        # self.fields['send_stop'].widget.attrs['readonly'] = True

class RecordDisplaySettingsForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = RecordDisplaySettings
        fields = '__all__'  # no use, form is customized, but without it server won't start
        # exclude = ['status']
        STATUS_CHOICES = (('Создана', 'Создана'), ('Запущена', 'Запущена'), ('Завершена', 'Завершена'),)
        widgets = {
            'field0': forms.Select(attrs={'id': 'status_select'}, choices=STATUS_CHOICES),
        }
