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

from notebook.forms import NotebookCreateForm, NotebookRecordCreateForm
from notebook.models import Notebook, NotebookRecord


class HomeView(generic.TemplateView):
    """
    домашняя страница: главное меню для регистрации и входа и выхода, кнопки управления.
    основное окно - три колонки: клиенты, сообщения и рассылки пользователя
    """
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ids = Notebook.objects.filter(owner=self.request.user).values_list('id', flat=True)
        last_notebook_id = 1
        if ids:
            last_notebook_id = ids.order_by('-id')[0]
        else:
            pass       # блокнот нужно создать

        print(f"last_notebook_id: {last_notebook_id}")
        if not isinstance(self.request.user, AnonymousUser):
            context.update({
                'notebooks': Notebook.objects.all().filter(owner=self.request.user),
                'last_notebook_id': last_notebook_id,
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
        # print(f"request.user: {request.user}")
        # эта песня посвещена борьбе за мир!
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
    model = NotebookRecord
    form_class = NotebookRecordCreateForm
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
        data = NotebookRecordCreateForm(request.POST)  # ФОРМА А НЕ ВИД!!!
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
