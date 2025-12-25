#!/usr/bin/env python3
"""Download and clean all recipe pages from Wayback Machine."""

import subprocess
import os
import time
from pathlib import Path

BASE_DIR = Path("/Users/joel/Documents/Side Projects/Code/lcookscraper")
ARCHIVES_DIR = BASE_DIR / "archives"
CLEAN_SCRIPT = BASE_DIR / "clean_html.py"

def download_and_clean(url_suffix, output_file, is_archives=True, retries=3):
    """Download a page from Wayback Machine and clean it."""
    url = f"https://web.archive.org/web/20051213034931/http://www.lemonscookbook.com/{url_suffix}"

    for attempt in range(retries):
        # Download with timeout
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "30", url],
            capture_output=True
        )

        if result.returncode != 0 or len(result.stdout) < 500:
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retry
                continue
            print(f"Failed to download {url_suffix} after {retries} attempts")
            return False

        # Clean
        args = ["python3", str(CLEAN_SCRIPT)]
        if is_archives:
            args.append("--archives")

        clean_result = subprocess.run(
            args,
            input=result.stdout,
            capture_output=True
        )

        if clean_result.returncode != 0:
            print(f"Failed to clean {url_suffix}: {clean_result.stderr.decode()}")
            return False

        # Write
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(clean_result.stdout)
        return True

    return False

def main():
    # Read recipe URLs
    with open(BASE_DIR / "recipe_urls.txt") as f:
        recipes = [line.strip() for line in f if line.strip()]

    print(f"Downloading {len(recipes)} recipes...")

    for i, url in enumerate(recipes, 1):
        filename = os.path.basename(url)
        output_path = ARCHIVES_DIR / filename

        # Check file size - redownload if < 1000 bytes
        if output_path.exists() and output_path.stat().st_size >= 1000:
            print(f"[{i}/{len(recipes)}] Skipped {filename} (already good)")
            continue

        if download_and_clean(url, output_path, is_archives=True):
            size = output_path.stat().st_size
            print(f"[{i}/{len(recipes)}] Downloaded {filename} ({size} bytes)")
        else:
            print(f"[{i}/{len(recipes)}] FAILED {filename}")

        # Longer delay between requests to avoid rate limiting
        time.sleep(2)

    print("Done!")

if __name__ == "__main__":
    main()
