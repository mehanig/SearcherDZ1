from os import listdir
from os.path import isfile, join
import sys
import pymorphy2
import re
morph = pymorphy2.MorphAnalyzer()


def indexator(dirPath,outIndexFile):
    onlyfiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
    invIndex = {}
    for i in onlyfiles:
        if (i == ".DS_Store"):
            continue
        input = open(dirPath + "/" + i, 'r').read().split('\n')
        for line in input:
            line = re.sub(r'[^\w]', " ", line)
            words = filter(bool, re.split(r'[ \t\n\r, ]+', line))
            for word in words:
                word = morph.parse(word)[0].normal_form
                if word in invIndex.keys():

                    if not i in invIndex[word]:
                        invIndex[word].append(i)
                else:
                    invIndex[word] = [i]
        print("Done with " + str(i))

    with open(outIndexFile, "wt") as out_file:
        for i in invIndex.keys():
            ind_str = "\t"
            for ind in invIndex[i]:
                ind_str += str(ind) + " "
            out_file.write(str(str(i) + ind_str + '\n'))


if __name__ == '__main__':
    indexator(sys.argv[1],sys.argv[2])
