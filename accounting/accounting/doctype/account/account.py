# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
# import NestedSet
from frappe.utils.nestedset import NestedSet

class Account(NestedSet):
	nsm_parent_field = "parent_account"

	def debit(self, amount):
		if self.account_type == "Asset" or self.account_type == "Expense":
			# +
			self.account_balance += amount
			self.save()
		else:
			# -
			self.account_balance -= amount
			self.save()
		if self.name == "Root":
			return
		if self.parent_account is not "Root":
			parent=frappe.get_doc("Account",self.parent_account)
			parent.debit(amount)
		return	

	def credit(self, amount):
		if self.account_type == "Asset" or self.account_type == "Expense":
			# -
			self.account_balance -= amount
			self.save()
		else:
			# +	
			self.account_balance += amount
			self.save()
		if self.name == "Root":
			return
		if self.parent_account is not "Root":
			parent=frappe.get_doc("Account",self.parent_account)
			parent.credit(amount)
		return	
