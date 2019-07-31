# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class PurchaseInvoice(Document):
	def save(self,*args,**kwargs):
		# Create general ledger entry here
		ledger_entry = frappe.new_doc('General Ledger')
		super.save(self,*args,**kwargs)
