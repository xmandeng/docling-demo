# Docling Element Iteration and Filtering Examples
# Demonstrates advanced techniques for finding and filtering document elements

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# Global document path
DOCUMENT_PATH = "documents/BHE_991.pdf"


def load_document():
    """Load document with table extraction enabled"""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(DOCUMENT_PATH)
    return result.document


# Example 1: Content-Based Filtering
def filter_by_content(document):
    """Filter elements based on their content patterns"""

    print("=== Content-Based Filtering ===")

    # Filter tables by content type
    financial_tables = []
    operational_tables = []

    for table in document.tables:
        try:
            df = table.export_to_dataframe()
            if not df.empty:
                # Check first row content for financial indicators
                first_row_text = " ".join(df.iloc[0].astype(str)).lower()

                if any(
                    keyword in first_row_text
                    for keyword in ["revenue", "income", "margin", "eps", "gaap"]
                ):
                    financial_tables.append(table)
                elif any(
                    keyword in first_row_text
                    for keyword in ["cash flow", "assets", "liabilities"]
                ):
                    financial_tables.append(table)
                else:
                    operational_tables.append(table)
        except Exception as e:
            print(f"Error analyzing table content: {e}")
            operational_tables.append(table)  # If can't analyze, assume operational

    print(f"Financial tables found: {len(financial_tables)}")
    print(f"Operational tables found: {len(operational_tables)}")

    # Filter text elements by content
    headings = [
        text
        for text in document.texts
        if hasattr(text, "text")
        and text.text
        and any(
            keyword in text.text.upper()
            for keyword in ["QUARTER", "RESULTS", "RELEASE"]
        )
    ]

    print(f"Document headings found: {len(headings)}")
    for heading in headings[:3]:  # Show first 3
        print(f"  - {heading.text[:50]}...")

    return financial_tables, operational_tables


# Example 2: Spatial Filtering
def filter_by_location(document):
    """Filter elements based on their spatial location"""

    print("\n=== Spatial Filtering ===")

    # Define regions (assuming standard letter-size page: 612x792 points)
    regions = {
        "top_half": lambda bbox: bbox.t > 396,  # Top half of page
        "bottom_half": lambda bbox: bbox.t <= 396,  # Bottom half
        "left_side": lambda bbox: bbox.l < 306,  # Left side
        "right_side": lambda bbox: bbox.l >= 306,  # Right side
    }

    for region_name, region_test in regions.items():
        print(f"\n{region_name.replace('_', ' ').title()}:")

        # Find tables in this region
        region_tables = [
            table
            for table in document.tables
            if table.prov and len(table.prov) > 0 and region_test(table.prov[0].bbox)
        ]

        # Find text elements in this region
        region_texts = [
            text
            for text in document.texts[:20]  # Limit to first 20 for brevity
            if text.prov and len(text.prov) > 0 and region_test(text.prov[0].bbox)
        ]

        print(f"  Tables: {len(region_tables)}")
        print(f"  Text elements: {len(region_texts)}")


# Example 3: Hierarchical Filtering
def explore_document_hierarchy(document):
    """Explore parent-child relationships in document structure"""

    print("\n=== Document Hierarchy ===")

    def explore_element(element, depth=0):
        """Recursively explore document structure"""
        indent = "  " * depth
        element_type = type(element).__name__

        # Get element info
        element_info = f"{indent}{element_type}"

        if hasattr(element, "text") and element.text:
            preview = element.text[:30].replace("\n", " ") if element.text else ""
            element_info += f": {preview}..."
        elif hasattr(element, "cref"):
            element_info += f" -> {element.cref}"

        print(element_info)

        # Explore children if they exist
        if hasattr(element, "children") and element.children:
            for child in element.children[:3]:  # Limit to first 3 children
                if hasattr(child, "resolve") and callable(child.resolve):
                    resolved = child.resolve(document)
                    if resolved:
                        explore_element(resolved, depth + 1)
                else:
                    explore_element(child, depth + 1)

    print("Document body structure:")
    explore_element(document.body)

    # Show reference resolution
    print(f"\nDocument contains {len(document.body.children)} top-level elements")

    # Count different reference types
    ref_types = {}
    for child in document.body.children:
        child_type = type(child).__name__
        ref_types[child_type] = ref_types.get(child_type, 0) + 1

    print("Reference types in body:")
    for ref_type, count in ref_types.items():
        print(f"  {ref_type}: {count}")


