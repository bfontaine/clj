import re

import clj


def test_version():
    assert re.match(r"^\d+\.\d+\.\d+", clj.__version__)
