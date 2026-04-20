# Property Management Frontend - Production Deployment Guide

## ✅ Configuration Complete - Matches Shaadi Exactly

The frontend is now configured exactly like Shaadi and ready for production deployment.

---

## 🔧 Key Configuration Changes Made

### 1. **Hooks Configuration** (`property_management/hooks.py`)
```python
# Routes root path to frontend (like Shaadi)
home_page = "frontend"

role_home_page = {
    "Property Manager": "frontend",
    "Property Owner": "frontend",
    "Tenant": "frontend",
    "System Manager": "frontend",
    "Guest": "frontend",
    "Website User": "frontend",
}

# Routes ALL paths to frontend
website_route_rules = [
    {"from_route": "/", "to_route": "frontend"},
    {"from_route": "/home", "to_route": "frontend"},
    {"from_route": "/account/login", "to_route": "frontend"},
    {"from_route": "/account/signup", "to_route": "frontend"},
    {"from_route": "/property", "to_route": "frontend"},
    {"from_route": "/properties", "to_route": "frontend"},
]
```

### 2. **Build Output Structure**
```
property_management/
├── public/
│   └── frontend/
│       ├── index.html
│       ├── favicon.png
│       └── assets/
│           ├── index-*.js
│           ├── frappe-ui-*.js
│           └── *.css
└── www/
    ├── frontend.html (Jinja template)
    └── frontend.py (Context provider)
```

### 3. **Asset Paths**
- **Base Path**: `/assets/property_management/`
- **Frontend Assets**: `/assets/property_management/frontend/assets/`
- **Favicon**: `/assets/property_management/frontend/favicon.png`

---

## 🚀 Deployment Steps for Production

### **Step 1: Build the Frontend**
```bash
cd apps/property_management/property_ui
yarn build
```

**Expected Output:**
```
✓ 2000 modules transformed
✓ built in ~6s
✓ Successfully cleaned up frontend.html
```

### **Step 2: Restart Frappe**
```bash
# From bench directory
bench restart
```

### **Step 3: Clear Cache**
```bash
bench --site real-estate.amitkumar.live clear-cache
```

### **Step 4: Migrate (if needed)**
```bash
bench --site real-estate.amitkumar.live migrate
```

### **Step 5: Verify Assets**
Check that assets are accessible:
```bash
curl -I https://real-estate.amitkumar.live/assets/property_management/frontend/favicon.png
```

Should return `200 OK`

---

## 🌐 Access URLs

After deployment, the frontend will be accessible at:

- **Root**: `https://real-estate.amitkumar.live/`
- **Frontend**: `https://real-estate.amitkumar.live/frontend`
- **Home**: `https://real-estate.amitkumar.live/home`
- **Login**: `https://real-estate.amitkumar.live/account/login`

All these routes will serve the same Vue.js frontend application.

---

## 🔍 Troubleshooting

### **Issue: Frontend not loading**

**Check 1: Verify hooks are loaded**
```bash
bench --site real-estate.amitkumar.live console
```
```python
import frappe
print(frappe.get_hooks("home_page"))
print(frappe.get_hooks("website_route_rules"))
```

**Check 2: Verify assets exist**
```bash
ls -la apps/property_management/property_management/public/frontend/
```

**Check 3: Check nginx/apache logs**
```bash
# For nginx
tail -f /var/log/nginx/error.log

# For apache
tail -f /var/log/apache2/error.log
```

**Check 4: Verify www/frontend.html exists**
```bash
ls -la apps/property_management/property_management/www/frontend.html
```

### **Issue: 404 on assets**

**Solution**: Rebuild and restart
```bash
cd apps/property_management/property_ui
yarn build
cd ../../..
bench restart
bench --site real-estate.amitkumar.live clear-cache
```

### **Issue: White screen / JavaScript errors**

**Check browser console** for errors. Common issues:
- CORS errors → Check nginx/apache configuration
- 404 on JS files → Rebuild frontend
- CSRF token errors → Clear browser cookies

---

## 📋 Configuration Comparison: Shaadi vs Property Management

| Aspect | Shaadi | Property Management | Status |
|--------|--------|---------------------|--------|
| **Home Page** | `shaadi` | `frontend` | ✅ Configured |
| **Root Route** | `/` → `shaadi` | `/` → `frontend` | ✅ Configured |
| **Asset Path** | `/assets/shaadi/` | `/assets/property_management/` | ✅ Correct |
| **Build Output** | `shaadi/public/` | `property_management/public/frontend/` | ✅ Working |
| **WWW Template** | `shaadi/www/shaadi.html` | `property_management/www/frontend.html` | ✅ Created |
| **Context Provider** | `shaadi/www/shaadi.py` | `property_management/www/frontend.py` | ✅ Created |
| **Vite Config** | Matches | Matches | ✅ Identical |
| **Package Scripts** | Matches | Matches | ✅ Identical |

---

## 🎯 Production Checklist

- [x] Frontend built successfully
- [x] Assets in `property_management/public/frontend/`
- [x] `www/frontend.html` template created
- [x] `www/frontend.py` context provider created
- [x] `hooks.py` configured with routes
- [x] Vite config matches Shaadi
- [x] Package.json build script correct
- [ ] **Deploy to production server**
- [ ] **Restart bench on production**
- [ ] **Clear cache on production**
- [ ] **Test access at https://real-estate.amitkumar.live/**

---

## 🔐 Security Notes

1. **CSRF Protection**: Enabled via `{{ csrf_token }}` in template
2. **Session Management**: Handled by Frappe's session system
3. **Authentication**: Vue router guards check `session.isLoggedIn`
4. **API Calls**: All use Frappe's whitelisted methods

---

## 📝 Maintenance

### **Rebuild After Code Changes**
```bash
cd apps/property_management/property_ui
yarn build
cd ../../..
bench restart
```

### **Update Dependencies**
```bash
cd apps/property_management/property_ui
yarn upgrade
```

### **Development Mode**
```bash
cd apps/property_management/property_ui
yarn dev
# Access at http://real-estate.amitkumar.live:8080/frontend
```

---

## 🎨 Customization

The frontend uses:
- **Vue 3** for reactive UI
- **Vue Router** for routing
- **Frappe UI** for components
- **TailwindCSS** for styling
- **Blue/Green** color scheme (vs Shaadi's Pink/Purple)

To customize:
- **Colors**: Edit `property_ui/tailwind.config.js`
- **Styles**: Edit `property_ui/src/index.css`
- **Routes**: Edit `property_ui/src/router.js`
- **Pages**: Add to `property_ui/src/pages/`

---

## ✅ Status: Production Ready

The Property Management frontend is now configured **exactly like Shaadi** and ready for production deployment on `https://real-estate.amitkumar.live/`.

**Next Action**: Deploy to production server and restart bench.
