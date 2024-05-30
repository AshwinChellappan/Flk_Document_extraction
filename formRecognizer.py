from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
import html
from azure.ai.formrecognizer import DocumentAnalysisClient
from tiktoken.model import encoding_for_model
from azure.search.documents import SearchClient
from dotenv import load_dotenv
import os

load_dotenv()


def get_all_text(filename, page_map):
    content = []
    for i, (section, pagenum) in enumerate(split_text(page_map, filename)):
        content.append(section)
    return " ".join(content)

def table_to_html(table):
    table_html = "<table>"
    rows = [sorted([cell for cell in table.cells if cell.row_index == i],
                   key=lambda cell: cell.column_index) for i in range(table.row_count)]
    for row_cells in rows:
        table_html += "<tr>"
        for cell in row_cells:
            tag = "th" if (
                cell.kind == "columnHeader" or cell.kind == "rowHeader") else "td"
            cell_spans = ""
            if cell.column_span > 1:
                cell_spans += f" colSpan={cell.column_span}"
            if cell.row_span > 1:
                cell_spans += f" rowSpan={cell.row_span}"
            table_html += f"<{tag}{cell_spans}>{html.escape(cell.content)}</{tag}>"
        table_html += "</tr>"
    table_html += "</table>"
    return table_html

def recognize_form(file_path, endpoint, key):
    # Set up the Form Recognizer client

    document_analysis_client = DocumentAnalysisClient(
            endpoint, AzureKeyCredential(key), headers={
                "x-ms-useragent": "azure-search-chat-demo/1.0.0"})
    
    #form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
    form_recognizer_client=document_analysis_client
    page_map = []
    offset = 0
    # Read the file
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Start the recognition process
    poller = form_recognizer_client.begin_analyze_document("prebuilt-layout",document=file_content)

    # Get the result
    form_recognizer_results = poller.result()

    # Extracted data from the result
    for page_num, page in enumerate(form_recognizer_results.pages):
            tables_on_page = [table for table in form_recognizer_results.tables if table.bounding_regions[0].page_number == page_num + 1]

            # mark all positions of the table spans in the page
            page_offset = page.spans[0].offset
            page_length = page.spans[0].length
            table_chars = [-1] * page_length
            for table_id, table in enumerate(tables_on_page):
                for span in table.spans:
                    # replace all table spans with "table_id" in table_chars
                    # array
                    for i in range(span.length):
                        idx = span.offset - page_offset + i
                        if idx >= 0 and idx < page_length:
                            table_chars[idx] = table_id

            # build page text by replacing charcters in table spans with table
            # html
            page_text = ""
            added_tables = set()
            for idx, table_id in enumerate(table_chars):
                if table_id == -1:
                    page_text += form_recognizer_results.content[page_offset + idx]
                elif table_id not in added_tables:
                    page_text += table_to_html(tables_on_page[table_id])
                    added_tables.add(table_id)

            page_text += " "
            page_map.append((page_num, offset, page_text))
            offset += len(page_text)
    return page_map

enc = encoding_for_model(model_name="gpt-4-32k")

def getImageContent(filepath):
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    # Replace with the path to your local PDF file
    file_path = filepath
    page_map=recognize_form(file_path, endpoint, key)
    return page_map


if __name__ == "__main__":
    # Replace with your Form Recognizer endpoint and key
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    # Replace with the path to your local PDF file
    file_path = "..\sourcefile\DN - FIN-20536-1.jpg"
    page_map=recognize_form(file_path, endpoint, key)
    print(page_map)