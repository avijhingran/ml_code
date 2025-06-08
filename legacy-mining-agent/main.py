import sys
from src.extractor import extract_zip
from src.analyzer import analyze_all_files
from src.doc_writer import save_reports

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <ZIP_URL>")
        sys.exit(1)

    zip_url = sys.argv[1]
    extract_path = "legacy_project"
    extract_zip(zip_url, extract_path)

    analysis_results = analyze_all_files(extract_path)
    save_reports(analysis_results, "output")

    print("Analysis complete. Reports saved to /output")
