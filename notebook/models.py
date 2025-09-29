import datetime

from django.db import models
from users.models import CustomUser


class RecordTemplatePart(models.Model):
    """
    модель части шаблона страницы блокнота
    """
    name = models.CharField(max_length=200, verbose_name="имя шаблона страницы блокнота")
    value_type = models.CharField(max_length=200, verbose_name="тип содержимого")
    sec_number = models.IntegerField(verbose_name='Порядковый номер в шаблоне')


class RecordTemplate(models.Model):
    """
    модель шаблона страницы блокнота
    """
    name = models.CharField(max_length=200, verbose_name="имя шаблона страницы блокнота")
    parts = models.ManyToManyField(RecordTemplatePart, verbose_name="Получатели")


class Notebook(models.Model):
    """
    модель записной книжки
    """
    title = models.CharField(max_length=200, verbose_name="Название записной книжки")

    owner = models.ForeignKey(CustomUser, editable=False, on_delete=models.SET_NULL, related_name='notebooks',
                              verbose_name='Владелец', blank=True, null=True)

    created_at = models.DateTimeField(verbose_name="Дата создания", auto_created=True, null=True)

    class Meta:
        verbose_name = "Блокнот"
        verbose_name_plural = "блокноты"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def records_count(self):
        result = Record.objects.filter(notebook__id=self.id).count()
        # result = Notebook.objects.filter(id=self.pk).records.count()
        return result


class RecordDisplaySettings(models.Model):
    """
    хранилище настроек отображения заголовков записей в форме списка
    """
    _number_order = models.IntegerField(default=-1)
    _title_order = models.IntegerField(default=-1)
    _created_at_order = models.IntegerField(default=0)
    _text_order = models.IntegerField(default=-1)
    _title_len = models.IntegerField(default=10)
    _text_len = models.IntegerField(default=10)
    datetime_format = models.CharField(blank=True, default="")

    @property
    def number_order(self):
        return self._number_order

    @property
    def title_order(self):
        return self._title_order

    @property
    def created_at_order(self):
        return self._created_at_order

    def fields(self) -> list:
        result = []
        i = self.number_order

        if  i >= 0:
            result.insert(i, 'number')

        i = self.title_order
        if  i >= 0:
            result.insert(i, 'title')

        i = self.created_at_order
        if i >= 0:
            result.insert(i, 'created_at')

        return result


class Record(models.Model):
    number = models.IntegerField(verbose_name='Номер страницы в блокноте')
    notebook = models.ForeignKey(Notebook, editable=False, on_delete=models.CASCADE, related_name='records',
                                 verbose_name='Блокнот', blank=True, null=True)
    template = models.ForeignKey(Notebook, editable=False, on_delete=models.CASCADE,
                                 related_name='this_template_Records',
                                 verbose_name='Блокнот', blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name="Заголовок записи", blank=True, default='')
    created_at = models.DateTimeField(verbose_name="Дата создания", null=True)

    text = models.TextField(blank=True)

    display_settings = models.ForeignKey(RecordDisplaySettings, editable=False, on_delete=models.SET_NULL,
                                         verbose_name='Настройки отображения записи в списке', blank=True, null=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "записи"
        ordering = ["number"]

    def __str__(self):
        result = f"{self.number}. {self.title}"
        if not self.display_settings:
            if RecordDisplaySettings.objects.count():
                self.display_settings = RecordDisplaySettings.objects.all()[0]
            else:
                self.display_settings =RecordDisplaySettings.objects.create()

        if self.display_settings:
            result = ""
            fieldnames = self.display_settings.fields()
            print(f"fieldnames: {fieldnames}")
            for fild_name in fieldnames:
                if fild_name == 'number':
                    result = f"{result} {self.number}.".strip()
                elif fild_name == 'title':
                    if self.display_settings.title_len:
                        title = self.title[:self.display_settings.title_len]
                    else:
                        title = self.title
                    result = f"{result} {title}.".strip()
                elif fild_name == 'created_at':
                    result = f"{result} {self.created_at}.".strip()

        return result


class ErrorMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название ошибки", unique=True)
