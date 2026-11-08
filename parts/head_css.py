# -*- coding: utf-8 -*-

HEAD_CSS = """<!DOCTYPE html>
<html lang="id" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AegisNet 3D - Live Cyber Threat Map &amp; Global Security Intelligence</title>
    <meta name="description" content="Platform Intelijen Keamanan Siber Real-Time berstandar SOC Enterprise dengan Peta Serangan Dunia Langsung (FortiGuard Style), Audit Postur Pribadi (WebRTC, DNS, WebCrypto), dan Klasifikasi Sektor Industri Terdampak.">
    <meta name="theme-color" content="#030712">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2300f0ff'><path d='M12 2L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-3zm0 2.18l7 2.33v4.49c0 4.54-3.14 8.78-7 9.9-3.86-1.12-7-5.36-7-9.9V6.51l7-2.33zM11 7v6h2V7h-2zm0 8v2h2v-2h-2z'/></svg>">
    <link rel="shortcut icon" href="favicon.ico">
    <link rel="icon" href="favicon.ico">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

    <!-- Tailwind Notice Filter (Suppresses harmless production advisory in console) -->
    <script>
        (function() {
            const _origWarn = console.warn;
            console.warn = function(...args) {
                if (args[0] && typeof args[0] === 'string' && args[0].includes('cdn.tailwindcss.com')) return;
                _origWarn.apply(console, args);
            };
        })();
    </script>

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace']
                    },
                    colors: {
                        cyber: {
                            bg: '#030712',
                            panel: 'rgba(11, 19, 43, 0.78)',
                            card: 'rgba(15, 23, 42, 0.85)',
                            border: 'rgba(56, 189, 248, 0.22)',
                            borderHover: 'rgba(56, 189, 248, 0.55)',
                            cyan: '#00f0ff',
                            emerald: '#10b981',
                            rose: '#f43f5e',
                            amber: '#f59e0b',
                            indigo: '#6366f1',
                            purple: '#a855f7'
                        },
                        sector: {
                            health: '#10b981',
                            finance: '#00f0ff',
                            gov: '#6366f1',
                            edu: '#38bdf8',
                            energy: '#f59e0b',
                            mfg: '#f97316',
                            tech: '#a855f7',
                            retail: '#f43f5e'
                        }
                    },
                    animation: {
                        'pulse-glow': 'pulseGlow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                        'radar-sweep': 'radarSweep 4s linear infinite',
                        'scanline': 'scanline 8s linear infinite',
                        'ping-slow': 'ping 2.5s cubic-bezier(0, 0, 0.2, 1) infinite'
                    },
                    keyframes: {
                        pulseGlow: {
                            '0%, 100%': { opacity: 1, filter: 'drop-shadow(0 0 10px rgba(0, 240, 255, 0.6))' },
                            '50%': { opacity: 0.6, filter: 'drop-shadow(0 0 3px rgba(0, 240, 255, 0.2))' }
                        },
                        radarSweep: {
                            '0%': { transform: 'rotate(0deg)' },
                            '100%': { transform: 'rotate(360deg)' }
                        },
                        scanline: {
                            '0%': { transform: 'translateY(-100%)' },
                            '100%': { transform: 'translateY(1000%)' }
                        }
                    }
                }
            }
        };
    </script>

    <!-- External Core Engines (Three.js + D3 + TopoJSON) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js"></script>

    <style>
        :root {
            --cyber-cyan: #00f0ff;
            --cyber-emerald: #10b981;
            --cyber-rose: #f43f5e;
            --cyber-amber: #f59e0b;
        }

        body {
            background-color: #030712;
            color: #f8fafc;
            overflow-x: hidden;
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.01em;
        }

        /* Glassmorphism Cyber Panels */
        .hud-panel {
            background: rgba(11, 19, 43, 0.82);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(56, 189, 248, 0.18);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 0 0 1px rgba(255, 255, 255, 0.04);
            transition: border-color 0.25s ease, box-shadow 0.25s ease;
        }

        .hud-panel:hover {
            border-color: rgba(56, 189, 248, 0.35);
        }

        .cyber-card {
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 0.75rem;
            transition: all 0.2s ease;
        }

        .cyber-card:hover {
            background: rgba(22, 34, 60, 0.85);
            border-color: rgba(56, 189, 248, 0.3);
        }

        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(3, 7, 18, 0.6);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(56, 189, 248, 0.28);
            border-radius: 9999px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(56, 189, 248, 0.55);
        }

        /* Scanline Overlay */
        .scanline-overlay {
            background: linear-gradient(
                rgba(18, 16, 16, 0) 50%, 
                rgba(0, 0, 0, 0.22) 50%
            ), linear-gradient(
                90deg,
                rgba(255, 0, 0, 0.015),
                rgba(0, 255, 0, 0.01),
                rgba(0, 0, 255, 0.015)
            );
            background-size: 100% 3px, 6px 100%;
            pointer-events: none;
        }

        .svg-icon {
            display: inline-block;
            width: 1rem;
            height: 1rem;
            stroke-width: 0;
            stroke: currentColor;
            fill: currentColor;
            vertical-align: -0.125em;
        }

        /* Tactical 2D Canvas & 3D WebGL Canvas Layering */
        #tactical-map-canvas, #canvas-container canvas {
            display: block;
            width: 100%;
            height: 100%;
        }

        /* 3D Tooltip Overlay */
        #node-tooltip-overlay {
            position: absolute;
            z-index: 60;
            pointer-events: auto;
            transform: translate(-50%, -110%);
            transition: opacity 0.15s ease;
        }

        /* Glowing Pulse Shockwave Animation for Impact */
        @keyframes shockwaveExpand {
            0% { transform: scale(0.2); opacity: 1; }
            100% { transform: scale(2.8); opacity: 0; }
        }
    </style>
</head>
"""
