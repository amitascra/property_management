# Copyright (c) 2026, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, cint, getdate, today


def execute(filters=None):
	"""Main report execution function"""
	columns = get_columns()
	data = get_data(filters)
	
	return columns, data


def get_columns():
	"""Define report columns"""
	return [
		{
			"fieldname": "project_name",
			"label": _("Project Name"),
			"fieldtype": "Link",
			"options": "Property Project",
			"width": 200
		},
		{
			"fieldname": "project_code",
			"label": _("Project Code"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "project_type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "location",
			"label": _("Location"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "total_buildings",
			"label": _("Buildings"),
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "total_units",
			"label": _("Total Units"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "available_units",
			"label": _("Available"),
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "rented_units",
			"label": _("Rented"),
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "sold_units",
			"label": _("Sold"),
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "occupancy_rate",
			"label": _("Occupancy %"),
			"fieldtype": "Percent",
			"width": 100
		},
		{
			"fieldname": "total_investment",
			"label": _("Investment"),
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "expected_completion_date",
			"label": _("Expected Completion"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "project_manager",
			"label": _("Project Manager"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 150
		}
	]


def get_data(filters):
	"""Get report data"""
	conditions = get_conditions(filters)
	
	# Get property projects data
	projects_data = frappe.db.sql(f"""
		SELECT 
			pp.name,
			pp.project_name,
			pp.project_code,
			pp.status,
			pp.project_type,
			pp.location,
			pp.total_buildings,
			pp.total_units,
			pp.available_units,
			pp.rented_units,
			pp.sold_units,
			pp.total_investment,
			pp.expected_completion_date,
			pp.project_manager,
			pp.company
		FROM `tabProperty Project` pp
		WHERE pp.docstatus < 2 {conditions}
		ORDER BY pp.project_name
	""", as_dict=True)
	
	# Calculate occupancy rates and format data
	for project in projects_data:
		total_units = cint(project.get('total_units', 0))
		available_units = cint(project.get('available_units', 0))
		
		if total_units > 0:
			occupied_units = total_units - available_units
			project['occupancy_rate'] = flt((occupied_units / total_units) * 100, 2)
		else:
			project['occupancy_rate'] = 0
		
		# Format currency
		project['total_investment'] = flt(project.get('total_investment', 0))
	
	return projects_data


def get_conditions(filters):
	"""Build SQL conditions based on filters"""
	conditions = ""
	
	if filters.get("company"):
		conditions += f" AND pp.company = '{filters.get('company')}'"
	
	if filters.get("status"):
		conditions += f" AND pp.status = '{filters.get('status')}'"
	
	if filters.get("project_type"):
		conditions += f" AND pp.project_type = '{filters.get('project_type')}'"
	
	if filters.get("location"):
		conditions += f" AND pp.location LIKE '%{filters.get('location')}%'"
	
	if filters.get("project_manager"):
		conditions += f" AND pp.project_manager = '{filters.get('project_manager')}'"
	
	return conditions
