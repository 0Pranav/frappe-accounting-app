# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import datetime
from accounting.accounting.doctype.general_ledger.general_ledger import GeneralLedger
import frappe
from frappe.model.document import Document


class PurchaseInvoice(Document):
    def before_submit(self, *args, **kwargs):
        total = 0
        for item in self.items:
            total += item.item_total
        if total != self.total:
            frappe.throw("Items totals and Invoice total doesn't match")
        supplier = frappe.get_doc("Supplier", self.supplier)
        supplier_account = frappe.get_doc("Account", supplier.supplier_account)
        stock_expense_account = frappe.get_doc("Account", "Stock Expense")
        supplier_account.credit(self.total)
        stock_expense_account.debit(self.total)
        GeneralLedger.make_double_entry(credit_account=supplier_account, debit_account=stock_expense_account,
                                        amount=self.total, txn_type="Purchase Invoice", txn_id=self.name)

    def before_cancel(self, *args, **kwargs):
        supplier = frappe.get_doc("Supplier", self.supplier)
        supplier_account = frappe.get_doc("Account", supplier.supplier_account)
        stock_expense_account = frappe.get_doc("Account", "Stock Expense")
        supplier_account.debit(self.total)
        stock_expense_account.credit(self.total)
        GeneralLedger.make_double_entry(credit_account=stock_expense_account, debit_account=supplier_account,
                                        amount=self.total, txn_type="Purchase Invoice", txn_id=self.name)
