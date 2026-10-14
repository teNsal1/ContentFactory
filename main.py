from pathlib import Path
import argparse
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"

def main():
    parser = argparse.ArgumentParser(description="ContentFactory")
    parser.add_argument("topic", help="Topic for the YouTube Short")
    args = parser.parse_args()

    job_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    job_dir = OUTPUT / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    job = {
        "topic": args.topic,
        "language": "English",
        "format": "9:16",
        "target_duration_seconds": 45,
        "status": "created",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    job_file = job_dir / "job.json"
    job_file.write_text(
        json.dumps(job, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("ContentFactory: job created")
    print(f"Topic: {args.topic}")
    print(f"Job folder: {job_dir}")
    print(f"Job file: {job_file}")

if __name__ == "__main__":
    main()
