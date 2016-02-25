#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser(
	description='Pixelizes depth map for use in the sad robot',
	epilog='Example: python main.py ./test/face2_small.jpg ./output/out -s 4')

# name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
# action - The basic type of action to be taken when this argument is encountered at the command line.
# nargs - The number of command-line arguments that should be consumed.
# const - A constant value required by some action and nargs selections.
# default - The value produced if the argument is absent from the command line.
# type - The type to which the command-line argument should be converted.
# choices - A container of the allowable values for the argument.
# required - Whether or not the command-line option may be omitted (optionals only).
# help - A brief description of what the argument does.
# metavar - A name for the argument in usage messages.
# dest - The name of the attribute to be added to the object returned by parse_args().

parser.add_argument('image',
				metavar='input image', 
				type=str, 
				nargs=1,
                help='Input depth map')

parser.add_argument('output',
				metavar='output file', 
				type=str, 
				nargs=1,
                help='Sets output path for generated OpenSCAD face')

parser.add_argument('-d', '--depth',
				metavar='z-depth', 
				type=int, 
				nargs=1,
                help='Z-axis resolution',
                required=False,
                default=[255])

parser.add_argument('-s', '--subsample',
				metavar='subsampling', 
				type=int, 
				nargs=1,
                help='Amount of x/y-axis subsampling to apply',
                required=False,
                default=1)

parser.add_argument('-v', '--visualize',
	help='Sets whether or not to visualize the generation process',
	action='store_true', default=False)