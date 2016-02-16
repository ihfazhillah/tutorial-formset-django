from django.db import models

class Kelas(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Murid(models.Model):
    namadepan = models.CharField(max_length=100)
    namabelakang = models.CharField(max_length=100)
    kelas = models.ForeignKey(Kelas, related_name='murid')

    def __str__(self):
        return self.namadepan