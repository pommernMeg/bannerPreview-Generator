#!/usr/bin/env python

"""generator.py: Python script to create a banner preview from the images for the missions of Ingress."""

import getopt
import glob
import os
import subprocess
import sys

import PIL
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

final_size = 512

def resize_aspect_fit(folder):

	path = f"{os.getcwd()}/input/{folder}/"
	tmpFolder = f"{path}/resize/"

	dirs = os.listdir( path )

	isExist = os.path.exists(tmpFolder)
	if not isExist:
		# Create a new directory because it does not exist 
		os.makedirs(tmpFolder)

	for item in dirs:
         if item == '.DS_Store':
             continue
         if os.path.isfile(path+item):
             im = Image.open(path+item)
             f, e = os.path.splitext(tmpFolder+item)
             size = im.size
             ratio = float(final_size) / size[0]
             new_image_size = tuple([int(x*ratio) for x in size])
             im = im.resize([new_image_size[0], new_image_size[1] ], resample=5)
             new_im = Image.new("RGBA", [new_image_size[0], new_image_size[1]])
             new_im.paste(im, (0,0))
             new_im.save(f + 'resized.png', 'PNG', quality=100)

def resize_preview( outputFolder, folder, scale):
	file = f"{outputFolder}/{folder}_preview.png"

	if os.path.isfile(file):
		im = Image.open(file)
		size = im.size
		im = im.resize([int(size[0] * (scale/100)), int(size[1] * (scale/100)) ], resample=5)
		new_im = Image.new("RGBA", [int(size[0] * (scale/100)), int(size[1] * (scale/100))])
		new_im.paste(im, (0,0))
		new_im.save(f'input/{folder}/{folder}_preview.png', 'PNG', quality=100)

def main():
	args = sys.argv[1:]
	scale = 100
	try:
		opts, args = getopt.getopt(args,"h:s",["scale="])
	except getopt.GetoptError:
		print('generator.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('generator.py -s <scale>')
			sys.exit()
		elif opt in ("-s", "--scale"):
			scale = int(args[0])


	for folder in next(os.walk('input'))[1]:
		print(folder)
		outputFolder = f'output/{folder}'

		folderExist = os.path.exists(outputFolder)
		if not folderExist:
		
			resize_aspect_fit(folder)

			list_im = sorted(glob.glob(f"input/{folder}/resize/*resized.png"),reverse=True)
			imgs    = [ PIL.Image.open(i) for i in list_im ]

			print(f"Pictures in Folder: {len(list_im)}")

			lines = len(list_im) // 6
			print(f"Lines: {lines}")


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


			subprocess.run(f"rm -rf input/{folder}/resize", shell=True)

			if( scale != 100):
				resize_preview( outputFolder, folder , scale )

if __name__ == "__main__":
	main()
