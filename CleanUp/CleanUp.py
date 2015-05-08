import os
import re

def down_clean_up(root):

    shows = []
    movies = []
    print(root)
    for subdir, dirs, files in os.walk(root):
        for file in files:

            file_name = os.path.relpath(file)
            abs_path = os.path.realpath(file)
            info = get_info(file_name)

            if info[0]:
                shows.append([info[0], info[1], abs_path])
            else:
                movies.append([info[1], abs_path])

    return shows

'''
:returns [se_number/False, parsed name of show/movie]
'''
def get_info(file_name):

    return [get_se_number(file_name), parse_name(file_name)]

'''
:returns 1: [Season, Episode] if file is show
         2: False             if file is movie
'''
def get_se_number(file_name):

    return [1, 1]


'''
:returns Parsed file name(string)
'''
def parse_name(file_name):
    return file_name


print(down_clean_up(os.path.dirname(os.path.realpath(__file__)) + '\\downloads'))