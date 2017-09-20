import os
from datetime import datetime
import subprocess
import hashlib
import pickle


# From: https://stackoverflow.com/questions/375154/how-do-i-get-the-time-a-file-was-last-modified-in-python
def create_time_line_view(abs_file, filename):
    mod_time = os.path.getmtime(abs_file)
    mod_time = datetime.fromtimestamp(mod_time)

    year = '{:0004d}'.format(mod_time.year)
    month = '{:02d}'.format(mod_time.month)
    day = '{:02d}'.format(mod_time.day)

    mod_time = "{}-{}-{}".format(year, month, day)
    print("Modified time: {}; File: {}".format(mod_time, abs_file))

    timeline_dir = os.path.join(output_dir, mod_time)
    if not os.path.exists(timeline_dir):
        os.makedirs(timeline_dir)

    src = abs_file
    dst = os.path.join(timeline_dir, filename)

    create_symbolic_link(src, dst)


def print_path_to_link(abs_file, filename):
    print(abs_file)


# From: https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def create_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# Builds an in-memory database
# https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
def create_corpus(abs_file, filename):

    if abs_file is None or filename is None:
        return

    raw_time = os.path.getmtime(abs_file)
    mod_time = datetime.fromtimestamp(raw_time)

    year = '{:0004d}'.format(mod_time.year)
    month = '{:02d}'.format(mod_time.month)
    day = '{:02d}'.format(mod_time.day)

    mod_time = "{}-{}-{}".format(year, month, day)
    print("Modified time: {}; File: {}".format(mod_time, abs_file))
    ext = filename.split('.')[-1]
    file_size = os.path.getsize(abs_file)

    mb_threshold_bytes = 1024*1024*20     # 20 MB

    if file_size <= mb_threshold_bytes:
        md5 = create_md5(abs_file)
    else:
        md5 = '{}.{}'.format(filename, file_size)
        print("File to big for initial MD5 using: {}".format(md5))

    row = {
        'Abs Path': abs_file,
        'Extension': ext,
        'Modified.Human': mod_time,
        'Modified.Timestamp': raw_time,
        'File Size.Bytes': file_size,
        'MD5 Hash': md5
    }

    add_to_corpus(row)


def add_to_corpus(row):
    if row is None:
        return

    dups = corpus.get(row['MD5 Hash'], [])
    dups.append(row)
    corpus[row['MD5 Hash']] = dups


def create_symbolic_link(src, dst):
    dst = dst.replace('/', '\\')
    dst = '"{}"'.format(dst)
    src = src.replace('/', '\\')
    src = '"{}"'.format(src)
    cmd = "mklink /H {} {}".format(dst, src)
    # print(cmd)
    stdoutdata = subprocess.getoutput(cmd)
    print(stdoutdata)


def recursive_traversal(root_dir, filename=None, fx_file_callback=None):
    for item in os.listdir(root_dir):
        # print type(item)

        if item is None:
            break

        abs_path = os.path.join(root_dir, item)
        if os.path.isfile(abs_path):
            fx_file_callback(abs_file=abs_path,
                             filename=item)
        else:
            print('Dir: {}'.format(abs_path))

            if item in black_list:
                return

            recursive_traversal(abs_path, fx_file_callback=fx_file_callback)


def get_system_entry_points():
    raw_entry_pts = [
            'C:/Users/tjh',
            'C:\D13',
            'C:\D13-Git',
            'C:\D13-Offline Websites',
            'C:\D13-Python Projects',
            'C:\D13-RawData',
            'C:\Freemind-To-Wiki-IO',
            'C:\mnt-HackRF Tutorials',
            'C:\TJ-Scanner',
            'C:\z_Archive',
        ]

    entry_pts = []
    for pt in raw_entry_pts:
        entry_pts.append(pt.replace('/', '\\'))

    return entry_pts


if __name__ == '__main__':

    print('Running on Windows 10')
    print('Open a command prompt in Administrator mode')
    print('Run this: ')
    print('DOS> "C:\Program Files (x86)\Python36-32\python" "C:\D13-Python Projects\microexperiments\Dir_Scanner\T_Scanner.py"')

    root_scan_dir = 'C:/Users/tjh/Documents'
    output_dir = 'C:/Users/tjh/Desktop/Timeline-Links'
    corpus = {}

    black_list = [
            '.git',
            'My Music',
            'bin',
            'Timeline-Links',
            'eclipse',
            'Program',
            'org'
        ]

    # recursive_traversal(root_dir=root_scan_dir, fx_file_callback=print_path_to_link)
    # recursive_traversal(root_dir=root_scan_dir, fx_file_callback=create_time_line_view)
    recursive_traversal(root_dir=root_scan_dir, fx_file_callback=create_corpus)

    print('Serialize corpus')
    corpus_file = os.path.join(output_dir, 'corpus.pickle')
    with open(corpus_file, 'wb') as handle:
        pickle.dump(corpus, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('Done: {}'.format(corpus_file))
