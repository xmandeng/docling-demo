import argparse
from pathlib import Path

from docling.document_converter import DocumentConverter


def convert_document(source: str | Path):
    if isinstance(source, str):
        source = Path(source)

    print(f"Converting: {source.as_posix()}")
    
    converter = DocumentConverter()
    result = converter.convert(source.as_posix())
    
    with open("output/" + source.name.replace(".pdf", ".md"), "w", encoding="utf-8") as f:
        f.write(result.document.export_to_markdown())
        
    print(f"Converted: {source.as_posix()}")


def cli_handler():
    parser = argparse.ArgumentParser(description="Convert PDF documents to Markdown using Docling")
    parser.add_argument("document", help="Path to the PDF document to convert")
    
    args = parser.parse_args()
    convert_document(args.document)


if __name__ == "__main__":
    cli_handler()
