#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, sys, shutil
from fuzzywuzzy import fuzz

sys.path.append('../lib/python')
from graphs import plot_data_to_file

# data source
current_data = '../data/31.03.2016.csv'
hyperlink = 'https://www.gov.uk/government/publications/private-finance-initiative-and-private-finance-2-projects-2016-summary-data'

# html paths
html_file = '../index.html'
plot_file = '../data/plot_data.json'

def make_link(link, nodes, source, target):
    """
    Utility function to make a link between two nodes
    """

    link['source'] = nodes.index(source)
    link['target'] = nodes.index(target)
    return link

def data_to_dict():
	"""
	Read in the data source, convert header names and row/column values into a list of dictionaries.
	One dictionary per project.
	"""
	pfi_data = []
	
	with open(current_data, 'rb') as data:
		reader = csv.reader(data)

		# skip empty header before the real header
		next(reader, None)
		headers = next(reader, None)

		for row in reader:

			project_data = {}

			for idx, column in enumerate(row):
				project_data[headers[idx]] = column

			# append to pfi_data
			pfi_data.append(project_data)

	return pfi_data

def prepare_plot_data(parsed_data):
	"""
	For every project, make a graph node. For all it's equity partners, make a node and link it to
	the project node.

	An attempt is made to match differently spelt equity partners, so that multiple nodes dont exist
	for what is essentially the same company / equity partner
	"""
	data = {'nodes' : [], 'links' : []}

	for d in parsed_data:

		# get the department name
		pfi_department_name = d['Department']

		# create the department dictionary and add to data
		department_node = {'name' : pfi_department_name, 'hovertext' : pfi_department_name, 'size' : 60, 'color' : 'red'}

		if not department_node in data['nodes']:
			data['nodes'].append(department_node)

		# get the name and the capital value of the project
		pfi_project_name = d['Project Name'] + ' - [ £' + str(d['Capital Value (£m)']) + 'm ]'

		# create the node dictionary and add to data
		project_node = {'name' : '', 'hovertext' : pfi_project_name, 'size' : 20, 'color' : 'orange'}
		data['nodes'].append(project_node)

		# link the project and department
		link = make_link({}, data['nodes'], project_node, department_node)
		data['links'].append(link)

		# potentially six equity partners
		for num in ['1', '2', '3', '4', '5', '6']:

			equity_partner = 'Equity Holder %s: Name' % num

			if equity_partner in d.keys():

				if d[equity_partner] != '':

					# create the equity partner node dictionary
					equity_name = d[equity_partner]
	                partner_node = {'name' : '', 'hovertext' : equity_name, 'size' : 10, 'color' : 'yellow'}

	                # lets check they dont already exist
	                found = partner_node
	                for each in data['nodes']:
	                	if fuzz.token_set_ratio(equity_name, each['hovertext']) >= 90:
	                		found = each
	                		# they exist already, lets increase the size
	                		each['size'] += 0.5

	                if found == partner_node:
	                	data['nodes'].append(found)

	                # make a link between the project and equity partner
	                link = make_link({}, data['nodes'], project_node, found)
	                if link not in data['links']:
	                	data['links'].append(link)

	return data

def write_file(html):
	"""
	write out the index.html file
	"""

	# copy the top
	shutil.copy2(top_html, html_file)

	# insert the plot div
	with open(html_file, "a") as myfile:
		myfile.write(html.encode("utf8"))

	# write the tail
	with open(html_file, "a") as fo:
		with open(tail_html, 'r') as fi:
			fo.write(fi.read())

data_dicts = data_to_dict()
plot_data = prepare_plot_data(data_dicts)
html = plot_data_to_file(plot_data, plot_file, hyperlink)

shutil.copy2('../lib/html/index.html', '../index.html')
