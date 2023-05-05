
import streamlit as st
from PIL import Image
import io
import img2pdf
import time
from PyPDF2 import PdfReader
import os
import base64
from pdftools import *
import streamlit.components.v1 as components


col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    image = Image.open('assets/pdfto.png')
    st.image(image, width=150)
with col2:
    st.write("# PDF2✨")


def img_to_pdf(image):
    # img_path = "D:/projects/Pdf2/quotes-on-life-14-maya-angelou.jpg"
    # storing pdf path
    pdf_path = "file.pdf"
    # opening image
    with open(image, 'rb') as f:
        image_bytes = f.read()
    # converting into chunks using img2pdf
    pdf_bytes = img2pdf.convert(image_bytes)
    # opening or creating pdf file
    with open(pdf_path, "wb") as f:
        # writing pdf files with chunks
        f.write(pdf_bytes)
    # closing pdf file
    return pdf_bytes


def get_image_download_link(pdf_bytes):
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="image.pdf">Download PDF</a>'
    return href


st.title("PDF Info")
st.write("Upload a PDF file and convert it to an image")


uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with io.BytesIO(uploaded_file.read()) as pdf_buffer:
        # Extract PDF file information
        pdf_reader = PdfReader(pdf_buffer)
        info = pdf_reader.documentInfo
        num_pages = len(pdf_reader.pages)
        st.write(f"Author: {info.author}")
        st.write(f"Creator: {info.creator}")
        st.write(f"Producer: {info.producer}")
        st.write(f"Subject: {info.subject}")
        st.write(f"Title: {info.title}")
        st.write(f"Number of pages: {num_pages}")

st.markdown("---")
st.title("PDF Merger")
st.write("Upload two PDF files and merge them into one")

uploaded_file1 = st.file_uploader("Choose the first PDF file", type="pdf")
uploaded_file2 = st.file_uploader("Choose the second PDF file", type="pdf")

if uploaded_file1 is not None and uploaded_file2 is not None:
    output_path = "merged.pdf"  # Replace with the desired output path
    pdfmerger(uploaded_file1, uploaded_file2, output_path)
    st.success("PDFs merged successfully!")
    with open("merged.pdf", "rb") as f:
        bytes = f.read()
        st.download_button(
            label="Download Pdf", data=bytes, file_name="merged.pdf", mime="application/pdf")

st.markdown("---")
st.title("PDF Splitter")
st.write("Upload a PDF file and split it into two")

uploaded_file = st.file_uploader("Choose a PDF file for splitting", type="pdf")

if uploaded_file is not None:
    pdf = uploaded_file.name
    with open(pdf, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # get the split page positions from the user
    splits = st.text_input(
        "Enter the split page positions (comma-separated)", placeholder="2,4")
    if splits:
        splits = [int(s) for s in splits.split(",")]

        # output PDF file name
        outputpdf = "splitted.pdf"

        # call the PDFsplit function to split the PDF
        PDFsplit(pdf, splits, outputpdf)
        # show a success message
        st.success(
            f"The PDF has been split into {len(splits)+1} parts and saved as {outputpdf}.")
        with open("splitted.pdf", "rb") as f:
            bytes = f.read()
            st.download_button(
                label="Download Pdf", data=bytes, file_name="splitted.pdf", mime="application/pdf")

st.markdown("---")
st.title("Image to PDF Converter")
st.write("Upload an image and convert it to PDF")
uploaded_file = st.file_uploader(
    "Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load the image from the uploaded file
    # image = Image.open(uploaded_file)
    # Convert the image to a PDF
    pdf_bytes = img_to_pdf(uploaded_file.name)
    # Display a link to download the PDF
    st.markdown(get_image_download_link(pdf_bytes), unsafe_allow_html=True)

st.markdown("---")
st.title("pdf2txt")
st.write("Upload a PDF file and convert it to text")

uploaded_file = st.file_uploader(
    "Choose a PDF file to convert into text", type="pdf")

if uploaded_file is not None:
    byte_text = convert_pdf_to_txt(uploaded_file)
    st.code(byte_text, language='text')
    st.download_button("Download Text", byte_text)
