# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a document conversion demo using the Docling library. The project converts PDF documents to Markdown format using IBM's Docling document AI library.

## Architecture

- **main.py**: Core conversion logic with `convert_document()` function
- **docs/**: Input directory containing PDF files to be processed
- **output/**: Generated Markdown files from PDF conversion
- **Dependencies**: Built on `docling>=2.45.0` for document processing

The main workflow:
1. `convert_document()` takes a PDF file path
2. Uses `DocumentConverter` from docling to process the PDF
3. Exports the result to Markdown format in the `output/` directory

## Development Commands

### Environment Setup
```bash
# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

### Running the Demo
```bash
# Run the main conversion script
python main.py

# Or run with uv
uv run python main.py
```

### Adding New Documents
Place PDF files in the `docs/` directory and update the `sources` list in `main.py` to include the new file paths.

## Project Structure

The codebase follows a simple flat structure:
- Single main module (`main.py`) handles all conversion logic
- Input/output directories separate source and generated content
- Uses uv for dependency management (pyproject.toml + uv.lock)