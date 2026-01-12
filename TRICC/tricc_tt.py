#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mon Nov 28 20:08:01 2022

@author: rafael kluender
'''
import inputs
import qualitychecks_pd as qcpd
import graphtools as gt
import odk_helpers as oh
import pandas as pd
import edgelogic as el
import networkx as nx
import cleanhtml as ch
import caretaker_advice as ca
import multiheadlinesplit as mhs
from datetime import datetime
from markdownify import markdownify as md
from utf8encoder import encodeUTF8 as utf8
from formconverters import df2xlsform  # makes xlsforms out of dataframes
from formconverters import xls2xform  # makes xlsforms out of dataframes
import xml_tools as xt
from CDSS_list_merge import merge_list


# %% Parameters - > choose your form (ped, yi, almsom) here
# TODO CHANGE THE PARAMETERS ACCORDING TO PROJECT!!!!
# import params_almsom_tt as p # for almanach Somalia TT
# import params_ped_rk as p # for msfecare Ped
# import params_msf_sti as p
# import params_ped as p # for msfecare Ped
import params_libya_rk as p # for Almanach Libya

import warnings
warnings.filterwarnings("ignore")

# %% Parse diagram
objects = inputs.parse_drawio(p.inputfile)  # parse drawing

# Put diagram elements in df_raw
df_raw = inputs.treetodataframe(objects)  # import drawing elements into a df
df_raw.fillna('', inplace=True)
# all content into the same column
df_raw.loc[df_raw['label'] != '', 'value'] = df_raw['label']

# this keeps specific tabs in the diagram
# Uncomment the line below for running LBY. We need to then change this
# And then do it for every group name in the LBY TT drawio
# Then you have to glue all the outputs of the different groups together into
# one treatment file

# df_raw = df_raw.loc[df_raw['activity']=='oral antibiotics']

# %% Focus on treatment only and strip off the follow up (FOR NOW, in Almsom TT)
# df_raw = df_raw.loc[df_raw['activity']!='Follow up advise']


# %% Quality checks
qcpd.check_node_type(df_raw)  # check if all objects have an odk_type
# check if all rhombus refer to an existing node
qcpd.check_rhombus_refer(df_raw)
qcpd.check_edge_connection(df_raw)  # check if all edges are well connected
types = ['rhombus', 'select_one yesno']
# check if all edges leaving rhombus and select_one yesno have Yes/No
qcpd.check_edge_yesno(df_raw, types)

# %% assign diagnosis names to rows in df_raw
df_raw = oh.assign_diagnosisname(p.diagnosis_order, df_raw)


# %% Split multiple header lines into singleton objects
if p.mhsplit:
    df_raw = mhs.split_mh(df_raw)


# %% Build the choices tab
df_choices = df_raw.loc[df_raw['odk_type'] == 'select_option']
df_choices = df_choices.merge(
    df_raw[['name', 'odk_type', 'id']], how='left', left_on='parent', right_on='id')
df_choices = df_choices[['name_y', 'name_x', 'value']]


# MPEA ADDED BECAUSE I WANTED TO TAKE CHOICES FROM DRUGS TO THE NEW XLS
df_choices.rename({'name_y': 'list_name', 'name_x': 'name',
                  'value': 'label::en'}, axis=1, inplace=True)
drug_choices = pd.read_excel(p.drugsfile, sheet_name="choices")
df_choices = pd.concat([df_choices, drug_choices])

# add rows for yesno
yes = pd.DataFrame({'list_name': 'yesno', 'name': 'Yes',
                   'label::en': 'Yes'}, index=['zzz_yes'])
no = pd.DataFrame({'list_name': 'yesno', 'name': 'No',
                  'label::en': 'No'}, index=['zzz_no'])
df_choices = pd.concat([df_choices, yes, no])
""" print(df_raw.columns)
df_arrows=df_raw.loc[(df_raw['source']!='') & (df_raw['target']!=''),['source','target','value']]
print(df_arrows.columns)
df_arrows=df_arrows.merge(df_raw[['name','odk_type']],how='left',left_on='source',right_index=True)
page_ids = df_raw.loc[df_raw['odk_type']=='container_page'].index
df_pageObjects = df_raw.loc[df_raw['parent'].isin(page_ids)]
df_raw.drop(df_pageObjects.index,inplace=True)
df_arrows_in_pages = df_arrows.loc[df_arrows['source'].isin(df_pageObjects.index) & \
                                df_arrows['target'].isin(df_pageObjects.index)]

df_arrows_out_pages = df_arrows.loc[df_arrows['source'].isin(df_pageObjects.index) & \
                                ~df_arrows['target'].isin(df_pageObjects.index)]
df_arrows.loc[df_arrows_out_pages.index,'source'] = df_arrows.loc[df_arrows_out_pages.index,'container_id']
df_arrows.drop(df_arrows_in_pages.index,inplace=True)
# make a new topological sort in the df without objects INSIDE pages, but page heads (begin_group) only: 
# in df_arrows, also drop the connectors which point from the page-root to the first object INSIDE the page
# reset index, because you have manually added page_connectors on top that have messed it up!
df_arrows.reset_index(inplace=True)
df_arrows.drop(columns=['index'],inplace=True)
df_arrows.drop(df_arrows.loc[df_arrows['source_type']=='container_page'].index,inplace=True)
# make a directed graph 
dg = nx.from_pandas_edgelist(df_arrows, source='source', target='target', create_using=nx.DiGraph)
order = list(nx.lexicographical_topological_sort(dg))
# change order of rows
df_raw=df_raw.reindex(order)
# group df_page_Objects by page
gk = df_pageObjects.groupby('parent')
# sort each page and put it into main dataframe df
for page, df_page in gk:
    df_arrows_in_page = df_arrows_in_pages.loc[df_arrows_in_pages['source'].isin(df_page.index)]
    
    if len(df_arrows_in_page)>0:
        # make a dag for the page
        dag = nx.from_pandas_edgelist(df_arrows_in_page, source='source', target='target', create_using=nx.DiGraph)
        order = list(nx.lexicographical_topological_sort(dag))
        
        # sort the page
        df_page=df_page.reindex(order)

# get split row
page_id = df_page['parent'][0]

# and 'end_group' row to its end
df_end = pd.DataFrame({'tag':'UserObject', 'xml-parent': page_id,'odk_type':'end group'}, index = [page_id+'_end'])
df_page = pd.concat([df_page, df_end])
df_page.fillna('', inplace = True)

# put it back in main dataframe df
# get split row
page_id = df_page['xml-parent'][0]

# split df
df_top = df_raw.loc[:page_id]
df_bottom = df_raw.loc[page_id:].drop(index=page_id)

# concat 
df_raw = pd.concat([df_top,df_page,df_bottom]) """

# %% DAG
# build a CDSS graph without images, WITH dataloader
dag = gt.build_graph_cdss(df_raw)

# make edge parents -> children (for select_xxx and pages)
dag = gt.connect_to_parents(dag, df_raw)

# connect shortcuts
dag = gt.connect_shortcuts(dag, df_raw)

# assign 'type', 'name', 'value' and group membership as attributes to nodes
dag = gt.add_nodeattrib(
    dag, df_raw['id'], df_raw['name'].apply(ch.html2plain), 'name')
dag = gt.add_nodeattrib(dag, df_raw['id'], df_raw['odk_type'], 'type')
dag = gt.add_nodeattrib(dag, df_raw['id'], df_raw['parent'], 'group')
# dag = gt.add_nodeattrib(dag, df_raw['id'], df_raw['y'], 'y')
# if you want to keep the html in the text:
if p.htmlcontent:
    dag = gt.add_nodeattrib(dag, df_raw['id'], df_raw['value'], 'content')
else:
    dag = gt.add_nodeattrib(
        dag, df_raw['id'], df_raw['value'].apply(ch.html2plain), 'content')

# assign content of edges as their 'logic' attribute -> there are edges in the form that contain 'Yes' or 'No'
dag = gt.add_edgeattrib(dag, df_raw, 'logic')


# %% Making duplicate calculates unique and adding a 'calculate sink'
# make also a diagnosis sink and convert duplicate diagnosis to calculates
# there are duplicate diagnosis in the dx diagrams
dag = gt.number_calculate_duplicates(dag, df_raw)


# %% Add diagnosis selector and dataloader to DAG

diagnosis_id_hierarchy = gt.get_diagnosis_sorting_id_from_graph(
    dag, p.diagnosis_order)  # make diagnosis id hierarchy list
# diagnosis_id_hierarchy = gt.get_diagnosis_sorting_id(df_raw, p.diagnosis_order) # make diagnosis id hierarchy list
id_dataloader = df_raw.loc[df_raw['value'] ==
                           'Load Data', 'id'].iloc[0]  # get ID of the dataloader

if p.activity == 'treatment':
    n = 'select_diagnosis'
    n_attrib = {'name': 'select_diagnosis', 'type': 'select_multiple',
                'content': 'Select diagnosis', 'group': 1}
    dag = gt.add_calculate_selector(dag, n, n_attrib, diagnosis_id_hierarchy)
    # add the content from the calculates as content to their predecessor select_options
    dag = gt.add_text_calculate_options(dag, 'select_diagnosis')

    # connect the dataloader with the 'select_multiple diagnosis' node
    # this insures that the dataloader elements show up on top of the form and not at the bottom

    # connect dataloader to select_diagnosis
    dag.add_edge(id_dataloader, 'select_diagnosis')

# add a 'data_load' multiple choice that points to the calculates of the dataloader
# this will allow to set them on startup
n = 'data_load'
n_attrib = {'name': 'data_load', 'type': 'select_multiple',
            'content': 'Select previous data', 'group': 1}
dataloader_calculates = [i for (i, j) in dag.in_edges(
    id_dataloader) if dag.nodes[i]['type'] == 'calculate']

dag = gt.add_calculate_selector(dag, n, n_attrib, dataloader_calculates)
# add the content from the calculates as content to their predecessor select_options
dag = gt.add_text_calculate_options(dag, 'data_load')


# %% Write 'expression' into NON rhombus edges

logic = {}  # {edge-tuple : sympy symbol for the logical expression, the negation ~ is not part of the symbolic expression}
logicmap = {}  # {sympy symbol of a logical expression: logical expression itself}
# map between negated sympy symbols and negated odk expressions (needed for converting sympy boolean expressions into odk-conform expressions)
negated_logicmap = {}
# on edges starting in nodes without any decision to be taken, just write S.true
# apply this also to select_one and select_multiple because the logic is on the edges starting from
# the 'select_option'
types = ['note', 'decimal', 'integer', 'text', 'container_page', 'container_hint_media',
         'goto', 'hint-message', 'help-message', 'select_one', 'select_multiple', '']
logic = el.edge_assign_true(dag, logic, types)

# on edges of calculate and diagnosis assign the souce_name.
# it subsitutes the expression but the source name.
# this happens because calculates are not contracted -> conceptual document for more information
types = ['calculate', 'diagnosis']
logic, logicmap, negated_logicmap = el.edge_assign_sourcename(
    dag, logic, logicmap, negated_logicmap, types)

# edges which have a source with type 'select_one yesno' get the tuple (name, value);
# value can be 'Yes' or 'No'
logic, logicmap, negated_logicmap = el.edge_add_name_to_logic(
    dag, logic, logicmap, negated_logicmap, ['select_one yesno'])

# edges starting from 'select_option' write the tuple of names of the predecessor and the select_option
# this will result in (select_xxx_name,select_option_name)
# (just like for select_one yesno, but for select_one, select_multiple, the select_option is not written on the edge)
logic, logicmap, negated_logicmap = el.edge_select_options(
    dag, logic, logicmap, negated_logicmap, ['select_option'])

# update edge logic
nx.set_edge_attributes(dag, logic, name='logic')


# %% Write expression into rhombus edges

# types a rhombus can potentially refer to
refer_types = ['select_one', 'select_one yesno', 'select_multiple',
               'calculate', 'diagnosis', 'count', 'integer', 'decimal']

# build expression for rhombus referring to nodes of type calculate, diagnosis
refers_to = ['calculate', 'diagnosis']
for value in ['Yes', 'No']:
    dag = el.assign_refername_to_edges(dag, refer_types, refers_to, value)

# build expression for rhombus referring to nodes of type select_one and select_multiple
refers_to = ['select_one', 'select_multiple']
for value in ['Yes', 'No']:
    dag = el.assign_refername_and_content_to_edges(
        dag, refer_types, refers_to, value)

# build expression for rhombus referring to nodes of type select_one yesno
refers_to = ['select_one yesno']
for value in ['Yes', 'No']:
    dag = el.assign_refername_and_edgevalue_to_edges(
        dag, refer_types, refers_to, value)

# build expression for rhombus referring to nodes of types integer and decimal
refers_to = ['integer', 'decimal', 'count']
for value in ['Yes', 'No']:
    dag, logicmap, negated_logicmap = el.assign_refername_and_content_equation(
        dag, logicmap, negated_logicmap, refer_types, refers_to, value)


# %% Build relevance for all nodes and assign as attribute
dag = gt.write_node_relevance(dag)  # make and write relevance to nodes


# %% Calculate longest path and select_option hierarchy

'''Calculating the longest possible path to reach a node when starting in root. This value is necessary for
correctly sorting the nodes into a CDSS form. The idea is that the sorting prioritises the finalisation of 
a branch of the diagram, before starting in new one (one does not want to mix up the branches) 
That value will be used in networkx 'lexicographical topological sort' function. 
The select options of a select_one/select_multiple all have the same 'longest path' but they also need a 
sorting priority according to their occurence in the drawing. The branch starting in the first select-option
should come first, then the second, and so on. 
Therefore, the select_options get a value added to their longest path which represents their hierarchy. 
They now no longer have the same sorting-value for the lexicographical topological sort)

