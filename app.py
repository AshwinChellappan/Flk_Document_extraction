import io
from fileinput import filename
from io import BytesIO
import time
from chatcompletion import getopenairesponse,getopenaiarabicresponse,getopenaiimageresponse
import streamlit as st
import base64
import os
from PyPDF2 import PdfReader
import csv
from dotenv import load_dotenv
import docTranslation
import formRecognizer
load_dotenv()

def download_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return data

language_type="English"
st.sidebar.markdown("## Instructions:")
st.sidebar.write("1. Upload the document to extract")
st.sidebar.write("2. Click extract to initiate the translation")
st.sidebar.write("3. Download the extracted document after extracting")

# Display the release notes in the sidebar
st.sidebar.markdown("## Release Notes:")
st.sidebar.write("1. This Application works for most of the document formats (e.g., Pdf, Doc..)")
count = 1
uploaded_file = st.file_uploader("Upload a document to translate...")
language = st.selectbox("Select the target language for translation",
                              ["Type or Select the Language", "English", "Arabic","Image"], key=count)
count += 1
st.write("")
if st.button("Extract"):
    language_type=language
    print("Language type..",language_type)
    if uploaded_file is not None:
        filename = uploaded_file.name
        # Read the uploaded file content with error handling
        filepath=""
            #laguage_type = os.getenv("LANGUAGE_TYPE")
        if language_type in 'English':
            try:
                pdf_reader = PdfReader(uploaded_file)
                num_pages = len(pdf_reader.pages)
                file_content = ""
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    file_content += page.extract_text()
                # Display the content
                print(file_content)
                response=getopenairesponse(file_content)
                filepath="../sourcefile/extracted_data.csv"
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        elif language_type in 'Image':
            print("Image data")
            file_content = uploaded_file.read()
            print("file_content",file_content)
            with open("../sourcefile/"+filename, 'wb') as f:
                    f.write(file_content)
            content =formRecognizer.getImageContent("../sourcefile/"+filename)
            print(content)
            response=getopenaiimageresponse(content)
            filepath="../sourcefile/extracted_data_image.csv"
        else:
            print("Inside else")
            file_content = uploaded_file.read()
            docTranslation.LocalToBlob(file_content, filename)
            docTranslation.Translate('en')
            content = docTranslation.BlobToLocal()
            print("content:",content)
            with open("../sourcefile/"+filename, 'wb') as f:
                    f.write(content)

            pdf_reader = PdfReader("../sourcefile/"+filename)
            num_pages = len(pdf_reader.pages)
            file_content = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                file_content += page.extract_text()
            # Display the content
            print(file_content)

            response=getopenaiarabicresponse(file_content)
            filepath="../sourcefile/extracted_data_arabic.csv"
        values = response.split("|")
        # Write to CSV file
        with open(filepath, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(values)
        st.write("Extracted Successfully")
        #file_path = "../sourcefile/extracted_data.csv"
        st.download_button(
        label="Download file",
        data=download_file(filepath),
        file_name="extracted_data.csv",
        mime="text/plain"
    )             
        
