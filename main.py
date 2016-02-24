#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from cli import parser
import skimage
from skimage import io, transform, color, exposure
import os
import matplotlib.pyplot as plt

def save(image, path):
	out_img = exposure.rescale_intensity(image, \
		out_range=(0,1))
	io.imsave(path, out_img)

def main():
	args = vars(parser.parse_args())
	filename = os.path.join(os.getcwd(), args["image"][0])

	image = skimage.img_as_uint(color.rgb2gray(io.imread(filename)))

	if (not args["subsample"] == 1):

		image = transform.downscale_local_mean(image, \
		 	(args["subsample"][0], args["subsample"][0]))

		image = transform.pyramid_expand(image, \
		 	args["subsample"][0], 0, 0)


	image_compressed = exposure.rescale_intensity(image, \
		out_range=(0,args["depth"]))

	if (args["visualize"]):
		io.imshow(image_compressed)
		io.show()

	output = os.path.join(os.getcwd(), args["output"][0] + '.png')
	save(image_compressed, output)

if __name__ == "__main__":
	main()
