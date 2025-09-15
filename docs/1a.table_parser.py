# Debug script to understand Docling document structure

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# Global document path
DOCUMENT_PATH = "documents/BHE_991.pdf"


def debug_document_structure():
    """Debug the actual document structure to understand element organization"""

    # Configure pipeline for table extraction
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(DOCUMENT_PATH)
    document = result.document

    print("=== Document Structure Debug ===")
    print(f"Document type: {type(document)}")
    print(f"Number of pages: {len(document.pages)}")
    print(f"Total body children: {len(document.body.children)}")

    # Check the correct structure - tables, texts, etc.
    print(f"Tables found: {len(document.tables)}")
    print(f"Texts found: {len(document.texts)}")
    print(f"Pictures found: {len(document.pictures)}")

    # Examine table elements specifically
    print("\n=== Table Elements ===")
    for i, table in enumerate(document.tables):
        print(f"\nTable {i + 1}:")
        print(f"  Type: {type(table).__name__}")
        print(f"  Has prov: {hasattr(table, 'prov')}")

        if hasattr(table, "prov") and table.prov:
            prov = table.prov[0]
            print(f"  Page number: {prov.page_no + 1}")  # +1 for human readable
            if hasattr(prov, "bbox"):
                print(f"  Bounding box: {prov.bbox}")

        # Check if table has data
        if hasattr(table, "data"):
            print(f"  Has table data: {table.data is not None}")
            if table.data:
                print(f"  Rows: {table.data.num_rows}, Cols: {table.data.num_cols}")

        # Try to get a preview of table content
        try:
            df = table.export_to_dataframe()
            print(f"  DataFrame shape: {df.shape}")
            print(f"  First few cells: {df.iloc[0, 0] if not df.empty else 'Empty'}")
        except Exception as e:
            print(f"  Error exporting to DataFrame: {e}")

    # Check text elements for context around tables
    print("\n=== Text Elements (first 5) ===")
    for i, text in enumerate(document.texts[:5]):
        print(f"\nText {i + 1}:")
        print(f"  Type: {type(text).__name__}")
        if hasattr(text, "prov") and text.prov:
            prov = text.prov[0]
            print(f"  Page number: {prov.page_no + 1}")
        if hasattr(text, "text"):
            preview = text.text[:100] if text.text else "No text"
            print(f"  Text preview: {preview}...")

    return document


if __name__ == "__main__":
    doc = debug_document_structure()
