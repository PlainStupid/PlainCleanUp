import re
import os

import sys

# Regexes are in from most used to least used regex for 
# a given file pattern.
regexShow = [
        '''
        # Matches with Show.S01E10.mp4
        ^ #Beginning of a string
        (?P<ShowName>.+?) #Show name
        [\.\_\-\s]+ #If it has dot, underscore or dash

        (?:s\s*|season\s*) #Case if starts with s or season
        (?P<SeasonNumber>\d+) #Show Season number
        [. _-]*

        (?:e\s*|episode\s*) #Case if starts with e or episode
        (?P<EpisodeNumber>\d+) #Show episode number
        [. _-]*
        ''',

        '''
        # Matches Show.Name -12x12.avi
        ^
        (?P<ShowName>.+)
        #Show name
        [._-]+ # char between show name and season number
        (?P<SeasonNumber>\d+)
        #Season number
        x #x between season and episode number
        (?P<EpisodeNumber>\d+)
        #Episode number
        ''',

        '''
        # Matches Show - [01x10].mp4
        ^
        (?P<ShowName>.+)
        \s*[-]*\s*\[
        (?P<SeasonNumber>\d+) #Season number
        x
        (?P<EpisodeNumber>\d+)
        ]
        ''',

        '''
        # Matches Show.Name.812.mp4
        ^
        (?P<ShowName>.+)
        [\.\-\_\s]
        [^(\(\d\))|(x\d)]
        (?P<SeasonNumber>\d{1})
        #Season number
        (?P<EpisodeNumber>\d{2})[^(th)]
        #Episode number
        ''',

        '''
        # Matches with Show03e10.mp4
        # eg. santi-dexterd07e10.hdrip.xvid
        ^(?P<ShowName>.{2,}) #Show name
        (?P<SeasonNumber>\d.+) #Season number
        (?:e|episode)(?P<EpisodeNumber>\d+) #Episode number
        '''
        ]

ignoreRegex = {'sample': '(^|[\W_])(sample\d*)[\W_]',
               'photos': '^AlbumArt.+{.+}'}

videoextensions = [ 'avi', 'mp4', 'mkv', 'mpg', '.mp3',
                    'm4v', 'divx', 'rm', 'mpeg', 'wmv',
                    'ogm', 'iso', 'img', 'm2ts', 'ts',
                    'flv', 'f4v', 'mov', 'rmvb', 'vob',
                    'dvr-ms', 'wtv', 'ogv', '3gp', 'xvid'
                    ]

subExtensions = ['srt', 'idx' 'sub']

otherExtension = ['nfo']

photoExtensions = ['jpg', 'jpeg', 'bmp', 'tbn']

junkFiles = ['.torrent', '.dat', '.url', '.txt', '.sfv']

movieFolder = 'Movies'
showsFolder = 'Shows'

def cleanUp(dirty_dir, clean_dir):
    # Absolute path to the dirty directory
    dirtyDir = os.path.abspath(dirty_dir)

    # Absolute path to the clean directory
    cleanDir = os.path.abspath(clean_dir)

    theShowDir = os.path.join(cleanDir, showsFolder)
    theMovieDir = os.path.join(cleanDir, movieFolder)

    for subdir, dirs, files in os.walk(dirtyDir):
        # Scan every file in dirtyDir
        for file in files:
            # Get the file name and its extension
            file_name, file_extension = os.path.splitext(file)

            # Absolute path to the old file
            oldFile = os.path.abspath(os.path.join(subdir, file))

            #print(oldFile)
            # Run through every regular expression, from best match to least match
            for y in regexShow:
                # First we compile the regular expression
                showReg = re.compile(y, re.IGNORECASE | re.MULTILINE | re.VERBOSE)

                # Get the show name if it exists
                showName = showReg.match(file)

                # We don't want sample files so we check if the current file is
                # a sample file
                isSample = re.search(ignoreRegex['sample'], file)

                #
                ignPhotos = re.match(ignoreRegex['photos'], file)

                # Check the shows files based on their extension and if they are not
                # a sample file
                if showName and not isSample and allowedExt(file_extension):
                    mkFullShowDir(theShowDir, showName)
                    moveTvFile(theShowDir, oldFile, showName)
                    break

                # Check the photos since we don't want all photos, eg. AlbumArt_....
                if showName and not isSample and not ignPhotos and file_extension[1:] in photoExtensions:
                    mkFullShowDir(theShowDir, showName)
                    moveTvFile(theShowDir, oldFile, showName)
                    break

                # Check if this is a movie
                if not showName and not isSample and allowedExt(file_extension):
                    mkFullMovieDir(theMovieDir)
                    moveMovieFolder(theMovieDir, oldFile)

            # Remove the file if it has junk extension
            if file_extension in junkFiles:
                if os.path.exists(oldFile):
                    os.remove(oldFile)

    # Go and clean the dirty folder, that is remove all empty folders
    cleanEmptyDirtyDir(dirtyDir)

    # Give the user a satisfying word
    print('Done')

