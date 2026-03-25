import tempfile
from pathlib import Path


def make_temp_dir(prefix="uvio_"):
    return Path(tempfile.mkdtemp(prefix=prefix))
