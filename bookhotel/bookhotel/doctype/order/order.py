# Copyright (c) 2023, Cargoshare and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff

class Order(Document):
	def validate(self):

		#Create variables for room, customer, and discount data
		master_room = frappe.get_doc("Room Type", self.room_type)
		master_customer = frappe.get_doc("Master Customer", self.master_customer)

		#Check if discount code is used
		if not self.code:
			discount = 0

		else:
			master_discount = frappe.get_doc("Discount Code", self.code)
			discount = frappe.get_value("Discount Code", self.code, "discount")

			#Update quota if a discount code is used
			if self.code == "NEWUSER":
				master_discount.quota = master_discount.quota - 1
				master_discount.save()

				master_customer.new_user = "False"
				master_customer.save()

			else:
				master_discount.quota = master_discount.quota - 1
				master_discount.save()

		#Sum final price and book a room
		if not self.is_new():

			#If the user is not a new user, the user cannot get any discount using the code "NEWUSER"
			if self.price > 0:
				if master_customer.new_user == "False" and self.code == "NEWUSER":
					discount = 0
					frappe.throw(title="Error", msg="Discount code ini hanya berlaku untuk pengguna baru")

				total_discount = self.price * (discount / 100)
				self.price = (self.price - total_discount) * date_diff(self.check_out, self.check_in)

				master_room.status = "Unavailable"
				master_room.save()

			else:
				self.price = 0

	#Create an invoice
	def on_submit(self):
		invoice = frappe.new_doc("Invoice")
		invoice.master_customer = self.master_customer
		invoice.master_hotel = self.master_hotel
		invoice.room_type = self.room_type
		invoice.check_in = self.check_in
		invoice.check_out = self.check_out
		invoice.price = self.price
		invoice.save()
