# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Customer(Document):
	def save(self,*args,**kwargs):
		customer_payments = frappe.get_doc("Account","Customer Payments")
		customer_account = frappe.new_doc("Account")
		customer_account.account_name = self.customer_name
		customer_account.account_type = "Asset"
		customer_account.account_balance = 0
		customer_account.parent_account = customer_payments.account_name
		customer_account.insert()
		self.customer_account = customer_account.name
		super().save(*args,**kwargs)