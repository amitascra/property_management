# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Building(Document):
	def autoname(self):
		"""Custom naming series for buildings"""
		if self.naming_series:
			self.name = make_autoname(self.naming_series)

	def validate(self):
		"""Validate building data"""
		self.update_total_units()
		self.validate_project_link()

	def validate_project_link(self):
		"""Validate that the property project exists and is active"""
		if self.property_project:
			project = frappe.get_doc("Property Project", self.property_project)
			if project.status == "Cancelled":
				frappe.throw(f"Cannot create building for cancelled project {self.property_project}")

	def update_total_units(self):
		"""Update total units count from floors"""
		if self.name:
			total_units = frappe.db.sql("""
				SELECT SUM(f.total_units)
				FROM `tabFloor` f
				WHERE f.building = %s
			""", self.name)[0][0] or 0
			self.total_units = total_units

	def on_update(self):
		"""Actions to perform on update"""
		# Update parent project statistics
		if self.property_project:
			project = frappe.get_doc("Property Project", self.property_project)
			project.update_project_statistics()
			project.save()

	def on_trash(self):
		"""Actions to perform before deletion"""
		# Check if building has floors
		floors_count = frappe.db.count("Floor", {"building": self.name})
		if floors_count > 0:
			frappe.throw(f"Cannot delete building {self.building_name}. It has {floors_count} floors. Please delete all floors first.")

	def get_dashboard_data(self):
		"""Return dashboard data for the building"""
		return {
			"fieldname": "building",
			"transactions": [
				{
					"label": "Floors & Units",
					"items": ["Floor", "Unit"]
				},
				{
					"label": "Maintenance",
					"items": ["Service Request"]
				},
				{
					"label": "Utilities",
					"items": ["Utility Meter", "Meter Reading"]
				}
			]
		}

	def create_asset(self):
		"""Create corresponding asset for the building"""
		if not self.asset_link:
			asset = frappe.new_doc("Asset")
			asset.asset_name = self.building_name
			asset.item_code = "Building"  # Assuming a generic Building item exists
			asset.company = self.company
			asset.cost_center = self.cost_center
			asset.location = self.address or "Property Location"
			asset.purchase_date = frappe.utils.today()
			asset.available_for_use_date = frappe.utils.today()
			asset.gross_purchase_amount = 0  # To be updated later
			asset.save()
			
			self.asset_link = asset.name
			self.save()
			
			return asset.name
