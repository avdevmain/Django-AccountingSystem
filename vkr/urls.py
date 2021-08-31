from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dochub/$', views.documenthub, name='dochub'),
    url(r'^saldo/$', views.saldo, name='saldo'),
    url(r'^services/$', views.ServiceListView.as_view(), name='services'),
    url(r'^service/(?P<pk>\d+)$', views.ServiceDetailView.as_view(), name='service-detail'),
]


urlpatterns += [
    url(r'^service/create/$', views.service_create, name='service_create'),
    url(r'^service/(?P<pk>\d+)/update/$', views.ServiceUpdate.as_view(), name='service_update'),
    url(r'^service/(?P<pk>\d+)/delete/$', views.ServiceDelete.as_view(), name='service_delete'),
]

urlpatterns += [
    url(r'^counterparties/$', views.CounterpartyListView.as_view(), name='counterparties'),
    url(r'^counterparty/(?P<pk>\d+)$', views.CounterpartyDetailView.as_view(), name='counterparty-detail'),
    url(r'^counterparty/(?P<pk>\d+)/delete$', views.CounterpartyDelete.as_view(), name='counterparty-delete'),
    url(r'^counterparty/create/$', views.counterparty_create, name='counterparty_create'),
    url(r'^counterparty/(?P<pk>\d+)/individual$', views.address_create, name='address_create'),
    url(r'^counterparty/(?P<pk>\d+)/individual$', views.individual_create, name='counterparty-setindividual'),
    url(r'^counterparty/(?P<pk>\d+)/legalentity$', views.legalentity_create, name='counterparty-setlegal'),
]


urlpatterns += [
    url(r'^agreements/$', views.AgreementListView.as_view(), name='agreements'),
    url(r'^agreement/(?P<pk>\d+)$', views.AgreementDetailView.as_view(), name='agreement-detail'),
    url(r'^agreement/create/$', views.agreement_create, name='agreement_create'),
    url(r'^agreement/(?P<pk>\d+)/servicesadd$', views.agreementservice_create, name='agreementservice_create'),
    url(r'^agreementservice/(?P<pk>\d+)/$', views.AgreementServiceUpdate.as_view(), name='agreementservice_update'),
    url(r'^agreement/(?P<pk>\d+)/update/$', views.AgreementUpdate.as_view(), name='agreement_update'),
]

urlpatterns += [
    url(r'^documents/$', views.DocumentListView.as_view(), name='documents'),
     url(r'^document/(?P<pk>\d+)$', views.AgreementDocumentDetailView.as_view(), name='document-detail'),
    url(r'^agreement/(?P<pk>\d+)/documentsadd$', views.document_add, name='document_create'),
    url(r'^document/(?P<pk>\d+)/update/$', views.DocumentUpdate.as_view(), name='document_update'),
    url(r'^document/(?P<pk>\d+)/delete/$', views.DocumentDelete.as_view(), name='document_delete'),
]

urlpatterns += [
url(r'^employees/$', views.UserListView.as_view(), name='employees'),
]

urlpatterns += [
url(r'^docgen/$', views.doc_test, name='docgen'),
]

