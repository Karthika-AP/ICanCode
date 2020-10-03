from rest_framework import serializers

from .models import File
from .models import File1

class FileSerializer(serializers.ModelSerializer):

  class Meta():
    model = File
    fields = ('file', 'filetype', 'project_id')

class FileSerializer1(serializers.ModelSerializer):

  class Meta():
    model = File1
    fields = ('file', 'filetype', 'project_id')
