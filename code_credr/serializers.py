from django.db.models import Q
from rest_framework import serializers
from code_credr.models import Transaction , Invoice

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ('id' , 'product', 'quantity', 'price' , 'line_total')
		read_only_fields = ('line_total',)

class InvoiceSerializer(serializers.ModelSerializer):
	transactions = TransactionSerializer(many=True)
	class Meta:
		model = Invoice
		fields = ('id' , 'customer', 'created_date' , 'total_quantity' , 'total_amount' ,'transactions')

	def create(self, validated_data):
		transactions = validated_data.pop('transactions')
		instance = Invoice.objects.create(**validated_data)	
		for t in transactions:
			t['invoice']= instance
			transaction = Transaction.objects.create(**t)

		return instance
	
	def update(self, instance , validated_data)	:
		transactions = validated_data.pop('transactions')
		instance.customer = validated_data.get('customer' , instance.customer)
		instance.save()

		present_transactions = []

		for t in transactions:
			t['invoice'] = instance
			pk = t.get('id' , None)
			if not pk:  
       			# create a new transaction since there in no PK
				transaction = Transaction.objects.create(**t)
       			present_transactions.append(transaction.pk)
       		else:
       			# update existing transaction since there is a PK 
       			transaction = Transaction.objects.get(pk=pk)
       			transaction.product = t.get('product', transaction.product)
       			transaction.quantity = t.get('quantity' , transaction.quantity)
       			transaction.price = t.get('price' , transaction.price)
       			transaction.save()
       			present_transactions.append(transaction.pk)


       	# Delete all tranactions not present in the updated data
		not_present_transactions = Transaction.objects.filter(~Q(pk__in = present_transactions))
		not_present_transactions.delete()
		return instance		





