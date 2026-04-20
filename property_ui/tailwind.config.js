module.exports = {
	content: [
		"./index.html",
		"./src/**/*.{vue,js,ts,jsx,tsx}",
		"./node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
		"../node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
	],
	darkMode: 'class',
	theme: {
		extend: {
			colors: {
				property: {
					// Primary brand colors
					blue: {
						50: '#EFF6FF',
						100: '#DBEAFE',
						200: '#BFDBFE',
						400: '#60A5FA',
						DEFAULT: '#3B82F6',
						600: '#2563EB',
						700: '#1D4ED8',
						dark: '#60A5FA',
						muted: '#1E3A8A',
					},
					green: {
						50: '#F0FDF4',
						100: '#DCFCE7',
						200: '#BBF7D0',
						400: '#4ADE80',
						DEFAULT: '#22C55E',
						600: '#16A34A',
						700: '#15803D',
						dark: '#4ADE80',
						muted: '#14532D',
					},
					// Background colors
					bg: {
						base: '#F9FAFB',
						surface: '#FFFFFF',
						raised: '#F3F4F6',
						overlay: '#E5E7EB',
					},
					// Dark backgrounds
					'dk-base': '#0F172A',
					'dk-surface': '#1E293B',
					'dk-raised': '#334155',
					'dk-overlay': '#475569',
					// Text colors
					ink: '#111827',
					body: '#6B7280',
					hint: '#9CA3AF',
					'dk-ink': '#F9FAFB',
					'dk-body': '#D1D5DB',
					'dk-hint': '#9CA3AF',
					// Borders
					border: '#E5E7EB',
					'border-mid': '#D1D5DB',
					'dk-border': '#374151',
					'dk-border-mid': '#4B5563',
				},
			},
			borderRadius: {
				'property-sm': '6px',
				'property-md': '10px',
				'property-lg': '14px',
				'property-xl': '20px',
			},
			borderWidth: {
				'property': '0.5px',
			},
		},
	},
	plugins: [],
}
