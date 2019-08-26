# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document

class GeneralLedger(Document):
	@staticmethod
	def make_double_entry(credit_account,debit_account,amount,txn_type,txn_id):
		# Get today
		today = datetime.date.today()
		# Credit Entry
		credit_entry = frappe.new_doc("General Ledger")
		credit_entry.posting_date = today
		credit_entry.account_affected = credit_account.name
		credit_entry.credited_amount = amount
		credit_entry.debited_amount = 0
		credit_entry.account_balance = credit_account.account_balance
		credit_entry.txn_type = txn_type
		credit_entry.txn_id = txn_id
		credit_entry.save()
		# Debit Entry
		debit_entry = frappe.new_doc("General Ledger")
		debit_entry.posting_date = today
		debit_entry.account_affected = debit_account.name
		debit_entry.credited_amount = 0
		debit_entry.debited_amount = amount
		debit_entry.account_balance = debit_account.account_balance
		debit_entry.txn_type = txn_type
		debit_entry.txn_id = txn_id
		debit_entry.save()

		return

