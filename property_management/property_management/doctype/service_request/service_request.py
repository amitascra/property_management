# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import today, now_datetime


class ServiceRequest(Document):
	def autoname(self):
		"""Custom naming series for service requests"""
		if self.naming_series:
			self.name = make_autoname(self.naming_series)

	def validate(self):
		"""Validate service request data"""
		self.validate_unit_link()
		self.validate_tenant_link()
		self.set_defaults()

	def validate_unit_link(self):
		"""Validate that the unit exists"""
		if self.unit:
			unit = frappe.get_doc("Unit", self.unit)
			if unit.status not in ["Rented", "Sold", "Available"]:
				frappe.throw(f"Cannot create service request for unit with status {unit.status}")

	def validate_tenant_link(self):
		"""Validate tenant and set tenancy if applicable"""
		if self.tenant and self.unit:
			# Find active tenancy for this tenant and unit
			active_tenancy = frappe.db.get_value("Tenancy", {
				"unit": self.unit,
				"tenant": self.tenant,
				"status": "Active"
			})
			if active_tenancy:
				self.tenancy = active_tenancy

	def set_defaults(self):
		"""Set default values"""
		if not self.requested_date:
			self.requested_date = today()
		
		# Auto-assign based on category if no assignment
		if not self.assigned_to and self.category:
			self.auto_assign_technician()

	def auto_assign_technician(self):
		"""Auto-assign technician based on category"""
		# This could be enhanced with a mapping table
		category_assignments = {
			"Plumbing": "Plumber",
			"Electrical": "Electrician",
			"AC/HVAC": "AC Technician",
			"Cleaning": "Housekeeping",
			"Security": "Security Manager"
		}
		
		role_to_find = category_assignments.get(self.category)
		if role_to_find:
			# Find users with the specific role
			users = frappe.get_all("Has Role", {
				"role": role_to_find,
				"parenttype": "User"
			}, ["parent"])
			
			if users:
				self.assigned_to = users[0].parent

	def on_update(self):
		"""Actions to perform on update"""
		self.send_notifications()
		self.update_resolution_date()

	def update_resolution_date(self):
		"""Update resolution date when status changes to resolved"""
		if self.status == "Resolved" and not self.resolution_date:
			self.resolution_date = today()

	def send_notifications(self):
		"""Send notifications based on status changes"""
		if self.has_value_changed("status"):
			self.notify_stakeholders()

	def notify_stakeholders(self):
		"""Notify relevant stakeholders about status changes"""
		# Notify tenant
		if self.tenant:
			tenant = frappe.get_doc("Tenant Profile", self.tenant)
			if tenant.email:
				self.send_email_notification(
					recipient=tenant.email,
					subject=f"Service Request {self.name} - Status Update",
					message=f"Your service request for {self.unit} has been updated to {self.status}"
				)
		
		# Notify assigned technician
		if self.assigned_to:
			user = frappe.get_doc("User", self.assigned_to)
			if user.email:
				self.send_email_notification(
					recipient=user.email,
					subject=f"Service Request {self.name} - Assignment",
					message=f"You have been assigned a {self.priority.lower()} priority {self.category} request for {self.unit}"
				)

	def send_email_notification(self, recipient, subject, message):
		"""Send email notification"""
		try:
			frappe.sendmail(
				recipients=[recipient],
				subject=subject,
				message=message,
				reference_doctype=self.doctype,
				reference_name=self.name
			)
		except Exception as e:
			frappe.log_error(f"Failed to send notification: {str(e)}")

	def create_expense_entry(self):
		"""Create expense entry for the service cost"""
		if self.cost and self.status == "Resolved":
			expense = frappe.new_doc("Expense Claim")
			expense.employee = self.assigned_to
			expense.expense_date = self.resolution_date or today()
			expense.company = self.company
			expense.cost_center = self.cost_center
			
			# Add expense detail
			detail = expense.append("expenses")
			detail.expense_type = f"{self.category} Maintenance"
			detail.description = f"Service request {self.name} - {self.description[:100]}"
			detail.amount = self.cost
			detail.sanctioned_amount = self.cost
			
			expense.save()
			return expense.name

	def get_dashboard_data(self):
		"""Return dashboard data for the service request"""
		return {
			"fieldname": "service_request",
			"transactions": [
				{
					"label": "Expenses",
					"items": ["Expense Claim"]
				}
			]
		}

	def calculate_resolution_time(self):
		"""Calculate time taken to resolve the request"""
		if self.resolution_date and self.requested_date:
			from frappe.utils import date_diff
			return date_diff(self.resolution_date, self.requested_date)
		return 0

	def get_similar_requests(self, limit=5):
		"""Get similar service requests for reference"""
		return frappe.get_all("Service Request", {
			"unit": self.unit,
			"category": self.category,
			"name": ["!=", self.name]
		}, ["name", "description", "status", "resolution_date", "cost"], 
		limit=limit, order_by="creation desc")
