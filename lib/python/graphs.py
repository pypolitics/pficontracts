# thirdparty libs
import igraph as ig
import plotly.offline as offline
import plotly.plotly as py
from plotly.graph_objs import *

def plot_data_to_file(data, hyperlink):
	"""
	Plotting library. A 3d scatter graph
	"""

	# number of nodes
	N = len(data['nodes'])

	# number of links
	L = len(data['links'])

	if L > 0:
		# for every link, create a tuple of source and target (ids, of nodes)
		Edges = [(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

		# create graph of lines
		G = ig.Graph(Edges, directed=False)

		node_color = []
		node_size = []
		node_name = []
		node_hovertext = []

		for node in data['nodes']:
			nn = node['name'].replace('_', ' ')
			node_name.append(nn)

			node_color.append(node['color'])
			node_size.append(node['size'])
			node_hovertext.append(node['hovertext'])

		# create a Kamada-Kawai layout
		layt = G.layout('kk', dim=3)
		# layt = G.layout(dim=3)

		# node co-ordinates
		Xn = [layt[k][0] for k in range(N)] # x-coordinates of nodes
		Yn = [layt[k][1] for k in range(N)] # y-coordinates
		Zn = [layt[k][2] for k in range(N)] # y-coordinates

		Xe = []
		Ye = []
		Ze = []

		for e in Edges:
		    Xe += [layt[e[0]][0],layt[e[1]][0], None] # x-coordinates of edge ends
		    Ye += [layt[e[0]][1],layt[e[1]][1], None]
		    Ze += [layt[e[0]][2],layt[e[1]][2], None]

		traces = []
		trace1_2d = Scatter3d(x = Xe,
		               y = Ye,
		               z =Ze,
		               mode = 'lines',
		               visible = True,
		               line = Line(color = 'gray', width = 3),
		               hoverinfo = 'none',
		               opacity = 0.4,
		               name = 'lines'
		               )
		traces.append(trace1_2d)

		trace2_2d = Scatter3d(x = Xn,
		               y = Yn,
		               z = Zn,
		               mode = 'markers+text',
		               name = 'nodes',
		               marker = Marker(
		                             size = node_size,
		                             color = node_color,
		                             line = Line(color = 'black', width = 2),
		                             ),
		               text = node_name,
		               textposition='middle',
		               hoverinfo = 'text',
		               hovertext = node_hovertext,
		               hoverlabel = {'bgcolor': node_color},		               
		               textfont=Font(size=12)
		               )
		traces.append(trace2_2d)
		
		axis = dict(showbackground=False,
		          showline=False,
		          zeroline=False,
		          showgrid=False,
		          showticklabels=False,
		          title='',
		          showspikes=False,
		          )

		# camera view - slight zoom in
		camera = dict(
			up=dict(x=0, y=0, z=1),
			center=dict(x=0, y=0, z=0),
			eye=dict(x=0.1, y=0.1, z=1)
			)

		layout = Layout(
			autosize=True,
			showlegend=False,
			scene=Scene(
				xaxis=XAxis(axis),
				yaxis=YAxis(axis),
				zaxis=ZAxis(axis),
				camera=camera),
			margin=Margin(
				l=10,
				r=10,
				b=20,
				t=25,
				pad=4
			),
			hovermode='closest',
			plot_bgcolor='rgba(0,0,0,0)',
			paper_bgcolor='rgba(0,0,0,0)',
			hidesources=True,
			font=Font(size=14, color="#444"),
			annotations=Annotations([
				Annotation(
					showarrow=False,
					text='<a style="color: black; font-weight: 200;"><b>Private Finance Initiative and Private Finance 2 projects: 2016 summary data</b></a>',
					xref='paper',
					yref='paper',
					x=0.5,
					y=1,
					font=Font(
						size=18, color="white")
					),
				Annotation(
					showarrow=False,
					text='<a style="color: rgb(250, 250, 250); font-weight: 100; font-size: 12px;">Data sources: </a><a href="%s">gov.uk/government/publications</a>' % hyperlink, 
					xref='paper',
					yref='paper',
					x=0,
					y=0,
					font=Font(
						size=12, color='white')
					),
			]),
				)

		data = Data(traces)
		fig = Figure(data=data, layout=layout)
		html = offline.plot(fig, auto_open=True)
		return