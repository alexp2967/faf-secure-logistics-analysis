from pathlib import Path
import zipfile
import logging

logging.basicConfig(
    filename = "logs/pipeline.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

#Path to csv file in laptop
faf_zip_path_2024 = Path("")

#
extract_path = Path("data/raw/extracted")

extract_path.mkdir(parents=True, exist_ok = True)

if not faf_zip_path_2024.exists():
    logging.error(f"ZIP file not found: {faf_zip_path_2024}")
    raise FileNotFoundError(f"ZIP file not found: {faf_zip_path_2024}")

with zipfile.ZipFile(faf_zip_path_2024, "r") as zip_ref:
    zip_ref.extractall(extract_path)

logging.info(f"Extracted {faf_zip_path_2024.name} to {extract_path}")

print(f"Extraction complete: {faf_zip_path_2024.name} -> {extract_path}")