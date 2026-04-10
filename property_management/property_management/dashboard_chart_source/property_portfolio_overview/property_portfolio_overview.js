frappe.query_reports["Property Portfolio Overview"] = {
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
		
		return value;
	}
};
