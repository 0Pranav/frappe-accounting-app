// Copyright (c) 2019, 0Pranav and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice','refresh',updateTotalForInvoice)
frappe.ui.form.on('Invoice List Item','item_unit_price',updateTotalForItem)
frappe.ui.form.on('Invoice List Item','item_units',updateTotalForItem)


function updateTotalForItem(frm,cdt, cdn){
	var d = locals[cdt][cdn];
	frappe.model.set_value(d.doctype,d.name,"item_total",d.item_unit_price*d.item_units);
	updateTotalForInvoice(frm,cdt,cdn)
}

function updateTotalForInvoice(frm,cdt,cdn){
	var total_amount = 0;
	$.each(frm.doc.items || [], function(i, d) {
	total_amount += flt(d.item_total);
	});
	frm.set_value("total", total_amount);
}

//frappe.ui.form.on('Invoice List Item', 'item', function (frm,cdt,cdn) {
//	var d = locals[cdt][cdn];
//	frappe.model.set_value(d.doctype,d.name,"item_unit_price",d.item.item_default_price);
//})