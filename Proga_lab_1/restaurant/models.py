from django.db import models


class Client(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.login


class Menu(models.Model):
    dish_name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.dish_name


class Order(models.Model):
    client = models.ForeignKey(Client)
    dishes = models.ManyToManyField(Menu)
    accepted_by_administrator = models.BooleanField(default=False)

    def __str__(self):
        return self.id.__str__() + ' by ' + self.client.login


class Bill(models.Model):
    client = models.ForeignKey(Client)
    order = models.ForeignKey(Order)

    def __str__(self):
        return self.id.__str__() + ' by ' + self.client.login


class Administrator(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return '#' + self.login
