import re
import os


# Regexes are in from most used to least used regex for 
# a given file pattern.
regexShow = [
		'''
		# Matches with Show.S01E10.mp4
		^ #Beginning of a string
		(?P<ShowName>.+?) #Show name
		[. _-]+ #If it has dot, underscore or dash

		(?:s|season) #Case if starts with s or season
		(?P<SeasonNumber>\d+) #Show Season number
		[. _-]*

		(?:e|episode) #Case if starts with e or episode
		(?P<EpisodeNumber>\d+) #Show episode number
		[. _-]*
		''',

		'''
		# Matches with Show.01x10.mp4
		^
		(?P<ShowName>.+) #Show name
		[._-]+ # char between show name and season number
		(?P<SeasonNumber>\d+) #Season number
		x #x between season and episode number
		(?P<EpisodeNumber>\d+) #Episode number
		''',

		'''
		# Matches Show - [01x10].mp4
		^
		(?P<ShowName>.+)
		\s*-\s*\[
		(?P<SeasonNumber>\d+)
		x
		(?P<EpisodeNumber>\d+)
		]
		''',

		'''
		# Matches with Show03e10.mp4
		# eg. santi-dexterd07e10.hdrip.xvid
		^(?P<ShowName>.+) #Show name
		(?P<SeasonNumber>\d.+) #Season number
		(?:e|episode)(?P<EpisodeNumber>\d+) #Episode number
		''']

def turboScanner(s, clean_dir):
    crap = s.split('\n')

    cleanDir = os.path.abspath(clean_dir)
    print('The path to clean dir is:',cleanDir)

    for x in crap:
        for y in regexShow:
            kkk = re.compile(y,re.IGNORECASE | re.MULTILINE | re.VERBOSE)
            fff = kkk.match(x)
            if fff is not None:
                # Create new directory if it doesn't exist, group(1) is the show name
                mkShowDir(cleanDir, fff)
                #movefile(fff)
                break
    return True

def mkShowDir(clean_dir, ff):
    """
    :argument Original file name(string)
    :returns Silently returns if exist or has been created, else raise error
    """

    # Substitute dot dash and underscore with one space character
    showName = re.sub('\.|-|_', ' ', ff.group(1)).title()
    print(showName)

    showDirectory = os.path.join(clean_dir,showName)
    formatedSeason = 'Season %02d' %(int(ff.group(2)))
    seasonDirectory = os.path.join(showDirectory,formatedSeason)
    print(showDirectory)
    print(seasonDirectory)
    #if not os.path.isdir(clean_dir):
    #os.mk

    #if os.path.isdir():


print(turboScanner('''shark.tank.season02e03.hdtv.xvid-2hd.avi
Would.I.Lie.To.You.S06E05.480p.HDTV.x264-mSD.mkv
santi-dexterd07e10.hdrip.xvid
8 Out of 10 Cats s07e02 (11th Sept 2008) [PDTV (DivX)].avi
Shark.attack.01x10.hdtv.mp4
Sharsk.Ultimate-[01x10].mp4''', './Clean'))