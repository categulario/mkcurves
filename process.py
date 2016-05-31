#!/usr/bin/env python3
import csv
from math import sin, pi, cos
from itertools import starmap

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
	return '%.4f'%(num)

ref = {
	'a': {
		'x': 714050,
		'y': 2153903,
		'z': 1210,
	},
	'b': {
		'x': 714067.938,
		'y': 2153907.1414,
		'z': 1201.343,
	},
}

if __name__ == '__main__':
	reader = csv.reader(open('data.csv'))
	writer = csv.writer(open('res.csv', 'w'))

	lines = []

	for line in reader:
		H   = float(line[4]) - float(line[6])
		D   = 100*H*sin(torad(line[3]))**2
		P_x = D*sin(torad(line[7]))
		P_y = D*cos(torad(line[7]))
		P_z = 100*H*cos(torad(line[3]))*sin(torad(line[3])) + float(line[1]) - float(line[5])

		lines.append([
			line[0],               # PV
		] + list(map(to4, [
			H,                     # H
			D,                     # D
			P_x, # P_x
			P_y, # P_y
			P_z,                   # P_z
			ref[line[8]]['x'] + P_x,
			ref[line[8]]['y'] + P_y,
			ref[line[8]]['z'] + P_z,
		])))

	writer.writerows(lines)
