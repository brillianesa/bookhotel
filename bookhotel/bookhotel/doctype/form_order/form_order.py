# Copyright (c) 2023, Cargoshare and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class FormOrder(Document):
    def on_submit(self):
        self.make_invoice()

    def make_invoice(self):
        invoice = frappe.get_doc({
            'doctype': 'Invoice Order',
            'tanggal_pemesanan': self.tanggal_pemesanan,
            'tanggal_checkin': self.tanggal_checkin,
            'tanggal_checkout': self.tanggal_checkout,
            'customer': self.customer,
            'nama_customer': self.nama_customer,
            'nomor_telepon': self.nomor_telepon,
            'email': self.email,
            'hotel': self.hotel,
            'room': self.room,
            'jenis_kamar': self.jenis_kamar,
            'nomor_kamar': self.nomor_kamar,
            'fasilitas': self.fasilitas,
            'deskripsi': self.deskripsi,
            'harga_kamarmalam': self.harga_kamarmalam,
            'gambar': self.gambar,
            'diskon': self.diskon,
            'total_harga': self.total_harga,
            'order_id': self.name,
            'status': 'Unpaid'
        })

        invoice.insert()  
        frappe.db.commit()  


@frappe.whitelist()
def check_availability(checkin, checkout, room, customer):
    booking_exists = frappe.db.exists(
        'Room Booking',
        {
            'room': room,
            'customer': customer,
            'check_in_date': ['<=', checkout],
            'check_out_date': ['>=', checkin],
            'status': 'Booked'
        }
    )

    if booking_exists:
        return _("Room is not available on the selected dates.")
        
    
    booking = frappe.new_doc('Room Booking')
    booking.room = room
    booking.customer = customer
    booking.check_in_date = checkin
    booking.check_out_date = checkout
    booking.status = 'Booked'
    booking.save()
    frappe.db.commit()
    return True
	
    

	
