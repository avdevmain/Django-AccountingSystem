from django.contrib import admin
from django.db.models.query_utils import InvalidQuery

# Register your models here.

from .models import Account,Country,AgreementDocument, Service, Servicetype, Measureunit, Street,City, Counterparty, Individual, LegalEntity, AddressType, Address, CounterpartyAddress, AgreementStatus,DocumentStatus, DocumentType, Agreement, AgreementService

admin.site.register(Servicetype)
admin.site.register(Measureunit)
admin.site.register(Service)
admin.site.register(Account)
admin.site.register(Street)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(AddressType)
admin.site.register(Address)
admin.site.register(Counterparty)
admin.site.register(Individual)
admin.site.register(LegalEntity)
admin.site.register(CounterpartyAddress)
admin.site.register(AgreementStatus)
admin.site.register(DocumentStatus)
admin.site.register(DocumentType)
admin.site.register(Agreement)
admin.site.register(AgreementService)
admin.site.register(AgreementDocument)