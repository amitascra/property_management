import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_featured_properties():
	"""Get featured properties for homepage"""
	try:
		properties = frappe.get_all(
			"Property Project",
			filters={
				"is_featured": 1,
				"is_available": 1
			},
			fields=[
				"name",
				"project_name as title",
				"location",
				"price",
				"project_type as property_type",
				"bedrooms",
				"bathrooms",
				"total_area as area",
				"status",
				"featured_image as image",
				"description"
			],
			limit=6,
			order_by="modified desc"
		)
		
		return properties
	except Exception as e:
		frappe.log_error(f"Error fetching featured properties: {str(e)}")
		return []

@frappe.whitelist(allow_guest=True)
def get_properties(filters=None, sort_by="newest"):
	"""Get properties with filters"""
	try:
		if isinstance(filters, str):
			import json
			filters = json.loads(filters)
		
		query_filters = {"is_available": 1}
		
		# Apply filters
		if filters:
			if filters.get("property_type"):
				query_filters["project_type"] = filters["property_type"]
			
			if filters.get("bedrooms"):
				query_filters["bedrooms"] = filters["bedrooms"]
			
			if filters.get("location"):
				query_filters["location"] = ["like", f"%{filters['location']}%"]
			
			# Price range filter
			if filters.get("price_min") or filters.get("price_max"):
				if filters.get("price_min"):
					query_filters["price"] = [">=", float(filters["price_min"])]
				if filters.get("price_max"):
					if "price" in query_filters:
						query_filters["price"] = ["between", [float(filters["price_min"]), float(filters["price_max"])]]
					else:
						query_filters["price"] = ["<=", float(filters["price_max"])]
		
		# Determine sort order
		order_by = "modified desc"
		if sort_by == "price_low":
			order_by = "price asc"
		elif sort_by == "price_high":
			order_by = "price desc"
		
		properties = frappe.get_all(
			"Property Project",
			filters=query_filters,
			fields=[
				"name",
				"project_name as title",
				"location",
				"price",
				"project_type as property_type",
				"bedrooms",
				"bathrooms",
				"total_area as area",
				"status",
				"featured_image as image",
				"description"
			],
			order_by=order_by,
			limit=50
		)
		
		return properties
	except Exception as e:
		frappe.log_error(f"Error fetching properties: {str(e)}")
		return []

@frappe.whitelist(allow_guest=True)
def get_property_details(property_id):
	"""Get detailed information about a specific property"""
	try:
		property_doc = frappe.get_doc("Property Project", property_id)
		
		# Get property images
		images = []
		if hasattr(property_doc, 'property_images') and property_doc.property_images:
			for img in property_doc.property_images:
				images.append({
					"image": img.image,
					"title": img.image_title if hasattr(img, 'image_title') else "",
					"description": img.description if hasattr(img, 'description') else "",
					"is_primary": img.is_primary if hasattr(img, 'is_primary') else 0
				})
		
		# Get amenities
		amenities = []
		if hasattr(property_doc, 'amenities') and property_doc.amenities:
			for amenity in property_doc.amenities:
				amenities.append({
					"name": amenity.amenity_name,
					"icon": amenity.icon if hasattr(amenity, 'icon') else "check-circle",
					"description": amenity.description if hasattr(amenity, 'description') else ""
				})
		
		return {
			"name": property_doc.name,
			"title": property_doc.project_name,
			"location": property_doc.location or "",
			"price": property_doc.price or 0,
			"price_per_sqft": property_doc.price_per_sqft if hasattr(property_doc, 'price_per_sqft') else 0,
			"property_type": property_doc.project_type or "",
			"bedrooms": property_doc.bedrooms or 0,
			"bathrooms": property_doc.bathrooms or 0,
			"parking_spaces": property_doc.parking_spaces if hasattr(property_doc, 'parking_spaces') else 0,
			"area": property_doc.total_area or 0,
			"floor_number": property_doc.floor_number if hasattr(property_doc, 'floor_number') else "",
			"furnishing_status": property_doc.furnishing_status if hasattr(property_doc, 'furnishing_status') else "",
			"property_age": property_doc.property_age if hasattr(property_doc, 'property_age') else "",
			"status": property_doc.status,
			"description": property_doc.description or "",
			"featured_image": property_doc.featured_image if hasattr(property_doc, 'featured_image') else "",
			"images": images,
			"amenities": amenities,
			"contact_person": property_doc.contact_person if hasattr(property_doc, 'contact_person') else "",
			"contact_phone": property_doc.contact_phone if hasattr(property_doc, 'contact_phone') else "",
			"contact_email": property_doc.contact_email if hasattr(property_doc, 'contact_email') else ""
		}
	except frappe.DoesNotExistError:
		frappe.throw(_("Property not found"), frappe.DoesNotExistError)
	except Exception as e:
		frappe.log_error(f"Error fetching property details: {str(e)}")
		frappe.throw(_("Error fetching property details"))

