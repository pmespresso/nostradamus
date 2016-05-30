#!/usr/bin/env python

import os
import sys

from clarifai.client import ClarifaiApi

images = []

def tag_images_in_directory(path, api):

	path = path.rstrip(os.sep)
	print("Stripped path is: " + path)

	for file_name in os.listdir(path):

		images.append((open(os.path.join(path, file_name), 'rb'), file_name))
	return api.tag_images(images)


def format_tags_with_filenames(clarifai_response, images):
	"""
	So what this should do is take the response given from tagging
	and map each filename to an array of the top 5 response's tags for the image.

	eg. {	"screenshot1.jpg": ["hot", "girl", "model", "young", "brunette"],
			"screenshot2.jpg": ["ugly", "boy", "beast", "abonmination", "awful"] 
		}

	"""
	image_and_tags_dict = {}

	i=0

	while i < len(images):

		image_and_tags_dict[str(images[i])] = clarifai_response['results'][i]['result']['tag']['classes'][0:5]
		i += 1

	print(image_and_tags_dict)

def rename_images_in_directory_with_tags():
	"""
		This should take each key in the output of format_tags_with_filenames()

		Then output a directory of the input files that have been renamed in order
		of their top5 tags. 

		eg. 
		- output_dir
			- hot_girl_model_young_brunette.jpg
			- ugly_boy_beast_abomination_awful.jpg
	"""




def main(argv):
  if len(argv) > 1:
    imageurl = argv[1]
  else:
    imageurl = 'http://clarifai-img.s3.amazonaws.com/test/toddler-flowers.jpeg'
    print("We will be using the default since you provided no local directories")

  api = ClarifaiApi()

  if imageurl.startswith('http'):
    response = api.tag_image_urls(imageurl)

  elif os.path.isdir(imageurl):
    response = tag_images_in_directory(imageurl, api)

    format_tags_with_filenames(response, images)

  elif os.path.isfile(imageurl):
    with open(imageurl,'rb') as image_file:
      response = api.tag_images(image_file)

  else:
    raise Exception("Must input url, directory path, or file path")

  # print(response)


if __name__ == '__main__':
  main(sys.argv)