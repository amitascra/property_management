# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class PropertyProject(Document):
	def autoname(self):
		"""Custom naming series for property projects"""
		if self.naming_series:
			self.name = make_autoname(self.naming_series)

	def validate(self):
		"""Validate property project data"""
		self.validate_dates()
		self.update_project_statistics()

	def validate_dates(self):
		"""Validate project dates"""
		if self.start_date and self.expected_completion_date:
			if self.start_date > self.expected_completion_date:
				frappe.throw("Start Date cannot be after Expected Completion Date")
		
		if self.actual_completion_date and self.start_date:
			if self.actual_completion_date < self.start_date:
				frappe.throw("Actual Completion Date cannot be before Start Date")

	def update_project_statistics(self):
		"""Update project statistics from related buildings and units"""
		# Count total buildings
		self.total_buildings = frappe.db.count("Building", {"property_project": self.name})
		
		# Count total units
		self.total_units = frappe.db.sql("""
			SELECT COUNT(u.name)
			FROM `tabUnit` u
			INNER JOIN `tabFloor` f ON u.floor = f.name
			INNER JOIN `tabBuilding` b ON f.building = b.name
			WHERE b.property_project = %s
		""", self.name)[0][0] or 0
		
		# Count sold units
		self.sold_units = frappe.db.sql("""
			SELECT COUNT(u.name)
			FROM `tabUnit` u
			INNER JOIN `tabFloor` f ON u.floor = f.name
			INNER JOIN `tabBuilding` b ON f.building = b.name
			WHERE b.property_project = %s AND u.status = 'Sold'
		""", self.name)[0][0] or 0
		
		# Count rented units
		self.rented_units = frappe.db.sql("""
			SELECT COUNT(u.name)
			FROM `tabUnit` u
			INNER JOIN `tabFloor` f ON u.floor = f.name
			INNER JOIN `tabBuilding` b ON f.building = b.name
			WHERE b.property_project = %s AND u.status = 'Rented'
		""", self.name)[0][0] or 0
		
		# Calculate available units
		self.available_units = self.total_units - self.sold_units - self.rented_units

	def on_update(self):
		"""Actions to perform on update"""
		# Update completion status based on actual completion date
		if self.actual_completion_date and self.status != "Completed":
			self.status = "Completed"
			self.save()

	def get_dashboard_data(self):
		"""Return dashboard data for the project"""
		return {
			"fieldname": "property_project",
			"transactions": [
				{
					"label": "Buildings",
					"items": ["Building"]
				},
				{
					"label": "Units",
					"items": ["Unit"]
				},
				{
					"label": "Tenancies",
					"items": ["Tenancy"]
				}
			]
		}