@frappe.whitelist(allow_guest=True)
def submit_enquiry(name, email, phone, message="", property_id=None, property_name=None):
	"""Submit an enquiry form"""
	try:
		# Create a Lead document (or custom Enquiry doctype if exists)
		lead = frappe.get_doc({
			"doctype": "Lead",
			"lead_name": name,
			"email_id": email,
			"mobile_no": phone,
			"notes": message,
			"source": "Website",
			"status": "Lead"
		})
		
		# Add property reference in notes if provided
		if property_id and property_name:
			lead.notes = f"Property Interest: {property_name} ({property_id})\n\n{message}"
		
		lead.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": "Enquiry submitted successfully"
		}
	except Exception as e:
		frappe.log_error(f"Error submitting enquiry: {str(e)}")
		frappe.throw(_("Failed to submit enquiry. Please try again."))

@frappe.whitelist(allow_guest=True)
def submit_contact(name, email, phone, subject, message):
	"""Submit a contact form"""
	try:
		# Create a Communication or Lead document
		lead = frappe.get_doc({
			"doctype": "Lead",
			"lead_name": name,
			"email_id": email,
			"mobile_no": phone,
			"notes": f"Subject: {subject}\n\n{message}",
			"source": "Website Contact Form",
			"status": "Lead"
		})
		
		lead.insert(ignore_permissions=True)
		frappe.db.commit()
		
		return {
			"success": True,
			"message": "Contact form submitted successfully"
		}
	except Exception as e:
		frappe.log_error(f"Error submitting contact form: {str(e)}")
		frappe.throw(_("Failed to submit contact form. Please try again."))

@frappe.whitelist(allow_guest=True)
def get_website_settings():
	"""Get website settings for frontend"""
	try:
		if not frappe.db.exists("Property Website Settings", "Property Website Settings"):
			return {
				"site_name": "Property Management",
				"tagline": "Your Dream Property Awaits",
				"contact_phone": "+91 1234567890",
				"whatsapp_number": "911234567890",
				"hero_slides": [],
				"show_featured_properties": True,
				"featured_properties_limit": 6,
				"featured_section_title": "Featured Properties",
				"featured_section_description": "Explore our handpicked selection of premium properties available for sale and rent.",
				"show_about_section": True,
				"about_section_title": "About Us",
				"about_section_content": "",
				"why_choose_title": "Why Choose Us",
				"why_choose_features": [],
				"show_cta_section": True,
				"cta_section_title": "Ready to Find Your Dream Property?",
				"cta_section_description": "Get in touch with our expert team today and let us help you find the perfect property.",
				"about_hero_title": "About Us",
				"about_hero_description": "Your trusted partner in real estate for over a decade",
				"company_story_title": "Our Story",
				"mission_title": "Our Mission",
				"vision_title": "Our Vision",
				"strengths_title": "Why Choose Us",
				"stats": [],
				"strengths": []
			}
		
		settings = frappe.get_doc("Property Website Settings", "Property Website Settings")
		
		# Get active slides
		active_slides = []
		for slide in settings.hero_slides:
			if slide.is_active:
				active_slides.append({
					"title": slide.title,
					"subtitle": slide.subtitle,
					"description": slide.description,
					"image": slide.slide_image,
					"button_text": slide.button_text,
					"button_link": slide.button_link
				})
		
		# Get why choose features
		features = []
		for feature in settings.why_choose_features:
			features.append({
				"icon": feature.icon,
				"title": feature.title,
				"description": feature.description
			})
		
		# Get stats
		stats = []
		for stat in settings.stats:
			stats.append({
				"label": stat.label,
				"value": stat.value,
				"suffix": stat.suffix or ""
			})
		
		# Get strengths
		strengths = []
		for strength in settings.strengths:
			strengths.append({
				"icon": strength.icon,
				"title": strength.title,
				"description": strength.description
			})
		
		return {
			"site_logo": settings.site_logo,
			"site_name": settings.site_name,
			"tagline": settings.tagline,
			"contact_phone": settings.contact_phone,
			"contact_email": settings.contact_email,
			"whatsapp_number": settings.whatsapp_number,
			"hero_slides": active_slides,
			"show_featured_properties": settings.show_featured_properties,
			"featured_properties_limit": settings.featured_properties_limit,
			"featured_section_title": settings.featured_section_title,
			"featured_section_description": settings.featured_section_description,
			"show_about_section": settings.show_about_section,
			"about_section_title": settings.about_section_title,
			"about_section_content": settings.about_section_content,
			"about_section_image": settings.about_section_image,
			"why_choose_title": settings.why_choose_title,
			"why_choose_features": features,
			"show_cta_section": settings.show_cta_section,
			"cta_section_title": settings.cta_section_title,
			"cta_section_description": settings.cta_section_description,
			"about_hero_title": settings.about_hero_title,
			"about_hero_description": settings.about_hero_description,
			"company_story_title": settings.company_story_title,
			"company_story_content": settings.company_story_content,
			"company_story_image": settings.company_story_image,
			"mission_title": settings.mission_title,
			"mission_content": settings.mission_content,
			"vision_title": settings.vision_title,
			"vision_content": settings.vision_content,
			"strengths_title": settings.strengths_title,
			"stats": stats,
			"strengths": strengths
		}
	except Exception as e:
		frappe.log_error(f"Error fetching website settings: {str(e)}")
		return {}

