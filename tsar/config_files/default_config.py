from whoosh import fields
from collections import OrderedDict
# tsar configuration file:


# _______________ KEYPRESSES ______________
"""
Some keypress actions are defined here.
"""



# _______________ SCHEMA __________________
"""
# http://whoosh.readthedocs.io/en/latest/schema.html
the "schema" specifies the fields and indexing of the searchable data.  Defaults use "timestamp" as a unique identifier and tags to aid association/browse functionality (the other fields are rather obvious).  See whoosh documentation for FIELD_TYPE keyword and arg values.
"""

SCHEMA_FIELDS = OrderedDict({
    'timestamp': fields.DATETIME(unique=True, stored=True, sortable=True),
    'name': fields.TEXT(stored=True),
    'content': fields.TEXT(stored=True),
    'tags': fields.KEYWORD(scorable=True, stored=True)
    })

#required for updating documents
UNIQUE_FIELD = 'timestamp'

FIELD_TYPES = OrderedDict({k:type(v) for k, v in SCHEMA_FIELDS.items()})
EDITABLE_TYPES = {fields.TEXT, fields.KEYWORD}
FIELD_NAMES = list(SCHEMA_FIELDS.keys())


# _______________ SEARCH SCREEN __________________
"""
- default fields to be searched.  To search fields explicitly, use syntax `field_x: keyword_x`
- define operators of the query synatax.  Default for union, intersection, and fuzzy search: `AND`, `OR`, `searchterm~`
- specficy search defaults that are displayed in search syntax
"""
DEFAULT_SEARCH_FIELDS = FIELD_NAMES[:]
SEARCH_DISPLAY_FIELD = FIELD_NAMES[1]
SEARCH_RESULT_LIMIT = None


AND = '&'
OR = '|'
FUZZY = '~'

# _______________ COLOR OPTIONS __________________
"""
The color/text format is defined by the PALETTE variable.  Each tuple represents markup that is applied to various text.  See urwid documentation for more information.  

foreground color string values:
'default'
'black'
'dark red'
'dark green'
'brown'
'dark blue'
'dark magenta'
'dark cyan'
'light gray'
'dark gray'
'light red'
'light green'
'yellow'
'light blue'
'light magenta'
'light cyan'
'white'

background color string values:
'black'
'dark red'
'dark green'
'brown'
'dark blue'
'dark magenta'
'dark cyan'
'light gray'

styling
'bold'
'underline'
'standout'
'blink'
'italics'
'strikethrough'
"""


PALETTE = [
('prompt_attr', 'dark cyan', 'default', 'default'),
('unselected_attr', 'default', 'default'),
('selected_attr', 'standout', 'default', 'default'),
('highlighted_attr', 'standout', 'default', 'default'),
('preview_attr', 'dark cyan', 'default', 'default'),
('default', 'default', 'default')]

