#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:02:12 2023

@author: rafael
"""


folder = '/home/rafael/Documents/git/MSFeCARE/forms-clinical/ped/release20230221/'
media_folder = folder+'media/images/'
inputfile_dx = folder+'dx.drawio'  # inputfile for jupyter notebook diagnostic
inputfile = folder+'tt.drawio' # inputfile for tricc-graph tt
diagnosis_order = folder+'diagnosis_order.csv'
drugsfile = 'medications_zscores.xlsx'
cafile = folder+'ca.xlsx'
summaryfile = folder+'summary.xlsx'
form_id = 'ped'
output_xls = folder + 'tt.xlsx'
output = folder + form_id + '.xlsx'
form_title = 'Ped'
input_trans = folder + 'ped_fr.xlsx'
updated_trans = folder + 'ped_fr_newest.xlsx'
#htmlfolder = '/home/rafael/Documents/git/almsom/html/' # folder where the html files are stored (that will replace the text in notes)
htmlcontent = True # whether the diagram  contains html in the content of objects
platform = 'cht'
headerfile = folder+'formheader_cht.xlsx'
headerfile_pause = folder+'formheader_cht_pause.xlsx'
testing = False
context_params_from_facility=True
mhsplit = False  # whether several nodes are combined into 1 (multiheadline split)
interrupt_flow = True
activity = 'treatment'