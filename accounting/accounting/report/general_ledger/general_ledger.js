// Copyright (c) 2016, 0Pranav and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger"] = {
	"filters": [
		{
			'fieldname': 'txn_type',
			'label': __('Transaction Type'),
			'fieldtype': 'Link',
			'options': 'DocType'
		},
		{
			'fieldname': 'txn_id',
			'label': __('Transaction ID'),
			'fieldtype': 'Data',
			// 'options': 'txn_type'
		},
		{
			'fieldname': 'from_date',
			'label': __('From date'),
			'fieldtype': 'Date',
			'default': frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		{
			'fieldname': 'to_date',
			'label': __('To Date'),
			'fieldtype': 'Date',
			'default': frappe.datetime.get_today()
		}
	]
};