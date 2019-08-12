# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document

class SalesInvoice(Document):
	def save(self, *args, **kwargs):
		customer = frappe.get_doc("Customer",self.customer)
		customer_account = frappe.get_doc("Account",customer.customer_account)
		sales_account = frappe.get_doc("Account","Sales Income")
		
		super().save(self,*args,**kwargs)
		
		# Adjust balance in accounts
		customer_account.account_balance = customer_account.account_balance + self.total
		customer_account.save()
		sales_account.account_balance = sales_account.account_balance + self.total
		sales_account.save()
		
		# Debit Entry
		debit_entry = frappe.new_doc("General Ledger")
		debit_entry.posting_date = datetime.date.today()
		debit_entry.account_affected = customer_account.name
		debit_entry.credited_amount = 0
		debit_entry.debited_amount = self.total
		debit_entry.account_balance = customer_account.account_balance
		debit_entry.txn_type = "Sales Invoice"
		debit_entry.txn_id = self.name
		debit_entry.save()

		# Credit Entry
		credit_entry = frappe.new_doc("General Ledger")
		credit_entry.posting_date = datetime.date.today()
		credit_entry.account_affected = sales_account.name
		credit_entry.credited_amount = self.total
		credit_entry.debited_amount = 0
		credit_entry.account_balance = sales_account.account_balance
		credit_entry.txn_type = "Sales Invoice"
		credit_entry.txn_id = self.name
		credit_entry.save()