// Copyright (c) 2023, Cargoshare and contributors
// For license information, please see license.txt

frappe.ui.form.on('Order', {
	//refresh: function(frm) {

	//}

	check_in:function(frm){
		const today = frappe.datetime.get_today();
		if(frm.doc.check_in < today){
			frm.set_value("check_in", frappe.datetime.get_today())
			frappe.throw(__("Invalid date"))
		}
	},

	check_out:function(frm){
		if(frm.doc.check_out < frm.doc.check_in){
			frm.set_value("check_out", frm.doc.check_in)
			frappe.throw(__("Invalid date"))
		}
	}
});

cur_frm.set_query("room_type", function(doc, cdt, cdn){
	return{
		filters: [
				["Room Type", "Status", "=", "Available"]
			]
	}
});
