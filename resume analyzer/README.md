# Resume Analyzer

A Python application for analyzing resumes in various formats (PDF, DOCX, TXT, RTF) and providing scores and recommendations for improvement.

## Features

- Parse resumes from multiple file formats (PDF, DOCX, TXT, RTF)
- Extract key information such as contact details, skills, experience, and education
- Score resumes based on content, format, and completeness
- Generate recommendations for resume improvement
- Export analysis results in HTML, JSON, or text format
- Simple graphical user interface for easy use

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode

To use the graphical user interface:

```bash
python -m resume_analyzer.ui.gui
```

### Command Line Mode

To analyze a single resume file:

```bash
python -m resume_analyzer.main analyze path/to/resume.pdf
```

To analyze all resumes in a directory:

```bash
python -m resume_analyzer.main analyze_dir path/to/directory
```

## Project Structure

```
resume_analyzer/
├── analyzers/         # Resume analysis modules
├── models/            # Data models
├── parsers/           # File format parsers
├── ui/                # User interface
└── utils/             # Utility functions
```

## Dependencies

- PyPDF2 - For parsing PDF files
- pdfminer.six - Alternative PDF parser
- python-docx - For parsing DOCX files
- striprtf - For parsing RTF files
- tkinter - For the graphical user interface
- nltk - For text processing and analysis

## License

MIT