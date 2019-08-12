# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class PaymentEntry(Document):
	def save(self,*args,**args):
		if self.invoice_type == "Sales Invoice":
			print("Sales Invoice")
		elif self.invoice_type == "Purchase Invoice":
			print("Purchase Invoice")
