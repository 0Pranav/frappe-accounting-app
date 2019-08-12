# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import datetime
import frappe
from frappe.model.document import Document


class PurchaseInvoice(Document):
    def on_submit(self, *args, **kwargs):
        # Create general ledger entry here
        supplier = frappe.get_doc("Supplier", self.supplier)
        supplier_account = frappe.get_doc("Account", supplier.supplier_account)
        stock_expense_account = frappe.get_doc("Account", "Stock Expense")
        super().save(self, *args, **kwargs)

        # Adjust Balance in accounts
        supplier_account.account_balance = supplier_account.account_balance - self.total
        supplier_account.save()
        stock_expense_account.account_balance = stock_expense_account.account_balance - self.total
        stock_expense_account.save()

        # Debit Entry
        debit_entry = frappe.get_doc({
            "doctype": "General Ledger",
            "posting_date": datetime.date.today(),
            "account_affected": supplier_account.name,
            "credited_amount": 0,
            "debited_amount": self.total,
            "account_balance": supplier_account.account_balance,
            "txn_type": "Purchase Invoice",
            "txn_id": self.name,
        })
        debit_entry.insert()

        # Credit Entry
        credit_entry = frappe.get_doc({
            "doctype": "General Ledger",
            "posting_date": datetime.date.today(),
            "account_affected": stock_expense_account.name,
            "account_balance": stock_expense_account.account_balance,
            "credited_amount": self.total,
            "debited_amount": 0,
            "txn_type": "Purchase Invoice",
            "txn_id": self.name,
        })
        credit_entry.insert()