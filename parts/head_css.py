# -*- coding: utf-8 -*-

HEAD_CSS = """<!DOCTYPE html>
<html lang="id" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AegisNet 3D - Live Cyber Defense Operations &amp; Global Threat Intelligence</title>
    <meta name="description" content="Platform Intelijen Keamanan Siber Real-Time &amp; Radar Ancaman Global 3D. 100% utilitas nyata: WebRTC leak, DNS audit, WebCrypto AES-GCM, HIBP breach check, serta live feed ransomware &amp; C2 botnet dunia.">
    <meta name="theme-color" content="#030712">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">

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
                            panel: 'rgba(11, 19, 43, 0.75)',
                            card: 'rgba(15, 23, 42, 0.85)',
                            border: 'rgba(56, 189, 248, 0.22)',
                            borderHover: 'rgba(56, 189, 248, 0.5)',
                            cyan: '#00f0ff',
                            emerald: '#10b981',
                            rose: '#f43f5e',
                            amber: '#f59e0b',
                            indigo: '#6366f1'
                        }
                    },
                    animation: {
                        'pulse-glow': 'pulseGlow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                        'radar-sweep': 'radarSweep 4s linear infinite',
                        'scanline': 'scanline 8s linear infinite'
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

    <!-- Three.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

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

        /* Cyber Panels */
        .hud-panel {
            background: rgba(11, 19, 43, 0.78);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(56, 189, 248, 0.18);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.45), inset 0 0 0 1px rgba(255, 255, 255, 0.03);
            transition: border-color 0.25s ease, box-shadow 0.25s ease;
        }

        .hud-panel:hover {
            border-color: rgba(56, 189, 248, 0.35);
        }

        .hud-panel-danger {
            background: rgba(30, 10, 20, 0.85);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(244, 63, 94, 0.35);
            box-shadow: 0 8px 32px 0 rgba(244, 63, 94, 0.2);
        }

        .cyber-card {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 0.75rem;
            transition: all 0.2s ease;
        }

        .cyber-card:hover {
            background: rgba(22, 34, 60, 0.75);
            border-color: rgba(56, 189, 248, 0.28);
        }

        /* Custom Scrollbar */
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
                rgba(0, 0, 0, 0.25) 50%
            ), linear-gradient(
                90deg,
                rgba(255, 0, 0, 0.02),
                rgba(0, 255, 0, 0.01),
                rgba(0, 0, 255, 0.02)
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

        /* 3D Tooltip Overlay */
        #node-tooltip-overlay {
            position: absolute;
            z-index: 60;
            pointer-events: auto;
            transform: translate(-50%, -110%);
            transition: opacity 0.15s ease;
        }
    </style>
</head>
"""
