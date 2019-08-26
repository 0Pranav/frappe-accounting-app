function add_custom_button(frm) {
	if (frm.doc.docstatus == 1 && (frm.doc.doctype == "Sales Invoice" || frm.doc.doctype == "Purchase Invoice")) {
		frm.add_custom_button("Make Payment Entry", () => { frappe.set_route("Form/Payment Entry/New Payment Entry", { payment_type: frm.doc.doctype, against_invoice: frm.doc.name }) });
		frm.add_custom_button("View Ledger", () => {
			debugger;
			frappe.route_options = { txn_type: frm.doc.doctype, txn_id: frm.doc.name };
			frappe.set_route("query-report/General Ledger")
		});
	}
}

function updateTotalForItem(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.model.set_value(d.doctype, d.name, "item_total", d.item_unit_price * d.item_units);
	updateTotalForInvoice(frm, cdt, cdn);
}

function updateTotalForInvoice(frm, cdt, cdn) {
	var total_amount = 0;
	$.each(frm.doc.items || [], function (i, d) {
		total_amount += flt(d.item_total);
	});
	frm.set_value("total", total_amount);
}
