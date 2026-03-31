#!/usr/bin/env python3
# ============================================================
# SIMPLE WIFI SPAMMER v1.0 - Windows Edition
# Author: lavashgovadina3
# Version: 1.0
# Platform: Windows 7, 8, 8.1, 10, 11
# ============================================================

import os
import sys
import time
import random
import subprocess
import ctypes
import threading
import string
import re
import json
import socket
import struct
import binascii
import hashlib
import tempfile
import queue
from datetime import datetime, timedelta
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor

# ============= ADMIN RIGHTS =============
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# ============= COLORS =============
class Colors:
    RED = ''
    GREEN = ''
    YELLOW = ''
    BLUE = ''
    CYAN = ''
    MAGENTA = ''
    WHITE = ''
    BOLD = ''
    DIM = ''
    RESET = ''
    
    BG_RED = ''
    BG_GREEN = ''
    BG_YELLOW = ''
    BG_BLUE = ''

# ============= SSID DATABASE =============
SSID_TEMPLATES = {
    # Public WiFi
    'public': [
        "FreeWiFi", "PublicWiFi", "GuestWiFi", "FreeInternet", "WiFi_Free",
        "Free_WiFi_Zone", "Public_Network", "Guest_Network", "Community_WiFi",
        "City_WiFi", "Metro_Free", "Transit_WiFi", "Station_WiFi", "Airport_Free",
        "Mall_WiFi", "Shopping_Free", "Restaurant_WiFi", "Cafe_Free", "Library_WiFi",
        "Park_WiFi", "Square_Free", "Beach_WiFi", "Resort_WiFi", "Hotel_Guest"
    ],
    
    # Coffee Shops
    'coffee': [
        "Starbucks_WiFi", "Starbucks_Guest", "Starbucks_Free", "Coffee_Bean_WiFi",
        "Dunkin_WiFi", "Dunkin_Free", "Tim_Hortons_WiFi", "Peets_Coffee",
        "Caribou_Coffee", "Costa_Coffee", "Nero_WiFi", "Lavazza_WiFi",
        "Illy_WiFi", "Espresso_House", "Coffee_Shop_Free", "Cafe_Latte_WiFi",
        "Brew_House", "Java_Joint", "Grind_Coffee", "Roast_Coffee"
    ],
    
    # Fast Food
    'fastfood': [
        "McDonalds_Free", "McDonalds_WiFi", "McDonalds_Guest", "McDonalds_5G",
        "KFC_Free", "KFC_WiFi", "KFC_Guest", "Burger_King_WiFi", "BK_Free",
        "Wendys_WiFi", "Taco_Bell_WiFi", "Subway_WiFi", "Subway_Free",
        "Pizza_Hut_WiFi", "Dominoes_WiFi", "Chick_fil_A_WiFi", "In_N_Out_WiFi",
        "Sonic_WiFi", "Arbys_WiFi", "Popeyes_WiFi", "Chipotle_WiFi"
    ],
    
    # Hotels
    'hotel': [
        "Marriott_WiFi", "Hilton_Guest", "Hyatt_Free", "Sheraton_WiFi",
        "Westin_Guest", "Radisson_Free", "Holiday_Inn_WiFi", "Best_Western_Guest",
        "Comfort_Inn", "Quality_Inn", "Days_Inn", "Motel_6_WiFi", "Super_8_WiFi",
        "Travelodge", "Ramada_WiFi", "Wyndham_Guest", "Four_Seasons_WiFi",
        "Ritz_Carlton", "Waldorf_Astoria", "InterContinental", "Crowne_Plaza"
    ],
    
    # Telecom Companies
    'telecom': [
        "ATT_WiFi", "ATT_Free", "Verizon_WiFi", "Verizon_Free", "T_Mobile_WiFi",
        "T_Mobile_Guest", "Sprint_WiFi", "Sprint_Free", "Comcast_WiFi", "Xfinity_WiFi",
        "Spectrum_WiFi", "Optimum_WiFi", "Cox_WiFi", "Mediacom_WiFi", "CenturyLink_WiFi",
        "Frontier_WiFi", "Windstream_WiFi", "Google_Fi", "Google_WiFi", "Project_Fi"
    ],
    
    # Device Hotspots
    'device': [
        "iPhone", "iPhone_5G", "iPhone_Hotspot", "iPhone_Guest", "iPhone_Ultra",
        "AndroidAP", "Android_Hotspot", "Samsung_WiFi", "Galaxy_Hotspot", "Galaxy_S24",
        "Pixel_Hotspot", "Pixel_WiFi", "Google_Pixel", "Xiaomi_Hotspot", "Mi_WiFi",
        "Huawei_WiFi", "P30_Hotspot", "OnePlus_WiFi", "Oppo_Hotspot", "Vivo_WiFi"
    ],
    
    # Router Brands
    'router': [
        "TP-Link", "TP-Link_5G", "TP-Link_Guest", "Netgear_WiFi", "Netgear_Guest",
        "Linksys", "Linksys_Smart", "Asus_WiFi", "Asus_Guest", "D-Link_WiFi",
        "Cisco_WiFi", "Meraki_WiFi", "Ubiquiti_WiFi", "UniFi", "MikroTik",
        "ZTE_WiFi", "Huawei_WiFi", "Xiaomi_Router", "Tenda_WiFi", "Belkin_WiFi"
    ],
    
    # Government/Surveillance
    'gov': [
        "FBI_Surveillance", "FBI_Van_6", "FBI_Mobile_Unit", "NSA_Ops", "NSA_Monitoring",
        "CIA_Field_Office", "CIA_Van", "DEA_Surveillance", "Police_Scanner", "Police_Net",
        "Sheriff_Department", "State_Patrol", "DHS_Monitoring", "DHS_Security",
        "TSA_WiFi", "Homeland_Security", "Military_Base", "US_Army_Net", "Air_Force_WiFi"
    ],
    
    # Funny/Prank
    'funny': [
        "Free_Virus", "Malware_Distro", "Honeypot_Network", "Hacker_Hotspot",
        "Dark_Web_Access", "Anonymous_Net", "Illegal_Downloads", "Free_Crypto",
        "Bitcoin_Faucet", "Free_ETH", "Gimme_Your_Pass", "We_Are_Watching",
        "Your_IP_Is_Logged", "I_See_You", "Come_Closer", "Totally_Safe",
        "Not_A_Trap", "Definitely_Legit", "Totally_Not_FBI", "Trust_Me_Bro"
    ],
    
    # Educational
    'edu': [
        "University_WiFi", "Campus_Network", "Student_WiFi", "Faculty_WiFi",
        "MIT_Guest", "Stanford_WiFi", "Harvard_Net", "Oxford_Guest", "Cambridge_WiFi",
        "UCLA_Guest", "NYU_WiFi", "Columbia_Net", "Princeton_Guest", "Yale_WiFi",
        "Cornell_Net", "Duke_WiFi", "Northwestern_Guest", "Johns_Hopkins"
    ],
    
    # Airports
    'airport': [
        "JFK_Free_WiFi", "LAX_Guest", "ORD_WiFi", "DFW_Free", "DEN_WiFi",
        "ATL_Guest", "SFO_WiFi", "SEA_Free", "LAS_WiFi", "MIA_Guest",
        "BOS_WiFi", "PHX_Free", "IAH_WiFi", "EWR_Guest", "MSP_WiFi"
    ],
    
    # Tech Companies
    'tech': [
        "Google_WiFi", "Google_Guest", "Facebook_WiFi", "Meta_Guest", "Apple_WiFi",
        "Microsoft_Guest", "Amazon_WiFi", "Netflix_Office", "Twitter_WiFi",
        "Tesla_WiFi", "SpaceX_Starlink", "SpaceX_Guest", "OpenAI_WiFi",
        "DeepSeek_Net", "NVIDIA_WiFi", "Intel_Guest", "AMD_WiFi", "Qualcomm_Net"
    ],
    
    # Gaming
    'gaming': [
        "PlayStation_Network", "Xbox_Live", "Nintendo_Switch", "Steam_WiFi",
        "Epic_Games_Net", "Riot_Games_WiFi", "Blizzard_Net", "Valve_WiFi",
        "Rockstar_Games", "Ubisoft_WiFi", "EA_Sports_Net", "Activision_WiFi",
        "CD_Projekt_Red", "Bethesda_Net", "Mojang_WiFi", "Minecraft_Server"
    ],
    
    # 5G Networks
    '5g': [
        "5G_Network", "5G_Ultra", "5G_Plus", "5G_Max", "5G_UltraWide",
        "5G_NSA", "5G_SA", "5G_Standalone", "5G_MMWave", "5G_C_Band",
        "5G_Ultra_Capacity", "5G_Extended", "5G_Home", "5G_Business"
    ]
}

