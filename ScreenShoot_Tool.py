import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional

import keyboard
import pyautogui
from urllib.parse import urlparse
from win32gui import GetForegroundWindow, GetWindowText
from win32process import GetWindowThreadProcessId, GetModuleFileNameEx
import win32api
import win32con

# Optional for Chrome DevTools
try:
    import pychrome
    CHROME_DEBUGGING = True
    CHROME_DEBUGGING_URL = "http://127.0.0.1:9222"
except ImportError:
    CHROME_DEBUGGING = False

# Configuration
ROOT_DIR: Path = Path.home() / "Videos" / "Screenshots"
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"


def setup_logging() -> None:
    """Configure logging for the utility."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def get_process_name(pid: int) -> str:
    """Retrieve the executable name for a given process ID using Win32 APIs."""
    try:
        handle = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
            False,
            pid
        )
        exe_path = GetModuleFileNameEx(handle, 0)
        return Path(exe_path).name
    except Exception:
        return "Unknown"


def get_active_window_info() -> Tuple[str, str]:
    """Return the process name and window title of the active window."""
    hwnd = GetForegroundWindow()
    title = GetWindowText(hwnd)
    _, pid = GetWindowThreadProcessId(hwnd)
    proc_name = get_process_name(pid)
    return proc_name, title


def get_chrome_url() -> Optional[str]:
    """Fetch the URL of the active Chrome/Chromium tab via DevTools Protocol."""
    if not CHROME_DEBUGGING:
        return None
    try:
        browser = pychrome.Browser(url=CHROME_DEBUGGING_URL)
        tabs = browser.list_tab()
        active = next((t for t in tabs if t.get("active")), None)
        return active.get("url") if active else None
    except Exception:
        return None


def sanitize(name: str) -> str:
    """Sanitize a string for safe file or folder names."""
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def extract_domain(text: str) -> Optional[str]:
    """Extract a domain (e.g., example.com) from a string using regex."""
    matches = re.findall(r"\b([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b", text)
    return matches[-1] if matches else None


def take_screenshot() -> None:
    """Capture a screenshot of the active window and save it to a structured folder."""
    proc_name, win_title = get_active_window_info()
    proc_key = sanitize(proc_name)
    title_text = win_title or "Untitled"
    win_key = None

    # Browser-specific extraction
    proc_lower = proc_name.lower()
    if proc_lower.startswith(("chrome", "chromium")):
        url = get_chrome_url()
        win_key = urlparse(url).netloc if url else extract_domain(title_text)
    elif "firefox" in proc_lower:
        win_key = extract_domain(title_text)
    # Fallback: use last segment after ' - '
    if not win_key:
        parts = title_text.rsplit(" - ", 1)
        win_key = parts[-1]

    folder = ROOT_DIR / proc_key / sanitize(win_key)
    folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime(DATE_FORMAT)
    filename = f"{timestamp} {sanitize(title_text)}.png"
    path = folder / filename

    img = pyautogui.screenshot()
    img.save(path)
    rel_path = path.relative_to(ROOT_DIR.parent)
    logging.info("Screenshot saved: %s", rel_path)


def main() -> None:
    """Entry point: registers hotkey and waits for events."""
    setup_logging()
    logging.info("Listening for F9 key to capture screenshots...")
    keyboard.add_hotkey("F9", take_screenshot)
    keyboard.wait()


if __name__ == "__main__":
    main()