@frappe.whitelist(allow_guest=True)
def signup(full_name, email, phone, password):
	"""Create a new user account with Customer and Tenant Profile"""
	# Check if user already exists
	if frappe.db.exists("User", email):
		frappe.throw(_("An account with this email already exists"))
	
	# Validate inputs
	if not full_name or not email or not phone or not password:
		frappe.throw(_("All fields are required"))
	
	if len(password) < 6:
		frappe.throw(_("Password must be at least 6 characters long"))
	
	try:
		# Use Administrator context to bypass all permission checks
		frappe.set_user("Administrator")
		
		# Create new user
		user = frappe.get_doc({
			"doctype": "User",
			"email": email,
			"first_name": full_name.split()[0] if full_name else email.split('@')[0],
			"last_name": " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else "",
			"mobile_no": phone,
			"enabled": 1,
			"new_password": password,
			"send_welcome_email": 0,
			"user_type": "Website User"
		})
		
		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True
		user.insert()
		
		# Assign Customer and Tenant roles
		if frappe.db.exists("Role", "Customer"):
			user.add_roles("Customer")
		if frappe.db.exists("Role", "Tenant"):
			user.add_roles("Tenant")
		
		# Create Customer record
		customer = frappe.get_doc({
			"doctype": "Customer",
			"customer_name": full_name,
			"customer_type": "Individual",
			"mobile_no": phone,
			"email_id": email,
			"customer_group": "Individual",
			"territory": "All Territories"
		})
		customer.insert()
		
		# Create Tenant Profile linked to Customer
		tenant_profile = frappe.get_doc({
			"doctype": "Tenant Profile",
			"tenant_name": full_name,
			"customer_link": customer.name,
			"contact_number": phone,
			"email": email,
			"status": "Active",
			"id_proof_type": "Aadhar Card",
			"id_proof_number": "XXXX-XXXX-XXXX"  # Placeholder - user can update later
		})
		tenant_profile.insert()
		
		frappe.db.commit()
		
		return {
			"success": True,
			"message": "Account created successfully",
			"customer_id": customer.name,
			"tenant_profile_id": tenant_profile.name
		}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Error creating user account: {str(e)}")
		frappe.throw(_("Failed to create account. Please try again."))
	finally:
		# Reset to guest user
		frappe.set_user("Guest")

