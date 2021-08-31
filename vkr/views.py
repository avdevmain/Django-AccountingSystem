from collections import UserList
from datetime import date, datetime, time
from typing import Counter
from django.db import models
from django.forms import forms
from django.forms.fields import NullBooleanField
from django.shortcuts import render, redirect
from django.views.generic.dates import timezone_today
from django.contrib.auth import get_user_model
from .models import Address, Agreement, AgreementDocument, AgreementService, Counterparty, CounterpartyAddress, Individual, LegalEntity, Service, Servicetype, Measureunit
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):

    return render(
        request,
        'index.html',
    )

def documenthub(request):

    return render(
        request,
        'documenthub.html',
    )

import io
from docx import Document
from docx.shared import Inches
from django.http import FileResponse
from docxtpl import DocxTemplate
from django.http import HttpResponse
from sortable_listview import SortableListView


def doc_test(request):
    doc = DocxTemplate("template.docx")
    context = { "enddate" : "sfsdfs", "pupa":"lupa", }
    doc.render(context)
    doc.save("generated_doc.docx")
    return HttpResponseRedirect(reverse('index') )


def saldo(request):
    doc = DocxTemplate("saldotemplate.docx")
    counterparties = Counterparty.objects.all()

    agreementList = [] #Список соглашений каждого контрагента
    cpCredits = [] #Сумма кредита контрагентов
    cpDebits = [] #Сумма дебита контрагентов

    for cp in counterparties:
        agreementList.append(Agreement.objects.filter(counterparty = cp))
    
    oborotcred = 0 #Общий оборот по кредиту

    servicesOfAgreement = [] #Услуги соглашений
    for agreementsOfCounterparty in agreementList: #Для соглашения каждого отдельного контрагента
        interdeb = 0
        intercred = 0
        for exactagreement in agreementsOfCounterparty: #Для каждого отдельного соглашения
            servicesOfAgreement.append(AgreementService.objects.filter(agreement = exactagreement))
            oborotcred = oborotcred + exactagreement.sumPaid
            interdeb = interdeb + exactagreement.sum
            intercred = intercred + exactagreement.sumPaid
        cpDebits.append(interdeb)
        cpCredits.append(intercred)
            

    oborotdeb = 0 #Общий оборот по дебиту
    
    for x in range(len(servicesOfAgreement)):
        for serv in servicesOfAgreement[x]:
            oborotdeb = oborotdeb + serv.total

    context = {"period":"все время",}
    context['counterpartiesList'] = counterparties
    context['agreementsList'] = agreementList
    context['servicesList'] = servicesOfAgreement


    context['startdeb'] = 0.00
    context['startcred'] = 0.00
    context['oborotdeb'] = oborotdeb
    context['oborotcred'] = oborotcred
    context['enddeb'] = oborotdeb
    context['endcred'] = oborotcred

    context['cpdeb'] = cpDebits
    context['cpcred'] = cpCredits

    doc.render(context)
    doc.save("generated_saldo.docx")
    return render(
        request,
        'saldo.html',
    )

class UserListView(SortableListView):
    template_name = 'vkr/employee_list.html'
    model = get_user_model()
    paginate_by = 10
    allowed_sort_fields = {'last_name': {'default_direction': '-', 'verbose_name': 'Имя'},
    'username': {'default_direction': '-', 'verbose_name': 'Логин'},
    'email': {'default_direction': '-', 'verbose_name': 'Электронная почта'}}
    default_sort_field = 'last_name'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        userList = get_user_model().objects.all()
        context['users'] = userList
        return context



def employees(request):
    User = get_user_model()
    userList =User.objects.all()



    return render(
        request,
        'employee_list.html',
        context={'users':userList},
    )

class ServiceListView(SortableListView):
    model = Service
    paginate_by = 10
    allowed_sort_fields = {'title': {'default_direction': '-', 'verbose_name': 'Название'},
    'costperunit': {'default_direction': '-', 'verbose_name': 'Стоимость'}}
    default_sort_field = 'title'

class ServiceDetailView(generic.DetailView):
    model = Service



class ServiceCreate(CreateView):
    model = Service
    fields = '__all__'
    

class ServiceUpdate(UpdateView):
    model = Service
    fields = '__all__'

class ServiceDelete(DeleteView):
    model = Service
    success_url = reverse_lazy('services')


