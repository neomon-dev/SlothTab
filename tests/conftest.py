import os
import sys

# Add project root and parent directory to sys.path so both
# `import backend...` and `import slothtab.backend...` resolve.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.dirname(PROJECT_ROOT)

for path in [PROJECT_ROOT, PARENT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)
