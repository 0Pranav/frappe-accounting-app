# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Supplier(Document):
	def save(self,*args,**kwargs):
		supplier_payment = frappe.get_doc("Account","Supplier Payment")
		supplier_account = frappe.new_doc("Account")
		supplier_account.account_name = self.supplier_name
		supplier_account.account_type = "Liability"
		supplier_account.account_balance = 0
		supplier_account.parent_account = supplier_payment.name
		supplier_account.insert()
		self.supplier_account = supplier_account.name
		super().save(*args,**kwargs)