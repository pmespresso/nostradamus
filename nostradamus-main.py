#!/usr/bin/env python

import os
import sys
import fnmatch

from clarifai.client import ClarifaiApi

images = []
image_and_tags_dict = {}
global_path = ""

def tag_images_in_directory(path, api):

	global_path = path.rstrip(os.sep)
	print("Stripped path is: " + path)

	for file_name in os.listdir(path):

		images.append((open(os.path.join(path, file_name), 'rb+'), file_name))
	return api.tag_images(images)


def format_tags_with_filenames(clarifai_response, images):
	"""
	So what this should do is take the response given from tagging
	and map each filename to an array of the top 5 response's tags for the image.

	eg. {	"screenshot1.jpg": ["hot", "girl", "model", "young", "brunette"],
			"screenshot2.jpg": ["ugly", "boy", "beast", "abonmination", "awful"] 
		}

	"""
	i=0
	while i < len(images):
		image_and_tags_dict[str(images[i][1])] = clarifai_response['results'][i]['result']['tag']['classes'][0:5]
		i += 1
	return image_and_tags_dict

def rename_images_in_directory_with_tags(image_and_tags_dict, path):
	"""
		This should take each key in the output of format_tags_with_filenames()

		Then output a directory of the input files that have been renamed in order
		of their top5 tags. 

		eg. 
		- output_dir
			- hot_girl_model_young_brunette.jpg
			- ugly_boy_beast_abomination_awful.jpg
	"""
	# print()
	# print(type(image_and_tags_dict[]))
	for fname in os.listdir(path):

		os.rename(path + "/" + fname, path + "/" + str.join("_", image_and_tags_dict[fname]) + ".png")
		print(fname)

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
    tags_list = tag_images_in_directory(imageurl, api)


    # this is a list of lists
    # you get simply something like ['hot', 'girl', 'model', 'young', 'brunette']
    # so take that, join it as one string with _ between each word 
    # and rename each file accordingly. 

    response = rename_images_in_directory_with_tags(format_tags_with_filenames(tags_list, images), imageurl)


  elif os.path.isfile(imageurl):
    with open(imageurl,'rb') as image_file:
      response = api.tag_images(image_file)

  else:
    raise Exception("Must input url, directory path, or file path")

  # print(response)


if __name__ == '__main__':
  main(sys.argv)