# SSID Suffixes
SSID_SUFFIXES = ["", "_5G", "_2.4G", "_Guest", "_Free", "_Public", "_Hotspot", 
                 "_WiFi6", "_WiFi7", "_6E", "_Mesh", "_Extender", "_Plus", "_Max",
                 "_Pro", "_Ultra", "_Lite", "_Express", "_Premium", "_Deluxe"]

# ============= MAC ADDRESS DATABASE =============
MAC_PREFIXES = {
    'apple': ['00:1E:C2', '00:25:00', '00:1F:5B', '00:1F:5B', '04:0C:CE', '08:00:07'],
    'samsung': ['00:1B:44', '00:1E:3D', '00:24:54', '38:AA:3C', '5C:51:4F'],
    'huawei': ['00:1A:1E', '00:1E:10', '04:BD:70', '08:2E:5F', '0C:96:BF'],
    'xiaomi': ['00:0C:E7', '00:11:22', '04:CF:8C', '08:3E:8E', '0C:37:DC'],
    'asus': ['00:0C:6E', '00:18:F3', '00:22:15', '04:D4:C4', '08:62:66'],
    'tp_link': ['00:0C:43', '00:14:78', '00:19:E0', '04:16:BD', '08:10:74'],
    'netgear': ['00:04:5A', '00:09:5B', '00:1B:2F', '04:8E:91', '08:36:C9'],
    'cisco': ['00:0D:28', '00:0F:23', '00:13:7F', '04:5A:9E', '08:6D:41'],
    'intel': ['00:0C:F1', '00:13:02', '00:15:00', '04:7C:16', '08:11:96'],
    'broadcom': ['00:10:18', '00:14:BF', '00:1A:6B', '04:0F:6E', '08:2E:5F']
}