class CounterpartyListView(SortableListView):
    model = Counterparty
    allowed_sort_fields = {'individual': {'default_direction': '-', 'verbose_name': 'Тип'},
    'email': {'default_direction': '-', 'verbose_name': 'Почта'}}
    default_sort_field = 'individual'
    paginate_by = 10

    

class CounterpartyDetailView(generic.DetailView):
    model = Counterparty


class CounterpartyCreate(CreateView):
    model = Counterparty
    fields = '__all__'

class CounterpartyDelete(DeleteView):
    model = Counterparty
    success_url = reverse_lazy('counterparties')

class AgreementListView(SortableListView):

    model = Agreement
    allowed_sort_fields = {'id': {'default_direction': '-', 'verbose_name': 'Идентификатор'},
    'startTerm': {'default_direction': '-', 'verbose_name': 'Дата заключения'}, 
    'endTerm': {'default_direction': '-', 'verbose_name': 'Дата окончания'},
    'status': {'default_direction': '-', 'verbose_name': 'Статус'}}
    default_sort_field = 'startTerm'
    paginate_by = 10
    template_name = 'vkr/agreement_list.html'
    


from .forms import AddressForm, AgreementForm, AgreementServiceForm, CounterpartyForm, DocumentAddForm, IndividualForm, LegalEntityForm
import urllib
def agreement_create(request):

    if request.method == 'POST':
        form = AgreementForm(request.POST)

        if form.is_valid():
            new_agreement = Agreement(user = request.user, counterparty = form.cleaned_data['counterparty'] , startTerm = form.startdate, endTerm = form.cleaned_data['enddate'], address = form.cleaned_data['address'], status = form.cleaned_data['status'], sum = form.sum, sumPaid = form.sumpaid )
            new_agreement.save()

            return redirect('agreement-detail', pk=new_agreement.id)
            #return HttpResponseRedirect(reverse('agreements') ) #После добавления услуг

    else:
        form = AgreementForm()

    return render(request,'vkr/agreement_form.html', {'form': form, 'header': 'Создание соглашения'})

def document_add(request, pk):
    template_name = 'vkr/document_form.html'
    if request.method == 'GET':
            form = DocumentAddForm(request.GET or None)
    elif request.method == 'POST':
            form = DocumentAddForm(request.POST, request.FILES)
            if form.is_valid():
                agreement = Agreement.objects.get(id = pk)
                type = form.cleaned_data.get('type')
                status = form.cleaned_data.get('status')
                file = form.cleaned_data.get('file')
  
                if file:
                    AgreementDocument(agreement = agreement, type = type, status = status, file = file).save()
                return redirect('agreement-detail', pk=pk)
    return render(request, template_name, {'form': form})

def agreementservice_create(request, pk):
    template_name = 'vkr/agreementservice_form.html'
    if request.method == 'GET':
        form = AgreementServiceForm(request.GET or None)
    elif request.method == 'POST':
        form = AgreementServiceForm(request.POST)
        if form.is_valid():
            agreement = Agreement.objects.get(id = pk)
            service = form.cleaned_data.get('service')
            amount = form.cleaned_data.get('amount')
            presum = service.costperunit * amount
            nds = service.nds * presum /100
            totalsum = presum + nds
            if service:
                AgreementService(agreement = agreement, service = service, amount = amount, sum = presum, nds = nds, total = totalsum).save()
                agreement.sum = agreement.sum + totalsum
                agreement.save()
        return redirect('agreement-detail', pk=pk)
    return render(request, template_name, {
        'form': form, 'header':'Добавление услуги к соглашению'})

def counterparty_create(request):
    template_name = 'vkr/counterparty_form.html'
    if request.method == 'POST':
        form = CounterpartyForm(request.POST)
        if form.is_valid():
            lname = form.cleaned_data['lastname']
            fname = form.cleaned_data['firstname']
            mname = form.cleaned_data['middlename']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            type = form.cleaned_data['type']
            if (lname!=None) & (fname!=None) & ((email!=None) | (phone!=None)):
                new_counterparty = Counterparty(lastname = lname, firstname = fname, middlename = mname, phone = phone, email = email)
                new_counterparty.save()
                if type == '1':
                    return redirect('counterparty-setindividual', pk = new_counterparty.id)
                else:
                    return redirect('counterparty-setlegal', pk = new_counterparty.id)
                #return redirect('counterparty-detail', pk = new_counterparty.id)

    else:
        form = CounterpartyForm()
    return render(request, template_name, {
        'form': form, 'header':'Создание контрагента'})

