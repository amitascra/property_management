# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def after_install():
	"""Run after app installation"""
	create_custom_roles()
	create_default_role_profiles()
	configure_doctype_permissions()
	frappe.db.commit()


def after_migrate():
	"""Run after migration - when DocTypes are fully synced"""
	import_workspace_fixtures()
	frappe.db.commit()


def import_workspace_fixtures():
	"""Import workspace fixtures"""
	try:
		# Import workspace from fixtures
		from frappe.core.doctype.data_import.data_import import import_doc
		import os
		
		workspace_path = os.path.join(
			frappe.get_app_path("property_management"),
			"property_management", 
			"workspace", 
			"property_management", 
			"property_management.json"
		)
		
		if os.path.exists(workspace_path):
			with open(workspace_path, 'r') as f:
				import json
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
		else:
			frappe.logger().error(f"Workspace file not found at: {workspace_path}")
			
	except Exception as e:
		frappe.logger().error(f"Error importing workspace: {str(e)}")


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
