from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Customer(models.Model):
    """Модель заказчика"""
    name = models.CharField('Заказчик', max_length=64)
    description = models.TextField('Описание',)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    """Расширение класса User для добавлние поля id telegramm"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    telegram_id = models.PositiveIntegerField('Телеграмм ID')

    def __str__(self):
        return str(self.user.username)

class Calendar(models.Model):
    """Модель с данными для создания моделей событий"""
    title = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Заказчик')
    start = models.DateTimeField('Дата начала')
    end = models.DateTimeField('Дата окончания')
    repeat = models.BooleanField('Повторяется ли событие?',default=False)
    price = models.PositiveIntegerField('Цена за услугу')
    telegrambool = models.BooleanField('Оповещать по телеграмм?', default=False)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, verbose_name='Пользователь')
    
    def __str__(self):
        return f'{str(self.title)} репетитора {str(self.user)}'
    
class Event(models.Model):
    """Создание ивентов репетиторства на основе модели Calendar"""
    date_event = models.DateTimeField('Дата события')
    paid = models.BooleanField('Произошла ли оплата?', default=False)
    master_event = models.ForeignKey(Calendar,on_delete=models.CASCADE, verbose_name='Событие')
    
    def __str__(self):
        return f'{str(self.master_event)} {str(self.date_event)}'