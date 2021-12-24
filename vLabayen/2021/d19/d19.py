#!/bin/python3
from collections import defaultdict
import re
import math
import numpy as np
from itertools import combinations

scanner_rgx = re.compile('--- scanner ([0-9]+) ---')
beacon_rgx  = re.compile('(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)')
def parse(file):
	scanners = defaultdict(list)
	with open(args.file, 'r') as f:
		for line in (l.strip() for l in f):
			if m := scanner_rgx.match(line):
				current_scanner = int(m.group(1))
				continue

			if m := beacon_rgx.match(line):
				coords = tuple(int(v) for v in m.groups())
				scanners[current_scanner].append(coords)
	return scanners


# python math.sin & math.cos can lead to small decimal numbers instead of 0
def sin(angle): return round(math.sin(math.pi * angle / 180))
def cos(angle): return round(math.cos(math.pi * angle / 180))

# As np.array/np.matrix are no hasheable, prepare translations matrix <--> set
def array2tuple(a) : return tuple(a)
def tuple2array(t) : return np.array(t)
def matrix2tuple(m): return tuple(tuple(row) for row in m)
def tuple2matrix(t): return np.matrix(t)

# https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
def rz(gamma): return np.array([
	[cos(gamma), -sin(gamma), 0],
	[sin(gamma),  cos(gamma), 0],
	[0         ,  0,          1]
])
def ry(beta): return np.array([
	[cos(beta) , 0, sin(beta)],
	[0,         1,         0],
	[-sin(beta), 0, cos(beta)]
])
def rx(alpha): return np.array([
	[1,          0,           0],
	[0, cos(alpha), -sin(alpha)],
	[0, sin(alpha),  cos(alpha)]
])
# https://stackoverflow.com/a/11839620
def r(gamma, beta, alpha): return matrix2tuple(rz(gamma) @ ry(beta) @ rx(alpha))

def rotation_matrices():
	angle_gen = ((gamma, beta, alpha) for alpha in range(0, 360, 90) for beta in range(0, 360, 90) for gamma in range(0, 360, 90))
	unique_matrices = {r(*angles) for angles in angle_gen}
	return [np.array(m) for m in unique_matrices]

def rotate(arr, rot_matrix): return arr @ rot_matrix
def rotate_beacons(beacons, rot_matrix): return [beacon @ rot_matrix for beacon in beacons]
#def unrotate_beacons(beacons, rot_matrix): return [beacon @ rot_matrix.transpose() for beacon in beacons]

# relative + offset = measured ----> relative = measured - offset
def beacons_relative_to_each_other(beacons): return [{'offset': (x,y,z), 'beacons': [np.array((_x - x,_y - y,_z - z)) for _x,_y,_z in beacons]} for x,y,z in beacons]
def unoffset(x_offset, y_offset, z_offset, x_relative, y_relative, z_relative): return (x_offset + x_relative, y_offset + y_relative, z_offset + z_relative)

def search_match(beacons_scanner_a, beacons_scanner_b, rm):
	for beacons_scanner_a_rel_beacon_i in beacons_scanner_a:
		offset_to_beacon_i = beacons_scanner_a_rel_beacon_i['offset']
		bsarbi = {array2tuple(beacon) for beacon in beacons_scanner_a_rel_beacon_i['beacons']}				# np.array to set

		for beacons_scanner_b_rel_beacon_j in beacons_scanner_b:
			offset_to_beacon_j = beacons_scanner_b_rel_beacon_j['offset']
			bsbrbj = beacons_scanner_b_rel_beacon_j['beacons']							# keep as np.array to rotate

			for rot_matrix in rm:
				rotated_bsbrbj = {array2tuple(beacon) for beacon in rotate_beacons(bsbrbj, rot_matrix)}		# np.array to set
				intersect = bsarbi.intersection(rotated_bsbrbj)
				if len(intersect) >= 12:
					# Unoffset all the beacons relative to the first scanner
					all_beacons_in_scanner_pair = bsarbi.union(rotated_bsbrbj)
					all_unoffset_beacons = [unoffset(*offset_to_beacon_i, *beacon) for beacon in all_beacons_in_scanner_pair]

					rotated_offset_to_beacon_j = rotate(offset_to_beacon_j, rot_matrix)
					j_x, j_y, j_z = rotated_offset_to_beacon_j
					i_x, i_y, i_z = offset_to_beacon_i
					between_scanners_offset = (i_x - j_x, i_y - j_y, i_z - j_z)

					return between_scanners_offset, all_unoffset_beacons
	return None, None

def p1(args):
	scanners = {scanner_n : beacons_relative_to_each_other(beacons) for scanner_n, beacons in parse(args.file).items()}
	rm = rotation_matrices()

	while len(scanners) > 1:
		scanner_combinations = combinations(list(scanners.keys()), 2)
		for scanner_a, scanner_b in scanner_combinations:
			_, match = search_match(scanners[scanner_a], scanners[scanner_b], rm)
			if match is not None:
				scanners[scanner_a] = beacons_relative_to_each_other(match)
				del scanners[scanner_b]

				print(f'Match between scanner {scanner_a} and {scanner_b}. {len(scanners)} scanners remaining. Beacons list size: {len(match)}')
				break				# Exit the combinations loop and restart with the expanded scanner

		else: break	# No matches were found

	print(sum(len(scanner_rel_beacons[0]['beacons']) for scanner_rel_beacons in scanners.values()))

def manhattan_distance(s1_x, s1_y, s1_z, s2_x, s2_y, s2_z): return abs(s1_x - s2_x) + abs(s1_y - s2_y) + abs(s1_z - s2_z)

def p2(args):
	scanners = {scanner_n : beacons_relative_to_each_other(beacons) for scanner_n, beacons in parse(args.file).items()}
	rm = rotation_matrices()

	offsets = []
	while len(scanners) > 1:
		scanner_combinations = combinations(list(scanners.keys()), 2)
		for scanner_a, scanner_b in scanner_combinations:
			offset, match = search_match(scanners[scanner_a], scanners[scanner_b], rm)
			if match is not None:
				scanners[scanner_a] = beacons_relative_to_each_other(match)
				del scanners[scanner_b]
				offsets.append(offset)

				print(f'Match between scanner {scanner_a} and {scanner_b}. {len(scanners)} scanners remaining. Beacons list size: {len(match)}')
				break

		else: break

	print(sum(len(scanner_rel_beacons[0]['beacons']) for scanner_rel_beacons in scanners.values()))
	print(max(manhattan_distance(*offset1, *offset2) for offset1, offset2 in combinations(offsets, 2)))

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	args = parser.parse_args()

#	p1(args)
	p2(args)
