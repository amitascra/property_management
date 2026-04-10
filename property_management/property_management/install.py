# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def after_install():
	"""Run after app installation"""
	create_custom_roles()
	create_default_role_profiles()
	configure_doctype_permissions()
	setup_erpnext_custom_fields()
	frappe.db.commit()


def after_migrate():
	"""Run after migration - when DocTypes are fully synced"""
	import_workspace_fixtures()
	setup_erpnext_custom_fields()
	frappe.db.commit()


def import_workspace_fixtures():
	"""Import workspace, dashboard charts, and number cards fixtures"""
	try:
		import os
		import json
		
		# Import workspace
		workspace_path = os.path.join(
			frappe.get_app_path("property_management"),
			"property_management", 
			"workspace", 
			"property_management", 
			"property_management.json"
		)
		
		if os.path.exists(workspace_path):
			with open(workspace_path, 'r') as f:
				workspace_data = json.load(f)
				
			# Check if workspace already exists
			if not frappe.db.exists("Workspace", workspace_data.get("name")):
				workspace_doc = frappe.get_doc(workspace_data)
				workspace_doc.insert(ignore_permissions=True)
				frappe.logger().info(f"Created workspace: {workspace_data.get('name')}")
			else:
				# Update existing workspace
				existing_workspace = frappe.get_doc("Workspace", workspace_data.get("name"))
				existing_workspace.update(workspace_data)
				existing_workspace.save(ignore_permissions=True)
				frappe.logger().info(f"Updated workspace: {workspace_data.get('name')}")
		
		# Import dashboard charts
		import_dashboard_charts()
		
		# Import number cards
		import_number_cards()
		
		# Import dashboard after charts and cards are created
		import_dashboard_fixtures()
			
	except Exception as e:
		frappe.logger().error(f"Error importing workspace fixtures: {str(e)}")


def import_dashboard_charts():
	"""Import dashboard chart sources"""
	import os
	import json
	
	charts_dir = os.path.join(
		frappe.get_app_path("property_management"),
		"property_management", 
		"dashboard_chart_source"
	)
	
	if os.path.exists(charts_dir):
		for chart_folder in os.listdir(charts_dir):
			chart_path = os.path.join(charts_dir, chart_folder, f"{chart_folder}.json")
			if os.path.exists(chart_path):
				with open(chart_path, 'r') as f:
					chart_data = json.load(f)
				
				if not frappe.db.exists("Dashboard Chart Source", chart_data.get("name")):
					chart_doc = frappe.get_doc(chart_data)
					chart_doc.insert(ignore_permissions=True)
					frappe.logger().info(f"Created dashboard chart: {chart_data.get('name')}")


def import_number_cards():
	"""Import number cards"""
	import os
	import json
	
	cards_dir = os.path.join(
		frappe.get_app_path("property_management"),
		"property_management", 
		"number_card"
	)
	
	if os.path.exists(cards_dir):
		for card_folder in os.listdir(cards_dir):
			card_path = os.path.join(cards_dir, card_folder, f"{card_folder}.json")
			if os.path.exists(card_path):
				with open(card_path, 'r') as f:
					card_data = json.load(f)
				
				if not frappe.db.exists("Number Card", card_data.get("name")):
					card_doc = frappe.get_doc(card_data)
					card_doc.insert(ignore_permissions=True)
					frappe.logger().info(f"Created number card: {card_data.get('name')}")


def create_custom_roles():
	"""Create custom roles for Property Management app"""
	roles = [
		{
			"role_name": "Property Manager",
			"desk_access": 1,
			"is_custom": 1
		},
		{
			"role_name": "Tenant",
			"desk_access": 1,
			"is_custom": 1
		},
		{
			"role_name": "Property Owner",
			"desk_access": 1,
			"is_custom": 1
		},
		{
			"role_name": "Maintenance Staff",
			"desk_access": 1,
			"is_custom": 1
		}
	]
	
	for role_data in roles:
		if not frappe.db.exists("Role", role_data["role_name"]):
			role = frappe.get_doc({
				"doctype": "Role",
				**role_data
			})
			role.insert(ignore_permissions=True)
			frappe.logger().info(f"Created role: {role_data['role_name']}")


