#!/usr/bin/env python3
import csv
from math import sin, pi, cos
from itertools import starmap
from matplotlib import pyplot as plt
import matplotlib.tri as tri
import numpy as np

def torad(deg):
	return sum(
		starmap(
			lambda i, x: int(x)/60**i,
			enumerate(filter(
				lambda x:x,
				deg.split('°')
			))
		)
	)*pi/180

def to4(num):
	return '%.4f'%num

ref = {
	'a': {
		'x': 714050,
		'y': 2153903,
		'z': 1210,
	},
	'b': {
		'x': 714019.4561,
		'y': 2153895.9484,
		'z': 1223.9183,
	},
}

if __name__ == '__main__':
	reader = csv.reader(open('data.csv'))
	writer = csv.writer(open('res.csv', 'w'))

	lines = []

	# Used for plotting
	x_data = []
	y_data = []
	titles = []

	for line in reader:
		H   = float(line[4]) - float(line[6])
		D   = 100*H*sin(torad(line[3]))**2
		P_x = D*sin(torad(line[7]))
		P_y = D*cos(torad(line[7]))
		P_z = 100*H*cos(torad(line[3]))*sin(torad(line[3])) + float(line[1]) - float(line[5])

		coord_x = ref[line[8]]['x'] + P_x
		coord_y = ref[line[8]]['y'] + P_y
		coord_z = ref[line[8]]['z'] + P_z

		lines.append([
			line[0],               # PV
		] + list(map(to4, [
			H,                     # H
			D,                     # D
			P_x, # P_x
			P_y, # P_y
			P_z,                   # P_z
			coord_x,
			coord_y,
			coord_z,
		])))

		x_data.append(coord_x)
		y_data.append(coord_y)
		titles.append(line[0])

	print('X max:', max(x_data), 'X min', min(x_data))
	print('Y max:', max(y_data), 'Y min', min(y_data))

	writer.writerows(lines)

	# Center and scale
	x_points = np.array(x_data) - np.mean(x_data)
	y_points = np.array(y_data) - np.mean(y_data)

	# make delaunai triangulation
	triangulation = tri.Triangulation(x_points, y_points)
	plt.triplot(triangulation, 'bo-')

	# Now the plotting thing
	plt.plot(x_points, y_points, 'o')

	for x, y, t in zip(x_points, y_points, titles):
		plt.text(x, y, t)

	plt.show()
