

from typing import ChainMap, Counter
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.db.models.lookups import IsNull
from django.urls import reverse




class Servicetype(models.Model):
    title = models.CharField(max_length=50, help_text="Введите название типа услуги", verbose_name= ('Название'))

    def __str__(self):
        return self.title

class Measureunit(models.Model):
    title = models.CharField(max_length=50, help_text="Введите название единицы измерения", verbose_name= ('Название'))

    def __str__(self):
        return self.title

class Account(models.Model):
    title = models.CharField(max_length=100, verbose_name=('Счет'))
    def __str__(self):
        return self.title


class Service(models.Model):
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null = True, blank= True)
    title = models.CharField(max_length=200, help_text="Введите название услуги", verbose_name= ('Название'))
    costperunit = models.DecimalField(max_digits=8, decimal_places=2, help_text="Цена услуги за единицу", verbose_name= ('Цена за единицу'))
    measure = models.ForeignKey('Measureunit', on_delete=models.SET_DEFAULT, default=0, verbose_name= ('Единица измерения'))
    type = models.ForeignKey('Servicetype', on_delete=models.SET_DEFAULT, default=0, verbose_name= ('Тип услуги'))
    nds = models.IntegerField(verbose_name="НДС", default=20)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service-detail', args=[str(self.id)])
    

class Country(models.Model):
    title = models.CharField(max_length=200, help_text="Введите название страны", verbose_name= ('Название'))
    def __str__(self):
        return self.title

class Street(models.Model):
    title = models.CharField(max_length=200, help_text="Введите название улицы", verbose_name= ('Название'))
    
    def __str__(self):
        return self.title

class City(models.Model):
    title = models.CharField(max_length=200, help_text="Введите название города", verbose_name= ('Название'))
    
    def __str__(self):
        return self.title

class AddressType(models.Model):
    title = models.CharField(max_length=50, help_text="Введите название типа адреса", verbose_name= ('Название'))

    def __str__(self):
        return self.title

class Address(models.Model):
    index = models.DecimalField(max_digits=6, decimal_places=0, verbose_name= ('Индекс'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null= True, blank=True, verbose_name=('Страна'))
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null= True, blank=True, verbose_name=('Город'))
    street = models.ForeignKey('Street', on_delete=models.SET_NULL, null= True, blank=True, verbose_name=('Улица'))
    building = models.CharField(max_length=4, verbose_name= ('Номер здания'))
    apartment_office = models.CharField(max_length=4,null=True, verbose_name= ('Номер помещения'))

    def __str__(self):
        return f'г. {self.city} ул. {self.street} {self.building} - {self.apartment_office}'

class Signature(models.Model):
    signature = models.CharField(max_length=200, verbose_name=('Подпись'))

class Counterparty(models.Model):
    lastname = models.CharField(max_length=40, verbose_name= ('Фамилия'))
    firstname = models.CharField(max_length=40, verbose_name= ('Имя'))
    middlename = models.CharField(max_length=40, verbose_name= ('Отчество'))
    phone = models.CharField(max_length=12, verbose_name= ('Номер телефона'))
    email = models.CharField(max_length=40, verbose_name=('Электронная почта'))

    def __str__(self):

        try:
            self.individual
            return f'{self.lastname} {self.firstname} {self.middlename}'
        except ObjectDoesNotExist:
            try:
                return self.legalentity.title
            except:
                return "Не определен тип"

    @property
    def type(self):
        try:
            self.individual
            return 'Физическое лицо'
        except ObjectDoesNotExist:
            try:
                return 'Юридическое лицо'
            except:
                return None
        
    def get_absolute_url(self):
        return reverse('counterparty-detail', args=[str(self.id)])


class CounterpartyAddress(models.Model):
    counterparty = models.ForeignKey('Counterparty', on_delete = models.CASCADE, verbose_name=('Контрагент'))
    address = models.ForeignKey('Address', on_delete= models.CASCADE, verbose_name=('Адрес'))
    type = models.ForeignKey('AddressType', on_delete=models.SET_DEFAULT, default=0, verbose_name= ('Тип адреса'))

    def __str__(self):
        return f'{self.counterparty} {self.address}, {self.type}'

class Individual (models.Model):
    counterparty = models.OneToOneField(Counterparty, on_delete=models.CASCADE, verbose_name=('Контактное лицо'))
    passport = models.DecimalField(max_digits=10, decimal_places=0, verbose_name=('Серия и номер паспорта'))

    def __str__(self):
        return f'{self.counterparty}'

class LegalEntity (models.Model):
    counterparty = models.OneToOneField(Counterparty, on_delete=models.CASCADE, verbose_name=('Контактное лицо'))
    INN = models.CharField(max_length=10, verbose_name= ('ИНН'))
    #Ещё 10 полей с разными данными
    title = models.CharField(max_length=100, verbose_name= ('Название компании'))

    def __str__(self):
        return f'{self.title}'

class AgreementStatus(models.Model):
    title = models.CharField(max_length=50, help_text="Введите название статуса соглашения", verbose_name= ('Статус соглашения'))

    def __str__(self):
        return self.title

class DocumentStatus(models.Model):
    title = models.CharField(max_length=50, help_text="Введите название статуса документа", verbose_name= ('Статус документа'))

    def __str__(self):
        return self.title


class DocumentType(models.Model):
    title = models.CharField(max_length=50, help_text="Введите название типа документа", verbose_name= ('Тип документа'))

    def __str__(self):
        return self.title

class Agreement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=('Сотрудник'))
    counterparty = models.ForeignKey('Counterparty', on_delete=models.SET_NULL, null=True, verbose_name=('Контрагент'))
    startTerm = models.DateField(verbose_name=('Дата создания'))
    endTerm = models.DateField(verbose_name=('Дата окончания'))
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, verbose_name=('Адрес заключения'))
    status = models.ForeignKey('AgreementStatus', on_delete=models.SET_NULL, null=True, verbose_name=('Статус'))
    sum = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name= ('Сумма услуг'))
    sumPaid = models.DecimalField(max_digits=8, decimal_places=2,default=0 ,verbose_name=('Оплачено'))
    def __str__(self):
        return f'{self.counterparty} от {self.startTerm}'

    def get_absolute_url(self):
        return reverse('agreement-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-startTerm']


class AgreementService(models.Model):
    agreement = models.ForeignKey('Agreement', on_delete=models.SET_NULL, null=True, verbose_name=('Соглашение'))
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, verbose_name=('Услуга'))
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=('Количество'))
    sum = models.DecimalField(max_digits=8, decimal_places=2, blank= True, null=True)
    nds = models.DecimalField(max_digits=8, decimal_places=2,blank= True, null=True)
    total = models.DecimalField(max_digits=8, decimal_places=2,blank= True, null=True)

    def __str__(self):
        return f'{self.agreement} {self.service}:{self.amount} {self.service.measure}'

    def get_absolute_url(self):
        return reverse('agreementservice_update', args=[str(self.id)])


class AgreementDocument(models.Model):
    agreement = models.ForeignKey('Agreement', on_delete=models.SET_NULL, null=True, verbose_name=('Соглашение'))
    type = models.ForeignKey('DocumentType', on_delete=models.SET_NULL, null=True, verbose_name=('Тип документа'))
    status = models.ForeignKey('DocumentStatus', on_delete=models.SET_NULL, null=True, verbose_name=('Статус документа'))
    file = models.FileField(verbose_name=('Файл'), null=True)

    def __str__(self):
        return f'{self.agreement} - {self.type}'
    def get_absolute_url(self):
        return reverse('document-detail', args=[str(self.id)])