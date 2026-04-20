# Frappe UI Installation & Configuration Analysis

## 🔍 CRITICAL FINDINGS

### **Version Mismatch Detected**

| App | frappe-ui Version | Status |
|-----|-------------------|--------|
| **Shaadi** | `0.1.105` | ✅ Working |
| **HRMS** | `0.1.105` | ✅ Working |
| **Property Management** | `^0.1.192` | ❌ **NEWER VERSION - POTENTIAL ISSUE** |

**Problem**: Property Management is using a MUCH newer version (0.1.192 vs 0.1.105) which may have breaking changes or different behavior.

---

## 📚 Frappe UI Vite Plugin Documentation

### **Build Configuration Options (from official docs)**

```javascript
frappeui({
  buildConfig: {
    outDir: '../app_name/public/frontend',        // Default: auto-calculated
    baseUrl: '/assets/app_name/frontend/',        // Default: auto-calculated
    indexHtmlPath: '../app_name/www/app_name.html', // Where to copy built index.html
    emptyOutDir: true,                            // Default: true
    sourcemap: true,                              // Default: true
  },
})
```

### **Key Insights from Documentation**

1. **`buildConfig` is OPTIONAL** - The plugin auto-calculates defaults
2. **`indexHtmlPath`** - Specifies where to COPY the built index.html
3. **Default `outDir`** - Automatically set to `../app_name/public/frontend`
4. **Default `baseUrl`** - Automatically set to `/assets/app_name/frontend/`

---

## 🔧 Current Configuration Issues

### **Property Management (Current - WRONG)**

```javascript
// vite.config.js
frappeui({
  buildConfig: {
    indexHtmlPath: path.resolve(__dirname, 'index.html')  // ❌ WRONG - This is SOURCE path
  }
})

build: {
  outDir: "../property_management/public/frontend",  // Correct
}

// package.json
"build": "vite build --base=/assets/property_management/frontend/ ..." // Correct
```

**Problem**: `indexHtmlPath` should be the DESTINATION path (where to copy), not the source path!

### **Shaadi (Working - But Different Pattern)**

```javascript
// vite.config.js
frappeui({
  buildConfig: {
    indexHtmlPath: path.resolve(__dirname, 'index.html')  // Source path
  }
})

build: {
  outDir: "../shaadi/public",  // NO /frontend subdirectory
}

// package.json
"build": "vite build --base=/assets/shaadi/ ..."  // NO /frontend in path
"copy-html-entry": "cp ../shaadi/public/index.html ..."  // Manual copy
```

**Shaadi's pattern**: Uses buildConfig but outputs to `public/` directly, then manually copies

### **HRMS (Working - Clean Pattern)**

```javascript
// vite.config.js
frappeui()  // NO buildConfig at all!

build: {
  outDir: "../hrms/public/frontend",  // Has /frontend subdirectory
}

// package.json
"build": "vite build --base=/assets/hrms/frontend/ ..."  // Has /frontend in path
"copy-html-entry": "cp ../hrms/public/frontend/index.html ..."  // Matches output
```

**HRMS's pattern**: No buildConfig, lets plugin use defaults, everything aligns perfectly

---

## ✅ CORRECT SOLUTION

### **Option 1: HRMS Pattern (RECOMMENDED)**

Remove `buildConfig` entirely and let the plugin handle everything with defaults:

```javascript
// vite.config.js
export default defineConfig({
  plugins: [
    vue(),
    frappeui()  // NO buildConfig - use defaults
  ],
  build: {
    outDir: "../property_management/public/frontend",  // Plugin default
  },
})
```

```json
// package.json
{
  "build": "vite build --base=/assets/property_management/frontend/ && yarn copy-html-entry",
  "copy-html-entry": "cp ../property_management/public/frontend/index.html ../property_management/www/frontend.html"
}
```

**Why this works**:
- Plugin auto-sets `outDir` to `public/frontend`
- Plugin auto-sets `baseUrl` to `/assets/property_management/frontend/`
- No source file corruption
- Clean, predictable behavior

### **Option 2: Shaadi Pattern (Alternative)**

Use buildConfig but configure it correctly:

```javascript
// vite.config.js
frappeui({
  buildConfig: {
    outDir: '../property_management/public',  // NO /frontend
    baseUrl: '/assets/property_management/',   // NO /frontend
    indexHtmlPath: '../property_management/www/frontend.html',  // DESTINATION path
  }
})
```

**Why this might work**:
- Explicit control over all paths
- Matches Shaadi's approach
- But requires correct indexHtmlPath (destination, not source)

---

## 🎯 ACTION PLAN

1. **Downgrade frappe-ui** to `0.1.105` (match working apps)
2. **Use HRMS pattern** (no buildConfig)
3. **Update package.json** to match HRMS exactly
4. **Clean rebuild** with correct configuration

---

## 📋 IMPLEMENTATION STEPS

### Step 1: Update package.json

```bash
cd property_ui
yarn remove frappe-ui
yarn add frappe-ui@0.1.105
```

### Step 2: Update vite.config.js

```javascript
import path from "path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [
    vue(),
    frappeui()  // Remove buildConfig
  ],
  build: {
    outDir: "../property_management/public/frontend",
    emptyOutDir: true,
    target: "es2015",
    commonjsOptions: {
      include: [/tailwind.config.js/, /node_modules/],
    },
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          "frappe-ui": ["frappe-ui"],
        },
      },
    },
  },
  // ... rest of config
})
```

### Step 3: Update package.json scripts

```json
{
  "build": "vite build --base=/assets/property_management/frontend/ && yarn copy-html-entry",
  "copy-html-entry": "cp ../property_management/public/frontend/index.html ../property_management/www/frontend.html"
}
```

### Step 4: Remove post-build.js (not needed with HRMS pattern)

Or update it to match the new paths if keeping it.

---

## 🔑 KEY TAKEAWAYS

1. **Version matters** - Use same frappe-ui version as working apps
2. **buildConfig is optional** - HRMS doesn't use it and works perfectly
3. **Let the plugin do its job** - Don't override defaults unless necessary
4. **Path consistency** - All paths must align (outDir, baseUrl, copy script)
5. **Source file protection** - HRMS pattern doesn't modify source index.html

---

## ✅ EXPECTED OUTCOME

After implementing HRMS pattern:

```
property_management/
├── public/
│   └── frontend/
│       ├── index.html (built by Vite)
│       ├── assets/
│       │   ├── index-*.js
│       │   ├── frappe-ui-*.js
│       │   └── *.css
│       └── favicon.png
└── www/
    ├── frontend.html (copied from public/frontend/index.html)
    └── frontend.py

Asset URLs: /assets/property_management/frontend/assets/index-*.js ✅
Base path: /assets/property_management/frontend/ ✅
Routes: / → frontend ✅
```
