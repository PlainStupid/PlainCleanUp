import os
import re


def down_clean_up(dirty_dir):

    # type of files we want to sort
    extensions = ['.avi', '.mp4', '.mkv', '.mpg', '.srt', '.mp3', '.m4v', '.sub', '.divx', '.rm']
    # type of files we want to delete
    junk = ['.torrent', '.nfo', '.dat', '.url', '.txt', '.sfv', '.idx']
    # type of files we want to put in the CoverArt folder
    pictures = ['.png', '.jpg']

    # temp storage for our data
    videos = []

    # change current working directory to the directory that is to be sorted
    os.chdir(dirty_dir)

    # crawl through every file in the dirty directory
    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:
            # name of current file
            file_name_with_extension = os.path.relpath(file)
            # the absolute path to the current file
            abs_path = os.path.abspath(subdir + '\\' + file_name_with_extension)
            # get file extension
            file_name, file_extension = os.path.splitext(file_name_with_extension)
            # only care about video files
            if file_extension.strip() in extensions or file_extension.strip() in pictures:

                info = get_info(file_name)

                if file_extension in pictures:
                    # [[season, episode]/False, name of show, absolute path, original name of file]
                    videos.append(['picture', info[1], abs_path, file_name_with_extension])
                else:
                    # [[season, episode]/False, name of show, absolute path, original name of file]
                    videos.append([info[0], info[1], abs_path, file_name_with_extension])

    # make a clean directory if it doesnt exist already
    os.chdir('..')
    if not os.path.exists('clean'):
        os.makedirs('clean')

    # change current working directory to the new clean directory
    os.chdir('clean')

    # order shows to the clean folder according to name and season
    for video in videos:

        # check if we have a movie/show/picture
        if video[0]:
            if video[0] == 'picture':
                destination = os.path.abspath('..\\CoverArt')
            else:
                destination = os.path.abspath(video[1]) + '\\' + 'season' + video[0][0]
        else:
            destination = os.path.abspath(video[1])

        # make destination folder if it doesnt exist already
        if not os.path.exists(destination):
            os.makedirs(destination)

        file_path = destination + '\\' + video[3]

        # move file to destination folder if there is no duplicates
        if not os.path.isfile(file_path):
            os.rename(video[2], file_path)

    # go back to dirty directory
    os.chdir('..')
    os.chdir(dirty_dir)

    # delete all junk
    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:

            # get absolute path and extension
            abs_path = os.path.abspath(subdir + '\\' + file)
            extension = os.path.splitext(file)[1]

            # check if junk extension
            if extension.strip().lower() in junk:
                os.remove(abs_path)

    # remove all empty dirs
    # TODO: Fix this
    remove_all_empty_dirs(os.getcwd())
    remove_all_empty_dirs(os.getcwd())
    remove_all_empty_dirs(os.getcwd())


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


def remove_all_empty_dirs(path_to_curr_dir):

    if not os.path.isdir(path_to_curr_dir):
        return

    items = os.listdir(path_to_curr_dir)

    if items:
        for item in items:
            abs_path = os.path.join(path_to_curr_dir, item)
            remove_all_empty_dirs(abs_path)

    if not items:
        os.rmdir(path_to_curr_dir)


print(down_clean_up('downloads'))