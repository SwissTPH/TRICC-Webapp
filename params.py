#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 08:53:26 2023

@author: rafael
Parameters for Almanach Somalia
"""

folder = '/home/rafael/Documents/git/almsom/diagrams/'
inputfile_tt = folder+'tt.drawio'
diagnosis_order = folder+'diagnosis_order.csv'
drugsfile = 'medications_zscores.xlsx'
cafile = folder+'ca.xlsx'
summaryfile = folder+'summary.xlsx'
form_id = 'almsom'
output_xls = folder + form_id+ '_tt.xlsx'
output_xml = folder + 'tt.xml'
output_commcare = folder + 'tt_commcare.xml'  # if the platform is commcare, we will make a commcare conform xform file
form_title = 'Almanach Somalia'
htmlfolder = '/home/rafael/Documents/git/almsom/html_en/' # folder where the html files are stored (that will replace the text in notes)
htmlcontent = False # whether the diagram contains html in the content of objects
platform = 'commcare'
headerfile = folder+'formheader_commcare.xlsx'
