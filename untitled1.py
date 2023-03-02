#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 14:07:17 2023

@author: rafael
"""

htmlpath = '/home/rafael/Documents/git/almsom/html/Amoxicillin treatment.htm'
with open(htmlpath, encoding ='ISO-8859-15', mode='r') as f:
    soup = BeautifulSoup(f, 'lxml')
soup = ch._replace_tag(soup, 'b', 'strong')
soup  = soup.body
#    s = soup.get_text()
#    s.encode('ascii', errors='ignore').decode("utf-8")