import exifread
import os
import logging
from datetime import datetime

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


base_dir = '/lunix1/data1/public/Media/Photo Imports/'
base_dir_target = '/lunix1/data1/public/Media/Gallery/Photos/'

files = []

whitelist_prefixes = ['IMG','DSC']
whitelist_suffixes = ['JPG', 'HEIC']

def file_list(root_dir):
    for r, d, f in os.walk(root_dir):
        for directory in d:
            file_list(os.path.join(r, directory))
            logger.info(f"Going into directory {directory}")
        for fi in f:
            #logger.info(f"Found file {fi}")
            for pre in whitelist_prefixes:
                if fi.startswith(pre):
                    for suf in whitelist_suffixes:
                        if fi.lower().endswith(suf.lower()):
                            files.append(os.path.join(r, fi))
                            logger.debug(f'Added file {fi} to list')
                            continue

# datetime format: 2023:10:28 13:05:29
def move_file(source_file, timestamp):
    f = datetime.strptime(str(timestamp), '%Y:%m:%d %H:%M:%S')
    new_date_path = f.strftime('%Y/%Y-%m/')
    try:
        os.makedirs(f"{base_dir_target}{new_date_path}")
        base_filename = os.path.basename(source_file)
        new_filename = f"{base_dir_target}{new_date_path}{f.strftime('%Y-%m-%d')}.{base_filename}"
        os.rename(source_file, new_filename)
        logger.info(f"Move file {source_file} to date {new_filename}")
        return True
    except Exception as e:
        logger.error(f'Unable to move file: {e}')
        return False


if __name__ == '__main__':
    file_list(base_dir)

    logger.info(f'List contains {len(files)} files')

    for f in files:
        with open(f, 'rb') as fh:
            try:
                tags = exifread.process_file(fh, stop_tag='DateTimeOriginal')
                for tag in tags.keys():
                    if 'date' in tag.lower():
                        logger.debug("Key: %s, value %s" % (tag, tags[tag]))
                        if tag == 'EXIF DateTimeOriginal':
                            move_file(f, tags[tag])

            except Exception as e:
                logger.error(f'Unable to get tags from {f}: {e}')
                continue

