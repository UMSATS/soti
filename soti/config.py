"""Application-level Configuration"""

APP_VERSION = "2.0"

# Define the colour palette for the UI here.
# For valid keywords, see: <https://urwid.org/manual/displayattributes.html>
PALETTE = [
    ('soti banner', 'default', 'default'),
    ('soti title', 'yellow,italics', 'default'),
    ('title', 'default', 'default'),
    ('button', 'white', 'default'),
    ('button focus', 'white,bold', 'dark blue'),
    ('accent', 'yellow,bold', 'default'),
    ('accent 2', 'light magenta,italics', 'default'),
    ('table header', 'white', 'dark blue'),
    ('table cell', 'default', 'default')
]

# Define icons here.
ICONS = {
    'PORT_DEFAULT': "🔌",
    'PORT_NONE': "❌",
}
