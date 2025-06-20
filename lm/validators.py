import re

from django.core.exceptions import ValidationError


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        reg = re.compile("^(https?://)?(www\\.)?(youtube\\.)com/?$")
        tmp_val = value
        if not bool(reg.match(tmp_val)):
            raise ValidationError("Ссылка недействительна. Разрешены только ссылки на youtube.com.")
