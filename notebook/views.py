import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from typing_extensions import Any

from notebook.forms import NotebookCreateForm, RecordCreateForm
from notebook.models import Notebook, Record


class HomeView(generic.TemplateView):
    """
    домашняя страница: главное меню для регистрации и входа и выхода, кнопки управления.
    основное окно -
    """
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not isinstance(self.request.user, AnonymousUser):
            notebooks = Notebook.objects.filter(owner=self.request.user)
            notebooks_count = notebooks.count()
            last_notebook_id = 0
            records = []
            if notebooks_count:
                if notebooks_count == 1:
                    last_notebook_id = notebooks[0].id
                    records = notebooks[0].records
                else:
                    ids = notebooks.values_list('id', flat=True)
                    if ids:
                        last_notebook_id = ids.order_by('-id')[0]
                        # records = notebooks[last_notebook_id].records
            else:  # блокнот нужно создать
                new_notebook = Notebook.objects.create(title="блокнот 1",
                                                       owner=self.request.user)
                last_notebook_id = new_notebook.id
                print(f"last_notebook_id: {last_notebook_id}")

            context.update({
                'notebooks': notebooks,
                'last_notebook_id': last_notebook_id,
                'records': records,
            })
        return context


class NotebookCreateView(generic.CreateView):
    """
    переход к форме нового сообщения
    """
    model = Notebook
    form_class = NotebookCreateForm
    template_name = 'new_notebook.html'
    context_object_name = 'notebook'

    extra_context = {
        'title': 'Новая записная книжка',
    }
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.model.owner = self.request.user
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs) -> Any:
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user
        data = NotebookCreateForm(request.POST)  # ФОРМА А НЕ ВИД!!!

        print(f"request.POST: {request.POST}")
        # print(f"request.user: {request.user}")
        # эта песня посвещена борьбе за мир!
        print(f"data: {data}")
        if data.is_valid():
            data.instance.owner = request.user
            update = data.save(commit=False)
            update.owner = request.user
            update.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            # print(f"request.POST: {request.POST}")
            # print(f"data: {data}")
            # errors = self.get_form().errors
            # print(f"errors: {errors}")
            # kwargs['errors_data'] = self.get_form().errors
            return HttpResponseRedirect(reverse('errors'))


class RecordCreateView(generic.CreateView):
    """
    переход к форме новой записи
    """
    model = Record
    form_class = RecordCreateForm
    template_name = 'new_record.html'
    context_object_name = 'record'

    extra_context = {
        'title': 'Новая запись',
    }
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.model.owner = self.request.user
        # self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        """
        :return:
        набор данных, которые будут переданы в конструктор формы создания/редактирования
        """
        kwargs = self.kwargs
        # print(f"get_form_kwargs: {kwargs}")
        notebook_id = kwargs.get('pk')
        # print(f"notebook_id: {notebook_id}")

        if notebook_id:
            notebook = get_object_or_404(Notebook, id=notebook_id)
            number = notebook.records.count() + 1
            kwargs.update({'number': number})

        print(f"get_form_kwargs in self: {kwargs}")
        return kwargs

    def post(self, request, *args, **kwargs) -> Any:
        print('/' * 100)
        print(f"request.POST: {request.POST}")
        request.POST = request.POST.copy()
        # request.POST['owner'] = request.user
        data = RecordCreateForm(request.POST)  # ФОРМА А НЕ ВИД!!!
        print(f"data to save: {data}")
        # print(f"request.user: {request.user}")
        # эта песня посвещена борьбе за мир!
        if data.is_valid():
            # data.instance.owner = request.user

            update = data.save(commit=False)
            # update.owner = request.user
            update.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            # print(f"request.POST: {request.POST}")
            # print(f"data: {data}")
            # errors = self.get_form().errors
            # print(f"errors: {errors}")
            # kwargs['errors_data'] = self.get_form().errors
            return HttpResponseRedirect(reverse('errors'))


class RecordsListView(generic.ListView):
    """
    Записи конкретного блокнота
    """
    model = Record
    template_name = "notebook_records_list.html"
    context_object_name = 'records'
    paginate_by = 50

    def get_queryset(self):
        notebook_id = self.kwargs.get('pk')
        if notebook_id:
            queryset = Record.objects.filter(notebook=notebook_id).order_by('created_at')
            # if self.kwargs.get('show_all', False):
            #     queryset = cache.get('all_mailing_list_queryset')
            #     if not queryset:
            #         queryset = NotebookRecord.objects.all().order_by('id')
            #         cache.set('all_mailing_list_queryset', queryset, 60 * 2)
            # else:
            #     queryset = cache.get('mailing_list_queryset')
            #     if not queryset:
            #         queryset = Mailing.objects.all().filter(owner=self.request.user).order_by('id')
            #         cache.set('mailing_list_queryset', queryset, 60 * 2)
            return queryset
        else:
            return None
