#!/usr/bin

import os

images_list =   
videos_list = []
directory_name = os.getcwd()

def get_file_list(path):
  os.chdir(path)
  dir_list = filter(os.path.isdir, os.listdir(path))
  temp_list = filter(os.path.isfile,os.listdir(path))
  if len(temp_list):
    file_list.append(temp_list)

  for directory in dir_list:
    get_file_list(os.path.join(path,directory))
  return True

print get_file_list(directory_name)

