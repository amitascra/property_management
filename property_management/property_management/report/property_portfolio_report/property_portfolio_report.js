// Copyright (c) 2026, Amit Kumar and contributors
// For license information, please see license.txt

frappe.query_reports["Property Portfolio Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nPlanning\nUnder Construction\nCompleted\nOn Hold\nCancelled"
		},
		{
			"fieldname": "project_type",
			"label": __("Project Type"),
			"fieldtype": "Select",
			"options": "\nResidential\nCommercial\nMixed Use\nIndustrial"
		},
		{
			"fieldname": "location",
			"label": __("Location"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "project_manager",
			"label": __("Project Manager"),
			"fieldtype": "Link",
			"options": "Employee"
		}
	],
	
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		if (column.fieldname == "status") {
			if (value == "Completed") {
				value = `<span style="color: green;">${value}</span>`;
			} else if (value == "Under Construction") {
				value = `<span style="color: orange;">${value}</span>`;
			} else if (value == "On Hold" || value == "Cancelled") {
				value = `<span style="color: red;">${value}</span>`;
			} else if (value == "Planning") {
				value = `<span style="color: blue;">${value}</span>`;
			}
		}
		
		if (column.fieldname == "occupancy_rate") {
			let rate = parseFloat(value) || 0;
			if (rate >= 90) {
				value = `<span style="color: green; font-weight: bold;">${value}%</span>`;
			} else if (rate >= 70) {
				value = `<span style="color: orange; font-weight: bold;">${value}%</span>`;
			} else if (rate > 0) {
				value = `<span style="color: red; font-weight: bold;">${value}%</span>`;
			} else {
				value = `<span style="color: gray;">${value}%</span>`;
			}
		}
		
		return value;
	}
};
