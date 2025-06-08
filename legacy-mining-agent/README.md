"""
# Legacy Mining Agent

This project analyzes legacy mainframe programs (COBOL, JCL, SQL, flat files) and generates:
- Program summaries
- Variable metadata
- Call relationships
- Mermaid flow diagrams
- Word document reports

## Modes
- `main.py`: CLI version for automation
- `main.ipynb`: Colab notebook for step-by-step use

## Folder Structure
```
legacy-mining-agent/
├── main.py                 # CLI tool
├── main.ipynb              # Interactive notebook (Colab-compatible)
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
├── sample_data/            # Sample legacy project ZIPs
│   └── legacy_project.zip
├── src/                    # Modular code
│   ├── extractor.py        # Downloads and unzips legacy project
│   ├── analyzer.py         # Program parsing and analysis
│   ├── openrouter_client.py# API interaction with OpenRouter
│   └── doc_writer.py       # Word document generation
└── output/                 # Auto-generated .docx reports
```

## Usage (CLI)
```bash
python main.py https://your-url.com/sample.zip
```

## Usage (Colab)
- Open `main.ipynb` in Google Colab
- Paste your GitHub-hosted ZIP URL when prompted
- Run all cells to download, analyze, and generate docs

## Requirements
```bash
pip install -r requirements.txt
```
"""
