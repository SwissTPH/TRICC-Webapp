# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
Quality checks for ancient TRICC
"""
import cleanhtml as ch #my own helper functions

# check if all objects have an odk_type
def check_node_type(df_raw):
    # drop diagrams.net related objects (do not belong to drawing)
    dfa = df_raw.drop([0,1])
    
    # nodes that do not have a proper odk_type
    odk_types = ['activity', 'select_one', 'select_one yesno', 'select_multiple', 'count', 'select_option', 'calculate', 'rhombus', 'decimal', 'integer', 'note', 'text', 'diagnosis', 'help-message', 'hint-message', 'container_page', 'container_hint_media', 'goto']
    dfa = dfa.loc[~dfa['odk_type'].isin(odk_types) & (dfa['source']=='') & (dfa['target']=='')].copy()
    
    if len(dfa)!=0:
        # for testing, get rid of formatting everywhere
        dfa['value']=dfa.value.apply(ch.html2plain)
        print('The following boxes have not a proper \'odk_type\':')
        for i, row in dfa.iterrows():
            print('ObjectID:', row['id'], '\nContent:', row['value'], '\nType:', row['odk_type'])

# check if all rhombus refer to an existing node
def check_rhombus_refer(df_raw):
    # drop diagrams.net related objects (do not belong to drawing)
    dfa = df_raw.drop([0,1])
    
    # quality check do rhombus refer to existing objects
    refer_types = ['decimal', 'integer', 'select_one', 'select_one yesno', 'select_multiple', 'calculate', 'diagnosis', 'count']
    refer_objects = dfa.loc[dfa['odk_type'].isin(refer_types), 'name']
    # refer_objects = 'stored_'+refer_objects
    dfa = dfa.loc[(dfa['odk_type']=='rhombus') & ~dfa['name'].isin(refer_objects)]
    if len(dfa)!=0:
        dfa['value']=dfa.value.apply(ch.html2plain)
        print('The following rhombus do not refer to an existing field:')
        for i, row in dfa.iterrows():
            row['name'] = row['name'][7:]
            print('ObjectID:', row['id'], '\nContent:', row['value'], '\nType:', row['odk_type'], '\nRefering to:', row['name'])
            
# check if all edges are well connected
def check_edge_connection(df_raw):
    # drop diagrams.net related objects (do not belong to drawing)
    dfa = df_raw.drop([0,1])
    dfa = dfa.loc[dfa['style'].str.contains('jettySize') & ((dfa['source']=='') | (dfa['target']==''))]
    if len(dfa)!=0:
        dfa['value']=dfa.value.apply(ch.html2plain)
        print('The following edges are not connected:\n')
        dfs = dfa.loc[dfa['source']=='']
        df_raw2 = df_raw.copy()
        df_raw2.value = df_raw2.value.apply(ch.html2plain)
        if len(dfs)!=0:
            print('Missing edge source:\n')
            for i, row in dfs.iterrows():
                target_id = row['target']
                target_name = df_raw2.loc[df_raw2['id']==target_id,'name'].iloc[0]
                target_type = df_raw2.loc[df_raw2['id']==target_id,'odk_type'].iloc[0]
                target_content = df_raw2.loc[df_raw2['id']==target_id,'value'].iloc[0]
                print('Pointing to:\nObjectID:', target_id, '\nName:',target_name, '\nContent:', target_content, '\nType:', target_type)             
        dft = dfa.loc[dfa['target']=='']
        if len(dft)!=0:
            print('\nMissing edge target:\n')
            for i, row in dft.iterrows():
                source_id = row['source']
                source_name = df_raw2.loc[df_raw2['id']==source_id,'name'].iloc[0]
                source_type = df_raw2.loc[df_raw2['id']==source_id,'odk_type'].iloc[0]
                source_content = df_raw2.loc[df_raw2['id']==source_id,'value'].iloc[0]
                print('Coming from:\nObjectID:', source_id, '\nName:',source_name, '\nContent:', source_content, '\nType:', source_type)
                
# check if all leaving edges have a Yes/No                
def check_edge_yesno(df_raw, types):
    # drop diagrams.net related objects (do not belong to drawing)
    dfa = df_raw.drop([0,1])
    nodes = dfa.loc[df_raw['odk_type'].isin(types), 'id']
    dfa['value'] = dfa['value'].apply(ch.html2plain)
    dfa = dfa.loc[dfa['source'].isin(nodes) & ~dfa['value'].isin(['Yes', 'No'])]
    if len(dfa)!=0:
        dfa['value']=dfa.value.apply(ch.html2plain)
        print('The following objects have outgoing edges without Yes/No. This is not allowed.')
        for i, row in dfa.iterrows():
            source_id = row['source']
            source_name = df_raw.loc[df_raw['id']==source_id,'name'].iloc[0]
            source_type = df_raw.loc[df_raw['id']==source_id,'odk_type'].iloc[0]
            source_content = df_raw.loc[df_raw['id']==source_id,'value'].iloc[0]
            print('ObjectID:', source_id, '\nName:',source_name, '\nContent:', source_content, '\nType:', source_type)     
        
    
                
