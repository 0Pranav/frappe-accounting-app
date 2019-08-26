# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger
import frappe
import datetime
from frappe.model.document import Document

class PaymentEntry(Document):
	def before_submit(self,*args,**kwargs):
		invoice = frappe.get_doc(self.payment_type,self.against_invoice)
		cash_account = frappe.get_doc("Account","Cash")

		entries = frappe.get_list('Payment Entry',fields=['name','payment_amount'],filters=[["against_invoice","=",self.against_invoice],["docstatus","=",1]])
		print(entries)
		total = 0
		for entry in entries:
			total+= entry.payment_amount
		pending_amount = invoice.total - total
		print("pending amount:"+str(pending_amount))
		if pending_amount < self.payment_amount:
			frappe.throw("Don't overpay bruh")
		if self.payment_type == "Sales Invoice":
			credit_account = frappe.get_doc("Account",invoice.customer)
			debit_account = cash_account
		elif self.payment_type == "Purchase Invoice":
			debit_account = frappe.get_doc("Account",invoice.supplier)
			credit_account = cash_account
		credit_account.credit(self.payment_amount)
		debit_account.debit(self.payment_amount)	
		GeneralLedger.make_double_entry(credit_account=credit_account,debit_account=debit_account,amount=self.payment_amount,txn_type="Payment Entry",txn_id=self.name)		
	
	def before_cancel(self):
		invoice = frappe.get_doc(self.payment_type,self.against_invoice)
		cash_account = frappe.get_doc("Account","Cash")
		if self.payment_type == "Sales Invoice":
			credit_account = frappe.get_doc("Account",invoice.customer)
			debit_account = cash_account
		elif self.payment_type == "Purchase Invoice":
			debit_account = frappe.get_doc("Account",invoice.supplier)
			credit_account = cash_account
		credit_account.debit(self.payment_amount)
		debit_account.credit(self.payment_amount)
		GeneralLedger.make_double_entry(credit_account=debit_account,debit_account=credit_account,amount=self.payment_amount,txn_type="Payment Entry",txn_id=self.name)