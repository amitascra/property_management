# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Floor(Document):
	def autoname(self):
		"""Custom naming series for floors"""
		if self.naming_series:
			self.name = make_autoname(self.naming_series)

	def validate(self):
		"""Validate floor data"""
		self.update_total_units()
		self.validate_building_link()

	def validate_building_link(self):
		"""Validate that the building exists and is active"""
		if self.building:
			building = frappe.get_doc("Building", self.building)
			if building.status == "Cancelled":
				frappe.throw(f"Cannot create floor for cancelled building {self.building}")

	def update_total_units(self):
		"""Update total units count from units on this floor"""
		if self.name:
			total_units = frappe.db.count("Unit", {"floor": self.name})
			self.total_units = total_units

	def on_update(self):
		"""Actions to perform on update"""
		# Update parent building statistics
		if self.building:
			building = frappe.get_doc("Building", self.building)
			building.update_total_units()
			building.save()

	def on_trash(self):
		"""Actions to perform before deletion"""
		# Check if floor has units
		units_count = frappe.db.count("Unit", {"floor": self.name})
		if units_count > 0:
			frappe.throw(f"Cannot delete floor {self.floor_number}. It has {units_count} units. Please delete all units first.")

	def get_dashboard_data(self):
		"""Return dashboard data for the floor"""
		return {
			"fieldname": "floor",
			"transactions": [
				{
					"label": "Units",
					"items": ["Unit"]
				},
				{
					"label": "Maintenance",
					"items": ["Service Request"]
				}
			]
		}
