import exifread
import os
import logging

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


base_dir = '/lunix1/data1/public/Media/Photo Imports/'

files = []

whitelist_prefixes = ['IMG']
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
                        if fi.endswith(suf):
                            files.append(os.path.join(r, fi))
                            logger.info(f'Added file {fi} to list')
                            continue


if __name__ == '__main__':
    file_list(base_dir)

    logger.info(f'List contains {len(files)} files')

    for f in files:
        with open(f, 'rb') as fh:
            try:
                tags = exifread.process_file(fh, stop_tag='DateTimeOriginal')
                for tag in tags.keys():
                    if tag.lower().contains('date'):
                        logger.info("Key: %s, value %s" % (tag, tags[tag]))
            except Exception as e:
                logger.error(f'Unable to get tags from {f}: {e}')
                continue

