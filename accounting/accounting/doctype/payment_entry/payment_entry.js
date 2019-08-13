// Copyright (c) 2019, 0Pranav and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
	// refresh: function(frm) {

	// }
	refresh : function(frm){
		frm.set_query("payment_type",()=>{
			return {
				filters : {
					name : ["in","Sales Invoice","Purchase Invoice"]
				}
			}
		})
	}
});
