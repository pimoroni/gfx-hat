"""Basic font helper module."""
import os
import glob

font_directory = os.path.abspath(os.path.dirname(__file__))

font_files = {}


def load_fonts(extension='ttf'):
    """Load fonts from current directory.

    :param extension: Font file extension eg: ttf, bdf

    """
    for font in list(glob.glob(os.path.join(font_directory, '*.' + extension))):
        font_name = os.path.basename(font).replace('.' + extension, '').replace('-Regular', '').replace('-', '')
        font_files[font_name] = font
        globals()[font_name] = font


load_fonts('ttf')
load_fonts('bdf')
