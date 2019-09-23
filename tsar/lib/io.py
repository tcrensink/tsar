"""file io utils
"""
import subprocess
from tsar import (
    config
)
from tsar.lib import (
    # search,
    # metadb,
    file_parser
)


def open_record(
    record_id,
    editor_path=config.EDITOR,
):
    """open file in editor, wait until file (process) is closed.
    """
    file_path = file_parser.to_Path(record_id)
    editor_cmd = '{} -w {}'.format(editor_path, str(file_path))
    subprocess.Popen(editor_cmd, shell=True).wait()
