from django import forms
from django.forms import ModelForm
from django.forms.fields import DateField, DecimalField
from django.http import request
from .models import Account, Address, AddressType, Agreement, AgreementStatus, City, Counterparty, Country, DocumentStatus, DocumentType, Measureunit, Service, Servicetype, Street
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from django.forms import formset_factory

class AgreementForm(forms.Form):
    
    counterparty = forms.ModelChoiceField(queryset=Counterparty.objects.all(), label='Контрагент')
    startdate = datetime.date.strftime( datetime.datetime.now().date(), format="%Y-%m-%d")
    enddate = forms.DateField(initial=startdate, label='Действие соглашения до')
    address = forms.ModelChoiceField(queryset=Address.objects.all(), label='Адрес')
    status = forms.ModelChoiceField(queryset=AgreementStatus.objects.all(), label='Статус')
    sum = 0#forms.DecimalField(max_digits=8, decimal_places=2, label='Сумма услуг') #Должно считаться автоматически по услугам
    sumpaid = 0#forms.DecimalField(max_digits=8, decimal_places=2, label='Оплачено') #Можно вписывать по счетам




CP_TYPE_CHOICES =(
    ("1", "Физическое лицо"),
    ("2", "Юридическое лицо"),
)

class CounterpartyForm(forms.Form):
    lastname = forms.CharField(max_length=40, label='Фамилия')
    firstname = forms.CharField(max_length=40, label='Имя')
    middlename = forms.CharField(max_length=40, label='Отчество', required=False)
    phone = forms.CharField(max_length=12,label='Телефон', required=False)
    email = forms.CharField(max_length=100,label='Электронная почта', required=False)
    type = forms.ChoiceField(choices=CP_TYPE_CHOICES, label='Тип')
    

class IndividualForm(forms.Form):
    passport = forms.CharField(max_length=10, label='Номер и серия паспорта', required=False)

class LegalEntityForm(forms.Form):
    companyTitle = forms.CharField(max_length=200,label='Полное название компании', required=False)
    inn = forms.CharField(max_length=20,label='ИНН', required=False)
    kpp = forms.CharField(max_length=20,label='КПП', required=False)
    rs = forms.CharField(max_length=20,label='Расчетный счет', required=False)
    ks = forms.CharField(max_length=20,label='Корреспондентский счет', required=False)
    bik = forms.CharField(max_length=20,label='БИК', required=False)
    okato = forms.CharField(max_length=20,label='ОКАТО', required=False)

class AddressForm(forms.Form):
    type = forms.ModelChoiceField(queryset=AddressType.objects.all(), label='Тип')
    country = forms.ModelChoiceField(queryset=Country.objects.all(), label='Страна')
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='Город')
    street = forms.ModelChoiceField(queryset=Street.objects.all(), label='Улица')
    building = forms.CharField(max_length=5, label='Строение')
    room = forms.CharField(max_length=5, label='Помещение')
    index = forms.CharField(max_length=6, label='Индекс')

class ServiceCreateForm(forms.Form):
    title = forms.CharField(max_length=200, help_text='Введите наименование услуги', label='Название')
    costperunit = forms.DecimalField(max_digits=8, decimal_places=2, label='Цена за единицу')
    type = forms.ModelChoiceField(queryset=Servicetype.objects.all(), label='Тип услуги')
    measure = forms.ModelChoiceField(queryset=Measureunit.objects.all(), label='Единица измерения')
    nds = DecimalField(max_digits=2, decimal_places=0, initial=20, label='Процент НДС')
    account = forms.ModelChoiceField(queryset=Account.objects.all(), label='Бухгалтерский счет') 

    def clean_nds(self):
        cleannds = self.cleaned_data['nds']

        if cleannds > 30:
            raise ValidationError(_('НДС не должен быть больше 30'))
        
        if cleannds <0:
            raise ValidationError(_('НДС не должен быть меньше 0'))

        return cleannds
    
    def clean_costperunit(self):
        cleancost = self.cleaned_data['costperunit']

        if cleancost < 0:
            raise ValidationError(_('Стоимость не должна быть меньше 0'))

        return cleancost


class DocumentAddForm(forms.Form):
    type = forms.ModelChoiceField(queryset=DocumentType.objects.all(), label='Тип документа')
    status = forms.ModelChoiceField(queryset=DocumentStatus.objects.all(),label='Статус документа')
    file = forms.FileField(label='Загрузка файла')


class AgreementServiceForm(forms.Form):
    service =  forms.ModelChoiceField(queryset=Service.objects.all(), label = 'Услуга')
    amount = forms.DecimalField(max_digits=8, decimal_places=2, label='Количество')
    #presum = forms.DecimalField(max_digits=8, decimal_places=2, label='Сумма без НДС')
    #nds = forms.DecimalField(max_digits=8, decimal_places=2, label='Объем надс')
    #totalsum = forms.DecimalField(max_digits=8, decimal_places=2, label='Полная сумма')

