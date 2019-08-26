// Copyright (c) 2019, 0Pranav and contributors
// For license information, please see license.txt
{% include 'accounting/public/js/invoice_functions.js' %}

frappe.ui.form.on('Purchase Invoice', 'refresh',add_custom_button)

frappe.ui.form.on('Invoice List Item', 'items_remove', updateTotalForInvoice);
frappe.ui.form.on('Invoice List Item', 'item_unit_price', updateTotalForItem);
frappe.ui.form.on('Invoice List Item', 'item_units', updateTotalForItem);