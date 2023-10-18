import re
from rest_framework import serializers


class URLValidator:

    def __init__(self, fields: list):
        self.fields = fields

    def __call__(self, value):
        for field in self.fields:
            field_value = dict(value).get(field) if dict(value).get(field) else ""
            reg = re.compile('https?://(?!youtube)\S+')
            if bool(reg.search(field_value)):
                raise serializers.ValidationError('Links is forbidden')
