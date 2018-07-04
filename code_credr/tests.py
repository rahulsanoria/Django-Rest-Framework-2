# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase


from django.test import TestCase
from rest_framework.test import APIClient
from invoice.models import Invoice, Transaction
from decimal import Decimal
import json

class InvoiceTests(TestCase):

    def test_invoice_post(self):
        client = APIClient()
        self.assertFalse(Invoice.objects.all().exists())
        data = {
            "customer": "test 2",
            "transactions": [ 
                { "product": "test product", "quantity": "4", "price": "10.00"},
                { "product": "test product 1", "quantity": "2", "price": "20.00"},
                { "product": "test product 2", "quantity": "3", "price": "15.00"} 
            ]
        }
        
        response = client.post('/invoices/', data, format="json")

        invoices = Invoice.objects.all()
        self.assertTrue(invoices.exists())
        self.assertEquals(invoices.count(), 1)

        i = invoices[0]
        self.assertEquals(i.total_quantity, 9)
        self.assertEquals(i.total_amount, Decimal(125))

        transactions = Transaction.objects.all()
        self.assertEquals(transactions.count(), 3)

        for t in transactions:
            self.assertEquals(t.line_total, t.price * t.quantity)

        invoices = Invoice.objects.all().delete()      


    def test_invoice_patch(self):
        client = APIClient()
        self.assertFalse(Invoice.objects.all().exists())
        data = {
            "customer": "test 2",
            "transactions": [ 
                { "product": "test product", "quantity": "4", "price": "10.00"},
                { "product": "test product 1", "quantity": "2", "price": "20.00"},
                { "product": "test product 2", "quantity": "3", "price": "15.00"} 
            ]
        }
        
        request = client.post('/invoices/', data, format='json')

        invoices = Invoice.objects.all()
        self.assertTrue(invoices.exists())
        self.assertEquals(invoices.count(), 1)

        i = invoices[0]
        self.assertEquals(i.total_quantity, 9)
        self.assertEquals(i.total_amount, Decimal(125))

        transactions = Transaction.objects.all()
        self.assertEquals(transactions.count(), 3)

        for t in transactions:
            self.assertEquals(t.line_total, t.price * t.quantity)

        response = client.get('/invoices/{0}/'.format(i.pk), format='json')
        json_invoice = json.loads(response.content)
        del json_invoice['total_quantity']
        del json_invoice['total_amount']

        json_invoice['transactions'].append({"product": "updated product", "quantity": "1", "price": "100.00" })
        deleted_transaction = json_invoice['transactions'].pop(0)

        response = client.put('/invoices/{0}/'.format(i.pk), json_invoice, format='json')

        invoices = Invoice.objects.all()
        self.assertTrue(invoices.exists())
        self.assertEquals(invoices.count(), 1)

        i = invoices[0]
        self.assertEquals(i.total_quantity, 9 - int(deleted_transaction['quantity']) + 1)
        self.assertEquals(i.total_amount, Decimal(125 + 100) - Decimal(deleted_transaction['line_total']))

        transactions = Transaction.objects.all()
        self.assertEquals(transactions.count(), 3)

        for t in transactions:
            self.assertEquals(t.line_total, t.price * t.quantity)

        Invoice.objects.all().delete()
