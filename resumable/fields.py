# -*- coding: utf-8 -*-
from django.forms.fields import FileField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from widgets import ResumableFileInput


class ResumableFileField(FileField):
    default_error_messages = dict(FileField.default_error_messages, **{
            'invalid_mime': _(u'Invalid file type')
    })
    widget = ResumableFileInput

    def __init__(self, *args, **kwargs):
        self.allowed_mimes = kwargs.pop('allowed_mimes', None)
        super(ResumableFileField, self).__init__(*args, **kwargs)

    @property
    def chunks_dir(self):
        if not hasattr(self.widget, 'chunks_dir'):
            raise Exception("You must set a `chunk_dir`.")
        return self.widget.storage

    @chunks_dir.setter
    def chunks_dir(self, chunks_dir):
        self.widget.chunks_dir = chunks_dir

    def clean(self, data, initial):
        f = super(ResumableFileField, self).clean(data, initial)
        if self.allowed_mimes is not None and \
                f.content_type not in self.allowed_mimes:
            raise ValidationError(self.error_messages['invalid_mime'])
        return value

    @property
    def upload_url(self):
        if not 'upload_url' in self.widget.attrs:
            raise Exception("You must set the upload url.")
        return self.widget.attrs['upload_url']

    @upload_url.setter
    def upload_url(self, url):
        self.widget.attrs['upload-url'] = url
