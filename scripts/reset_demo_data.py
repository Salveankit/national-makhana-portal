from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.data import reset_demo_dataset


if __name__ == "__main__":
    reset_demo_dataset()
    print("Demo dataset reset complete.")
