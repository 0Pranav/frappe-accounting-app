// Copyright (c) 2019, 0Pranav and contributors
// For license information, please see license.txt

frappe.ui.form.on('Account',
	"onload",
	function (frm) {
		frm.set_query('parent_account', () => {
			return {
				filters: {
					is_group: "1"
				}
			}
		})

	});

