#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 10:02:12 2023

@author: rafael
"""


folder = '/home/rafael/Documents/git/MSFeCARE/forms-clinical/ped/release20230213/'
inputfile_tt = folder+'tt.drawio'
diagnosis_order = folder+'diagnosis_order.csv'
drugsfile = 'medications_zscores.xlsx'
cafile = folder+'ca.xlsx'
summaryfile = folder+'summary.xlsx'
form_id = 'ped'
output_xls = folder + 'tt.xlsx'
form_title = 'Ped'
#htmlfolder = '/home/rafael/Documents/git/almsom/html/' # folder where the html files are stored (that will replace the text in notes)
htmlcontent = True # whether the diagram  contains html in the content of objects
platform = 'cht'
headerfile = folder+'formheader_cht.xlsx'
testing = False
context_params_from_facility=False