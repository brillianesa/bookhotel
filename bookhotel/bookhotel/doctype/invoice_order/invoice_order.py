# Copyright (c) 2023, Cargoshare and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class InvoiceOrder(Document):
    def validate(self):
            if self.status == 'Paid':  
               
                discount_code = frappe.get_all(
                    'Discount Code',
                    filters={
                        'code_name': self.diskon,
					},
                    fields=['name', 'quota']
				)
                if discount_code:
                    disc_doc = frappe.get_doc('Discount Code', discount_code[0].name)
                    disc_doc.quota -= 1
                    disc_doc.save()
                    
                frappe.db.commit()

    def on_submit(self):
        if self.status == 'Checked Out': 
            room_booking = frappe.get_all(
                'Room Booking',
                filters={
                    'room': self.room,
                    'customer': self.customer,
                    'check_in_date': ['=', self.tanggal_checkin],
                    'check_out_date': ['=', self.tanggal_checkout],
                    'status': 'Booked'
                },
                fields=['name', 'status']
            )

            if room_booking:
                booking_doc = frappe.get_doc('Room Booking', room_booking[0].name)
                booking_doc.status = 'Checked Out'
                booking_doc.save()

            frappe.db.commit()