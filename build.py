#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AegisNet 3D Monolithic Compiler
Combines modular parts from parts/ into production-ready index.html.
Developed by Mabedth Digital Creation
"""

import sys
import os

PARTS_DIR = os.path.join(os.path.dirname(__file__), 'parts')
sys.path.append(PARTS_DIR)

import head_css
import svg_icons
import header_nav
import personal_view
import global_view
import modals
import footer
import js_code

def build():
    output_path = os.path.join(os.path.dirname(__file__), 'index.html')
    
    sections = [
        head_css.HEAD_CSS.strip(),
        header_nav.HEADER_NAV.strip(),
        svg_icons.SVG_ICONS.strip(),
        personal_view.PERSONAL_VIEW.strip(),
        global_view.GLOBAL_VIEW.strip(),
        modals.MODALS.strip(),
        footer.FOOTER.strip(),
        js_code.JS_CODE.strip()
    ]
    
    content = "\n\n".join(sections) + "\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"[OK] index.html compiled successfully ({len(content)} bytes, {len(content.splitlines())} lines)")

if __name__ == '__main__':
    build()
