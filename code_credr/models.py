# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db.models import Sum

class Invoice(models.Model):
	customer = models.TextField()
	created_date = models.DateTimeField(auto_now_add = True)

	@property
	def total_quantity(self):
		return self.transactions.aggregate(total=Sum('quantity'))['total'] or 0.0

	@property
	def total_amount(self):
		return self.transactions.aggregate(total=Sum('quantity'))['total'] or 0.0

class Transaction(models.Model):
	
	invoice = models.ForeignKey(Invoice, related_name='transactions')
	product = models.TextField()
	quantity = models.IntegerField()	
	price = models.DecimalField(decimal_places = 2, max_digits = 10)
	line_total = models.DecimalField(decimal_places = 2 , max_digits = 10)

	def save(self , *args, **kwargs):
		self.line_total = self.quantity * self.price
		super(Transaction , self).save(*args, **kwargs)		