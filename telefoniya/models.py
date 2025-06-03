from django.db import models
from django.contrib.auth.models import User

class Tarif(models.Model):
    nomi = models.CharField(max_length=100)
    narx = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nomi

class Abonent(models.Model):
    FIO = models.CharField(max_length=150)
    telefon = models.CharField(max_length=20, unique=True)
    tarif = models.ForeignKey(Tarif, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)  # Aktiv yoki bloklangan

    def __str__(self):
        return f'{self.FIO} - {self.telefon}'

class Tolov(models.Model):
    abonent = models.ForeignKey(Abonent, on_delete=models.CASCADE, related_name='tolovlar')
    sana = models.DateField(auto_now_add=True)
    summa = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.abonent} - {self.summa} so‘m'

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    abonent = models.OneToOneField(Abonent, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username
