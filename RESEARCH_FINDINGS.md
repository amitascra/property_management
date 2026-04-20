# Comprehensive Research: Shaadi vs HRMS vs Property Management Frontend Architecture

## 📊 CRITICAL FINDINGS

### 1. **Build Output Structure Analysis**

#### **Shaadi App (Working Reference)**
```
shaadi_ui/
├── vite.config.js
│   ├── outDir: "../shaadi/public"
│   └── frappeui({ buildConfig: { indexHtmlPath: 'index.html' }})
├── package.json
│   ├── build: "vite build --base=/assets/shaadi/"
│   └── copy-html-entry: "cp ../shaadi/public/index.html ../shaadi/www/shaadi.html"
└── index.html (source - clean, no build refs)

shaadi/
├── public/
│   ├── index.html (built - has asset refs)
│   ├── assets/
│   │   ├── index-CR3hM1lZ.js
│   │   ├── frappe-ui-BFkBDKMR.js
│   │   └── *.css
│   ├── favicon.png
│   └── manifest.json
└── www/
    ├── shaadi.html (copied from public/index.html, cleaned by post-build)
    └── shaadi.py (context provider)

hooks.py:
  home_page = "shaadi"
  website_route_rules = [
    {"from_route": "/", "to_route": "shaadi"}
  ]

Asset URLs: /assets/shaadi/assets/index-*.js
```

#### **HRMS App (Alternative Pattern)**
```
frontend/
├── vite.config.js
│   ├── outDir: "../hrms/public/frontend"
│   └── frappeui() (NO buildConfig)
├── package.json
│   ├── build: "vite build --base=/assets/hrms/frontend/"
│   └── copy-html-entry: "cp ../hrms/public/frontend/index.html ../hrms/www/hrms.html"
└── index.html (source - clean)

hrms/
├── public/
│   └── frontend/
│       ├── index.html (built)
│       └── assets/
└── www/
    ├── hrms.html (copied)
    └── hrms.py

hooks.py:
  # home_page = "login" (commented)
  website_route_rules = [
    {"from_route": "/hrms/<path:app_path>", "to_route": "hrms"}
  ]

Asset URLs: /assets/hrms/frontend/assets/index-*.js
```

#### **Property Management (Current - BROKEN)**
```
property_ui/
├── vite.config.js
│   ├── outDir: "../property_management/public"  ❌ MISMATCH
│   └── frappeui({ buildConfig: { indexHtmlPath: 'index.html' }})
├── package.json
│   ├── build: "vite build --base=/assets/property_management/"  ❌ MISMATCH
│   └── copy-html-entry: "cp ../property_management/public/frontend/index.html ..."
└── index.html (CORRUPTED - has build asset refs)  ❌ CRITICAL

property_management/
├── public/
│   └── frontend/  ← frappe-ui plugin creates this subdirectory
│       ├── index.html (built)
│       └── assets/
└── www/
    ├── frontend.html
    └── frontend.py

hooks.py:
  home_page = "frontend"
  website_route_rules = [
    {"from_route": "/", "to_route": "frontend"}
  ]

Asset URLs: /assets/property_management/frontend/assets/index-*.js
But base path is: /assets/property_management/  ❌ MISMATCH
```

---

## 🔍 ROOT CAUSE ANALYSIS

### **Issue #1: frappe-ui Plugin Behavior**

The `frappeui()` plugin has **TWO different behaviors**:

**WITH `buildConfig.indexHtmlPath`** (Shaadi pattern):
- Plugin creates output at `outDir` directly
- Plugin modifies source `index.html` file during build
- Requires post-build cleanup script
- Output: `public/index.html`

**WITHOUT `buildConfig`** (HRMS pattern):
- Plugin creates `/frontend` subdirectory automatically
- Plugin does NOT modify source file
- No cleanup needed
- Output: `public/frontend/index.html`

### **Issue #2: Property Management Hybrid Mistake**

Property Management is using:
- ✅ `buildConfig.indexHtmlPath` (like Shaadi)
- ❌ But expecting `/frontend` subdirectory (like HRMS)
- ❌ Base path doesn't match output structure

**Result**: 
- Build outputs to `public/frontend/` (plugin behavior)
- Base path is `/assets/property_management/` (missing `/frontend`)
- Asset paths are `/assets/property_management/frontend/assets/`
- **PATH MISMATCH = 404 errors**

### **Issue #3: Source index.html Corruption**

When using `buildConfig.indexHtmlPath`, the plugin **modifies the source file**:

Before build:
```html
<script type="module" src="/src/main.js"></script>
```

After build (source file modified):
```html
<script type="module" crossorigin src="/assets/property_management/frontend/assets/index-ZY0cPXhT.js"></script>
```

Next build attempt:
```
Error: Rollup failed to resolve import "/assets/property_management/frontend/assets/index-ZY0cPXhT.js"
```

**This is why builds keep failing!**

---

## 🎯 SOLUTION OPTIONS

### **Option A: Pure Shaadi Pattern** ⭐ RECOMMENDED
```
vite.config.js:
  outDir: "../property_management/public"
  frappeui({ buildConfig: { indexHtmlPath: 'index.html' }})

package.json:
  build: "vite build --base=/assets/property_management/ && yarn copy-html-entry && node scripts/post-build.js"
  copy-html-entry: "cp ../property_management/public/index.html ../property_management/www/frontend.html"

Output:
  property_management/public/index.html
  property_management/public/assets/
  
Asset URLs: /assets/property_management/assets/index-*.js ✅
```

