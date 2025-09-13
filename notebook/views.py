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
from notebook.models import Notebook, Record, ErrorMessage


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

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({'request': self.request})
        # print(f"get_form_kwargs kwargs['user']: {self.request.user}")
        return form_kwargs

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.model.owner = self.request.user
    #     self.object.owner = self.request.user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.model.owner = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs) -> Any:
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user
        form_data = NotebookCreateForm(request.POST)  # ФОРМА А НЕ ВИД!!!

        if form_data.is_valid():
            form_data.instance.owner = request.user
            form_data.instance.created_at = datetime.datetime.now()
            update = form_data.save(commit=False)
            update.owner = request.user
            update.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        #     return redirect(reverse_lazy('mailing_details', kwargs={'pk': mailing.id}))
        else:
            print(f"request.POST: {request.POST}")
            print(f"form_data: {form_data}")
            # errors = self.get_form().errors
            # print(f"errors: {errors}")
            # kwargs['errors_data'] = self.get_form().errors
            return redirect(reverse_lazy('error', kwargs={'pk': 101}))



        #     # return reverse_lazy('errors', kwargs={'errors': errors})
        #     result = HttpResponseRedirect(reverse_lazy('errors', kwargs={'errors': errors}))
        #     # print(f"-----------result: {result}")
        #     return result


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not isinstance(self.request.user, AnonymousUser):
            notebook_id = self.kwargs.get('pk')
            # print('/' * 100)
            # print(f"notebook_id: {notebook_id}")
            context.update({'notebook_id': notebook_id})
            # mailings_list = []
            # mailings = Mailing.objects.filter(owner=self.request.user)
            # for m in mailings:
            #     m_dict = {'id': m.id, 'topic': m.message.topic, 'message_id': m.message.id,
            #               'total_attempts': Attempt.objects.filter(mailing=m.id).count(),
            #               'successful_attempts': Attempt.objects.filter(mailing=m.id).filter(
            #                   is_successful=True).count(), }
            #     if m_dict.get('total_attempts'):
            #         mailings_list.append(m_dict)
            #
            # context.update({
            #     'total_attempts_count':
            #         Attempt.objects.all().filter(owner=self.request.user).count(),
            #     'successful_attempts_count':
            #         Attempt.objects.all().filter(owner=self.request.user).filter(is_successful=True).count(),
            #     'mailings_list': mailings_list,
            #     # 'clients_count':
            #     #     Client.objects.all().filter(owner=self.request.user).count()
            # })
        return context

    def get_queryset(self):
        notebook_id = self.kwargs.get('pk')
        # print('/' * 100)
        # print(f"notebook_id: {notebook_id}")
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

    # def get(self, request, *args, **kwargs) -> Any:
    #     print('/' * 100)
    #     print(f"kwargs: {kwargs}")
    #     notebook_id =


class ErrorView(generic.DetailView):
    """
    сообщение об ошибках при редактировании или создании объектов
    """
    template_name = 'error_message.html'

    model = ErrorMessage
    context_object_name = 'error_message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            # 'owner': self.model.owner,
            'user': self.request.user,
        })

        return context

    # def get(self, request, **kwargs):
    #     error_message = get_object_or_404(ErrorMessage, pk=kwargs.get('error_id', -1))
    #     # if kwargs.get('disable'):
    #     #     mailing = get_object_or_404(Mailing, pk=kwargs.get('pk', -1))
    #     #     mailing.enabled = not mailing.enabled
    #     #     mailing.save()
    #     #     return redirect(request.META['HTTP_REFERER'])
    #     return super().get(self, request, **kwargs)



