import argparse
import random
from shutil import copyfile
import sys
import logging
import os

PROGRAM_INTRO='''
Code Memorizer: help you to memorize code

This program replaces some code lines to the blank comment lines.
If you have such a good example source code that you really want to memorize it,
you can remove some lines of the example source with this program and fill out the blank lines.
First try level 1 (replace only one line) and then try higher levels.
(This program removes only real source code, not comment or too short line)
'''

CODELINE_MIN = 10
BACKUP_POSTFIX = ".memory.bak"
SKIP_COMMENT = "codememory:skip"

def check_codeline(line, prefix):
    global CODELINE_MIN

    l = line.replace(" ", "")
    if len(l) < CODELINE_MIN:
        return False
    if l.startswith(prefix):
        return False
    if SKIP_COMMENT in l:
        return False
    return True

def count_codelines(lines, prefix: str):
    count = 0

    for l in lines:
        if check_codeline(l, prefix):
            count += 1
    return count

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(description=PROGRAM_INTRO,
        usage='python {} [OPTIONS]... SOURCE-FILE'.format(__file__),
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-l', '--level', help='how many lines to be commented', default=1)
    parser.add_argument('-p', '--prefix', help='string with which comment starts', default='//')
    parser.add_argument('-o', '--output', help='do not replace source file and write result to another file',
        default='')
    parser.add_argument('filename', help='file to memorize')

    args = parser.parse_args()
    logging.debug("level=%s", args.level)
    logging.debug("prefix=%s", args.prefix)
    logging.debug("output=%s", args.output)
    logging.debug("sourcefile=%s", args.filename)

    source_file = args.filename.strip()
    level = int(args.level)
    prefix = args.prefix

    if len(args.output) == 0:
        backup_file = source_file + BACKUP_POSTFIX
        logging.info("output file is not specified, then replace the source file")
        # If a backup file exist, the source file is already modified.
        # So it has to revert the source file, and then do replacing.
        if os.path.isfile(backup_file):
            logging.debug("revert source file to a backup file:%s", backup_file)
            copyfile(backup_file, source_file)
        else:
            logging.debug("make a backup file:%s", backup_file)
            copyfile(source_file, backup_file)
        output = source_file
    else:
        logging.info("write output file=%s", args.output)
        output = args.output

    f = open(source_file)
    lines = f.readlines()
    f.close()

    num_codelines = count_codelines(lines, prefix)
    if level >= int(num_codelines / 2):
        logging.error('You tried too high level, please try again with lower level')
        sys.exit(1)

    logging.debug("extract only codeline=%d/%d",num_codelines, len(lines))

    num_removelines = random.sample(range(1, num_codelines), level)
    logging.debug("remove line-numbers:{}".format(' '.join(map(str, num_removelines))))

    f = open(output, "w")
    lcount = 0
    for l in lines:
        if check_codeline(l, prefix):
            lcount += 1
            if lcount in num_removelines:
                f.write(prefix + " ADD CODE HERE!!!!!!!!!!!!!!!!!\n")
                continue
        f.write(l)

