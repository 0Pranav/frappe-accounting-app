# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import datetime
import frappe
from frappe.model.document import Document


class PurchaseInvoice(Document):
    def save(self, *args, **kwargs):
        # Create general ledger entry here
        supplier = frappe.get_doc("Supplier", self.supplier)
        supplier_account = frappe.get_doc("Account", supplier.supplier_account)
        stock_account = frappe.get_doc("Account", "Stock Expense")

        super().save(self, *args, **kwargs)
        supplier_account.account_balance = supplier_account.account_balance - self.total
        stock_account.account_balance = stock_account.account_balance + self.total
        debit_entry = frappe.get_doc({
            "doctype": "General Ledger",
            "posting_date": datetime.date.today(),
            "account_affected": stock_account.name,
            "credited_amount": 0,
            "debited_amount": self.total,
            "account_balance": stock_account.account_balance,
            "txn_type": "Purchase Invoice",
            "txn_id": self.name,
        })
        credit_entry = frappe.get_doc({
            "doctype": "General Ledger",
            "posting_date": datetime.date.today(),
            "account_affected": supplier_account.name,
            "account_balance": supplier_account.account_balance,
            "credited_amount": self.total,
            "debited_amount": 0,
            "txn_type": "Purchase Invoice",
            "txn_id": self.name,
        })
        debit_entry.insert()
        credit_entry.insert()
        supplier_account.save()
        stock_account.save()