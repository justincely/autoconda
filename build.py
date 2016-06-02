from subprocess import Popen,PIPE
import subprocess
import shutil
import re
import os
import glob
import sys

all_packages = [item for item in glob.glob('./*/') if os.path.isdir(item)]

for package in all_packages:
    print("Building {}".format(package))
    regex_pattern = '\# \$ anaconda upload (.+\.tar\.bz2)'
    process = Popen(['conda', 'build', package], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout, stderr)

    outpkg = re.findall(regex_pattern, stdout)[0]
    process = Popen(['conda', 'convert', outpkg, '-p', 'all', '-o', package], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout, stderr)

for package in all_packages:
    print("Building {}".format(package))
    process = Popen(['conda', 'build', package, '--python', '3.5'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout, stderr)

    outpkg = re.findall(regex_pattern, stdout)[0]
    process = Popen(['conda', 'convert', outpkg, '-p', 'all', '-o', package], stdout=PIPE, stderr=PIPE)
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
