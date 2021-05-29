#!/usr/bin/env python3

import logging
import os
import sys
from PIL import Image
from PIL import ImageOps
from PIL import UnidentifiedImageError
from .args import parse_args
from ._version import print_version_info

log = logging.getLogger()


class LogFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            self._style._fmt = "%(message)s"
        else:
            self._style._fmt = "%(levelname)s: %(message)s"
        return super().format(record)


def process_sheet_file(file, args):
    config = vars(args)
    log.debug('config: %s', config)
    try:
        image = Image.open(file)
        inverted_image = ImageOps.invert(image)
        inverted_image = inverted_image.convert('1')

        bounding_box = inverted_image.getbbox()
        print(bounding_box)

        left_column = (bounding_box[0], 0, bounding_box[0]+1, image.height)
        cropped = image.crop(left_column)
        if cropped.height < 100:
            logging.error(f"Can't process image {file}")
            return

        staves = [y for y in range(cropped.height) if cropped.getpixel((0, y)) < (128, 128, 128)]

        gaps = [[s, e] for s, e in zip(staves, staves[1:]) if s+1 < e]
        edges = iter(staves[:1] + sum(gaps, []) + staves[-1:])

        staves = list(zip(edges, edges))
        logging.info(f'found staves: {staves}')

        # TODO: more sanity checks
        if len(staves) > 10:
            logging.error(f'Too many staves found ({len(staves)}), skipping')

        for (index, staff) in enumerate(staves):
            staff_height = 1200
            h_padding = 500
            mid = (staff[0] + staff[1])//2
            logging.info(f'Processing staff {index}, height={staff_height}, mid={mid}')
            x1 = max(0, bounding_box[0]-(h_padding//2))
            x2 = min(image.width, bounding_box[2]+(h_padding//2))
            y1 = max(0, (mid-(staff_height)//2))
            y2 = min(mid+(staff_height//2), image.height)
            region = (x1, y1, x2, y2)
            logging.info(f'cropping region: {region}')
            cropped = image.crop(region)
            (name, ext) = os.path.splitext(file)
            outFile = f'{name}-{index}{ext}'
            logging.info(f'saving to : {outFile}')
            cropped.save(outFile)

    except FileNotFoundError:
        logging.error(f'Unable to read file {file}')
    except UnidentifiedImageError:
        logging.error(f"File {file} doesn't seem to be an image")
    except:
        logging.error("Unexpected error:", sys.exc_info()[0])


def main(argv):
    args = parse_args(argv[1:])

    if args.version:
        print_version_info()
        return

    # Configure logging
    old_loglevel = log.level
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter())
    log.setLevel(args.loglevel)
    log.addHandler(handler)

    try:
        if args.infile:
            for file in args.infile:
                log.info(f'processing {file}')
                process_sheet_file(file, args)
        else:
            log.warning('Nothing to do')
    finally:
        # Reset log in case we're not running as a standalong app
        log.removeHandler(handler)
        log.setLevel(old_loglevel)


if __name__ == '__main__':
    MIN_PYTHON = (3, 6)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)
    main(sys.argv)
