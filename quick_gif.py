#!/usr/bin/python

import sys, os, argparse, subprocess, shutil
from PIL import Image, ImageFont, ImageDraw

def drawText(draw, x, y, text, font):
		# black outline
		draw.text((x-1, y),text,(0,0,0),font=font)
		draw.text((x+1, y),text,(0,0,0),font=font)
		draw.text((x, y-1),text,(0,0,0),font=font)
		draw.text((x, y+1),text,(0,0,0),font=font)

		# white text
		draw.text((x, y),text,(255,255,255),font=font)

def main():
	directory = "screenshots"

	parser = argparse.ArgumentParser(description='Create a gif.')
	parser.add_argument('-f', '--file', required=True, help='input video file')
	parser.add_argument('-s', '--start', type=int, required=True, help='start time in seconds')
	parser.add_argument('-e', '--end', type=int, required=True, help='end time in seconds')
	parser.add_argument('-o', '--output', type=str, nargs='?', default='output.gif', help='name of the output file')
	parser.add_argument('--text', type=str, nargs='?', help='text to put on the bottom of the gif')
	parser.add_argument('--fontsize', type=int, nargs='?', default=16, help='the size of the font to use for the gif')
	parser.add_argument('--padding', type=int, nargs='?', default=5, help='the amount of distance from the bottom the text should appear')
	args = parser.parse_args()

	if not os.path.exists(directory):
		os.makedirs(directory)

	subprocess.call(['ffmpeg', '-i', args.file, '-ss', str(args.start), '-to', str(args.end), os.path.join(directory, 'image-%05d.png')])

	if args.text:
		file_names = sorted((fn for fn in os.listdir(directory)))
		images = []
		font = ImageFont.truetype("fonts/DejaVuSansCondensed-BoldOblique.ttf", args.fontsize)

		for f in file_names:
			image = Image.open(os.path.join(directory,f))
			draw = ImageDraw.Draw(image)

			# reddit tells me this patten sucks, but I like it
			try:
					image_size
			except NameError:
					image_size = image.size

			text_size = font.getsize(args.text)
			x = (image_size[0]/2) - (text_size[0]/2)
			y = image_size[1] - text_size[1] - args.padding
			drawText(draw, x, y, args.text, font)
			image.save(os.path.join(directory,f))

	# for some reason when I tried this with an array it didn't like my 0?
	subprocess.call('convert -loop 0 ' + os.path.join(directory, '*') + ' ' + args.output, shell=True)

	shutil.rmtree(directory)

if __name__ == '__main__':
	main()