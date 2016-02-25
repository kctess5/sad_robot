#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from cli import parser
import skimage
from skimage import io, transform, color, exposure
import os
import matplotlib.pyplot as plt
import numpy as np
import random
from jinja2 import Template, Environment, DictLoader, ChoiceLoader, FileSystemLoader


FLICKERED_COLORS = [{
	"color": "[.7,.95,1]",
	"inclusion_prob": .1
},{
	"color": "[.1,.4,.95]",
	"inclusion_prob": .1
}]
SOLID_COLORS = ["[.7,.95,1]", "[.2,.6,.95]"]

FLICKER_SPEED = 20

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
def get_template():
	j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
	return j2_env.get_template('face.template')

def min_neighbor(x, y, image, subsample):
	samples = (
		(y, x + subsample),
		(y, x - subsample),
		(y + subsample, x),
		(y - subsample, x),
		# corners
		(y + subsample, x + subsample),
		(y - subsample, x + subsample),
		(y + subsample, x - subsample),
		(y - subsample, x - subsample)
	)

	min_val = 10000000000;

	for sample in samples:
		# pixel is on edge, reutn
		if (sample[0] >= image.shape[0] or sample[0] < 0 \
			or sample[1] >= image.shape[1] or sample[1] < 0):
			return 0
		else:
			# pixel is surrounded by neighbors
			min_val = min(min_val, image[sample[0], sample[1]])

	return min_val


def pick_color():
	r = random.random()
	for fg in range(len(FLICKERED_COLORS)):
		inclusion_prob = FLICKERED_COLORS[fg]["inclusion_prob"]
		if r < inclusion_prob:
			return False, fg
		r = r - inclusion_prob

	return True, random.choice(range(len(SOLID_COLORS)))

def generate_face(image, subsample, depth, flicker=1):
	height = image.shape[0]
	width = image.shape[1]

	voxels = {
		"solid": {},
		"flickered": {}
	}

	for c in range(len(SOLID_COLORS)):
		voxels["solid"][c] = []

	for c in range(len(FLICKERED_COLORS)):
		voxels["flickered"][c] = []

	assignments = {
		"solid_colors": SOLID_COLORS,
		"flickered": []
	}
	breakpoints = np.linspace(0,1,flicker+1)

	for i in xrange(0, flicker):
		assignments["flickered"].append({
			'min': breakpoints[i],
			'max': breakpoints[i+1],
			'colors': map(lambda x: x["color"], sorted(FLICKERED_COLORS, key=lambda k: random.random()))
		})

	# generate list of voxels necessary
	for x in xrange(0,width, subsample):
		for y in xrange(0,height, subsample):
			first_voxel = image[y, x]
			last_voxel = min_neighbor(x, y, image, subsample)

			back = first_voxel

			while back > last_voxel - 1 and back > -1:
				is_solid, group_number = pick_color()

				voxel = {
					'x': x / subsample,
					'y': y / subsample,
					'z': back
				}
				if is_solid:
					voxels["solid"][group_number].append(voxel)
				else:
					voxels["flickered"][group_number].append(voxel)

				back = back - 1

	flat_voxels = {
		"solid": {},
		"flickered": {}
	}

	for c in range(len(SOLID_COLORS)):
		flat_voxels["solid"][c] = []

	for c in range(len(FLICKERED_COLORS)):
		flat_voxels["flickered"][c] = []

	for x in xrange(0,width, subsample):
		for y in xrange(0,height, subsample):
			is_solid, group_number = pick_color()

			voxel = {
				'x': x / subsample,
				'y': y / subsample,
				'z': 0
			}
			if is_solid:
				flat_voxels["solid"][group_number].append(voxel)
			else:
				flat_voxels["flickered"][group_number].append(voxel)

	# if len(voxels) > 4000:
	# 	print "Warning: Number of voxels exceeds 4000, OpenSCAD may fail to render the whole thing."

	# generate openscad source code
	return get_template().render(
		assignments=assignments,
		voxel_groups=voxels, 
		flat_voxels=flat_voxels,
		width=width/subsample, 
		height=height/subsample, 
		depth=depth)

def save(image, path):
	out_img = exposure.rescale_intensity(image, \
		out_range=(0,1))
	io.imsave(path, out_img)

def main():
	args = vars(parser.parse_args())
	filename = os.path.join(os.getcwd(), args["image"][0])

	image = skimage.img_as_uint(color.rgb2gray(io.imread(filename)))

	subsample = 1

	if (not args["subsample"] == 1):
		subsample = args["subsample"][0]

		image = transform.downscale_local_mean(image, (subsample, subsample))
		image = transform.pyramid_expand(image, subsample, 0, 0)

	image = exposure.rescale_intensity(image, out_range=(0,args["depth"][0]))

	if (args["visualize"]):
		io.imshow(image)
		io.show()

	source = generate_face(image, subsample, args["depth"][0], FLICKER_SPEED)

	if source:
		with open(args["output"][0], 'w') as file_:
			file_.write(source)
	else:
		print "Attempted to generate source code, failed."

if __name__ == "__main__":
	main()
