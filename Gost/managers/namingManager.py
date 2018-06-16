import re
import os


def nm_run(song_name):
    regex = r"(.*?)\s-\s(.*)-\s(.*)"
    tittle = ''
    author = ''
    style = ''
    matches = re.finditer(regex, song_name, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        author = match.groups()[0]
        tittle = match.groups()[1]
        style = match.groups()[2].split('.')[0]
        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
             
            print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
    return author, tittle, style

