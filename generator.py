#!/usr/bin/env python

"""generator.py: Python script to create a banner preview from the images for the missions of Ingress."""

import PIL
from PIL import Image
import glob

import os, sys

#subfolders = [ f.path for f in os.scandir("input") if f.is_dir() ]

for folder in next(os.walk('input'))[1]:
	print(folder)

	list_im = sorted(glob.glob(f"input/{folder}/*"),reverse=True)
	imgs    = [ PIL.Image.open(i) for i in list_im ]

	print(f"Pictures in Folder: {len(list_im)}")

	lines = len(list_im) // 6
	print(f"Lines: {lines}")

	outputFolder = f'output/{folder}'

	# Check whether the specified path exists or not
	isExist = os.path.exists(outputFolder)

	if not isExist:
		# Create a new directory because it does not exist 
		os.makedirs(outputFolder)

	y = 544
	x = 3232
	
	new_im = Image.new("RGBA", [x, y * lines])
	temp = Image.open("template/6er maske.png")

	x = 0
	y = 0

	for i in range(1,lines +1):

		new_im.paste(temp, (x, y))
		y += 544
	
	new_im.save( f'{outputFolder}/{folder}_preview.png' )

	temp = Image.open("template/6er maske.png")

	pos_x = 0
	pos_y = 16
    
	cnt = 1

	for img in imgs:

		if (cnt % 6) == 0:
			# print("Add Picture")
			new_im.paste(img, (pos_x, pos_y))
			pos_x += img.size[0]
			# print("New Line")
			pos_x = 0
			pos_y += img.size[1]
			pos_y += 32
		
		else:
			# print("Add Picture")
			new_im.paste(img, (pos_x, pos_y))
			pos_x += img.size[0]
			pos_x += 32

		cnt += 1

	new_im.save( f'{outputFolder}/{folder}_background.png' )

	# Opening the primary image (used in background)
	img1 = Image.open(f"{outputFolder}/{folder}_background.png")
	
	# Opening the secondary image (overlay image)
	img2 = Image.open( f'{outputFolder}/{folder}_preview.png' )
	
	# Pasting img2 image on top of img1 
	# starting at coordinates (0, 0)
	img1.paste(img2, (0,0), mask = img2)

	img1.save( f'{outputFolder}/{folder}_preview.png' )

	os.remove(f"{outputFolder}/{folder}_background.png")

