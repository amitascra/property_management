# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Unit(Document):
	def autoname(self):
		"""Custom naming series for units"""
		if self.naming_series:
			self.name = make_autoname(self.naming_series)

	def validate(self):
		"""Validate unit data"""
		self.validate_floor_link()
		self.validate_areas()
		self.create_item_if_needed()

	def validate_floor_link(self):
		"""Validate that the floor exists and is active"""
		if self.floor:
			floor = frappe.get_doc("Floor", self.floor)
			if floor.status == "Cancelled":
				frappe.throw(f"Cannot create unit for cancelled floor {self.floor}")

	def validate_areas(self):
		"""Validate area measurements"""
		if self.carpet_area and self.built_up_area:
			if self.carpet_area > self.built_up_area:
				frappe.throw("Carpet Area cannot be greater than Built-up Area")
		
		if self.built_up_area and self.super_built_up_area:
			if self.built_up_area > self.super_built_up_area:
				frappe.throw("Built-up Area cannot be greater than Super Built-up Area")

	def create_item_if_needed(self):
		"""Create corresponding item for the unit if not exists"""
		if not self.item_code:
			# Check if item already exists
			item_name = f"{self.unit_number} - {self.unit_type}"
			existing_item = frappe.db.exists("Item", {"item_name": item_name})
			
			if not existing_item:
				item = frappe.new_doc("Item")
				item.item_code = f"UNIT-{self.unit_number}"
				item.item_name = item_name
				item.item_group = "Properties"  # Assuming this item group exists
				item.stock_uom = "Nos"
				item.is_stock_item = 0
				item.is_sales_item = 1
				item.is_purchase_item = 0
				item.standard_rate = self.base_price or 0
				item.save()
				
				self.item_code = item.name
			else:
				self.item_code = existing_item

	def on_update(self):
		"""Actions to perform on update"""
		# Update parent floor statistics
		if self.floor:
			floor = frappe.get_doc("Floor", self.floor)
			floor.update_total_units()
			floor.save()

	def on_trash(self):
		"""Actions to perform before deletion"""
		# Check if unit has active tenancies
		active_tenancies = frappe.db.count("Tenancy", {
			"unit": self.name,
			"status": ["in", ["Active", "Draft"]]
		})
		if active_tenancies > 0:
			frappe.throw(f"Cannot delete unit {self.unit_number}. It has {active_tenancies} active tenancies.")

	def get_dashboard_data(self):
		"""Return dashboard data for the unit"""
		return {
			"fieldname": "unit",
			"transactions": [
				{
					"label": "Tenancy",
					"items": ["Tenancy"]
				},
				{
					"label": "Utilities",
					"items": ["Utility Meter", "Meter Reading"]
				},
				{
					"label": "Maintenance",
					"items": ["Service Request"]
				}
			]
		}

	def get_current_tenant(self):
		"""Get current active tenant for this unit"""
		active_tenancy = frappe.db.get_value("Tenancy", {
			"unit": self.name,
			"status": "Active"
		}, ["tenant", "lease_start_date", "lease_end_date"], as_dict=True)
		
		return active_tenancy

	def calculate_rental_yield(self, monthly_rent):
		"""Calculate rental yield based on current market value"""
		if self.current_market_value and monthly_rent:
			annual_rent = monthly_rent * 12
			yield_percentage = (annual_rent / self.current_market_value) * 100
			return yield_percentage
		return 0
