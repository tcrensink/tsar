from tsar.lib.record_defs.wiki_record import WikiRecord
from tsar.lib.collection import Collection

DEFAULT_COLL = "default"


if Collection.db_meta.empty:

    Collection.new(collection_name="default", RecordDef=WikiRecord)
