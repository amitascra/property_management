import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	// Public routes
	{
		path: "/",
		name: "PublicHome",
		component: () => import("@/pages/public/PublicHome.vue"),
		meta: { requiresAuth: false, layout: "public" },
	},
	{
		path: "/properties",
		name: "PropertyListing",
		component: () => import("@/pages/public/PropertyListing.vue"),
		meta: { requiresAuth: false, layout: "public" },
	},
	{
		path: "/properties/:id",
		name: "PropertyDetail",
		component: () => import("@/pages/public/PropertyDetail.vue"),
		meta: { requiresAuth: false, layout: "public" },
	},
	{
		path: "/about",
		name: "AboutUs",
		component: () => import("@/pages/public/AboutUs.vue"),
		meta: { requiresAuth: false, layout: "public" },
	},
	{
		path: "/contact",
		name: "Contact",
		component: () => import("@/pages/public/Contact.vue"),
		meta: { requiresAuth: false, layout: "public" },
	},
	// Auth routes
	{
		name: "Login",
		path: "/signin",
		component: () => import("@/pages/Login.vue"),
		meta: { requiresAuth: false, layout: "public" },
	},
	{
		name: "SignUp",
		path: "/signup",
		component: () => import("@/pages/SignUp.vue"),
		meta: { requiresAuth: false, layout: "public" },
	},
	// Tenant routes
	{
		path: "/dashboard",
		name: "TenantDashboard",
		component: () => import("@/pages/TenantDashboard.vue"),
		meta: { requiresAuth: true, layout: "public" },
	},
	// Admin routes
	{
		path: "/admin",
		name: "AdminDashboard",
		component: () => import("@/pages/Home.vue"),
		meta: { requiresAuth: true, layout: "admin" },
	},
]

const router = createRouter({
	history: createWebHistory("/"),
	routes,
})

router.beforeEach(async (to, from, next) => {
	const requiresAuth = to.meta.requiresAuth !== false
	
	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}

	if (to.name === "Login" && isLoggedIn) {
		next({ name: "TenantDashboard" })
	} else if (requiresAuth && !isLoggedIn) {
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router
