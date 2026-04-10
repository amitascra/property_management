# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import today, add_months, getdate


class Tenancy(Document):
	def autoname(self):
		"""Custom naming series for tenancy"""
		if self.naming_series:
			self.name = make_autoname(self.naming_series)

	def validate(self):
		"""Validate tenancy data"""
		self.validate_dates()
		self.validate_unit_availability()
		self.validate_rent_due_date()

	def validate_dates(self):
		"""Validate lease dates"""
		if self.lease_start_date and self.lease_end_date:
			if getdate(self.lease_start_date) >= getdate(self.lease_end_date):
				frappe.throw("Lease Start Date must be before Lease End Date")

	def validate_unit_availability(self):
		"""Check if unit is available for the lease period"""
		if self.unit and self.lease_start_date and self.lease_end_date:
			# Check for overlapping tenancies
			overlapping_tenancies = frappe.db.sql("""
				SELECT name FROM `tabTenancy`
				WHERE unit = %s 
				AND name != %s
				AND status IN ('Active', 'Draft')
				AND (
					(lease_start_date <= %s AND lease_end_date >= %s) OR
					(lease_start_date <= %s AND lease_end_date >= %s) OR
					(lease_start_date >= %s AND lease_end_date <= %s)
				)
			""", (self.unit, self.name or "", 
				  self.lease_start_date, self.lease_start_date,
				  self.lease_end_date, self.lease_end_date,
				  self.lease_start_date, self.lease_end_date))
			
			if overlapping_tenancies:
				frappe.throw(f"Unit {self.unit} is not available for the selected period. Overlapping tenancy exists.")

	def validate_rent_due_date(self):
		"""Validate rent due date"""
		if self.rent_due_date and (self.rent_due_date < 1 or self.rent_due_date > 31):
			frappe.throw("Rent Due Date must be between 1 and 31")

	def on_submit(self):
		"""Actions to perform on submission"""
		self.status = "Active"
		self.update_unit_status()
		self.create_subscription()

	def on_cancel(self):
		"""Actions to perform on cancellation"""
		self.status = "Terminated"
		self.update_unit_status()
		self.cancel_subscription()

	def update_unit_status(self):
		"""Update unit status based on tenancy status"""
		if self.unit:
			unit = frappe.get_doc("Unit", self.unit)
			if self.status == "Active":
				unit.status = "Rented"
			elif self.status in ["Terminated", "Expired"]:
				unit.status = "Available"
			unit.save()

	def create_subscription(self):
		"""Create ERPNext subscription for automated rent billing"""
		if not self.subscription_link and self.monthly_rent:
			# Get tenant's customer link
			tenant = frappe.get_doc("Tenant Profile", self.tenant)
			if not tenant.customer_link:
				frappe.throw("Tenant must have a linked Customer to create subscription")

			subscription = frappe.new_doc("Subscription")
			subscription.party_type = "Customer"
			subscription.party = tenant.customer_link
			subscription.start_date = self.lease_start_date
			subscription.end_date = self.lease_end_date
			subscription.generate_invoice_at_period_start = 1
			subscription.submit_invoice = 0
			subscription.generate_new_invoices_past_due_date = 1
			
			# Add subscription plan
			plan = subscription.append("plans")
			plan.plan = self.get_or_create_subscription_plan()
			plan.qty = 1
			
			subscription.save()
			subscription.submit()
			
			self.subscription_link = subscription.name
			self.save()

	def get_or_create_subscription_plan(self):
		"""Get or create subscription plan for this tenancy"""
		plan_name = f"Rent Plan - {self.unit}"
		existing_plan = frappe.db.exists("Subscription Plan", plan_name)
		
		if not existing_plan:
			plan = frappe.new_doc("Subscription Plan")
			plan.plan_name = plan_name
			plan.item = self.get_unit_item()
			plan.price_determination = "Fixed Rate"
			plan.cost = self.monthly_rent
			plan.billing_interval = "Month"
			plan.billing_interval_count = 1
			plan.save()
			return plan.name
		
		return existing_plan

	def get_unit_item(self):
		"""Get or create item for the unit"""
		unit = frappe.get_doc("Unit", self.unit)
		if unit.item_code:
			return unit.item_code
		else:
			frappe.throw(f"Unit {self.unit} must have an associated Item Code")

	def cancel_subscription(self):
		"""Cancel the associated subscription"""
		if self.subscription_link:
			subscription = frappe.get_doc("Subscription", self.subscription_link)
			if subscription.docstatus == 1:
				subscription.cancel()

	def add_rent_payment(self, payment_date, amount, payment_mode="Cash"):
		"""Add rent payment to history"""
		rent_entry = self.append("rent_history")
		rent_entry.payment_date = payment_date
		rent_entry.amount = amount
		rent_entry.payment_mode = payment_mode
		rent_entry.status = "Paid"
		self.save()

	def get_dashboard_data(self):
		"""Return dashboard data for the tenancy"""
		return {
			"fieldname": "tenancy",
			"transactions": [
				{
					"label": "Billing",
					"items": ["Sales Invoice", "Payment Entry"]
				},
				{
					"label": "Maintenance",
					"items": ["Service Request"]
				}
			]
		}

	def calculate_outstanding_rent(self):
		"""Calculate outstanding rent amount"""
		if not self.subscription_link:
			return 0
		
		# Get unpaid invoices from subscription
		unpaid_invoices = frappe.db.sql("""
			SELECT SUM(outstanding_amount)
			FROM `tabSales Invoice`
			WHERE subscription = %s
			AND outstanding_amount > 0
			AND docstatus = 1
		""", self.subscription_link)
		
		return unpaid_invoices[0][0] if unpaid_invoices[0][0] else 0
