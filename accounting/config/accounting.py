from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
        {
            "label":_("Components"),
            "icon":"octicon-person",
            "items":[
                {
                    "type":"doctype",
                    "name":"Account",
                    "label":_("Accounts"),
                    "description":_("Accounts to credit and debit from")
                },
                {
                    "type":"doctype",
                    "name":"Item",
                    "label":_("Items"),
                    "description":_("Items to buy and sell")
                }
            ]
        },
        {
            "label":_("Buy"),
            "icon":"octicon-sign-in",
            "items":[
                {
                    "type":"doctype",
                    "name":"Purchase Invoice",
                    "label":_("Purchase Invoices"),
                    "description":_("none")
                },
                {
                    "type":"doctype",
                    "name":"Supplier",
                    "label":_("Suppliers"),
                    "description":_("Suppliers to buy items from")
                }
            ]
        },
        {
            "label":_("Sell"),
            "icon":"",
            "items":[
                {
                    "type":"doctype",
                    "name":"Sales Invoice",
                    "label":_("Sales Invoices"),
                    "description":_("none")
                },
                {
                    "type":"doctype",
                    "name":"Customer",
                    "label":_("Customers"),
                    "description":_("Customers to sell items to")
                }
            ]
        }
    ]