@frappe.whitelist()
def get_tenant_dashboard():
	"""Get tenant dashboard data for logged-in user"""
	try:
		user = frappe.session.user
		
		# Get tenant profile directly by email
		tenant_profile = frappe.db.get_value("Tenant Profile", {"email": user}, "name")
		if not tenant_profile:
			return {"error": "No tenant profile found"}
		
		# Get tenant profile details
		tenant = frappe.get_doc("Tenant Profile", tenant_profile)
		
		# Get active tenancy
		active_tenancy = frappe.db.get_value(
			"Tenancy",
			{"tenant": tenant_profile, "status": "Active"},
			["name", "unit", "monthly_rent", "security_deposit", "maintenance_charges", 
			 "lease_start_date", "lease_end_date", "rent_due_date", "agreement_type"],
			as_dict=True
		)
		
		# Get unit details if tenancy exists
		unit_details = None
		if active_tenancy:
			unit_doc = frappe.get_doc("Unit", active_tenancy.unit)
			unit_details = {
				"name": unit_doc.name,
				"unit_number": unit_doc.unit_number,
				"unit_type": unit_doc.unit_type,
				"carpet_area": unit_doc.carpet_area,
				"built_up_area": unit_doc.built_up_area,
				"facing": unit_doc.facing if hasattr(unit_doc, 'facing') else "",
				"building": unit_doc.building,
				"floor": unit_doc.floor,
				"description": unit_doc.description if hasattr(unit_doc, 'description') else ""
			}
		
		# Get service requests
		service_requests = frappe.get_all(
			"Service Request",
			filters={"tenant": tenant_profile},
			fields=["name", "unit", "request_type", "category", "priority", "status", 
			        "requested_date", "description", "resolution_date"],
			order_by="requested_date desc",
			limit=10
		)
		
		# Get rent history if tenancy exists
		rent_history = []
		if active_tenancy:
			rent_history = frappe.get_all(
				"Rent History",
				filters={"parent": active_tenancy.name},
				fields=["payment_date", "amount", "status", "payment_mode", "month_year", "due_date"],
				order_by="payment_date desc",
				limit=6
			)
		
		# Get invoices for the tenancy
		invoices = []
		if active_tenancy:
			invoices = frappe.get_all(
				"Sales Invoice",
				filters={"tenancy": active_tenancy.name},
				fields=["name", "posting_date", "due_date", "grand_total", "outstanding_amount", 
				        "status", "docstatus", "customer"],
				order_by="posting_date desc"
			)
			
			# Get payment details for each invoice
			for invoice in invoices:
				# Get payment entries linked to this invoice
				payment_refs = frappe.db.sql("""
					SELECT 
						pe.name, pe.posting_date, pe.paid_amount, 
						pe.mode_of_payment, pe.reference_no, per.allocated_amount
					FROM `tabPayment Entry` pe
					INNER JOIN `tabPayment Entry Reference` per ON per.parent = pe.name
					WHERE per.reference_name = %s 
					AND per.reference_doctype = 'Sales Invoice'
					AND pe.docstatus = 1
					ORDER BY pe.posting_date DESC
				""", (invoice['name'],), as_dict=True)
				
				invoice['payments'] = payment_refs
		
		return {
			"tenant_profile": {
				"name": tenant.name,
				"tenant_name": tenant.tenant_name,
				"email": tenant.email,
				"contact_number": tenant.contact_number,
				"status": tenant.status
			},
			"active_tenancy": active_tenancy,
			"unit_details": unit_details,
			"service_requests": service_requests,
			"rent_history": rent_history,
			"invoices": invoices
		}
	except Exception as e:
		frappe.log_error(f"Error fetching tenant dashboard: {str(e)}")
		return {"error": str(e)}

@frappe.whitelist()
def create_service_request(unit, request_type, category, priority, description):
	"""Create a new service request"""
	try:
		user = frappe.session.user
		
		# Get tenant profile
		customer = frappe.db.get_value("Customer", {"email_id": user}, "name")
		tenant_profile = frappe.db.get_value("Tenant Profile", {"customer_link": customer}, "name")
		
		if not tenant_profile:
			frappe.throw(_("Tenant profile not found"))
		
		# Get active tenancy for this unit
		tenancy = frappe.db.get_value(
			"Tenancy",
			{"tenant": tenant_profile, "unit": unit, "status": "Active"},
			"name"
		)
		
		# Get company from unit
		company = frappe.db.get_value("Unit", unit, "cost_center")
		if not company:
			company = frappe.get_single_value("Global Defaults", "default_company")
		
		# Create service request
		service_request = frappe.get_doc({
			"doctype": "Service Request",
			"unit": unit,
			"tenant": tenant_profile,
			"tenancy": tenancy,
			"request_type": request_type,
			"category": category,
			"priority": priority,
			"description": description,
			"status": "Open",
			"company": company or "Property Management Company"
		})
		service_request.insert()
		frappe.db.commit()
		
		return {
			"success": True,
			"message": "Service request created successfully",
			"request_id": service_request.name
		}
	except Exception as e:
		frappe.log_error(f"Error creating service request: {str(e)}")
		frappe.throw(_("Failed to create service request"))
