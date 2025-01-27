#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:02:12 2023

@author: rafael
"""

### General
form_id = 'almanach_libya'
form_title = 'Almanach Libya'
htmlcontent = False # whether the diagram  contains html in the content of objects
platform = 'cht'
testing = False
context_params_from_facility=False
mhsplit = True  # whether several nodes are combined into 1 (multiheadline split)
interrupt_flow = True
activity = 'treatment'
hide_diagnoses = ['d_critical_condition','d_non_critical_condition','d_no_malnut']
### Input Streamlit webapp folder
folder = 'U:/Projects/Almanach-Libya/L3/release20221025/Libya/'
resource_folder = './resources/'
inputfile_dx = folder+'ALM LBY_Diagnostic.drawio'  # inputfile for jupyter notebook diagnostic
inputfile = folder+'ALM LBY_Treatment_grouped.drawio' # inputfile for tricc-graph tt
diagnosis_order = folder+'diagnose_order.csv'
input_trans = folder + '../../../form/translation.xlsx'
htmlfolder = folder + '../../../form/htm_files/' # folder where the html files are stored (that will replace the text in notes)
images_to_import =['icon-healthcare-diagnosis.svg']

### Resources
cafile = resource_folder+'ca.xlsx'
summaryfile = resource_folder+'summary.xlsx'

### Output
output_folder = folder+'output_for_zip/' # folder where output files will be stored
output_xls = folder+'tt.xlsx'
output = output_folder+form_id+'.xlsx'
media_folder = output_folder+'media/images/'
updated_trans = folder + 'to_be_translated.xlsx'
zipfile = folder+'output/output'

### Input TRICC Repo folder
repo_folder = './TRICC/'
drugsfile = folder+'medications_zscores.xlsx'
headerfile = folder+'formheader_cht.xlsx'
headerfile_pause = folder+'formheader_cht_pause.xlsx'
breakpoints = repo_folder+'breakpoints.csv'