# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger
import datetime
from frappe.model.document import Document


class SalesInvoice(Document):

    def before_submit(self, *args, **kwargs):
        total = 0
        for item in self.items:
            total += item.item_total
        if total != self.total:
            frappe.throw("Items totals and Invoice total doesn't match")
        customer = frappe.get_doc("Customer", self.customer)
        customer_account = frappe.get_doc("Account", customer.customer_account)
        sales_account = frappe.get_doc("Account", "Sales Income")
        customer_account.debit(self.total)
        sales_account.credit(self.total)
        GeneralLedger.make_double_entry(credit_account=sales_account, debit_account=customer_account,
                                        amount=self.total, txn_id=self.name, txn_type="Sales Invoice")

    def before_cancel(self):
        customer = frappe.get_doc("Customer", self.customer)
        customer_account = frappe.get_doc("Account", customer.customer_account)
        sales_account = frappe.get_doc("Account", "Sales Income")
        customer_account.credit(self.total)
        sales_account.debit(self.total)
        GeneralLedger.make_double_entry(credit_account=customer_account, debit_account=sales_account,
                                        amount=self.total, txn_id=self.name, txn_type="Sales Invoice")