**Pros:**
- Matches working Shaadi exactly
- Simpler path structure
- Well-tested pattern
- Easier debugging

**Cons:**
- Requires post-build cleanup script
- Source file gets modified (need to restore)

### **Option B: Pure HRMS Pattern**
```
vite.config.js:
  outDir: "../property_management/public/frontend"
  frappeui() // NO buildConfig

package.json:
  build: "vite build --base=/assets/property_management/frontend/ && yarn copy-html-entry"
  copy-html-entry: "cp ../property_management/public/frontend/index.html ../property_management/www/frontend.html"

Output:
  property_management/public/frontend/index.html
  property_management/public/frontend/assets/
  
Asset URLs: /assets/property_management/frontend/assets/index-*.js ✅
```

**Pros:**
- Source file never modified
- No cleanup script needed
- Matches HRMS pattern

**Cons:**
- Longer asset paths
- Different from Shaadi

### **Option C: Current (BROKEN) - DO NOT USE**
- Hybrid approach causes mismatches
- Source file corruption
- Build failures

---

## 📋 DETAILED COMPARISON TABLE

| Aspect | Shaadi | HRMS | Property Mgmt (Current) | Recommended Fix |
|--------|--------|------|-------------------------|-----------------|
| **vite outDir** | `../shaadi/public` | `../hrms/public/frontend` | `../property_management/public` | `../property_management/public` |
| **buildConfig** | ✅ Has indexHtmlPath | ❌ None | ✅ Has indexHtmlPath | ✅ Keep |
| **Build base** | `/assets/shaadi/` | `/assets/hrms/frontend/` | `/assets/property_management/` | `/assets/property_management/` |
| **Output location** | `public/index.html` | `public/frontend/index.html` | `public/frontend/index.html` ❌ | `public/index.html` ✅ |
| **Asset path** | `/assets/shaadi/assets/` | `/assets/hrms/frontend/assets/` | `/assets/property_management/frontend/assets/` ❌ | `/assets/property_management/assets/` ✅ |
| **Copy script** | `public/index.html` | `public/frontend/index.html` | `public/frontend/index.html` ❌ | `public/index.html` ✅ |
| **Post-build** | ✅ Cleanup script | ❌ Not needed | ✅ Has script | ✅ Update paths |
| **Source corruption** | ⚠️ Yes, cleaned | ❌ No | ⚠️ Yes, NOT cleaned ❌ | ✅ Will clean |

---

## 🔧 EXACT CHANGES NEEDED (Option A - Shaadi Pattern)

### 1. **Remove buildConfig from vite.config.js**
```javascript
// WRONG (current):
frappeui({
    buildConfig: {
        indexHtmlPath: path.resolve(__dirname, 'index.html')
    }
})

// RIGHT (Shaadi pattern):
frappeui()
```

**OR keep buildConfig but ensure outDir is correct** (Shaadi actually uses buildConfig)

### 2. **Update package.json copy script**
```json
// WRONG (current):
"copy-html-entry": "cp ../property_management/public/frontend/index.html ../property_management/www/frontend.html"

// RIGHT:
"copy-html-entry": "cp ../property_management/public/index.html ../property_management/www/frontend.html"
```

### 3. **Update post-build.js paths**
```javascript
// WRONG (current):
const htmlPath = path.join(__dirname, '../../property_management/www/frontend.html');

// Already correct, but verify it exists
```

### 4. **Clean source index.html**
Remove ALL build-generated asset references:
```html
<!-- REMOVE THESE LINES: -->
<script type="module" crossorigin src="/assets/property_management/frontend/assets/index-ZY0cPXhT.js"></script>
<link rel="modulepreload" crossorigin href="/assets/property_management/frontend/assets/frappe-ui-DEQ5Erq6.js">
<link rel="stylesheet" crossorigin href="/assets/property_management/frontend/assets/frappe-ui-DEpoj0UM.css">
<link rel="stylesheet" crossorigin href="/assets/property_management/frontend/assets/index-B37u3ppB.css">

<!-- KEEP ONLY: -->
<script type="module" src="/src/main.js"></script>
```

### 5. **Clean build output directory**
```bash
rm -rf ../property_management/public/*
```

---

## ✅ IMPLEMENTATION CHECKLIST

- [ ] Remove `buildConfig` from vite.config.js (or verify outDir matches)
- [ ] Update `copy-html-entry` script in package.json
- [ ] Clean source `index.html` file
- [ ] Clean `public/` directory
- [ ] Run fresh build
- [ ] Verify output at `public/index.html` (not `public/frontend/index.html`)
- [ ] Verify assets at `public/assets/`
- [ ] Verify `www/frontend.html` created
- [ ] Test on production: `https://real-estate.amitkumar.live/`

---

## 🎯 FINAL RECOMMENDATION

**Use Option A (Shaadi Pattern)** because:

1. ✅ Shaadi is the proven working reference
2. ✅ Simpler asset path structure
3. ✅ Your hooks already configured correctly
4. ✅ Just need to fix build output location
5. ✅ Post-build script already exists

**Key insight**: The frappe-ui plugin creates a `/frontend` subdirectory when `buildConfig.indexHtmlPath` is used, but Shaadi works around this by... **WAIT - need to verify Shaadi's actual output!**

Let me check if Shaadi actually outputs to `public/` directly or `public/frontend/`...

**CORRECTION NEEDED**: Need to verify actual Shaadi build output structure!
