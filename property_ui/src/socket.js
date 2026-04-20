import { io } from "socket.io-client"

let socket = null
let isInitialized = false

export function initSocket() {
	if (isInitialized && socket) {
		return socket
	}

	try {
		const siteName = window.site_name || window.location.hostname.split(":")[0]
		const host = window.location.hostname
		const port = window.location.port
		
		// Frappe's socketio server runs on port 9000 by default
		const socketPort = port === '8080' ? '9000' : (port || '9000')
		const protocol = window.location.protocol === 'https:' ? 'https' : 'http'
		
		// Connect to Frappe's realtime server with site namespace
		const url = `${protocol}://${host}:${socketPort}/${siteName}`
		
		console.log('Initializing socket connection to:', url)
		
		socket = io(url, {
			withCredentials: true,
			reconnectionAttempts: 5,
			reconnectionDelay: 1000,
			transports: ['websocket', 'polling'],
			auth: {
				// Frappe uses cookies for authentication
			}
		})

		socket.on('connect', () => {
			console.log('Socket connected successfully')
			isInitialized = true
		})

		socket.on('connect_error', (error) => {
			console.warn('Socket connection error:', error.message)
		})

		socket.on('disconnect', (reason) => {
			console.log('Socket disconnected:', reason)
			if (reason === 'io server disconnect') {
				socket.connect()
			}
		})

		return socket
	} catch (error) {
		console.error('Failed to initialize socket:', error)
		return null
	}
}

export function useSocket() {
	return socket
}

export function getSocket() {
	if (!socket || !isInitialized) {
		return initSocket()
	}
	return socket
}
