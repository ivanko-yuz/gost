import re
import os


def nm_run(song_name):
    regex = r"(.*?)\s-\s(.*)"
    tittle = ''
    author = ''
    matches = re.finditer(regex, song_name, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        tittle = match.groups()[0]
        author = match.groups()[1].split('.')[0]
        
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
             
            print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
    return tittle , author