# ============= PASSWORD DATABASE =============
PASSWORDS = [
    None, "", "password", "12345678", "1234567890", "qwerty123", "admin123",
    "welcome123", "password123", "passw0rd", "letmein123", "123456789a"
]

# ============= STATISTICS CLASS =============
class SpamStats:
    def __init__(self):
        self.networks_created = 0
        self.networks_deleted = 0
        self.failures = 0
        self.start_time = time.time()
        self.history = deque(maxlen=100)
        self.current_networks = []
        
    def add_network(self, ssid):
        self.networks_created += 1
        self.current_networks.append(ssid)
        self.history.append(('create', ssid, time.time()))
        
    def remove_network(self, ssid):
        self.networks_deleted += 1
        if ssid in self.current_networks:
            self.current_networks.remove(ssid)
        self.history.append(('delete', ssid, time.time()))
        
    def add_failure(self):
        self.failures += 1
        
    def get_speed(self):
        elapsed = time.time() - self.start_time
        return self.networks_created / elapsed if elapsed > 0 else 0
        
    def get_stats(self):
        elapsed = time.time() - self.start_time
        return {
            'created': self.networks_created,
            'deleted': self.networks_deleted,
            'active': len(self.current_networks),
            'failures': self.failures,
            'elapsed': elapsed,
            'speed': self.get_speed()
        }

