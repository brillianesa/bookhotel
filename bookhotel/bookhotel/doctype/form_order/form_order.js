// Copyright (c) 2023, Cargoshare and contributors
// For license information, please see license.txt

function calculateNumberOfDays(frm) {
    var checkInDate = frm.doc.tanggal_checkin;
    var checkOutDate = frm.doc.tanggal_checkout;

    if (checkInDate && checkOutDate) {
        var numberOfDays = frappe.datetime.get_diff(checkOutDate, checkInDate);
        frm.doc.number_of_days = numberOfDays;
        frm.refresh_field('number_of_days');
    }
}


function calculateTotalHarga(frm, discount) {
    var hargaPerMalam = frm.doc.harga_kamarmalam;
    var numberOfDays = frm.doc.number_of_days;

    if (hargaPerMalam && numberOfDays) {
        var totalHarga = hargaPerMalam * numberOfDays;
        console.log("Total Harga sebelum diskon: " + totalHarga);
        if (discount) {
            totalHarga -= totalHarga * (discount / 100);
        }
        console.log("Total Harga setelah diskon: " + totalHarga);
        frm.doc.total_harga = totalHarga;
        frm.refresh_field('total_harga');
    }
}

function applyDiscountCode(frm) {
    var discountCode = frm.doc.diskon;
    console.log("Kode Diskon: " + discountCode);

    if (discountCode) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Discount Code",
                fields: ["code_name", "discount"],
                filters: { "code_name": discountCode },
                limit_page_length: 1
            },
            callback: function(r) {
                console.log(r.message)
                if (r.message && r.message.length > 0) {
                    var discount = r.message[0].discount;
                    console.log("Diskon: " + discount);
                    calculateTotalHarga(frm, discount);
                } else {
                    frappe.msgprint(__("Kode diskon tidak valid."));
                    frm.set_value('diskon', '');
                    calculateTotalHarga(frm, 0); 
                }
            }
        });
    } else {
        calculateTotalHarga(frm, 0); 
    }
}

frappe.ui.form.on('Form Order', {
    
    onload: function(frm) {
        frm.set_value('tanggal_pemesanan', frappe.datetime.nowdate());
		
    },
    tanggal_checkin: function(frm) {
        var currentDate = frappe.datetime.now_date();
    if (frm.doc.tanggal_checkin < currentDate) {
        frappe.msgprint(__("Tanggal check-in tidak bisa kurang dari hari ini."));
        frm.set_value('tanggal_checkin', ''); 
        return;
    }else{
        calculateNumberOfDays(frm);
        calculateTotalHarga(frm);
    }
    },

    tanggal_checkout: function(frm) {
        if (!frm.doc.tanggal_checkin || frm.doc.tanggal_checkout <= frm.doc.tanggal_checkin) {
            frappe.msgprint(__("Tanggal check-out harus melebihi tanggal check-in."));
            frm.set_value('tanggal_checkout', '');
            return;
        }else{
            calculateNumberOfDays(frm);
            calculateTotalHarga(frm);
        }
        
    },

    harga_kamarmalam: function(frm) {
        calculateTotalHarga(frm);
    },
	hotel: function(frm) {
        
        var kamarField = frm.fields_dict.room;
        kamarField.get_query = function() {
            var selectedHotel = frm.doc.hotel;
            return {
                filters: { hotel: selectedHotel }
            };
			
        };
		frm.refresh_field("room");
    },
    diskon: function(frm) {
        applyDiscountCode(frm);
    },
    room: function(frm) {
		if (frm.doc.gambar) {
			$(frm.fields_dict['gambar'].wrapper)
				.html('<img src="'+ frm.doc.gambar +'" style="max-width: 100%;">');
		} else {
			$(frm.fields_dict['gambar'].wrapper).html('');
		}
	},
    refresh: function(frm) {
		if (frm.doc.gambar) {
			$(frm.fields_dict['gambar'].wrapper)
				.html('<img src="'+ frm.doc.gambar +'" style="max-width: 100%;">');
		}
	},
    before_submit: function(frm) {
        frappe.call({
            method: 'bookhotel.bookhotel.doctype.form_order.form_order.check_availability',
            args: {
                checkin: frm.doc.tanggal_checkin,
                checkout: frm.doc.tanggal_checkout,
                room: frm.doc.room,
                customer: frm.doc.customer
            },
            async: false,
            callback: function(r) {
                if (r.message !== true) {
                    validated = false;
                    frappe.msgprint(r.message);
                }
            }
        });
    }
	
	
    
});



