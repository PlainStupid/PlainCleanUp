import os
import re


def down_clean_up(dirty_dir):

    # type of files we want to sort
    extensions = ['.avi', '.mp4', '.mkv']

    # temp storage for our data
    shows = []
    movies = []

    # change current working directory to the directory that is to be sorted
    os.chdir(dirty_dir)

    # crawl through every file in the dirty directory
    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:
            # name of current file
            file_name = os.path.relpath(file)
            # the absolute path to the current file
            abs_path = os.path.abspath(subdir + '\\' + file_name)

            # only care about video files (TODO: check other useful files like .srt)
            if file_name[-4:] in extensions:

                info = get_info(file_name)

                if info[0]:
                    # [[season, episode], name of show, absolute path, original name of file]
                    shows.append([info[0], info[1], abs_path, file_name])
                else:
                    # [name of movie, absolute path, original name of file]
                    movies.append([info[1], abs_path, file_name])

    # make a clean directory if it doesnt exist already
    os.chdir('..')
    if not os.path.exists('clean'):
        os.makedirs('clean')

    # change current working directory to the new clean directory
    os.chdir('clean')

    # order shows to the clean folder according to name and season
    for show in shows:

        destination = os.path.abspath(show[1]) + '\\' + 'season' + show[0][0]

        # make destination folder if it doesnt exist already
        if not os.path.exists(destination):
            os.makedirs(destination)

        file_path = destination + '\\' + show[3]

        # move file to destination folder if there is no duplicates
        if not os.path.isfile(file_path):
            os.rename(show[2], file_path)

    # TODO: combine these two loops more more DRYness
    # doing the exact same thing with the movies
    for movie in movies:

        destination = os.path.abspath(movie[0])

        if not os.path.exists(destination):
            os.makedirs(destination)

        file_path = destination + '\\' + movie[2]

        if not os.path.isfile(file_path):
            os.rename(movie[1], file_path)

    pass


def get_info(file_name):
    """
    :argument Original file name
    :returns [[Season, Episode]/False, Parsed name of show/movie]
    """

    return [get_se_number(file_name), parse_name(file_name)]


def get_se_number(file_name):
    """
    :argument Original file name
    :returns 1: [Season, Episode] if file is show
             2: False             if file is movie
    """

    # TODO: improve/optimise regex for finding se_number
    season = re.findall(r"(?:s|season)(\d{2})", file_name, re.I)
    episode = re.findall(r"(?:e|x|episode|\n)(\d{2})", file_name, re.I)

    if season and episode:
        return [season[0], episode[0]]
    return False


def parse_name(file_name):
    """
    :argument Original file name(string)
    :returns Parsed file name(string)
    """

    # TODO: improve/optimise regex for finding show/movie name
    names = re.findall(r"""(.*)[\._][S,s][0-9]{2}[E,e][0-9]{2}|(.*)\sS[0-9]{2}E[0-9]{2}|([^-]+)""", file_name, re.VERBOSE)

    return max(names[0],  key=len).replace('.', ' ').lower()


print(down_clean_up('downloads'))