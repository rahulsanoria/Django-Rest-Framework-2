# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from code_credr.models import Invoice , Transaction
from code_credr.serializers import InvoiceSerializer , TransactionSerializer 
from rest_framework import generics

def login(request):
    return render(request, 'code_credr/login.html')


class InvoiceList(generics.ListCreateAPIView):

	queryset = Invoice.objects.all()
	serializer_class = InvoiceSerializer

class InvoiceDetail(generics.RetrieveUpdateDestroyAPIView):
	
	queryset = Invoice.objects.all()
	serializer_class = InvoiceSerializer	