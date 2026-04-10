# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import flt


class MeterReading(Document):
	def autoname(self):
		"""Custom naming series for meter readings"""
		if self.naming_series:
			self.name = make_autoname(self.naming_series)

	def validate(self):
		"""Validate meter reading data"""
		self.validate_meter_link()
		self.validate_reading_values()
		self.calculate_consumption()
		self.calculate_amount()

	def validate_meter_link(self):
		"""Validate that the utility meter exists and is active"""
		if self.utility_meter:
			meter = frappe.get_doc("Utility Meter", self.utility_meter)
			if meter.status != "Active":
				frappe.throw(f"Cannot create reading for inactive meter {self.utility_meter}")

	def validate_reading_values(self):
		"""Validate reading values"""
		if self.current_reading < 0:
			frappe.throw("Current Reading cannot be negative")
		
		if self.previous_reading and self.current_reading < self.previous_reading:
			frappe.throw("Current Reading cannot be less than Previous Reading")

	def calculate_consumption(self):
		"""Calculate consumption based on current and previous readings"""
		if self.current_reading and self.previous_reading:
			self.consumption = flt(self.current_reading - self.previous_reading, 3)
		elif self.current_reading and not self.previous_reading:
			self.consumption = flt(self.current_reading, 3)
		else:
			self.consumption = 0

	def calculate_amount(self):
		"""Calculate amount based on consumption and rate"""
		if self.consumption and self.rate_per_unit:
			self.amount = flt(self.consumption * self.rate_per_unit, 2)
		else:
			self.amount = 0

	def before_save(self):
		"""Actions before saving"""
		# Get previous reading from meter
		if self.utility_meter and not self.previous_reading:
			meter = frappe.get_doc("Utility Meter", self.utility_meter)
			self.previous_reading = meter.last_reading_value or 0

	def on_submit(self):
		"""Actions to perform on submission"""
		self.status = "Submitted"
		self.update_meter_last_reading()

	def on_cancel(self):
		"""Actions to perform on cancellation"""
		self.status = "Draft"

	def update_meter_last_reading(self):
		"""Update the meter's last reading information"""
		if self.utility_meter:
			meter = frappe.get_doc("Utility Meter", self.utility_meter)
			meter.update_last_reading(self.current_reading, self.reading_date)

	def create_utility_invoice(self):
		"""Create sales invoice for utility consumption"""
		if self.status != "Submitted" or not self.amount:
			frappe.throw("Reading must be submitted and have an amount to create invoice")

		# Get tenant information
		unit = frappe.get_doc("Unit", self.unit)
		active_tenancy = frappe.db.get_value("Tenancy", {
			"unit": self.unit,
			"status": "Active"
		}, ["name", "tenant"], as_dict=True)

		if not active_tenancy:
			frappe.throw(f"No active tenancy found for unit {self.unit}")

		tenant = frappe.get_doc("Tenant Profile", active_tenancy.tenant)
		if not tenant.customer_link:
			frappe.throw("Tenant must have a linked Customer to create invoice")

		# Create sales invoice
		invoice = frappe.new_doc("Sales Invoice")
		invoice.customer = tenant.customer_link
		invoice.posting_date = self.reading_date
		invoice.due_date = frappe.utils.add_days(self.reading_date, 30)
		invoice.company = self.company
		invoice.cost_center = self.cost_center

		# Add invoice item
		item = invoice.append("items")
		item.item_code = f"{frappe.get_value('Utility Meter', self.utility_meter, 'utility_type')} Consumption"
		item.description = f"Utility consumption for {self.utility_meter} - {self.consumption} units"
		item.qty = self.consumption
		item.rate = self.rate_per_unit
		item.amount = self.amount

		invoice.save()
		
		# Update status to billed
		self.status = "Billed"
		self.save()
		
		return invoice.name
