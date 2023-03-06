#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:02:12 2023

@author: rafael
"""

#%% General settings
form_id = 'ped'
form_title = 'Ped'
htmlcontent = True # whether the diagram  contains html in the content of objects (content is in the diagram)
htmlfolder = '/home/rafael/Documents/git/almsom/html/' # folder where the html files are stored (that will replace the text in notes)
platform = 'cht'
testing = False
context_params_from_facility=True


#%% Form specific input files and settings
folder = '/home/rafael/Documents/git/MSFeCARE/forms-clinical/ped/release20230221/'
inputfile_dx = folder+'dx.drawio'  # diagnostic inputfile for legacy notebook (currently AlmLib, MSF PED, MSF YI)
inputfile = folder+'tt.drawio' # inputfile for tricc-graph tt
activity = 'treatment' # activity that should be built from inputfile (for MSF there is only 'treatment')
input_trans = folder + 'ped_fr.xlsx' # file with translated strings
diagnosis_order = folder+'diagnosis_order.csv' # hierarchy of diagnosis
drugsfile = 'medications_zscores.xlsx' # global medication lookup
cafile = 'ca.xlsx' # Table for Caretaker advice message logic
summaryfile = 'summary.xlsx' # Template for the summary
interrupt_flow = True # whether the form has pauses and uses CHT tasks
mhsplit = False  # multiheadline split: whether several nodes are combined into 1 object in the diagram


#%% output files made by TRICC
output_folder = folder + 'output_for_zip/' # folder where output files will be stored
media_folder = output_folder+'media/images/'
output = output_folder + form_id + '.xlsx'
zipfile = folder + 'output/output'


#%% TRICC internal settings & parameters
output_xls = folder + 'tt.xlsx'  # where to write the TT part
updated_trans = output_folder + 'ped_fr_newest.xlsx' # where to save updated translations
headerfile = folder+'formheader_cht.xlsx'  # Formheader for the base form
headerfile_pause = folder+'formheader_cht_pause.xlsx' # Formheader for the CHT tasks form
