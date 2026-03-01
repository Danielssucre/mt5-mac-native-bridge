# MT5 Mac Native Bridge 🍏📈

Native Python injection method for MetaTrader 5 on macOS (Apple Silicon). Bypasses critical Wine IPC & Docker connection freezes on `mt5.initialize()`. By hijacking MetaEditor with an Embedded Python & `.pth` auto-launch, it runs a headless RPyC server inside the MT5 terminal memory, allowing ultra-fast algorithm trading without Docker.

---

## 🆚 Old Method (Docker) vs. New Method (Native Injection)

**Old Method (`siliconmt5` with Docker/Colima):**
- **Architecture:** Required a full Linux VM running inside macOS (via Colima), which in turn used Wine to emulate Windows and run MetaTrader 5.
- **Connection:** The bot connected from the Mac to this isolated container using mapped network ports.
- **Drawbacks:** CPU-heavy. Extremely fragile to updates. Any slight change in Linux, Docker, or Wine 9.0+ caused the IPC (Inter-Process Communication) pipes to break, resulting in MetaTrader ignoring commands and freezing permanently.

**New Method (Native IDE Injection):**
- **Architecture:** Completely eliminates Docker. Uses the native MetaTrader 5 application already installed on your Mac (which uses lightweight CrossOver under the hood).
- **Connection:** An "invisible" Python engine lives inside the very memory of MetaTrader 5. It auto-executes and shares the exact same graphical session.
- **Advantages:** Much faster, lower RAM/Battery consumption. By not crossing network or heavy VM boundaries, API commands (like `mt5.initialize()`) execute natively, making the bot immune to network disconnects or IPC "Timeouts" that broke the old method.

---

## 🚀 Easy Setup Guide

To bypass the CrossOver graphical memory isolation wall, the solution is to **inject a pure Python server from inside MetaTrader 5**, using an official software button so that it inherits all permissions as if it were part of the program itself.

### Step 1: Download Lightweight "Embeddable" Python
Do not use installers or `brew`. Download the official, ultra-light Windows embedded version: **[Python 3.9 Embeddable](https://www.python.org/ftp/python/3.9.13/python-3.9.13-embed-amd64.zip)**.

Extract its contents directly inside the folder where MetaTrader keeps its binaries on your Mac's hard drive:
```bash
# Typical destination on Mac (Your MT5 Wine Prefix)
~/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/
```

### Step 2: Hijack MetaEditor64
The MT5 app has a button called **"IDE" (or press F4)** which traditionally opens `metaeditor64.exe`. 
1. Rename the original `metaeditor64.exe` to `metaeditor64.exe.bak`.
2. Rename our new `python.exe` (from the Embeddable zip) to `metaeditor64.exe`.

By doing this, when clicking "IDE" in MetaTrader, **we run Python with graphics system admin privileges without Mac/Wine noticing.**

### Step 3: The Auto-Boot File (`.pth`)
Since Python Embeddable doesn't execute scripts by default unless passed as arguments, we leverage Windows Python `_pth` files.
Create a file named `metaeditor64._pth` in that same folder, containing the following:

```text
python39.zip
.
Lib\site-packages

# Auto import on boot
import site
import rpyc_start
```
*(Check the `metaeditor64._pth` file example in this repository).*
*Important Note:* Adding `Lib\site-packages` fixes the "module not found" error that would cause the IDE window to instantly close.

### Step 4: Add the Payload (`rpyc_start.py`)
Upload the `rpyc_start.py` file from this repository to the same folder. This script boots the invisible RPyC server on port **18812** and gets trapped in an infinite loop to keep Python alive. You will see a small, dark console window open in the background.

```python
import sys
from rpyc.utils.server import ThreadedServer
from rpyc.core.service import ClassicService

def run_server():
    print("Starting RPyC Classic Server on Port 18812...")
    config = {'allow_all_attrs': True, 'allow_public_attrs': True, 'sync_request_timeout': 60}
    server = ThreadedServer(ClassicService, port=18812, protocol_config=config)
    server.start()

run_server()
```

---

## 🛡️ Adapting your Trading Bot
Since the server is now native but the Python library crashes looking for the explicit `terminal64` process or encounters the authentication barrier (`Error -6`), your bot's connection script must be patched. 

When initializing via port from your Mac local terminal, you MUST pass your credentials instantly. 

**Critical Implementation Reference:**
```python
import MetaTrader5 as mt5

# Mac port-forwards the 18812 to 8001 or uses the exact same localhost
mt5 = MetaTrader5(port=18812) 

mt5.initialize(
    path='C:\\Program Files\\MetaTrader 5\\terminal64.exe', 
    portable=True, 
    login=12345678,        # YOUR LOGIN INT
    password="PASSWORD",   # YOUR PASSWORD STR
    server="Broker-Demo"   # YOUR BROKER SERVER STR
)

print(mt5.terminal_info())
```

## 🔄 Daily Usage
1. Open your Native MetaTrader 5 app on your Mac.
2. At the top toolbar, click the yellow **"IDE"** button (or press F4).
3. A small minimizable black window will appear. That is your active RPyC server! 
4. Run your python bot algorithms locally on your Mac. Enjoy the zero-latency experience.

---

*Found this useful? Star this repo! ⭐*