def individual_create(request, pk):
    template_name = 'vkr/individual_form.html'
    if request.method == 'GET':
        form = IndividualForm(request.GET or None)
    elif request.method == 'POST':
        form = IndividualForm(request.POST)
        if form.is_valid():
            counterparty = Counterparty.objects.get(id = pk)
            passport = form.cleaned_data.get('passport')
   
            if passport:
                new_individual = Individual(counterparty = counterparty, passport = passport).save()
        return redirect('counterparty-detail', pk=pk)
    return render(request, template_name, {
        'form': form, 'header':'Добавление данных физического лица'})
def legalentity_create(request, pk):
    template_name = 'vkr/legalentity_form.html'
    if request.method == 'GET':
        form = LegalEntityForm(request.GET or None)
    elif request.method == 'POST':
        form = LegalEntityForm(request.POST)
        if form.is_valid():
            counterparty = Counterparty.objects.get(id = pk)
            title = form.cleaned_data['companyTitle']
            inn = form.cleaned_data['inn']
            kpp = form.cleaned_data['kpp']
            rs = form.cleaned_data['rs']
            ks = form.cleaned_data['ks']
            bik = form.cleaned_data['bik']
            okato = form.cleaned_data['okato']
   
            if inn!=None:
                new_legalentity = LegalEntity(counterparty = counterparty, INN = inn, title = title).save()
        return redirect('counterparty-detail', pk=pk)
    return render(request, template_name, {
        'form': form, 'header':'Добавление данных юридического лица'})

def address_create(request, pk):
    template_name = 'vkr/address_form.html'
    if request.method == 'GET':
        form = AddressForm(request.GET or None)
    elif request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            counterparty = Counterparty.objects.get(id = pk)
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            building = form.cleaned_data['building']
            room = form.cleaned_data['room']
            type = form.cleaned_data['type']
            index = form.cleaned_data['index']
            new_address = Address(index = index, country = country, city = city, street = street, building = building, apartment_office = room)
            new_address.save()
            if new_address:
                new_cpaddress = CounterpartyAddress(counterparty = counterparty, address = new_address, type = type)
                new_cpaddress.save()
            return redirect('counterparty-detail', pk=pk)
    return render(request, template_name, {
        'form': form, 'header':'Добавление адреса'})

from .forms import ServiceCreateForm

def service_create(request):

    if request.method == 'POST':
        
        form = ServiceCreateForm(request.POST)
        if form.is_valid():
            new_service = Service(account=form.cleaned_data['account'], title = form.cleaned_data['title'], costperunit = form.cleaned_data['costperunit'], nds = form.cleaned_data['nds'], type = form.cleaned_data['type'], measure = form.cleaned_data['measure'])
            new_service.save()
            return HttpResponseRedirect(reverse('services') )
    else:
        form = ServiceCreateForm()

        
    return render(request,'vkr/service_form.html', {'form':form})




class AgreementUpdate(UpdateView):
    model = Agreement
    fields = ('endTerm','status', 'sumPaid')

class AgreementServiceUpdate(UpdateView):
    model = AgreementService
    fields = ('service', 'amount',)


class AgreementDetailView(generic.DetailView):
    model = Agreement
   # initial={'startTerm': datetime.now().date,}
    
class AgreementServiceUpdateView(generic.UpdateView):
    model = AgreementService

class AgreementDocumentDetailView(generic.DetailView):
    model = AgreementDocument

class DocumentListView(SortableListView):
    model = AgreementDocument
    paginate_by = 10
    allowed_sort_fields = {'id': {'default_direction': '-', 'verbose_name': 'Идентификатор'},
    'type': {'default_direction': '-', 'verbose_name': 'Тип'}, 
    'status': {'default_direction': '-', 'verbose_name': 'Статус'}}
    default_sort_field = 'id'

class DocumentCreate(CreateView):
    model = AgreementDocument
    fields = '__all__'

class DocumentUpdate(UpdateView):
    model = AgreementDocument
    fields = '__all__'

class DocumentDelete(DeleteView):
    model = AgreementDocument


