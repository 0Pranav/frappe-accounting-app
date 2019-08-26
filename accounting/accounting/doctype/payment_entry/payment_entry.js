// Copyright (c) 2019, 0Pranav and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	refresh: function (frm) {
		if (frm.is_dirty()) {
			console.log("h");
			set_amount_to_remaining(frm)
		}
		frm.set_query("payment_type", () => {
			return {
				filters: {
					name: ["in", ["Sales Invoice", "Purchase Invoice"]]
				}
			}
		})
	}
});

frappe.ui.form.on("Payment Entry", "against_invoice", set_amount_to_remaining)

async function set_amount_to_remaining(frm) {
	let invoice = await frappe.db.get_doc(frm.doc.payment_type, frm.doc.against_invoice)
	let payment_entries = await frappe.db.get_list('Payment Entry', {
		fields: ['name', 'payment_amount'],
		filters: {
			against_invoice: frm.doc.against_invoice,
			docstatus: 1
		}
	})
	let paid_amount;
	paid_amount = payment_entries.reduce(get_paid_amount, 0)
	let pending_amount = invoice.total - paid_amount;
	frappe.model.set_value(frm.doctype, frm.docname, "payment_amount", pending_amount)
	console.log([paid_amount, pending_amount, invoice.total]);
	debugger
}

function get_paid_amount(total, entry) {
	return total + entry.payment_amount
}