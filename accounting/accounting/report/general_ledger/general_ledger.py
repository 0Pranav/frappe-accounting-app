# Copyright (c) 2013, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	from_date = filters.pop("from_date",None)
	to_date = filters.pop("to_date",None)
	columns, data = [], []
	columns = get_columns() 
	data = frappe.get_list("General Ledger",filters=filters,fields="*")
	return columns, data

def _get_gl_entries(filters):
	return frappe.get_list("General Ledger",filters=filters,fields="*")

def _get_data(filters,from_date,to_date):
	gl_entries = _get_gl_entries(filters=filters)
	gl_entries_before_start , gl_entries_after_start = _seperate_entries(from_date,gl_entries)
	gl_entries_in_period , gl_entries_after_end = _seperate_entries(to_date,gl_entries_after_start)
	data = []
	opening = _get_credit_debit_balance(gl_entries_before_start)
	data.append(opening)
	for entry in gl_entries_in_period:
		data.append(entry)
	closing = _get_credit_debit_balance(gl_entries_in_period)
	data.append(closing)
	# total = _add_balance_dict(opening,closing)

def _add_balance_dict(opening,closing):
	total_dict = {}
	total_dict["credited_amount"] = opening["credited_amount"] - closing["credited_amount"]
	total_dict["debited_amount"] = opening["debited_amount"] - closing["debited_amount"]
	

def _get_credit_debit_balance(gl_entries):
	balance_dict = {}
	for entry in gl_entries:
		balance_dict["credited_amount"] += entry.credited_amount
		balance_dict["debited_amount"] += entry.debited_amount
	balance_dict["account_balance"] = balance_dict["debited_amount"] - balance_dict["credited_amount"]
	return balance_dict

def _seperate_entries(from_date, gl_entries):
	before, after = [], []
	for entry in gl_entries:
		if entry.posting_date < from_date:
			before.append(entry)
		else:
			after.append(entry)
	return before,after

def get_columns():
	columns = [
		{
			"fieldname":"posting_date",
			"label":"Posting Date",
			"fieldtype":"Date",
		},
		{
			"fieldname":"account_affected",
			"label":"Account",
			"fieldtype":"Link",
			"options":"Account"
		},
		{
			"fieldname":"credited_amount",
			"label":_("Credit"),
			"fieldtype":"Currency",
		},
		{
			"fieldname":"debited_amount",
			"label":_("Debit"),
			"fieldtype":"Currency",
		},
		{
			"fieldname":"account_balance",
			"label":_("Account Balance"),
			"fieldtype":"Currency"
		},
		{
			"fieldname":"txn_type",
			"label": _("Transaction type"),
			"fieldtype":"Link",
			"options":"Doctype"
		},
		{
			"fieldname":"txn_id",
			"label":_("Transaction ID"),
			"fieldtype":"Dynamic Link",
			"options":"txn_type"
		}
	]
	return columns