def cleanEmptyDirtyDir(dirtyDir):
    # get number of subdirectories
    curr = len([x[0] for x in os.walk(dirtyDir)])

    while True:
        # remove all empty dirs
        remove_all_empty_dirs(dirtyDir)
        temp = len([x[0] for x in os.walk(dirtyDir)])
        # if no empty directory was found we stop
        if curr == temp:
            break
        curr = temp


def allowedExt(file_extension):
    """
    :argument File extension
    :returns Returns true if the file extension is in current extensions groups
    """
    # Get the file extension without the dot
    fileExt = file_extension[1:]

    # Return True if it exist in extensions groups
    return (fileExt in subExtensions or
            fileExt in videoextensions or
            fileExt in otherExtension)

def cleanShowName(file):
    """
    :argument Original file name(string)
    :returns Returns clean show name, eg. Show Name
    """
    return re.sub('\.|-|_', ' ', file.group('ShowName')).strip().title()

def dottedShowName(file):
    """
    :argument Original file name(string)
    :returns Returns dotted show name, eg. Show.Name
    """
    return re.sub('-|_|\s', '.', file.group('ShowName')).strip().title()

def moveMovieFolder(fullDir, file):

    newfile = os.path.basename(file)
    newFilePath = os.path.join(fullDir, newfile)

    if not os.path.isfile(newFilePath):
        os.rename(file, newFilePath)
    else:
        print('The old file exist in new path:',file)
        pass


def mkFullMovieDir(fullDir):
    if not os.path.isdir(fullDir):
        if os.path.isfile(fullDir):
            raise OSError('A file with the same name as the folder already exist: %s' % (fullDir))
        else:
            try:
                os.makedirs(fullDir)
                pass
            except:
                raise OSError('Something went wrong creating the folders: %s' % (fullDir))
    pass


def moveTvFile(clean_dir, oldFile, newFile):
    """
    :argument Path to the clean directory, old file including its path, regex file
    :returns Silently returns if exist or has been created, else raise error
    """

    # Get the clean show name - Show Name
    showName = cleanShowName(newFile)

    # And the season number
    seasonNumber = int(newFile.group('SeasonNumber'))

    # String with clean Show directory - ./clean/Show Name/
    showDirectory = os.path.join(clean_dir,showName)

    # Season string with leading zero - Season 03
    formatedSeason = 'Season %02d' %(seasonNumber)

    # Full path to the newly created clean path - ./clean/Show Name/Season ##/
    fullDir = os.path.join(showDirectory,formatedSeason)

    # Get the base name of the old file - ./dirty/Seasn9/TheFileS##E##.avi -> TheFileS##E##.avi
    oldFileName = os.path.basename(oldFile)

    # New file path to the clean folder - ./clean/Show Name/Season ##/TheFile.avi
    newFilePath = os.path.join(fullDir, oldFileName)

    # If it doesn't exist we rename it, otherwise just notify user about it
    if not os.path.isfile(newFilePath):
        os.rename(oldFile, newFilePath)
    else:
        print('The old file exist in new path:',oldFile)
        pass


def mkFullShowDir(clean_dir, file):
    """
    :argument Original file name(string)
    :returns Silently returns if exist or has been created, else raise error
    """

    # Get the clean show name - Show Name
    showName = cleanShowName(file)

    # And the season number
    seasonNumber = int(file.group('SeasonNumber'))

    # String with clean Show directory - ./clean/Show Name/
    showDirectory = os.path.join(clean_dir,showName)

    # Season string with leading zero - Season 03
    formatedSeason = 'Season %02d' %(seasonNumber)

    # Full path to the newly created clean path - ./clean/Show Name/Season ##/
    fullDir = os.path.join(showDirectory,formatedSeason)

    # Create the folder if it doesn't exist, raise error if there is a file
    # with the same name
    if not os.path.isdir(fullDir):
        if os.path.isfile(fullDir):
            raise OSError('A file with the same name as the folder already exist: %s' % (fullDir))
        else:
            try:
                os.makedirs(fullDir)
                pass
            except:
                raise OSError('Something went wrong creating the folders: %s' % (fullDir))
    pass

def remove_all_empty_dirs(path_to_curr_dir):
    """
    :argument Path to dirty directory
    :returns Nothing
    """

    # check if path exists
    if not os.path.isdir(path_to_curr_dir):
        return

    # get all items in the current directory
    items = os.listdir(path_to_curr_dir)

    # if directory is not empty, we call recursively for each item
    if items:
        for item in items:
            abs_path = os.path.join(path_to_curr_dir, item)
            remove_all_empty_dirs(abs_path)
    # Empty folder removed
    else:
        os.rmdir(path_to_curr_dir)


if __name__ == "__main__":
    cleanUp(sys.argv[1], sys.argv[2])