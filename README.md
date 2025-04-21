# ScreenShoot-Tool

Smart screenshot utility for Windows.

Capture the active window with a single hotkey press (F9), automatically detect the application and content (website domain or window title), and organize screenshots into a clean folder hierarchy.

## Features

- **Global Hotkey**: Press **F9** to instantly capture the active window.
- **Application Detection**: Identifies processes such as `firefox.exe`, `chrome.exe`, games, and other applications.
- **Content Parsing**:
  - **Browser Domains**: Extracts domain names from Firefox window titles or via Chrome DevTools Protocol (optional).
  - **Fallback**: Uses the last segment of the window title when no domain is found.
- **Auto-Organization**: Saves screenshots under:

  ```
  ~/Videos/Screenshots/
  ├─ Firefox/
  │   └─ example.com/
  ├─ Chrome/
  │   └─ youtube.com/
  └─ GameName/
      └─ Level1/
  ```

- **Timestamped Filenames**: `YYYY-MM-DD_HH-MM-SS WindowTitle.png` format for easy sorting.
- **Configurable**: Change the base save path or logging level by editing constants in the script.

## Requirements

- **Operating System**: Windows 10 or later
- **Python**: 3.8 or newer
- **Python Packages**:
  - `pyautogui`
  - `keyboard`
  - `pywin32`
  - `pychrome` *(optional, for Chrome URL fetching)*

## Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. *(Optional)* To enable Chrome URL extraction, start Chrome/Chromium with:
   ```bash
   chrome.exe --remote-debugging-port=9222
   ```

## Usage

1. **Run the tool**:
   ```bash
   python ScreenShoot_Tool.py
   ```
2. **Focus** the window you want to capture.
3. **Press F9** to capture the screenshot.
4. **Locate** saved images in `~/Videos/Screenshots/<App>/<Content>/`.

## Configuration

- **ROOT_DIR**: Modify the `ROOT_DIR` constant at the top of `ScreenShoot_Tool.py` to change the base save path.
- **Logging**: Adjust the logging format or level in the `setup_logging()` function.





