# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class TenantProfile(Document):
	def autoname(self):
		"""Custom naming series for tenant profiles"""
		if self.naming_series:
			self.name = make_autoname(self.naming_series)

	def validate(self):
		"""Validate tenant profile data"""
		self.validate_contact_details()
		self.create_customer_if_needed()

	def validate_contact_details(self):
		"""Validate contact information"""
		if self.email:
			frappe.utils.validate_email_address(self.email, True)
		
		# Check for duplicate contact number
		existing_tenant = frappe.db.exists("Tenant Profile", {
			"contact_number": self.contact_number,
			"name": ["!=", self.name]
		})
		if existing_tenant:
			frappe.throw(f"Tenant with contact number {self.contact_number} already exists")

	def create_customer_if_needed(self):
		"""Create corresponding customer if not exists"""
		if not self.customer_link:
			# Check if customer already exists with same name
			existing_customer = frappe.db.exists("Customer", {"customer_name": self.tenant_name})
			
			if not existing_customer:
				customer = frappe.new_doc("Customer")
				customer.customer_name = self.tenant_name
				customer.customer_type = "Individual"
				customer.customer_group = "Individual"  # Assuming this group exists
				customer.territory = "All Territories"  # Default territory
				
				# Add contact details
				if self.email:
					customer.email_id = self.email
				if self.contact_number:
					customer.mobile_no = self.contact_number
				
				customer.save()
				self.customer_link = customer.name
			else:
				self.customer_link = existing_customer

	def on_update(self):
		"""Actions to perform on update"""
		# Update linked customer details if exists
		if self.customer_link:
			customer = frappe.get_doc("Customer", self.customer_link)
			customer.customer_name = self.tenant_name
			if self.email:
				customer.email_id = self.email
			if self.contact_number:
				customer.mobile_no = self.contact_number
			customer.save()

	def on_trash(self):
		"""Actions to perform before deletion"""
		# Check if tenant has active tenancies
		active_tenancies = frappe.db.count("Tenancy", {
			"tenant": self.name,
			"status": ["in", ["Active", "Draft"]]
		})
		if active_tenancies > 0:
			frappe.throw(f"Cannot delete tenant {self.tenant_name}. They have {active_tenancies} active tenancies.")

	def get_dashboard_data(self):
		"""Return dashboard data for the tenant"""
		return {
			"fieldname": "tenant",
			"transactions": [
				{
					"label": "Tenancy",
					"items": ["Tenancy"]
				},
				{
					"label": "Payments",
					"items": ["Sales Invoice", "Payment Entry"]
				}
			]
		}

	def get_active_tenancies(self):
		"""Get all active tenancies for this tenant"""
		return frappe.get_all("Tenancy", {
			"tenant": self.name,
			"status": "Active"
		}, ["name", "unit", "lease_start_date", "lease_end_date", "monthly_rent"])

	def calculate_total_monthly_rent(self):
		"""Calculate total monthly rent from all active tenancies"""
		active_tenancies = self.get_active_tenancies()
		total_rent = sum([tenancy.get("monthly_rent", 0) for tenancy in active_tenancies])
		return total_rent