As indicated in the conceptual document, this step must be done before contracting the nodes, 
in orrder to avaid that diagnosis branches are mixed up after the contraction. 
In the contracted node, the "longest path from root" will the maximum of the longest paths of the contracted
nodes.'''

# %% SORTING: Make hierarchy for yesno branching
opt_prio_yesno = gt.hierarchy_yesno(dag)

# %% SORTING: Make hierarchy of select options
# hierarchy of select_options in the form
opt_prio = gt.hierarchy_select_options(df_raw)
# %% SORTING: Combine select_options and select yesno hierarchies
opt_prio = opt_prio | opt_prio_yesno

if p.activity == 'treatment':
    # make a hierarchy for the select_diagnosis options
    d = gt.hierarchy_diagnosis(dag, diagnosis_id_hierarchy)
    # combine diagnosis_sorting with select_option sorting
    opt_prio = d | opt_prio


# get a graph entry point (typically a node pointing to the dataloader)
rootnode = gt.get_graph_entry_point(dag)
# calculate the distance of the longest path between the rootnode and each node
dist = gt.get_longest_path_lengths(dag, rootnode, opt_prio)
# assign distance (longest_path_length) to the nodes in dag
nx.set_node_attributes(dag, dist, name='distance_from_root')


# %% CDSS adapted topological sort
# MODIFIED MPEA, CAUSE THIS IS ONLY DONE FOR DX
# topo_order = gt.topo_sort_cdss_attrib(dag, 'distance_from_root') # the complete sorting of the graph
# ADDED BY MPEA
if p.activity == 'treatment':
    # the sorting for this case is based on merging lists. We build first a `list of lists` of nodes for each diagnosis
    # this must happen prior to contracting nodes.
    # it picks each diagnosis for the hierarchy and makes a CDSS sorted list of successor nodes
    d = gt.make_sorted_nodes_list(dag, diagnosis_id_hierarchy, opt_prio)
    # we have to remove 'rhombus' nodes from the list of lists, to avoid that they get merged into one
    d_new = [gt.pop_rhombus(n, dag) for n in d]  # list of lists

    d = d_new
'''
# this approach is good, but not for Treatment or any other activity where diagnosis graphs are parallel
if p.activity!='treatment':
    topo_order = gt.topo_sort_cdss_attrib(dag, 'distance_from_root') # the complete sorting of the graph
