from django.contrib.auth.models import User
from django.db import models

# Create your models here.




class Translator(models.Model):
    translator_user = models.ForeignKey(User, on_delete=models.CASCADE)
    word_eng = models.CharField(max_length=200)
    word_pol = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        words = "Eng: {} - Pol: {}".format(self.word_eng, self.word_pol)
        return words