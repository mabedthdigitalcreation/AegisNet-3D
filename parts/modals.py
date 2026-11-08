# -*- coding: utf-8 -*-

MODALS = """
    <!-- Modal 1: AI SOC Co-Pilot Modal -->
    <div id="ai-copilot-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <div class="hud-panel rounded-2xl w-full max-w-2xl p-4 sm:p-5 flex flex-col gap-3 shadow-2xl border border-cyan-500/40 bg-slate-950/95 max-h-[90vh]">
            <div class="flex items-center justify-between border-b border-cyan-500/30 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-cyan-400 w-5 h-5"><use href="#ic-sparkle"></use></svg>
                    <h3 class="font-bold text-sm text-white">AI SOC Co-Pilot (Analisis TTPs &amp; Intelijen Mitigasi)</h3>
                </div>
                <button onclick="closeModal('ai-copilot-modal')" class="text-slate-400 hover:text-white p-1">✕</button>
            </div>
            
            <p class="text-xs text-slate-400">
                Co-Pilot menganalisis telemetri real-time, mengidentifikasi signature malware, dan menyusun playbook respon insiden sesuai framework MITRE ATT&CK.
            </p>

            <div id="ai-copilot-output" class="flex-1 min-h-[220px] max-h-[360px] overflow-y-auto bg-slate-900/90 rounded-xl p-3 border border-slate-800 font-mono text-xs text-slate-300 space-y-2 select-text">
                <div class="text-cyan-400 font-bold">[AEGIS-AI READY] Menunggu input analisis atau pilih target dari radar...</div>
                <div class="text-slate-400 text-[11px]">Saran: Klik tombol "AI Analisis" pada salah satu IP target C2 di panel kanan, atau ketik pertanyaan investigasi di bawah.</div>
            </div>

            <div class="flex gap-2">
                <input id="ai-user-query" type="text" placeholder="Tanyakan analisis ancaman, playbook mitigasi, atau decode TTP..." class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs font-mono text-slate-100 focus:outline-none focus:border-cyan-400">
                <button onclick="askAICopilot()" class="px-4 py-2 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/50 text-cyan-200 font-semibold text-xs font-mono transition">
                    Kirim Query
                </button>
            </div>
        </div>
    </div>

    <!-- Modal 2: Multi-Sensor Ground Truth & Validity Laboratory Modal -->
    <div id="validity-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <div class="hud-panel rounded-2xl w-full max-w-2xl p-4 sm:p-5 flex flex-col gap-3 shadow-2xl border border-cyan-500/40 bg-slate-950/95 max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between border-b border-cyan-500/30 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-cyan-400 w-5 h-5"><use href="#ic-award"></use></svg>
                    <h3 class="font-bold text-sm text-white">Laboratorium Validitas Multi-Sensor &amp; Bukti Keaslian</h3>
                </div>
                <button onclick="closeModal('validity-modal')" class="text-slate-400 hover:text-white p-1">✕</button>
            </div>
            
            <p class="text-xs text-slate-300">
                AegisNet 3D beroperasi dengan prinsip <strong>Zero-Simulation</strong>. Semua data yang disajikan di audit dan diverifikasi langsung melalui browser Anda tanpa mock-up sintetis.
            </p>

            <div class="space-y-2 text-xs font-mono">
                <div class="cyber-card p-2.5">
                    <strong class="text-cyan-300 block mb-1">1. Quorum Egress IP &amp; BGP ASN</strong>
                    <div class="text-slate-400 text-[11px]">
                        IP Publik diuji silang terhadap 3 penyedia upstream independen (Cloudflare Trace, ipify, RIPE NCC) untuk menjamin akurasi routing BGP.
                    </div>
                </div>
                <div class="cyber-card p-2.5">
                    <strong class="text-emerald-300 block mb-1">2. STUN Server ICE Leak Test</strong>
                    <div class="text-slate-400 text-[11px]">
                        Menggunakan koneksi WebRTC langsung ke Google STUN Server (<code class="text-emerald-400">stun:stun.l.google.com:19302</code>) untuk mendeteksi IP LAN lokal dan kebocoran tunnel VPN.
                    </div>
                </div>
                <div class="cyber-card p-2.5">
                    <strong class="text-amber-300 block mb-1">3. K-Anonymity HIBP Audit</strong>
                    <div class="text-slate-400 text-[11px]">
                        Hanya 5 karakter pertama dari hash SHA-1 kata sandi yang dikirimkan. Password utuh tidak pernah keluar dari memori lokal browser.
                    </div>
                </div>
                <div class="cyber-card p-2.5">
                    <strong class="text-rose-300 block mb-1">4. Live Cyber Attack Feeds (Ransomwatch, Botnet C2, CISA KEV)</strong>
                    <div class="text-slate-400 text-[11px]">
                        Menghubungkan langsung ke repository telemetri open-source dan mirror CISA resmi via CORS proxy Cloudflare Workers.
                    </div>
                </div>
            </div>

            <div class="pt-2 flex justify-end">
                <button onclick="closeModal('validity-modal')" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono transition">
                    Tutup
                </button>
            </div>
        </div>
    </div>

    <!-- Modal 3: Firewall & SOAR Script Generator Modal -->
    <div id="firewall-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <div class="hud-panel rounded-2xl w-full max-w-2xl p-4 sm:p-5 flex flex-col gap-3 shadow-2xl border border-rose-500/40 bg-slate-950/95 max-h-[90vh]">
            <div class="flex items-center justify-between border-b border-rose-500/30 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-rose-400 w-5 h-5"><use href="#ic-firewall"></use></svg>
                    <h3 class="font-bold text-sm text-white">Generator Skrip Mitigasi Firewall &amp; SOAR Otomatis</h3>
                </div>
                <button onclick="closeModal('firewall-modal')" class="text-slate-400 hover:text-white p-1">✕</button>
            </div>
            
            <p class="text-xs text-slate-400">
                Pilih format aturan pemblokiran untuk target IP yang dipilih guna diterapkan langsung pada firewall gateway Anda:
            </p>

            <div class="flex items-center gap-2">
                <button onclick="generateFirewallRule('iptables')" class="px-3 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/40 text-rose-200 text-xs font-mono font-bold transition">iptables</button>
                <button onclick="generateFirewallRule('nftables')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono transition">nftables</button>
                <button onclick="generateFirewallRule('cisco')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono transition">Cisco ACL</button>
                <button onclick="generateFirewallRule('pfsense')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono transition">pfSense</button>
                <button onclick="generateFirewallRule('mikrotik')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono transition">MikroTik</button>
                <button onclick="generateFirewallRule('windows')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono transition">Windows Netsh</button>
            </div>

            <div class="relative">
                <textarea id="firewall-rule-output" readonly rows="7" class="w-full bg-slate-900 rounded-xl p-3 border border-slate-800 font-mono text-xs text-emerald-300 select-all focus:outline-none"></textarea>
                <button onclick="copyFirewallRule()" class="absolute top-2 right-2 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-300 text-[11px] font-mono border border-slate-700 flex items-center gap-1">
                    <svg class="svg-icon w-3 h-3"><use href="#ic-copy"></use></svg>
                    <span>Salin</span>
                </button>
            </div>

            <div class="flex justify-between items-center pt-2">
                <span id="firewall-copied-toast" class="text-xs text-emerald-400 font-mono hidden">Berhasil disalin ke clipboard!</span>
                <button onclick="closeModal('firewall-modal')" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono transition ml-auto">
                    Tutup
                </button>
            </div>
        </div>
    </div>

    <!-- Modal 4: Defense Pillars Architecture Modal -->
    <div id="defense-pillars-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <div class="hud-panel rounded-2xl w-full max-w-2xl p-4 sm:p-5 flex flex-col gap-3 shadow-2xl border border-cyan-500/40 bg-slate-950/95 max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between border-b border-cyan-500/30 pb-2">
                <div class="flex items-center gap-2">
                    <svg class="svg-icon text-cyan-400 w-5 h-5"><use href="#ic-layers"></use></svg>
                    <h3 class="font-bold text-sm text-white">4 Pilar Arsitektur Pertahanan AegisNet</h3>
                </div>
                <button onclick="closeModal('defense-pillars-modal')" class="text-slate-400 hover:text-white p-1">✕</button>
            </div>
            
            <div class="space-y-3 text-xs font-mono">
                <div class="cyber-card p-3 border-cyan-500/30">
                    <div class="text-cyan-300 font-bold mb-1 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
                        PILAR 1: Verifikasi Postur Identitas &amp; Jaringan
                    </div>
                    <p class="text-slate-400 text-[11px]">
                        Multi-sensor audit untuk memastikan tidak ada kebocoran WebRTC, manipulasi DNS lokal via DoH query, serta verifikasi kekuatan password secara k-anonymity.
                    </p>
                </div>
                <div class="cyber-card p-3 border-emerald-500/30">
                    <div class="text-emerald-300 font-bold mb-1 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                        PILAR 2: Zero-Trust WebCrypto Security Vault
                    </div>
                    <p class="text-slate-400 text-[11px]">
                        Enkripsi data sensitif langsung di sisi klien menggunakan modul Web Cryptography API berstandar militer AES-GCM 256-bit dengan derivation PBKDF2 (100.000 iterasi).
                    </p>
                </div>
                <div class="cyber-card p-3 border-amber-500/30">
                    <div class="text-amber-300 font-bold mb-1 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-amber-400"></span>
                        PILAR 3: Radar Ancaman Dunia Berbasis Telemetri
                    </div>
                    <p class="text-slate-400 text-[11px]">
                        Visualisasi real-time infrastruktur Command &amp; Control (C2), situs pemerasan ransomware, serta feed KEV CISA dalam proyeksi peta dunia dan 3D Globe interaktif.
                    </p>
                </div>
                <div class="cyber-card p-3 border-rose-500/30">
                    <div class="text-rose-300 font-bold mb-1 flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-rose-400"></span>
                        PILAR 4: Mitigasi Aktif &amp; SOAR Response
                    </div>
                    <p class="text-slate-400 text-[11px]">
                        Generator otomatis firewall blocking scripts (iptables, nftables, pfSense, Cisco ACL, Windows Defender) untuk menghentikan ancaman seketika.
                    </p>
                </div>
            </div>

            <div class="pt-2 flex justify-end">
                <button onclick="closeModal('defense-pillars-modal')" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono transition">
                    Tutup
                </button>
            </div>
        </div>
    </div>

    <!-- Modal 5: Industry Sector Forensic Detail Modal (NEW!) -->
    <div id="industry-detail-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <div class="hud-panel rounded-2xl w-full max-w-3xl p-4 sm:p-5 flex flex-col gap-3 shadow-2xl border border-rose-500/40 bg-slate-950/95 max-h-[90vh]">
            <div class="flex items-center justify-between border-b border-rose-500/30 pb-2">
                <div class="flex items-center gap-2">
                    <span id="ind-modal-icon" class="text-lg">🏥</span>
                    <div>
                        <h3 id="ind-modal-title" class="font-bold text-sm text-white">Sektor Kesehatan &amp; Medis</h3>
                        <div id="ind-modal-subtitle" class="text-[10px] text-slate-400 font-mono">Daftar Korban Nyata &amp; Telemetri Eksploitasi</div>
                    </div>
                </div>
                <button onclick="closeModal('industry-detail-modal')" class="text-slate-400 hover:text-white p-1">✕</button>
            </div>

            <!-- Stats Bar -->
            <div class="grid grid-cols-3 gap-2 text-center text-xs font-mono">
                <div class="p-2 rounded-xl bg-slate-900 border border-slate-800">
                    <div class="text-slate-400 text-[10px]">Total Insiden Terdeteksi</div>
                    <div id="ind-modal-count" class="text-rose-400 font-bold text-base">0</div>
                </div>
                <div class="p-2 rounded-xl bg-slate-900 border border-slate-800">
                    <div class="text-slate-400 text-[10px]">Pangsa Serangan Global</div>
                    <div id="ind-modal-share" class="text-amber-400 font-bold text-base">0%</div>
                </div>
                <div class="p-2 rounded-xl bg-slate-900 border border-slate-800">
                    <div class="text-slate-400 text-[10px]">Tingkat Ancaman</div>
                    <div id="ind-modal-level" class="text-rose-500 font-bold text-base">KRITIS</div>
                </div>
            </div>

            <!-- Victims List Container -->
            <div class="flex-1 min-h-[220px] max-h-[360px] overflow-y-auto space-y-1.5 pr-1 font-mono text-xs">
                <div id="ind-modal-victims-container" class="space-y-1.5">
                    <div class="text-slate-500 text-center py-4 text-xs">Memuat daftar insiden sektor...</div>
                </div>
            </div>

            <!-- Footer Action -->
            <div class="pt-2 flex items-center justify-between border-t border-slate-800">
                <button id="ind-modal-filter-btn" onclick="applyIndustryFilterFromModal()" class="px-3.5 py-1.5 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 border border-rose-500/50 text-rose-200 text-xs font-mono font-bold transition flex items-center gap-1.5">
                    <svg class="svg-icon w-3.5 h-3.5"><use href="#ic-filter"></use></svg>
                    <span>Filter Peta ke Sektor Ini</span>
                </button>
                <button onclick="closeModal('industry-detail-modal')" class="px-4 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono transition">
                    Tutup
                </button>
            </div>
        </div>
    </div>
"""
