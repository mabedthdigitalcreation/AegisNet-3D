# -*- coding: utf-8 -*-

SVG_ICONS = """
    <!-- SVG Defs -->
    <svg xmlns="http://www.w3.org/2000/svg" class="hidden">
        <symbol id="ic-shield" viewBox="0 0 24 24">
            <path d="M12 2L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-3zm0 2.18l7 2.33v4.49c0 4.54-3.14 8.78-7 9.9-3.86-1.12-7-5.36-7-9.9V6.51l7-2.33zM11 7v6h2V7h-2zm0 8v2h2v-2h-2z"/>
        </symbol>
        <symbol id="ic-crosshair" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="2" x2="12" y2="6" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="18" x2="12" y2="22" stroke="currentColor" stroke-width="2"/>
            <line x1="2" y1="12" x2="6" y2="12" stroke="currentColor" stroke-width="2"/>
            <line x1="18" y1="12" x2="22" y2="12" stroke="currentColor" stroke-width="2"/>
            <circle cx="12" cy="12" r="2" fill="currentColor"/>
        </symbol>
        <symbol id="ic-globe" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="2" y1="12" x2="22" y2="12" stroke="currentColor" stroke-width="2"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-map" viewBox="0 0 24 24">
            <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="8" y1="2" x2="8" y2="18" stroke="currentColor" stroke-width="2"/>
            <line x1="16" y1="6" x2="16" y2="22" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-topology" viewBox="0 0 24 24">
            <circle cx="12" cy="5" r="3" fill="none" stroke="currentColor" stroke-width="2"/>
            <circle cx="5" cy="19" r="3" fill="none" stroke="currentColor" stroke-width="2"/>
            <circle cx="19" cy="19" r="3" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="8" x2="5" y2="16" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="8" x2="19" y2="16" stroke="currentColor" stroke-width="2"/>
            <line x1="8" y1="19" x2="16" y2="19" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-layers" viewBox="0 0 24 24">
            <polygon points="12 2 2 7 12 12 22 7 12 2" fill="none" stroke="currentColor" stroke-width="2"/>
            <polyline points="2 17 12 22 22 17" fill="none" stroke="currentColor" stroke-width="2"/>
            <polyline points="2 12 12 17 22 12" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-key" viewBox="0 0 24 24">
            <path d="M21 2l-2 2m-1.5 1.5L16 7l-2-2-4 4 1.5 1.5-2 2-1.5-1.5-3 3A5.5 5.5 0 1 1 2 11a5.5 5.5 0 0 1 9-4.24l2-2 1.5 1.5 2-2 1.5 1.5L21 2z" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-lock" viewBox="0 0 24 24">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-award" viewBox="0 0 24 24">
            <circle cx="12" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="2"/>
            <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-sparkle" viewBox="0 0 24 24">
            <path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z" fill="currentColor"/>
        </symbol>
        <symbol id="ic-alert" viewBox="0 0 24 24">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="17" x2="12.01" y2="17" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-refresh" viewBox="0 0 24 24">
            <polyline points="23 4 23 10 17 10" fill="none" stroke="currentColor" stroke-width="2"/>
            <polyline points="1 20 1 14 7 14" fill="none" stroke="currentColor" stroke-width="2"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-download" viewBox="0 0 24 24">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" fill="none" stroke="currentColor" stroke-width="2"/>
            <polyline points="7 10 12 15 17 10" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-wifi" viewBox="0 0 24 24">
            <path d="M5 12.55a11 11 0 0 1 14.08 0" fill="none" stroke="currentColor" stroke-width="2"/>
            <path d="M1.42 9a16 16 0 0 1 21.16 0" fill="none" stroke="currentColor" stroke-width="2"/>
            <path d="M8.53 16.11a6 6 0 0 1 6.95 0" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="20" x2="12.01" y2="20" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-cpu" viewBox="0 0 24 24">
            <rect x="4" y="4" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>
            <rect x="9" y="9" width="6" height="6" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="9" y1="1" x2="9" y2="4" stroke="currentColor" stroke-width="2"/>
            <line x1="15" y1="1" x2="15" y2="4" stroke="currentColor" stroke-width="2"/>
            <line x1="9" y1="20" x2="9" y2="23" stroke="currentColor" stroke-width="2"/>
            <line x1="15" y1="20" x2="15" y2="23" stroke="currentColor" stroke-width="2"/>
            <line x1="20" y1="9" x2="23" y2="9" stroke="currentColor" stroke-width="2"/>
            <line x1="20" y1="14" x2="23" y2="14" stroke="currentColor" stroke-width="2"/>
            <line x1="1" y1="9" x2="4" y2="9" stroke="currentColor" stroke-width="2"/>
            <line x1="1" y1="14" x2="4" y2="14" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-terminal" viewBox="0 0 24 24">
            <polyline points="4 17 10 11 4 5" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="19" x2="20" y2="19" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-bug" viewBox="0 0 24 24">
            <rect x="6" y="9" width="12" height="12" rx="6" fill="none" stroke="currentColor" stroke-width="2"/>
            <path d="M12 9V5" stroke="currentColor" stroke-width="2"/>
            <path d="M8 3l2 2" stroke="currentColor" stroke-width="2"/>
            <path d="M16 3l-2 2" stroke="currentColor" stroke-width="2"/>
            <line x1="4" y1="13" x2="6" y2="13" stroke="currentColor" stroke-width="2"/>
            <line x1="18" y1="13" x2="20" y2="13" stroke="currentColor" stroke-width="2"/>
            <line x1="4" y1="17" x2="6" y2="17" stroke="currentColor" stroke-width="2"/>
            <line x1="18" y1="17" x2="20" y2="17" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-search" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="8" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-copy" viewBox="0 0 24 24">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" fill="none" stroke="currentColor" stroke-width="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-firewall" viewBox="0 0 24 24">
            <rect x="3" y="3" width="18" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="3" y1="9" x2="21" y2="9" stroke="currentColor" stroke-width="2"/>
            <line x1="3" y1="15" x2="21" y2="15" stroke="currentColor" stroke-width="2"/>
            <line x1="9" y1="3" x2="9" y2="9" stroke="currentColor" stroke-width="2"/>
            <line x1="15" y1="3" x2="15" y2="9" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="9" x2="12" y2="15" stroke="currentColor" stroke-width="2"/>
            <line x1="7" y1="15" x2="7" y2="21" stroke="currentColor" stroke-width="2"/>
            <line x1="17" y1="15" x2="17" y2="21" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-pause" viewBox="0 0 24 24">
            <rect x="6" y="4" width="4" height="16" fill="currentColor"/>
            <rect x="14" y="4" width="4" height="16" fill="currentColor"/>
        </symbol>
        <symbol id="ic-play" viewBox="0 0 24 24">
            <polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/>
        </symbol>
        <symbol id="ic-filter" viewBox="0 0 24 24">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>

        <!-- 8 Industry Sector Symbols -->
        <symbol id="ic-health" viewBox="0 0 24 24">
            <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="12" y1="7" x2="12" y2="13" stroke="currentColor" stroke-width="2"/>
            <line x1="9" y1="10" x2="15" y2="10" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-finance" viewBox="0 0 24 24">
            <line x1="3" y1="21" x2="21" y2="21" stroke="currentColor" stroke-width="2"/>
            <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/>
            <polyline points="12 3 2 10 22 10" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="6" y1="10" x2="6" y2="21" stroke="currentColor" stroke-width="2"/>
            <line x1="10" y1="10" x2="10" y2="21" stroke="currentColor" stroke-width="2"/>
            <line x1="14" y1="10" x2="14" y2="21" stroke="currentColor" stroke-width="2"/>
            <line x1="18" y1="10" x2="18" y2="21" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-gov" viewBox="0 0 24 24">
            <path d="M12 2L2 7v3c0 5.5 3.8 10.7 10 12 6.2-1.3 10-6.5 10-12V7l-10-5z" fill="none" stroke="currentColor" stroke-width="2"/>
            <circle cx="12" cy="11" r="3" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-edu" viewBox="0 0 24 24">
            <path d="M22 10v6M2 10l10-5 10 5-10 5z" fill="none" stroke="currentColor" stroke-width="2"/>
            <path d="M6 12v5c3 3 9 3 12 0v-5" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-energy" viewBox="0 0 24 24">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" fill="currentColor"/>
        </symbol>
        <symbol id="ic-mfg" viewBox="0 0 24 24">
            <path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-tech" viewBox="0 0 24 24">
            <rect x="2" y="2" width="20" height="8" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>
            <rect x="2" y="14" width="20" height="8" rx="2" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="6" y1="6" x2="6.01" y2="6" stroke="currentColor" stroke-width="2"/>
            <line x1="6" y1="18" x2="6.01" y2="18" stroke="currentColor" stroke-width="2"/>
        </symbol>
        <symbol id="ic-retail" viewBox="0 0 24 24">
            <circle cx="9" cy="21" r="1" fill="currentColor"/>
            <circle cx="20" cy="21" r="1" fill="currentColor"/>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" fill="none" stroke="currentColor" stroke-width="2"/>
        </symbol>
    </svg>
"""
