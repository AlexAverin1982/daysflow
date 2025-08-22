from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from notebook.forms import NotebookCreateForm
from notebook.models import Notebook


class ClientCreateView(generic.CreateView):
    """
    Представление создания блокнота
    """
    model = Notebook
    form_class = NotebookCreateForm
    # fields = ['name', 'price', 'category', 'image', 'description']
    template_name = 'new_notebook.html'
    context_object_name = 'notebook'

    extra_context = {
        'title': 'Новый блокнот',
    }
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.model.owner = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user
        data = NotebookCreateForm(request.POST)
        # print(f"request.user: {request.user}")

        if data.is_valid():
            data.instance.owner = request.user
            update = data.save(commit=False)
            update.owner = request.user
            update.save()
            # data.save_m2m()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            # print(f"request.POST: {request.POST}")
            # print(f"data: {data}")
            # errors = self.get_form().errors
            # print(f"errors: {errors}")
            # kwargs['errors_data'] = self.get_form().errors
            return HttpResponseRedirect(reverse('errors'))

# class MessageListView(generic.ListView):
#     """
#     окно списка сообщений
#     """
#     model = Message
#     template_name = "messages_list.html"
#     context_object_name = 'messages'
#     paginate_by = 50
#
#     def get_queryset(self):
#         queryset = cache.get('messages_list_queryset')
#         if not queryset:
#             queryset = Message.objects.all().filter(owner=self.request.user).order_by('id')
#             cache.set('messages_list_queryset', queryset, 60 * 2)
#         return queryset