# ============= WIFI SPAMMER CORE =============
class WiFiSpammerSimple:
    def __init__(self):
        self.running = False
        self.networks = {}
        self.stats = SpamStats()
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.active_threads = []
        self.interval = 5  # seconds between network creation
        self.max_networks = 20  # max concurrent networks
        self.auto_rotate = True
        self.rotation_time = 30  # seconds before rotating networks
        self.use_mac_spoof = True
        self.use_passwords = True
        
    def clear_screen(self):
        os.system('cls')
        
    def random_ssid(self, category=None):
        """Generate random SSID with variations"""
        if category and category in SSID_TEMPLATES:
            templates = SSID_TEMPLATES[category]
        else:
            # Merge all categories
            all_templates = []
            for cat in SSID_TEMPLATES:
                all_templates.extend(SSID_TEMPLATES[cat])
            templates = all_templates
            
        base = random.choice(templates)
        suffix = random.choice(SSID_SUFFIXES)
        num = random.randint(1, 999)
        
        # Random variations
        variants = [
            base,
            f"{base}{suffix}",
            f"{base}_{num}",
            f"{base}{suffix}_{num}",
            f"{base}_{num}{suffix}",
            f"{base}_{random.choice(['Home', 'Office', 'Store', 'Cafe', 'Lounge'])}",
            f"{base}_{random.choice(['1', '2', '3', '4', '5'])}G",
            f"{base}_{random.choice(['A', 'B', 'C', 'D', 'E'])}",
        ]
        
        return random.choice(variants)
        
    def random_mac(self, brand=None):
        """Generate random MAC address with optional brand prefix"""
        if brand and brand in MAC_PREFIXES:
            prefix = random.choice(MAC_PREFIXES[brand])
        else:
            all_prefixes = []
            for brand_prefixes in MAC_PREFIXES.values():
                all_prefixes.extend(brand_prefixes)
            prefix = random.choice(all_prefixes)
            
        suffix = ':'.join(f'{random.randint(0x00, 0xff):02x}' for _ in range(3))
        return f"{prefix}:{suffix}"
        
    def random_password(self):
        """Generate random password"""
        if not self.use_passwords or random.random() > 0.7:
            return None
            
        passwords = [
            f"password{random.randint(100, 999)}",
            f"pass{random.randint(1000, 9999)}",
            f"wifi{random.randint(100, 999)}",
            f"free{random.randint(100, 999)}",
            f"guest{random.randint(100, 999)}",
            f"{random.choice(['admin', 'user', 'test'])}{random.randint(100, 999)}",
            f"{random.choice(['123', 'abc', 'qwe'])}{random.randint(100, 999)}",
            f"welcome{random.randint(100, 999)}",
            f"connect{random.randint(100, 999)}",
            f"internet{random.randint(100, 999)}"
        ]
        return random.choice(passwords)
        
    def create_network(self, ssid, password=None):
        """Create a hosted network in Windows"""
        try:
            # Set SSID
            if password:
                cmd = f'netsh wlan set hostednetwork mode=allow ssid="{ssid}" key="{password}"'
            else:
                cmd = f'netsh wlan set hostednetwork mode=allow ssid="{ssid}"'
                
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                return False, result.stderr
                
            # Start network
            result = subprocess.run('netsh wlan start hostednetwork', shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 or "already started" in result.stdout:
                return True, "Success"
            else:
                return False, result.stderr
                
        except Exception as e:
            return False, str(e)
            
    def delete_network(self):
        """Stop and delete all hosted networks"""
        try:
            subprocess.run('netsh wlan stop hostednetwork', shell=True, capture_output=True)
            subprocess.run('netsh wlan set hostednetwork mode=disallow', shell=True, capture_output=True)
            return True
        except:
            return False
            
    def spoof_mac(self, interface, mac):
        """Spoof MAC address (requires registry editing)"""
        try:
            # Find interface GUID
            result = subprocess.run('netsh wlan show interfaces', shell=True, capture_output=True, text=True)
            
            # This is simplified - full implementation would require registry editing
            # Windows 7-11 have different methods
            return True
        except:
            return False
            
    def spam_worker(self):
        """Worker thread for creating networks"""
        while self.running:
            try:
                # Check if we've reached max networks
                if len(self.stats.current_networks) >= self.max_networks:
                    time.sleep(1)
                    continue
                    
                # Generate SSID
                ssid = self.random_ssid()
                password = self.random_password() if self.use_passwords else None
                
                # Create network
                success, msg = self.create_network(ssid, password)
                
                if success:
                    with self.lock:
                        self.networks[ssid] = {
                            'ssid': ssid,
                            'password': password,
                            'created': time.time(),
                            'mac': self.random_mac()
                        }
                        self.stats.add_network(ssid)
                        
                    print(f"{Colors.GREEN}[+] Created: {ssid} {Colors.DIM}({password or 'open'}){Colors.RESET}")
                else:
                    self.stats.add_failure()
                    print(f"{Colors.RED}[-] Failed: {ssid} - {msg}{Colors.RESET}")
                    
                # Wait before next creation
                time.sleep(self.interval)
                
            except Exception as e:
                print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")
                time.sleep(1)
                
    def rotation_worker(self):
        """Worker thread for rotating networks"""
        while self.running and self.auto_rotate:
            time.sleep(self.rotation_time)
            
            if len(self.stats.current_networks) > 0:
                # Remove oldest networks
                to_remove = list(self.networks.keys())[:len(self.networks)//2]
                
                for ssid in to_remove:
                    self.delete_network()
                    with self.lock:
                        if ssid in self.networks:
                            del self.networks[ssid]
                            self.stats.remove_network(ssid)
                    print(f"{Colors.YELLOW}[~] Rotated: {ssid}{Colors.RESET}")
                    
    def start_spam(self, interval=5, max_networks=20, auto_rotate=True, rotation_time=30):
        """Start spamming WiFi networks"""
        self.interval = interval
        self.max_networks = max_networks
        self.auto_rotate = auto_rotate
        self.rotation_time = rotation_time
        self.running = True
        
        # Clear existing networks
        self.delete_network()
        
        # Start worker threads
        for i in range(5):  # 5 concurrent creators
            t = threading.Thread(target=self.spam_worker)
            t.daemon = True
            t.start()
            self.active_threads.append(t)
            
        if auto_rotate:
            t = threading.Thread(target=self.rotation_worker)
            t.daemon = True
            t.start()
            self.active_threads.append(t)
            
        print(f"{Colors.GREEN}[+] Spamming started!{Colors.RESET}")
        print(f"    Interval: {interval}s | Max networks: {max_networks}")
        print(f"    Auto-rotate: {auto_rotate} | Rotation: {rotation_time}s")
        print(f"\n{Colors.YELLOW}Press Ctrl+C to stop...{Colors.RESET}\n")
        
        # Stats printer
        try:
            while self.running:
                time.sleep(1)
                stats = self.stats.get_stats()
                print(f"\r{Colors.CYAN}Active: {stats['active']:3} | Created: {stats['created']:4} | Speed: {stats['speed']:.1f}/s | Fail: {stats['failures']}{Colors.RESET}", end="")
        except KeyboardInterrupt:
            self.stop_spam()
            
    def stop_spam(self):
        """Stop spamming and cleanup"""
        self.running = False
        print(f"\n\n{Colors.YELLOW}[!] Stopping spam...{Colors.RESET}")
        
        # Delete all networks
        self.delete_network()
        
        # Clear stats
        with self.lock:
            self.networks.clear()
            
        print(f"{Colors.GREEN}[+] Cleanup complete{Colors.RESET}")
        
    def print_menu(self):
        """Print main menu"""
        self.clear_screen()
        
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔════════════════════════════════╗
║SIMPLE WIFI SPAMMER v1.0               ║
║Author: lavashgovadina3         ║
║Platform: Windows 7/8/8.1/10/11 ║
╚════════════════════════════════╝
{Colors.RESET}
"""
        print(banner)
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}SSID CATEGORIES:{Colors.RESET}")
        categories = list(SSID_TEMPLATES.keys())
        for i, cat in enumerate(categories[:12]):
            print(f"  {Colors.GREEN}{i+1:2}.{Colors.RESET} {cat.capitalize():15} ({len(SSID_TEMPLATES[cat])} templates)")
            
        print(f"\n{Colors.CYAN}{Colors.BOLD}STATISTICS:{Colors.RESET}")
        stats = self.stats.get_stats()
        print(f"  Networks Created: {stats['created']}")
        print(f"  Currently Active: {stats['active']}")
        print(f"  Failures: {stats['failures']}")
        
        print(f"\n{Colors.YELLOW}{Colors.BOLD}SETTINGS:{Colors.RESET}")
        print(f"  Interval: {self.interval}s")
        print(f"  Max Networks: {self.max_networks}")
        print(f"  Auto-Rotate: {self.auto_rotate}")
        print(f"  Rotation Time: {self.rotation_time}s")
        print(f"  Use Passwords: {self.use_passwords}")
        
    def settings_menu(self):
        """Settings configuration menu"""
        self.clear_screen()
        print(f"\n{Colors.CYAN}{Colors.BOLD}SETTINGS MENU{Colors.RESET}")
        print(f"  1. Interval between networks [{self.interval}s]")
        print(f"  2. Max concurrent networks [{self.max_networks}]")
        print(f"  3. Auto-rotate [{self.auto_rotate}]")
        print(f"  4. Rotation time [{self.rotation_time}s]")
        print(f"  5. Use passwords [{self.use_passwords}]")
        print(f"  6. Back to main menu")
        
        choice = input(f"\n{Colors.YELLOW}Select: {Colors.RESET}").strip()
        
        if choice == '1':
            val = input(f"Interval (1-60): ")
            if val.isdigit():
                self.interval = min(60, max(1, int(val)))
        elif choice == '2':
            val = input(f"Max networks (1-50): ")
            if val.isdigit():
                self.max_networks = min(50, max(1, int(val)))
        elif choice == '3':
            self.auto_rotate = not self.auto_rotate
        elif choice == '4':
            val = input(f"Rotation time (5-300): ")
            if val.isdigit():
                self.rotation_time = min(300, max(5, int(val)))
        elif choice == '5':
            self.use_passwords = not self.use_passwords
            
    def ssid_category_menu(self):
        """SSID category selection"""
        self.clear_screen()
        print(f"\n{Colors.CYAN}{Colors.BOLD}SSID CATEGORIES{Colors.RESET}")
        
        categories = list(SSID_TEMPLATES.keys())
        for i, cat in enumerate(categories):
            print(f"  {Colors.GREEN}{i+1:2}.{Colors.RESET} {cat.capitalize():15} ({len(SSID_TEMPLATES[cat])} templates)")
        print(f"  {Colors.GREEN}99.{Colors.RESET} ALL CATEGORIES")
        print(f"  {Colors.GREEN}0.{Colors.RESET} Back")
        
        choice = input(f"\n{Colors.YELLOW}Select category: {Colors.RESET}").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(categories):
                return categories[idx]
            elif choice == '99':
                return 'all'
        return None
        
    def preview_ssids(self, category=None, count=20):
        """Preview SSIDs that will be generated"""
        self.clear_screen()
        print(f"\n{Colors.CYAN}{Colors.BOLD}SSID PREVIEW{Colors.RESET}")
        print(f"Category: {category or 'all'}\n")
        
        for i in range(count):
            ssid = self.random_ssid(category)
            print(f"  {Colors.GREEN}{i+1:2}.{Colors.RESET} {ssid}")
            
        input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
        
    def run(self):
        """Main application loop"""
        while True:
            self.print_menu()
            
            print(f"\n{Colors.YELLOW}{Colors.BOLD}MAIN MENU{Colors.RESET}")
            print(f"  {Colors.GREEN}1.{Colors.RESET} Start Spamming")
            print(f"  {Colors.GREEN}2.{Colors.RESET} Select SSID Category")
            print(f"  {Colors.GREEN}3.{Colors.RESET} Preview SSIDs")
            print(f"  {Colors.GREEN}4.{Colors.RESET} Settings")
            print(f"  {Colors.GREEN}5.{Colors.RESET} Clear All Networks")
            print(f"  {Colors.GREEN}6.{Colors.RESET} Show Statistics")
            print(f"  {Colors.RED}7.{Colors.RESET} Exit")
            
            choice = input(f"\n{Colors.YELLOW}Select: {Colors.RESET}").strip()
            
            if choice == '1':
                # Start spamming
                print(f"\n{Colors.YELLOW}Starting spam...{Colors.RESET}")
                self.start_spam(
                    interval=self.interval,
                    max_networks=self.max_networks,
                    auto_rotate=self.auto_rotate,
                    rotation_time=self.rotation_time
                )
                self.stop_spam()
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '2':
                category = self.ssid_category_menu()
                if category:
                    print(f"\n{Colors.GREEN}Selected category: {category}{Colors.RESET}")
                    # Store selected category for later use
                    # In full version, you'd modify random_ssid to use this category
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '3':
                self.preview_ssids(count=30)
                
            elif choice == '4':
                self.settings_menu()
                
            elif choice == '5':
                print(f"\n{Colors.YELLOW}Clearing all networks...{Colors.RESET}")
                self.delete_network()
                with self.lock:
                    self.networks.clear()
                    self.stats.current_networks.clear()
                print(f"{Colors.GREEN}Done!{Colors.RESET}")
                time.sleep(1)
                
            elif choice == '6':
                self.clear_screen()
                stats = self.stats.get_stats()
                print(f"\n{Colors.CYAN}{Colors.BOLD}STATISTICS{Colors.RESET}")
                print(f"  Networks Created: {stats['created']}")
                print(f"  Networks Deleted: {stats['deleted']}")
                print(f"  Currently Active: {stats['active']}")
                print(f"  Failures: {stats['failures']}")
                print(f"  Elapsed Time: {stats['elapsed']:.1f}s")
                print(f"  Creation Speed: {stats['speed']:.2f} networks/s")
                
                if self.stats.history:
                    print(f"\n{Colors.YELLOW}Recent Activity:{Colors.RESET}")
                    for action, ssid, ts in list(self.stats.history)[-10:]:
                        icon = f"{Colors.GREEN}+{Colors.RESET}" if action == 'create' else f"{Colors.RED}-{Colors.RESET}"
                        print(f"  {icon} {ssid[:40]}")
                        
                input(f"\n{Colors.WHITE}Press Enter to continue...{Colors.RESET}")
                
            elif choice == '7':
                print(f"\n{Colors.GREEN}Cleaning up...{Colors.RESET}")
                self.delete_network()
                print(f"{Colors.GREEN}Exiting...{Colors.RESET}")
                sys.exit(0)
                
# ============= ENTRY POINT =============
if __name__ == "__main__":
    try:
        # Set console
        if os.name == 'nt':
            os.system('color')
            
        # Enable ANSI if possible
        try:
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        except:
            pass
            
        # Run app
        app = WiFiSpammerSimple()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        input("Press Enter to exit...")