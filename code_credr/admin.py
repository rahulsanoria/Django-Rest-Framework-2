# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Invoice, Transaction
# Register your models here.
admin.site.register(Invoice)
admin.site.register(Transaction)

