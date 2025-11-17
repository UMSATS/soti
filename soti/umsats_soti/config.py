"""Application-level Configuration"""

from pathlib import Path

APP_VERSION = "2.0"

ROOT_DIR = Path(__file__).resolve().parent

SAVE_DATA_DIR = ROOT_DIR / "save-data"

SESSIONS_DIR = SAVE_DATA_DIR / "sessions"

RES_DIR = ROOT_DIR / "res"

# Used to name session files with datetime.strftime()
SESSION_FILE_FORMAT = "%Y-%m-%d_%H%M%S"

# Define the colour palette for the UI here.
# For valid keywords, see: <https://urwid.org/manual/displayattributes.html>
PALETTE = [
    ('soti banner', 'default', 'default'),
    ('soti title', 'yellow,italics', 'default'),
    ('title', 'white,bold', 'default'),
    ('button', 'white', 'default'),
    ('button focus', 'white,bold', 'dark blue'),
    ('accent', 'yellow,bold', 'default'),
    ('accent 2', 'light magenta,italics', 'default'),
    ('cli prompt', 'default', 'dark gray'),
    ('cli prompt prefix', 'standout', 'default'),
    ('table header', 'white', 'dark blue'),
    ('table cell', 'default', 'default')
]

# Define icons here.
ICONS = {
    'PORT_DEFAULT': "🔌",
    'PORT_NONE': "❌",
}