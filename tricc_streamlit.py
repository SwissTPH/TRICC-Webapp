# Imports
import glob
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import lxml.etree as etree
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from PIL import Image
from yaml.loader import SafeLoader

current_datetime = str(datetime.now().strftime("%Y%m%dT%H%M%S"))
path = os.getcwd()

### Variables
TRICC_SCRIPT_FILE = os.path.join(path, "TRICC/merge-dx-tt.py")
TRICC_LOGO = os.path.join(path, "tricc_logo.png")
UPLOAD_FOLDER = os.path.join(path, "uploaded_files/")
UPLOAD_FOLDER_FILES = os.path.join(path, "uploaded_files/*")
ZIP_OUTPUT = "output/output.zip"
OUTPUT_FILENAME = "tricc_output"

### AUTH
disabled_bool = True

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("Logout", "main")
    welcome_message = st.markdown(f"Welcome {name}!")
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")

### APP
if authentication_status:
    image = Image.open(TRICC_LOGO)
    tricc_logo = st.image(image, use_column_width=True)
    intro_message = st.markdown("""
    This app allows you to **convert clinical workflow diagrams from .drawio files 
    into structured Xform data** for later use in CommCare or CHT platform.

    **Credits**
    - App by [Patrick Meier](https://www.swisstph.ch/en/people-teaser-detail/teaser-detail/patrick-meier#pageRecord)
    - TRICC by [Rafael Kluender](https://www.swisstph.ch/en/people-teaser-detail/teaser-detail/rafael-kluender#pageRecord)
    """)

def remove_files():
    # Remove uploaded files after download of the zip
    files = glob.glob(UPLOAD_FOLDER_FILES)
    for f in files:
        os.remove(f)

def store_file(file, file_name):
    save_folder = UPLOAD_FOLDER

    save_path = Path(save_folder, file_name)
    with open(save_path, mode="wb") as w:
        w.write(file.getvalue())

def run_TRICC():
    tricc_script_output = subprocess.run([f"{sys.executable}", TRICC_SCRIPT_FILE])

def filedownload(file):
    xml_file = file
    href = f'<a href="data:file/{xml_file}" download="prediction.csv">Download Predictions</a>'
    return href

### Sidebar
if authentication_status:
    with st.sidebar.expander("Usage Instructions"):
            st.markdown("""
                1. Upload workflows and diagnosis order files
                2. Click on convert
                3. Wait for TRICC to perform the conversion
                4. Download the converted files as zip
            """)

    with st.sidebar.header("1. Upload workflow files"):
        dx_file = st.sidebar.file_uploader(
            "Upload DIAGNOSTIC file", type=[".drawio"], key="dx.drawio")

        tt_file = st.sidebar.file_uploader(
            "Upload TREATMENT file", type=[".drawio"], key="tt.drawio")
        
        diagnosis_order_file = st.sidebar.file_uploader(
            "Upload DIAGNOSIS ORDER file", type=[".csv"], key="diagnosis_order.csv")
        
        translation_file = st.sidebar.file_uploader(
            "Upload TRANSLATION file", type=[".xlsx"], key="ped_fr.xlsx")
        
        # Check if all files have been uploaded
        if dx_file and tt_file and diagnosis_order_file and translation_file is not None:
            disabled_bool = False
        else:
            disabled_bool = True
        
### Main file handling and conversion using TRICC
if authentication_status:
    st.sidebar.header("2. Convert the files using TRICC")
    if st.sidebar.button("Convert", disabled=disabled_bool):
        # Clear previous info on start of conversion
        welcome_message.empty()
        tricc_logo.empty()
        intro_message.empty()

        # Remove previous files
        remove_files()  

        # Store uploaded files one by one with a predefined name per specific file
        store_file(dx_file, "dx.drawio")
        store_file(tt_file, "tt.drawio")
        store_file(diagnosis_order_file, "diagnosis_order.csv")
        store_file(translation_file, "ped_fr.xlsx")

        # Print information on uploaded files
        bytes_data = tt_file.read()
        st.header("TRICC Input")
        st.write("**Diagnostic File:**", dx_file.name)
        st.write("**Treatment File:**", tt_file.name)
        st.write("**DIAGNOSIS Order File:**", diagnosis_order_file.name)
        st.write("**Translation File:**", translation_file.name)
        st.write("___")

        ### TRICC
        st.header("3. TRICC conversion")
        with st.spinner("Doing the TRICC.. (~15min)"):
            run_TRICC()
        st.write("___")


        ### Output
        # Enable the download of the output files as zip
        st.header("Output")
        st.success("4. The output files can now be downloaded")


        with open(ZIP_OUTPUT, "rb") as fp:
            btn = st.download_button(
                label="Download ZIP",
                data=fp,
                file_name=OUTPUT_FILENAME + "_" + current_datetime + ".zip",
                mime="application/zip"
        )
    else:
        st.info("Upload draw.io workflow data in the sidebar to start!")