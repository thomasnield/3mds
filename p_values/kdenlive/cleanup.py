# import required module
import os
import shutil

# iterate over m4a files in other_assets directory
m4a_files = []
for filename in os.listdir('other_assets'):
    f = os.path.join('other_assets', filename)
    # checking if it is a file
    if os.path.isfile(f) and f.endswith(r".m4a"):
        m4a_files.append(f)

# create trash folder
if not os.path.exists("trash"):
    os.mkdir(r"trash")

# iterate m4a files and trash if not in kdenlive project
with open(r'p_values.kdenlive', 'r') as file:
    # read all content from a file using read()
    content = file.read()
    # check if string present or not
    for m4a_file in m4a_files:
        if m4a_file not in content:
            shutil.move(m4a_file, os.path.join('trash', m4a_file.split("/")[1]))