def create_default_role_profiles():
	"""Create default role profiles"""
	role_profiles = {
		"Property Management Admin": [
			"Property Manager",
			"System Manager"
		],
		"Property Manager Profile": [
			"Property Manager",
			"Employee"
		],
		"Tenant Profile": [
			"Tenant"
		],
		"Property Owner Profile": [
			"Property Owner"
		],
		"Maintenance Staff Profile": [
			"Maintenance Staff",
			"Employee"
		]
	}
	
	for role_profile_name, roles in role_profiles.items():
		if frappe.db.exists("Role Profile", role_profile_name):
			continue
		
		role_profile = frappe.new_doc("Role Profile")
		role_profile.role_profile = role_profile_name
		for role in roles:
			role_profile.append("roles", {"role": role})
		
		role_profile.insert(ignore_permissions=True)
		frappe.logger().info(f"Created role profile: {role_profile_name}")


def configure_doctype_permissions():
	"""Configure permissions for all Property Management DocTypes"""
	
	# Property Project - Property Managers and Owners can manage
	set_doctype_permissions("Property Project", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
		{"role": "Property Owner", "read": 1, "write": 1, "create": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Building - Property Managers can manage
	set_doctype_permissions("Building", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Property Owner", "read": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Floor - Property Managers can manage
	set_doctype_permissions("Floor", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Property Owner", "read": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Unit - Property Managers can manage, Tenants can view their units
	set_doctype_permissions("Unit", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Property Owner", "read": 1, "write": 1},
		{"role": "Tenant", "read": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Tenant Profile - Property Managers can manage, Tenants can view/edit their own
	set_doctype_permissions("Tenant Profile", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Tenant", "read": 1, "write": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Tenancy - Property Managers can manage, Tenants can view their tenancy
	set_doctype_permissions("Tenancy", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
		{"role": "Property Owner", "read": 1},
		{"role": "Tenant", "read": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Utility Meter - Property Managers can manage
	set_doctype_permissions("Utility Meter", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Maintenance Staff", "read": 1, "write": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Meter Reading - Property Managers and Maintenance Staff can manage
	set_doctype_permissions("Meter Reading", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1},
		{"role": "Maintenance Staff", "read": 1, "write": 1, "create": 1, "submit": 1},
		{"role": "Tenant", "read": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Service Request - All roles can create, Property Managers can manage
	set_doctype_permissions("Service Request", [
		{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
		{"role": "Tenant", "read": 1, "write": 1, "create": 1},
		{"role": "Maintenance Staff", "read": 1, "write": 1},
		{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
	])
	
	# Child Tables
	child_tables = [
		"Building Amenity", "Unit Amenity", "Tenant Reference", 
		"Rent History", "Service Request Attachment"
	]
	
	for child_table in child_tables:
		set_doctype_permissions(child_table, [
			{"role": "Property Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
			{"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
		])


def set_doctype_permissions(doctype, permissions):
	"""Helper function to set permissions for a DocType"""
	try:
		# Clear existing custom permissions
		frappe.db.delete("Custom DocPerm", {"parent": doctype})
		
		# Add new permissions
		for perm in permissions:
			if not frappe.db.exists("Custom DocPerm", {"parent": doctype, "role": perm["role"]}):
				doc_perm = frappe.get_doc({
					"doctype": "Custom DocPerm",
					"parent": doctype,
					"parenttype": "DocType",
					"parentfield": "permissions",
					"role": perm["role"],
					"read": perm.get("read", 0),
					"write": perm.get("write", 0),
					"create": perm.get("create", 0),
					"delete": perm.get("delete", 0),
					"submit": perm.get("submit", 0),
					"cancel": perm.get("cancel", 0),
					"amend": perm.get("amend", 0),
					"report": perm.get("report", 1) if perm.get("read", 0) else 0,
					"export": perm.get("export", 1) if perm.get("read", 0) else 0,
					"print": perm.get("print", 1) if perm.get("read", 0) else 0,
					"email": perm.get("email", 1) if perm.get("read", 0) else 0,
					"share": perm.get("share", 1) if perm.get("write", 0) else 0
				})
				doc_perm.insert(ignore_permissions=True)
		
		frappe.logger().info(f"Configured permissions for {doctype}")
	except Exception as e:
		frappe.logger().error(f"Error configuring permissions for {doctype}: {str(e)}")


def setup_erpnext_custom_fields():
	"""Setup custom fields in ERPNext DocTypes for property management integration"""
	try:
		from property_management.property_management.setup.custom_fields import setup_property_management_custom_fields
		
		print("\n🔧 Setting up Property Management custom fields in ERPNext DocTypes...")
		result = setup_property_management_custom_fields()
		
		if result.get("success"):
			print(f"✅ Property Management custom fields created successfully ({result.get('fields_created', 0)} fields)")
		else:
			print("⚠️  Custom fields setup completed with warnings")
			
	except Exception as e:
		frappe.log_error(
			message=f"Failed to create Property Management custom fields: {str(e)}",
			title="Property Management Custom Fields Setup Failed"
		)
		print(f"⚠️  Warning: Failed to create custom fields: {str(e)}")
		print("   You can create them manually later using:")
		print("   bench --site <sitename> console")
		print("   >>> from property_management.property_management.setup.custom_fields import setup_property_management_custom_fields")
		print("   >>> setup_property_management_custom_fields()")


def import_dashboard_fixtures():
	"""Import dashboard fixtures following ERPNext patterns"""
	try:
		dashboard_name = "Property Management"
		
		if not frappe.db.exists("Dashboard", dashboard_name):
			# Verify required cards exist
			required_cards = ["Total Properties", "Active Tenancies", "Available Units", "Monthly Rental Income", "Open Service Requests"]
			cards_exist = all(frappe.db.exists("Number Card", card) for card in required_cards)
			
			if cards_exist:
				# Create dashboard following successful console approach
				dashboard_doc = frappe.get_doc({
					"doctype": "Dashboard",
					"dashboard_name": dashboard_name,
					"module": "Property Management",
					"is_default": 1,
					"is_standard": 1
				})
				
				# Add property-specific charts
				property_charts = ["Property Portfolio Overview", "Rental Income Trends"]
				for chart_name in property_charts:
					if frappe.db.exists("Dashboard Chart", chart_name):
						dashboard_doc.append('charts', {'chart': chart_name, 'width': 'Half'})
					else:
						print(f"⚠️  Dashboard Chart '{chart_name}' not found, skipping")
				
				# Add number cards
				for card_name in required_cards:
					if frappe.db.exists("Number Card", card_name):
						dashboard_doc.append('cards', {'card': card_name})
				
				dashboard_doc.insert(ignore_permissions=True)
				frappe.logger().info(f"Created dashboard: {dashboard_name}")
				print(f"✅ Created dashboard: {dashboard_name}")
			else:
				missing_cards = [card for card in required_cards if not frappe.db.exists("Number Card", card)]
				frappe.logger().warning(f"Cannot create dashboard - missing cards: {missing_cards}")
				print(f"⚠️  Cannot create dashboard - missing cards: {missing_cards}")
		else:
			frappe.logger().info(f"Dashboard {dashboard_name} already exists")
			print(f"ℹ️  Dashboard {dashboard_name} already exists")
			
	except Exception as e:
		frappe.logger().error(f"Error creating dashboard: {str(e)}")
		print(f"❌ Error creating dashboard: {str(e)}")
