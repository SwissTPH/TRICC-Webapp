# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:47:42 2022
To extract and inject English strings from the excel and to update the translation file
@author: kluera
"""

import pandas as pd
from cleanhtml import html2plain

def make_transtable(df_survey, df_choices):
    # Extracting strings from survey tab:
    dfl1 = df_survey.filter(like = '::') # extract text columns (for translation)
    # combine with 'type' and 'name' column
    dfl1 = pd.concat([df_survey[['type', 'name']], dfl1], axis = 1) 
    # drop 'calculate', 'end group', 'hidden', 'string', 'db:person' and empty rows ''
    dfl1 = dfl1[~dfl1['type'].isin(['calculate', 'end group', 'hidden', 'string', 'db:person', ''])]
    
    # Extracting strings from choices tab:
    dfl2 = df_choices.filter(like = '::') # extract text columns (for translation)
    # combine with 'list_name' and 'name' column
    dfl2 = pd.concat([df_choices[['list_name', 'name']], dfl2], axis = 1) 
    # drop empty rows ''
    dfl2 = dfl2[dfl2['list_name']!='']
    
    # combine survey and choices to one df
    dfl = pd.concat([dfl1, dfl2])
    dfl.fillna('', inplace = True)
    
    # sort columns so that label::en and label::fr are together, but put 'type', 'list_name', 'name' in front
    cols = sorted(dfl.filter(like = '::').columns)
    cols[:0] = ['type', 'list_name', 'name']
    dfl = dfl[cols]
    
    # sort rows alphabetically    
    dfl.sort_values(by=['type', 'list_name', 'name'], ascending=True, inplace = True)
    
    # drop image columns, they are not translated
    img_cols = dfl.filter(like = 'image').columns
    dfl.drop(columns = img_cols, inplace = True)
    
    return dfl


# update translation table by the xls table
# update criteria: 
# when the en column in the translation table does not exist, it gets created
# when the en column in the translation table exists, but is differnt, it gets updated
# input are the two translation tables, dfl from xls form and dft from the translation file
def update_trans(dfl, dft):
    
    encols = dfl.filter(like = '::en').columns # get the names of 'English' columns    
    encols = encols[~encols.str.contains('image')] # DROP IMAGE COLUMNS
    headcols = dfl.filter(regex = '^(?!.*(::)).*$').columns # get the non-text columns 
    frcols = dft.filter(regex = '::fr$').columns # get the names of the 'French' columns from the translation file
    
    # make list of columns the final output should have
    cols = encols.append(frcols).sort_values()
    cols = headcols.append(cols)
    
    # merge xls table and translation table on 'type', 'list_name', 'name'; that combo is unique to each row
    # the 'en' columns from the translation table will have a '_t' suffix
    dft_updated = dfl.merge(dft, on=['type', 'list_name', 'name'], how = 'left', suffixes= ('', '_t')) 
    dft_updated.fillna('', inplace = True)
    
    # update the EN text columns of the translation table by those from the xls form
    for col in encols:
        # rows where en exists, but en_t column is empty (new strings)
        newrows = dft_updated.loc[(dft_updated[col]!='') & (dft_updated[col + '_t']=='')].index+2
        if len(list(newrows))>0:
            print('The following rows contain new English ', col, 'fields: ', list(newrows))
        
        # rows where en_t exists but does not match with en (updated English strings) (without html formatting)
        dft_updated[[col + '_clean', col + '_t_clean']] = dft_updated[[col, col + '_t']].applymap(html2plain)
        updated_rows = dft_updated.loc[(dft_updated[col + '_clean']!=dft_updated[col + '_t_clean']) & (dft_updated[col + '_t_clean']!='')].index+2
        if len(list(updated_rows))>0:
            print('The following rows contain updated English ', col, 'fields: ', list(updated_rows))
                 
    dft_updated = dft_updated[cols]
    # dft_updated.rename(columns=lambda x: re.sub('_t$','',x), inplace = True)
    
    return dft_updated


# update translations in the xls-form by the translation file
def import_trans(df, df_trans):
    imcols = df.filter(like = 'image').columns
    # the df has only EN columns at this stage
    if 'list_name' not in df.columns:
        df_updated = df.merge(df_trans, on = ['type', 'name'], how = 'left', suffixes= ('', '_t'))
        # df_updated.drop(columns = ['list_name'], inplace = True)
    else:         
        df_updated = df.merge(df_trans, on = ['list_name', 'name'], how = 'left', suffixes= ('', '_t'))
        # df_updated.drop(columns = ['type'], inplace = True)        
        

    textcols = df_trans.filter(like = '::').columns # get the names of textcolumns from the translation file (the xls file has only 'EN' at this stage)
    headcols = df.filter(regex = '^(?!.*(::)).*$').columns # get the non-text columns from the xls file
    cols = headcols.append(textcols) 
    cols = cols.append(imcols) # columns of the output xls table
    
    df_updated = df_updated[cols]
    df_updated['image::fr'] = df_updated['image::en'] # make a French column with the same images as in En
    df_updated.fillna('', inplace = True)
    
    return df_updated


