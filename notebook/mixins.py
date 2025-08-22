class FormControlMixin:
    """
    класс-примесь, чтобы формы выглядели прилично
    """
    def __init__(self, *args, **kwargs):
        # del kwargs['request']
        super(FormControlMixin, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
