# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, add_days, getdate


def check_lease_expiry():
	"""Check for leases expiring in the next 30 days and send notifications"""
	expiring_leases = frappe.get_all("Tenancy", {
		"status": "Active",
		"lease_end_date": ["between", [today(), add_days(today(), 30)]]
	}, ["name", "unit", "tenant", "lease_end_date", "monthly_rent"])
	
	for lease in expiring_leases:
		days_to_expiry = (getdate(lease.lease_end_date) - getdate(today())).days
		
		# Send notification to property manager
		frappe.sendmail(
			recipients=get_property_managers(),
			subject=f"Lease Expiring Soon - {lease.unit}",
			message=f"""
			<p>Lease for unit {lease.unit} is expiring in {days_to_expiry} days.</p>
			<p><strong>Details:</strong></p>
			<ul>
				<li>Tenant: {lease.tenant}</li>
				<li>Expiry Date: {lease.lease_end_date}</li>
				<li>Monthly Rent: {lease.monthly_rent}</li>
			</ul>
			<p>Please contact the tenant for lease renewal.</p>
			""",
			reference_doctype="Tenancy",
			reference_name=lease.name
		)


def send_rent_reminders():
	"""Send rent payment reminders for overdue payments"""
	overdue_invoices = frappe.db.sql("""
		SELECT si.name, si.customer, si.due_date, si.outstanding_amount,
			   t.unit, tp.tenant_name, tp.email, tp.contact_number
		FROM `tabSales Invoice` si
		INNER JOIN `tabTenancy` t ON si.subscription = t.subscription_link
		INNER JOIN `tabTenant Profile` tp ON t.tenant = tp.name
		WHERE si.outstanding_amount > 0
		AND si.due_date < %s
		AND si.docstatus = 1
	""", (today(),), as_dict=True)
	
	for invoice in overdue_invoices:
		days_overdue = (getdate(today()) - getdate(invoice.due_date)).days
		
		if invoice.email:
			frappe.sendmail(
				recipients=[invoice.email],
				subject=f"Rent Payment Overdue - Unit {invoice.unit}",
				message=f"""
				<p>Dear {invoice.tenant_name},</p>
				<p>Your rent payment for unit {invoice.unit} is overdue by {days_overdue} days.</p>
				<p><strong>Payment Details:</strong></p>
				<ul>
					<li>Due Date: {invoice.due_date}</li>
					<li>Outstanding Amount: {invoice.outstanding_amount}</li>
				</ul>
				<p>Please make the payment at your earliest convenience.</p>
				""",
				reference_doctype="Sales Invoice",
				reference_name=invoice.name
			)


def generate_maintenance_reports():
	"""Generate weekly maintenance reports"""
	# Get service requests from the past week
	from frappe.utils import add_days
	week_ago = add_days(today(), -7)
	
	service_requests = frappe.get_all("Service Request", {
		"creation": [">=", week_ago]
	}, ["name", "unit", "category", "priority", "status", "cost"])
	
	if service_requests:
		# Generate summary report
		total_requests = len(service_requests)
		total_cost = sum([sr.get("cost", 0) for sr in service_requests])
		resolved_requests = len([sr for sr in service_requests if sr.status == "Resolved"])
		
		report_content = f"""
		<h3>Weekly Maintenance Report</h3>
		<p><strong>Summary:</strong></p>
		<ul>
			<li>Total Requests: {total_requests}</li>
			<li>Resolved Requests: {resolved_requests}</li>
			<li>Resolution Rate: {(resolved_requests/total_requests*100):.1f}%</li>
			<li>Total Cost: {total_cost}</li>
		</ul>
		"""
		
		# Send to property managers
		frappe.sendmail(
			recipients=get_property_managers(),
			subject="Weekly Maintenance Report",
			message=report_content
		)


def update_property_valuations():
	"""Update property valuations monthly (placeholder for future enhancement)"""
	# This could integrate with external valuation APIs
	# For now, just log the task
	frappe.logger().info("Monthly property valuation update task executed")


def get_property_managers():
	"""Get list of property manager email addresses"""
	property_managers = frappe.get_all("Has Role", {
		"role": "Property Manager",
		"parenttype": "User"
	}, ["parent"])
	
	emails = []
	for pm in property_managers:
		user = frappe.get_doc("User", pm.parent)
		if user.email and user.enabled:
			emails.append(user.email)
	
	return emails
