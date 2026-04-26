from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Conta(models.Model):
    TYPE_CHOICES = [
        ('corrente', 'Conta Corrente'),
        ('poupanca', 'Conta Poupança'),
    ]

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.bank} - {self.number}"