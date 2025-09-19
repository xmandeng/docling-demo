# Docling Document Loading and Parsing Pipeline Examples
# Complete demonstration of pipeline capabilities for table extraction

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# Global document path - the only document we'll use
DOCUMENT_PATH = "documents/BHE_991.pdf"
DOCUMENT_PATH = "documents/TMUS_Q225_992.pdf"
DOCUMENT_PATH = "documents/TMUS_992_Q423.pdf"


# Example 1: Basic Document Loading
def basic_document_loading():
    """Basic document conversion with default settings"""

    # Initialize converter with default configuration
    converter = DocumentConverter()

    # Convert PDF to intermediate document representation
    result = converter.convert(DOCUMENT_PATH)

    # Access the intermediate document object
    document = result.document

    print(f"Document loaded with {len(document.pages)} pages")
    print(f"Total elements found: {len(document.body.children)}")

    return document


# Example 2: Configurable Backend Selection
def configurable_backend_example():
    """Demonstrates backend selection with enhanced table detection"""

    # Configure pipeline options for better table detection
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True
    pipeline_options.do_ocr = True  # Enable OCR if needed

    # Initialize converter with specific options
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # Convert with enhanced table extraction
    result = converter.convert(DOCUMENT_PATH)
    document = result.document

    print(f"OCR enabled: {pipeline_options.do_ocr}")
    print(f"Table extraction: {pipeline_options.do_table_structure}")

    return document


# Example 3: Advanced Pipeline Configuration
def advanced_pipeline_configuration():
    """Shows advanced pipeline configuration options"""

    # Create detailed pipeline options
    pipeline_options = PdfPipelineOptions()

    # Table-specific configurations
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True

    # OCR configurations
    pipeline_options.do_ocr = True
    # OCR options are automatically configured with defaults (EasyOCR)

    # Layout analysis options
    pipeline_options.images_scale = 2.0  # Higher resolution for better detection

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(DOCUMENT_PATH)
    document = result.document

    # Inspect pipeline results
    print("Pipeline Configuration:")
    print(f"  Table extraction: {pipeline_options.do_table_structure}")
    print(f"  OCR enabled: {pipeline_options.do_ocr}")
    print(f"  Image scale: {pipeline_options.images_scale}")

    return document, result


# Example 4: Consistent Pipeline Processing
def consistent_pipeline_example():
    """Demonstrate consistent pipeline processing"""

    # Configure pipeline once for consistency
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    try:
        print(f"Processing: {DOCUMENT_PATH}")
        result = converter.convert(DOCUMENT_PATH)
        document = result.document

        # Store document with metadata
        doc_info = {
            "path": DOCUMENT_PATH,
            "document": document,
            "page_count": len(document.pages),
            "table_count": len(document.tables),
            "status": result.status,
        }

        print(
            f"  Completed: {doc_info['page_count']} pages, {doc_info['table_count']} tables"
        )
        return doc_info

    except Exception as e:
        print(f"  Error processing {DOCUMENT_PATH}: {e}")
        return None


# Example 5: Examining Document Structure
def explore_document_structure(document):
    """Explore the structure of the intermediate document object"""

    print("=== Document Structure Analysis ===")

    # Basic document properties
    print(f"Document type: {type(document)}")
    print(f"Number of pages: {len(document.pages)}")

    # Explore document metadata
    if hasattr(document, "metadata"):
        print(f"Document metadata: {document.metadata}")

    # Examine document body structure
    body = document.body
    print(f"Document body contains {len(body.children)} top-level elements")

    # Check the correct structure - tables, texts, etc.
    print(f"Tables found: {len(document.tables)}")
    print(f"Texts found: {len(document.texts)}")
    print(f"Pictures found: {len(document.pictures)}")

    # Count different element types
    element_types = {}
    for element in body.children:
        element_type = type(element).__name__
        element_types[element_type] = element_types.get(element_type, 0) + 1

    print("Element type distribution:")
    for elem_type, count in element_types.items():
        print(f"  {elem_type}: {count}")

    return element_types


# Example 6: Page-by-Page Analysis
def page_by_page_analysis(document):
    """Analyze document structure on a per-page basis"""

    print("\n=== Page-by-Page Analysis ===\n")

    for page_num in range(1, len(document.pages) + 1):
        print(f"Page {page_num} - ", end="")

        # Count tables on this page (page_no is already 1-based)
        page_tables = [
            table
            for table in document.tables
            if table.prov and len(table.prov) > 0 and table.prov[0].page_no == page_num
        ]

        # Count text elements on this page (page_no is already 1-based)
        page_texts = [
            text
            for text in document.texts
            if text.prov and len(text.prov) > 0 and text.prov[0].page_no == page_num
        ]

        print(f"Tables: {len(page_tables)}, Text elements: {len(page_texts)}")


# Example 7: Basic Table Access
def show_table_basics(document):
    """Demonstrate basic table access from pipeline output"""

    print("\n=== Table Access Demo ===\n")

    md_list = []

    for i, table in enumerate(document.tables, 1):
        if table.prov and len(table.prov) > 0:
            page_no = table.prov[0].page_no  # Already 1-based, no conversion needed
            print(f"Table {i}: Page {page_no}: ", end="")

            # Show table can be converted to DataFrame
            try:
                df = table.export_to_dataframe()
                md_list.append(table.export_to_markdown(doc=document))
                print(f"Shape: {df.shape}, First cell: '{df.iloc[0, 0]}'")
            except Exception as e:
                print(f"  Export error: {e}")

    for num, md in enumerate(md_list, 1):
        header = f"= Table {num} ="
        print()
        print("-" * len(header))
        print(f"{header}")
        print("-" * len(header), f"\n\n{md}")


# Example usage and testing
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print(f"Processing document: {DOCUMENT_PATH}")
    print("=" * 50)

    # Example 1: Basic pipeline usage
    try:
        doc = basic_document_loading()
        element_types = explore_document_structure(doc)
        page_by_page_analysis(doc)
        show_table_basics(doc)

    except Exception as e:
        print(f"Basic pipeline error: {e}")

    # Example 2: Backend configuration
    try:
        print("\n" + "=" * 30)
        print("Backend Configuration:")
        doc = configurable_backend_example()

    except Exception as e:
        print(f"Backend config error: {e}")

    # Example 3: Advanced configuration
    try:
        print("\n" + "=" * 30)
        print("Advanced Configuration:")
        doc, result = advanced_pipeline_configuration()
        print(f"Completed: {len(doc.pages)} pages, {len(doc.tables)} tables")

    except Exception as e:
        print(f"Advanced config error: {e}")

    # Example 4: Consistent processing
    try:
        print("\n" + "=" * 30)
        print("Consistent Processing:")
        doc_info = consistent_pipeline_example()

    except Exception as e:
        print(f"Consistent processing error: {e}")
