#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:02:12 2023

@author: rafael
"""

# General
form_id = 'msf_sti'
form_title = 'STI'
htmlcontent = True  # whether the diagram  contains html in the content of objects
platform = 'cht'
testing = False
context_params_from_facility = True
# whether several nodes are combined into 1 (multiheadline split)
mhsplit = False
interrupt_flow = True
activity = 'treatment'
hide_diagnoses = ['d_ct_urine', 'd_ng_urine', 'd_ct_rectal', 'd_ng_rectal', 'd_ct_vaginal', 'd_ct_discharge', 'd_ng_discharge', 'd_ng_vaginal', 'd_ct_pharynx', 'd_ng_pharynx', 'd_pharyngitis_no_sti', 'p_high_risk',
                  'd_trichomonas_vaginalis', 'd_mycoplasma_genitalium']
# Input Streamlit webapp folder
folder = 'U:/Projects/msf_sti/'
resource_folder = folder+'resources/'
# inputfile for jupyter notebook diagnostic
inputfile_dx = folder+'/L2/diagrams/diagnostic_v2.drawio'
inputfile = folder+'/L2/diagrams/tt.drawio'  # inputfile for tricc-graph tt
diagnosis_order = folder+'L2/diagnose_order.csv'
input_trans = folder + 'L2/translation.xlsx'
# folder where the html files are stored (that will replace the text in notes)
htmlfolder = folder + 'L2/html/'
images_to_import = ['icon-healthcare-diagnosis.svg']
version = '1.1.0'
# Resources
cafile = resource_folder+'ca.xlsx'
summaryfile = resource_folder+'summary.xlsx'

# Output
# folder where output files will be stored
output_folder = folder+'output_for_zip/'
output_xls = folder+'tt.xlsx'
output = output_folder+form_id+'.xlsx'
media_folder = output_folder+'media/images/'
updated_trans = folder + 'to_be_translated.xlsx'
zipfile = folder+'L3/xlsforms/output'

# Input TRICC Repo folder
repo_folder = './TRICC/'
drugsfile = folder+'L3/xlsforms/medications_zscores.xlsx'
headerfile = repo_folder+'formheader_cht.xlsx'
headerfile_pause = repo_folder+'formheader_cht_pause.xlsx'
breakpoints = repo_folder+'breakpoints.csv'
