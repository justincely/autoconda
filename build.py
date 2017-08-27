import argparse
from subprocess import Popen,PIPE
import subprocess
import shutil
import re
import os
import glob
import sys

#-------------------------------------------------------------------------------

def parse_args():
    '''
    Parse command line arguments.  Returns args object.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('pkgs', type=str, nargs='*',
                        help='local package names to build and deploy, defaults to all.')

    args = parser.parse_args()
    return args

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    args = parse_args()

    if not len(args.pkgs):
        all_packages = [item for item in glob.glob('./*/') if os.path.isdir(item)]
    else:
        all_packages = args.pkgs

    for package in all_packages:
        print("Building {}".format(package))
        regex_pattern = b'anaconda upload (.+\.tar\.bz2)'
        process = Popen(['conda-build', package, '--python', '2.7', '--output-folder', 'lightcurve'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout, stderr)

        outpkg = re.findall(regex_pattern, stdout)[0]
        process = Popen(['conda', 'convert', outpkg, '-p', 'all', '-f', '-o', package], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout, stderr)

    for package in all_packages:
        print("Building {} for python".format(package))
        process = Popen(['conda-build', package, '--python', '3.5', '--output-folder', 'lightcurve'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout, stderr)

        outpkg = re.findall(regex_pattern, stdout)[0]
        process = Popen(['conda', 'convert', outpkg, '-p', 'all', '-f', '-o', package], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout, stderr)

    for package in all_packages:
        for root, dirs, files in os.walk(package):
            for filename in files:
                if not filename.endswith('.tar.bz2'):
                    continue

                file_to_upload = os.path.join(root, filename)
                process = Popen(['anaconda', 'upload', '--user', 'justincely', file_to_upload, '--force'], stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                print(stdout, stderr)
