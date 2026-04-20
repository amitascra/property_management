#!/usr/bin/env node

/**
 * Post-build script to clean up frontend.html
 * Removes problematic script blocks and fixes asset paths
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const htmlPath = path.join(__dirname, '../../property_management/www/home.html');

console.log('Cleaning up home.html...');

try {
    let html = fs.readFileSync(htmlPath, 'utf8');
    
    // Remove problematic script blocks that jinjaBootData might add
    const problematicBlock = /\s*<script>\s*{% for key in boot %}[\s\S]*?{% endfor %}\s*<\/script>\s*/g;
    html = html.replace(problematicBlock, '');
    
    // Fix double slashes in asset paths
    html = html.replace(/\/assets\/property_management\/frontend\/\//g, '/assets/property_management/frontend/');
    
    fs.writeFileSync(htmlPath, html, 'utf8');
    
    console.log('✓ Successfully cleaned up home.html');
} catch (error) {
    console.error('Error cleaning up home.html:', error.message);
    process.exit(1);
}
