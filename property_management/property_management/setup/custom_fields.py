"""
Custom Fields for Property Management Integration with ERPNext
Creates fields for linking property management entities with ERPNext DocTypes
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_property_management_custom_fields():
    """
    Add custom fields to ERPNext DocTypes for property management integration
    """
    
    custom_fields = {
        "Sales Invoice": [
            {
                "fieldname": "property_management_section",
                "label": "Property Management",
                "fieldtype": "Section Break",
                "insert_after": "is_internal_customer",
                "collapsible": 1,
                "collapsible_depends_on": "eval:doc.tenancy || doc.unit || doc.property_project"
            },
            {
                "fieldname": "tenancy",
                "label": "Tenancy",
                "fieldtype": "Link",
                "options": "Tenancy",
                "insert_after": "property_management_section",
                "description": "Link to tenancy agreement for rent invoices"
            },
            {
                "fieldname": "unit",
                "label": "Unit",
                "fieldtype": "Link",
                "options": "Unit",
                "insert_after": "tenancy",
                "description": "Property unit for this invoice"
            },
            {
                "fieldname": "column_break_property",
                "fieldtype": "Column Break",
                "insert_after": "unit"
            },
            {
                "fieldname": "property_project",
                "label": "Property Project",
                "fieldtype": "Link",
                "options": "Property Project",
                "insert_after": "column_break_property",
                "description": "Property project for this invoice"
            },
            {
                "fieldname": "service_request",
                "label": "Service Request",
                "fieldtype": "Link",
                "options": "Service Request",
                "insert_after": "property_project",
                "description": "Service request if this is a maintenance invoice"
            }
        ],
        
        "Purchase Invoice": [
            {
                "fieldname": "property_management_section",
                "label": "Property Management",
                "fieldtype": "Section Break",
                "insert_after": "represents_company",
                "collapsible": 1,
                "collapsible_depends_on": "eval:doc.service_request || doc.unit || doc.property_project"
            },
            {
                "fieldname": "service_request",
                "label": "Service Request",
                "fieldtype": "Link",
                "options": "Service Request",
                "insert_after": "property_management_section",
                "description": "Service request for maintenance expenses"
            },
            {
                "fieldname": "unit",
                "label": "Unit",
                "fieldtype": "Link",
                "options": "Unit",
                "insert_after": "service_request",
                "description": "Property unit for this expense"
            },
            {
                "fieldname": "column_break_property_pi",
                "fieldtype": "Column Break",
                "insert_after": "unit"
            },
            {
                "fieldname": "property_project",
                "label": "Property Project",
                "fieldtype": "Link",
                "options": "Property Project",
                "insert_after": "column_break_property_pi",
                "description": "Property project for this expense"
            }
        ],
        
        "Customer": [
            {
                "fieldname": "property_management_section",
                "label": "Property Management",
                "fieldtype": "Section Break",
                "insert_after": "represents_company",
                "collapsible": 1,
                "collapsible_depends_on": "eval:doc.tenant_profile"
            },
            {
                "fieldname": "tenant_profile",
                "label": "Tenant Profile",
                "fieldtype": "Link",
                "options": "Tenant Profile",
                "insert_after": "property_management_section",
                "description": "Link to tenant profile if customer is a tenant"
            },
            {
                "fieldname": "is_tenant",
                "label": "Is Tenant",
                "fieldtype": "Check",
                "insert_after": "tenant_profile",
                "default": 0,
                "description": "Check if this customer is a property tenant"
            }
        ],
        
        "Supplier": [
            {
                "fieldname": "property_management_section",
                "label": "Property Management",
                "fieldtype": "Section Break",
                "insert_after": "represents_company",
                "collapsible": 1,
                "collapsible_depends_on": "eval:doc.is_maintenance_supplier"
            },
            {
                "fieldname": "is_maintenance_supplier",
                "label": "Is Maintenance Supplier",
                "fieldtype": "Check",
                "insert_after": "property_management_section",
                "default": 0,
                "description": "Check if this supplier provides maintenance services"
            },
            {
                "fieldname": "service_categories",
                "label": "Service Categories",
                "fieldtype": "Small Text",
                "insert_after": "is_maintenance_supplier",
                "description": "Types of maintenance services provided"
            }
        ],
        
        "Item": [
            {
                "fieldname": "property_management_section",
                "label": "Property Management",
                "fieldtype": "Section Break",
                "insert_after": "is_purchase_item",
                "collapsible": 1,
                "collapsible_depends_on": "eval:doc.is_property_item"
            },
            {
                "fieldname": "is_property_item",
                "label": "Is Property Item",
                "fieldtype": "Check",
                "insert_after": "property_management_section",
                "default": 0,
                "description": "Check if this item is used for property management"
            },
            {
                "fieldname": "property_item_type",
                "label": "Property Item Type",
                "fieldtype": "Select",
                "options": "\nRent\nMaintenance\nUtility\nSecurity Deposit\nOther",
                "insert_after": "is_property_item",
                "depends_on": "eval:doc.is_property_item",
                "description": "Type of property-related item"
            }
        ],
        
        "Asset": [
            {
                "fieldname": "property_management_section",
                "label": "Property Management",
                "fieldtype": "Section Break",
                "insert_after": "purchase_receipt",
                "collapsible": 1,
                "collapsible_depends_on": "eval:doc.unit || doc.property_project"
            },
            {
                "fieldname": "unit",
                "label": "Unit",
                "fieldtype": "Link",
                "options": "Unit",
                "insert_after": "property_management_section",
                "description": "Property unit where this asset is located"
            },
            {
                "fieldname": "property_project",
                "label": "Property Project",
                "fieldtype": "Link",
                "options": "Property Project",
                "insert_after": "unit",
                "description": "Property project for this asset"
            },
            {
                "fieldname": "column_break_property_asset",
                "fieldtype": "Column Break",
                "insert_after": "property_project"
            },
            {
                "fieldname": "utility_meter",
                "label": "Utility Meter",
                "fieldtype": "Link",
                "options": "Utility Meter",
                "insert_after": "column_break_property_asset",
                "description": "Link to utility meter if this asset is a meter"
            }
        ]
    }
    
    try:
        create_custom_fields(custom_fields, update=True)
        frappe.db.commit()
        
        print("✅ Property Management custom fields created successfully")
        return {
            "success": True,
            "message": "Custom fields created successfully",
            "fields_created": sum(len(fields) for fields in custom_fields.values())
        }
        
    except Exception as e:
        frappe.log_error(
            message=f"Failed to create property management custom fields: {str(e)}",
            title="Property Management Custom Fields Setup Failed"
        )
        print(f"❌ Failed to create custom fields: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }

def remove_property_management_custom_fields():
    """
    Remove property management custom fields (for cleanup/uninstall)
    """
    try:
        # List of custom fields to remove
        fields_to_remove = [
            # Sales Invoice fields
            ("Sales Invoice", "property_management_section"),
            ("Sales Invoice", "tenancy"),
            ("Sales Invoice", "unit"),
            ("Sales Invoice", "column_break_property"),
            ("Sales Invoice", "property_project"),
            ("Sales Invoice", "service_request"),
            
            # Purchase Invoice fields
            ("Purchase Invoice", "property_management_section"),
            ("Purchase Invoice", "service_request"),
            ("Purchase Invoice", "unit"),
            ("Purchase Invoice", "column_break_property_pi"),
            ("Purchase Invoice", "property_project"),
            
            # Customer fields
            ("Customer", "property_management_section"),
            ("Customer", "tenant_profile"),
            ("Customer", "is_tenant"),
            
            # Supplier fields
            ("Supplier", "property_management_section"),
            ("Supplier", "is_maintenance_supplier"),
            ("Supplier", "service_categories"),
            
            # Item fields
            ("Item", "property_management_section"),
            ("Item", "is_property_item"),
            ("Item", "property_item_type"),
            
            # Asset fields
            ("Asset", "property_management_section"),
            ("Asset", "unit"),
            ("Asset", "property_project"),
            ("Asset", "column_break_property_asset"),
            ("Asset", "utility_meter")
        ]
        
        for doctype, fieldname in fields_to_remove:
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": fieldname}):
                frappe.delete_doc("Custom Field", {"dt": doctype, "fieldname": fieldname})
        
        frappe.db.commit()
        print("✅ Property Management custom fields removed successfully")
        
    except Exception as e:
        frappe.log_error(
            message=f"Failed to remove property management custom fields: {str(e)}",
            title="Property Management Custom Fields Removal Failed"
        )
        print(f"❌ Failed to remove custom fields: {str(e)}")

if __name__ == "__main__":
    setup_property_management_custom_fields()
