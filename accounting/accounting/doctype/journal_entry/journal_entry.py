# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger
import frappe
from frappe.model.document import Document

class JournalEntry(Document):
	def before_submit(self,*args,**kwargs):
		credit_account = frappe.get_doc("Account",self.credit_account)
		credit_account.credit(self.amount)
		debit_account = frappe.get_doc("Account",self.debit_account)
		debit_account.debit(self.amount)
		GeneralLedger.make_double_entry(credit_account=credit_account,debit_account=debit_account,amount=self.amount,txn_type="Journal Entry",txn_id=self.name)
