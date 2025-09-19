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


class ErrorMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название ошибки", unique=True)