# Example 4: Multi-Criteria Filtering
def advanced_filtering(document):
    """Combine multiple filtering criteria"""

    print("\n=== Advanced Multi-Criteria Filtering ===")

    # Complex filter: Financial tables in top half of pages
    financial_top_tables = []

    for table in document.tables:
        # Criteria 1: Spatial (top half)
        spatial_match = (
            table.prov and len(table.prov) > 0 and table.prov[0].bbox.t > 396
        )

        # Criteria 2: Content (financial keywords)
        content_match = False
        try:
            df = table.export_to_dataframe()
            if not df.empty:
                table_text = " ".join(df.iloc[0].astype(str)).lower()
                content_match = any(
                    keyword in table_text
                    for keyword in ["revenue", "income", "margin", "gaap", "earnings"]
                )
        except Exception as e:
            print(f"Error analyzing table for advanced filtering: {e}")

        if spatial_match and content_match:
            financial_top_tables.append(table)

    print(f"Financial tables in top half: {len(financial_top_tables)}")

    # Complex filter: Large tables (>= 4 columns) with specific page range
    large_tables_middle_pages = [
        table
        for table in document.tables
        if (
            table.prov
            and len(table.prov) > 0
            and 3 <= table.prov[0].page_no <= 6  # Pages 3-6
            and hasattr(table, "data")
            and table.data
            and table.data.num_cols >= 4
        )  # At least 4 columns
    ]

    print(f"Large tables on pages 3-6: {len(large_tables_middle_pages)}")

    # Show details of filtered results
    for i, table in enumerate(large_tables_middle_pages, 1):
        page_no = table.prov[0].page_no
        cols = table.data.num_cols if table.data else 0
        rows = table.data.num_rows if table.data else 0
        print(f"  Table {i}: Page {page_no}, {rows}×{cols} cells")


# Example 5: Element Proximity Analysis
def analyze_element_proximity(document):
    """Find elements that are close to each other spatially"""

    print("\n=== Element Proximity Analysis ===")

    # Find text elements near tables (potential table titles/captions)
    for i, table in enumerate(document.tables, 1):
        if not (table.prov and len(table.prov) > 0):
            continue

        table_bbox = table.prov[0].bbox
        table_page = table.prov[0].page_no

        # Find text elements on same page within reasonable distance
        nearby_texts = []
        for text in document.texts:
            if not (text.prov and len(text.prov) > 0):
                continue

            text_bbox = text.prov[0].bbox
            text_page = text.prov[0].page_no

            # Same page and within 100 points vertically
            if (
                text_page == table_page
                and abs(text_bbox.t - table_bbox.t) < 100
                and hasattr(text, "text")
                and text.text
            ):
                nearby_texts.append(
                    {
                        "text": text.text.strip(),
                        "distance": abs(text_bbox.t - table_bbox.t),
                    }
                )

        # Sort by distance and take closest
        nearby_texts.sort(key=lambda x: x["distance"])

        print(f"Table {i} (Page {table_page}):")
        for text_info in nearby_texts[:2]:  # Show 2 closest
            print(
                f"  Nearby: {text_info['text'][:40]}... (distance: {text_info['distance']:.1f})"
            )


# Main execution
if __name__ == "__main__":
    print("Docling Element Iteration and Filtering Examples")
    print("=" * 60)

    # Load document
    document = load_document()
    print(
        f"Loaded document with {len(document.tables)} tables and {len(document.texts)} text elements\n"
    )

    # Run filtering examples
    financial_tables, operational_tables = filter_by_content(document)
    filter_by_location(document)
    explore_document_hierarchy(document)
    advanced_filtering(document)
    analyze_element_proximity(document)
