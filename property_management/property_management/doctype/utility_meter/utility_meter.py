# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class UtilityMeter(Document):
	def validate(self):
		"""Validate utility meter data"""
		self.validate_unit_link()
		self.validate_meter_number()

	def validate_unit_link(self):
		"""Validate that the unit exists"""
		if self.unit:
			unit = frappe.get_doc("Unit", self.unit)
			if unit.status == "Sold":
				frappe.msgprint(f"Warning: Unit {self.unit} is marked as Sold")

	def validate_meter_number(self):
		"""Validate meter number uniqueness"""
		existing_meter = frappe.db.exists("Utility Meter", {
			"meter_number": self.meter_number,
			"name": ["!=", self.name]
		})
		if existing_meter:
			frappe.throw(f"Meter with number {self.meter_number} already exists")

	def on_update(self):
		"""Actions to perform on update"""
		self.create_asset_if_needed()

	def create_asset_if_needed(self):
		"""Create corresponding asset for the meter if not exists"""
		if not self.asset_link and self.status == "Active":
			asset = frappe.new_doc("Asset")
			asset.asset_name = f"{self.utility_type} Meter - {self.meter_number}"
			asset.item_code = f"{self.utility_type} Meter"  # Assuming generic meter items exist
			asset.company = self.company
			asset.cost_center = self.cost_center
			asset.location = self.meter_location or f"Unit {self.unit}"
			asset.purchase_date = self.installation_date or frappe.utils.today()
			asset.available_for_use_date = self.installation_date or frappe.utils.today()
			asset.gross_purchase_amount = 0  # To be updated later
			asset.save()
			
			self.asset_link = asset.name
			self.save()

	def update_last_reading(self, reading_value, reading_date):
		"""Update last reading information"""
		self.last_reading_value = reading_value
		self.last_reading_date = reading_date
		self.save()

	def get_dashboard_data(self):
		"""Return dashboard data for the meter"""
		return {
			"fieldname": "utility_meter",
			"transactions": [
				{
					"label": "Readings",
					"items": ["Meter Reading"]
				}
			]
		}

	def get_consumption_history(self, months=12):
		"""Get consumption history for specified months"""
		return frappe.db.sql("""
			SELECT 
				DATE_FORMAT(reading_date, '%%Y-%%m') as month,
				SUM(consumption) as total_consumption,
				AVG(consumption) as avg_consumption,
				COUNT(*) as reading_count
			FROM `tabMeter Reading`
			WHERE utility_meter = %s
			AND reading_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
			AND docstatus = 1
			GROUP BY DATE_FORMAT(reading_date, '%%Y-%%m')
			ORDER BY month DESC
		""", (self.name, months), as_dict=True)

	def calculate_average_consumption(self, months=6):
		"""Calculate average monthly consumption"""
		history = self.get_consumption_history(months)
		if history:
			total_consumption = sum([h.total_consumption for h in history])
			return total_consumption / len(history)
		return 0
