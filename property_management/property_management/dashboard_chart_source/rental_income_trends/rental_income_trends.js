frappe.query_reports["Rental Income Trends"] = {
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
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.nowdate(), -12)
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.nowdate()
		},
		{
			"fieldname": "property_project",
			"label": __("Property Project"),
			"fieldtype": "Link",
			"options": "Property Project"
		}
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		if (column.fieldname == "monthly_income") {
			// Format as currency
			if (value && !isNaN(value)) {
				value = frappe.format(value, {fieldtype: "Currency"});
			}
		}
		
		if (column.fieldname == "occupancy_rate") {
			// Color code occupancy rates
			let rate = parseFloat(value) || 0;
			if (rate >= 90) {
				value = `<span style="color: green; font-weight: bold;">${value}%</span>`;
			} else if (rate >= 70) {
				value = `<span style="color: orange; font-weight: bold;">${value}%</span>`;
			} else if (rate > 0) {
				value = `<span style="color: red; font-weight: bold;">${value}%</span>`;
			}
		}
		
		return value;
	}
};