else:
    # the sorting for treatment (and for its groups) is based on merging lists. We build first a `list of lists` of nodes for each diagnosis

    d = gt.make_sorted_nodes_list(dag, diagnosis_id_hierarchy, opt_prio)

    # we have to remove 'rhombus' nodes from the list of lists, to avoid that they get merged into one    
    d_new = [gt.pop_rhombus(n, dag) for n in d]
    d=d_new
    
    topo_order = d[0] # variable for the globally sorted nodes, we start with the diagnosis_sort of the most severe diagnosis
    for diagnosis_sort in d[1:]:
        topo_order = merge_list(diagnosis_sort, topo_order)
        print(topo_order)


# before this, for the TT, we need to contract nodes, and update the list_of_lists with the new IDs, then only can we merge the lists
'''

# %% Contract nodes
'''
Questions that repeat in the drawing should be contracted into one instance of that question in order to 
avoid repetition if more than 1 diagnosis is triggered. All elements except rhombus, diagnosis and calculate
can be contracted. After contraction the graph must still be a DAG, meaning it must not have cycles. 
Further on, the relevance of the contracted nodes must be combined. For more info see the conceptual doc
'''

# this makes only sense for the treatment
if p.activity == 'treatment':

    # types of nodes that can potentially be contracted. rhombus and calculates cannot be contracted
    # (calculates have sinks and rhombus are not real nodes)
    contract_types = ['decimal', 'integer', 'note',
                      'select_one yesno', 'help-message', 'hint-message']

    '''before contraction, write the relevance of the to be contracted node into the 
    selected successors of that node add the relevance expression of the contracted node into the one that has been created
    '''
    # Added d
    # dag,d  = gt.contract_duplicates(dag, contract_types, d)
    dag, d = gt.contract_duplicates(dag, contract_types, d)

    # flatten relevance by combining it with 'contracted' relevances in each node
    [gt.make_node_relevance(dag, n)
     for n in dag.nodes if 'contraction' in dag.nodes[n]]

    # flatten also the distance-from-root. It
    [gt.make_node_distance_from_root(
        dag, n) for n in dag.nodes if 'contraction' in dag.nodes[n]]

# ADDED MPEA
if p.activity == 'treatment':
    # the sorting for treatment (and for its groups) is based on merging lists. We build first a `list of lists` of nodes for each diagnosis
    # must happen prior to contracting nodes, moved up
    # d = gt.make_sorted_nodes_list(dag, diagnosis_id_hierarchy, opt_prio)

    # we have to remove 'rhombus' nodes from the list of lists, to avoid that they get merged into one
    # d_new = [gt.pop_rhombus(n, dag) for n in d]
    # d=d_new
    # MPEA : inverted list to try different approach
    # inverted_diagnostic_list = d[::-1]
    # variable for the globally sorted nodes, we start with the diagnosis_sort of the most severe diagnosis
    topo_order = d[0]
    for diagnosis_sort in d[1:]:
        topo_order = merge_list(diagnosis_sort, topo_order)
# %% Reset group relevance in group children
# set group relevance to true for all nodes inside that group (exemple caretaker advice in Ped TT)

# get ids of all groups
group_ids = [n for n in dag.nodes if 'type' in dag.nodes[n]
             and dag.nodes[n]['type'] == 'container_page']

# get ids of all nodes that are in groups
nodes_in_groups = [n for n in dag.nodes if 'group' in dag.nodes[n].keys(
) and dag.nodes[n]['group'] in group_ids]

# substitute in relevance the group relevance by S.true (only if `full relevance` is used)
# [gt.substitute_group_relevance(n, dag) for n in nodes_in_groups]

# %% Write help and hint fields as node attributes
dag = gt.make_help_attributes(dag)

# %% Extract images
dag = gt.extract_images(dag, df_raw, p.media_folder)

# %% Handle duplicate names
''' Not contracted nodes still have duplicate names, that needs to be dealt with. This solution is not
working for select_xxx because it renames those but not the relevance expressions. Fix needed'''

# types of nodes where a duplicate name is a problem
types = ['decimal', 'integer', 'note', 'select_one yesno',
         'select_one', 'select_multiple', 'container-page']
dag = gt.rename_duplicates(dag, types)


# %% Replace sympy expressions with ODK-expressions
''' The relevance logic expressions are generic Sympy expressions. As we will be using Enketo based solutions, 
we must convert them into odk conform expressions. The maping between sympy expressions and odk is given in the 
dictionaries negated_logicmap and logicmap'''
""" for n in dag.nodes:
    print(dag.nodes[n]) """

for n in dag.nodes:
    dag.nodes[n]['relevance'] = el.parse_sympy_logic(
        dag.nodes[n]['relevance'], negated_logicmap, logicmap)

# %% Build choices tab from dag
# list_name = {n:dag.nodes[list(dag.predecessors(n))[0]]['name'] for n in dag.nodes if dag.nodes[n]['type']=='select_option'}
# df_listname = pd.DataFrame.from_dict(list_name, orient='index')
# d = {n:dag.nodes[n] for n in dag.nodes if dag.nodes[n]['type']=='select_option'}
# df_choices = pd.DataFrame.from_dict(d, orient='index')

# %% Replace note headings with content from html files
# first, insure that all html files are encoded in UTF-8
if p.form_id == 'almsom' or p.form_id == 'almanach_libya':
    for n in dag.nodes:
        if 'type' in dag.nodes[n] and dag.nodes[n]['type'] in ['note', 'select_one', 'select_one yesno', 'select_multiple']:
            utf8(p.htmlfolder + dag.nodes[n]['content'] + '.htm')

if p.form_id == 'almsom' or p.form_id == 'almanach_libya':
    content = {n: ch.cleanhtml_fromfile(p.htmlfolder + dag.nodes[n]['content'] + '.htm') for n in dag.nodes if 'type' in dag.nodes[n]
               and dag.nodes[n]['type'] in ['note', 'select_one', 'select_one yesno', 'select_multiple']}
    nx.set_node_attributes(dag, content, 'content')

# %% Convert html strings to markdown for inferiour platforms
# exclude nodes which have no content (None)
if p.platform == 'commcare':
    content = {n: md(dag.nodes[n]['content'], escape_underscores=False) for n in dag.nodes if dag.nodes[n]['type'] in [
        'note', 'select_one', 'select_one yesno', 'select_multiple'] and dag.nodes[n]['content'] is not None}
    content.update({n: dag.nodes[n]['name'] for n in dag.nodes if dag.nodes[n]['type'] in [
                   'note', 'select_one', 'select_one yesno', 'select_multiple'] and dag.nodes[n]['content'] is None})
    nx.set_node_attributes(dag, content, 'content')
    # next step so that for missing files, there is the filename at least


# %% Move from graph to dataframe
df = oh.dag_to_df(dag)

# sort the dataframe according to the CDSS topo sorting
df = df.reindex(topo_order)

# types to be kept in df
types = ['decimal', 'integer', 'diagnosis', 'select_multiple', 'select_one', 'calculate',
         'note', 'select_one yesno', 'container_page']

df.drop(df.loc[~df['type'].isin(types)].index, inplace=True)

# %% Group page-elements
'''The sorting is ignoring pages, therefore we group them independently here.'''
# TODO Commented out MPEA
# df = oh.group_pages(df)

df.drop(columns=['group'], inplace=True)

# %% Make df conform to odk
df = oh.frame_to_odk(df, p.drugsfile, p.form_id)

# %% Add the header specific for defined platform (such as CHT)
'''The merge script that would add the dx part, cleans this away'''
df = oh.add_header(df, p.headerfile)
# %% Update relevance expression of caretaker advice messages
d = ca.ca_expressions(df_raw, p.cafile)
df = ca.update_ca_relevance(df, d)

# %% For CHT put help fields in a standard note field, just below the row the help is attached to
# necessary for CHT but not for Commcare because it natively supports help pop up fields
if p.platform == 'cht':
    df = oh.helpfields_tt(df)
# %% Make a settings tab
now = datetime.now()
version = now.strftime('%Y%m%d%H%M')
indx = [[1]]

settings = {'form_title': p.form_title, 'form_id': p.form_id,
            'version': version, 'default_language': 'en', 'style': 'pages'}
df_settings = pd.DataFrame(settings, index=indx)
df_settings.head()

# %% Add select_diagnosis and data_load to df_choices
'''Currently done by hand, later based on graph. See issue posted on github'''


def diagnosis_to_dfchoices(dag, df_choices, listname):
    d = {n: dag.nodes[n] for n in dag.nodes if 'type' in dag.nodes[n] and (
        dag.nodes[n]['type'] == 'select_option') and (dag.nodes[n]['group'] == listname)}
    df_select_diagnosis = pd.DataFrame.from_dict(d, orient='index')
    df_select_diagnosis = df_select_diagnosis[['group', 'name', 'content']]
    df_select_diagnosis.rename(
        columns={'group': 'list_name', 'content': 'label::en'}, inplace=True)
    df_choices = pd.concat([df_select_diagnosis, df_choices])

    return df_choices


if p.activity == 'treatment':
    # a diagnosis selector is only for treatment (will take this out there, too)
    df_choices = diagnosis_to_dfchoices(dag, df_choices, 'select_diagnosis')


df_choices = diagnosis_to_dfchoices(dag, df_choices, 'data_load')

# %% Make a summary  -> for treatment, this has moved to the DX jupyter script, because there you get the real relevance for diagnosis

'''The summary is built based on the triggered diagnosis. It is built here and saved to disk. 
It is then re-used by the merge script'''
'''
import summary
df_summary = summary.make_summary(df, df_choices, diagnosis_id_hierarchy, p.summaryfile)

# store df_summary
import pickle

with open(p.folder+'df_summary.pickle', 'wb') as handle:
    pickle.dump(df_summary, handle, protocol=pickle.HIGHEST_PROTOCOL)
'''
# %% Write xls form to file
df2xlsform(df, df_choices, df_settings, p.output_xls)

# %% Convert xlsform to xform
if p.platform == 'commcare':
    xls2xform(p.output_xls, p.output_xml)

# %% Make xform compatible to Commcare
if p.platform == 'commcare':
    xt.xform2commcare(p.output_xml, p.output_commcare)

# %% Compile and upload into local CHT instance
'''
if p.platform == 'cht':
    import os
    os.system('cd /home/rafael/cht-local-setup/upgrade/cht-core/config/ecare/ | cht --url=https://medic:password@localhost --accept-self-signed-certs convert-app-forms upload-app-forms -- almsom')

'''
