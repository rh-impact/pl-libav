#
# libav ds ChRIS plugin app
#
# (c) 2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from chrisapp.base import ChrisApp
from PIL import Image
from pydicom import dcmread
from pydicom.pixel_data_handlers.util import apply_voi_lut
import subprocess as sp
import numpy as np
import os
import re


Gstr_title = r"""
 _ _ _
| (_) |
| |_| |__   __ ___   __
| | | '_ \ / _` \ \ / /
| | | |_) | (_| |\ V /
|_|_|_.__/ \__,_| \_/


"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       libav

    SYNOPSIS

        docker run --rm fnndsc/pl-libav libav                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-libav libav                        \
                /incoming /outgoing

    DESCRIPTION

        `libav` uses the avconv command line tool to create an MP4 video in
        the outgoing directory from DCM images in the incoming directory.

    ARGS

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.
"""


class Libav(ChrisApp):
    """
    Convert, manipulate and stream a variety of multimedia formats.
    """
    PACKAGE                 = __package__
    TITLE                   = 'A ChRIS plugin for libav'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 2000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 8000  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        parser = ArgumentParser("Parses libav command", formatter_class=ArgumentDefaultsHelpFormatter)

        # By default this libav plugin will use the avconv tool.
        # FIXME: Additional functionality for the avconv tool needs to be added
        # as optional arguments. Likewise, options for using additional tools
        # included in the libav package should be added, as well.
        parser.add_argument('-i', type=str, help="input path")
        parser.add_argument('outputpath', type=str, help="output path")

        print('Creating MP4 video in directory %s from DICOM images in %s'
              % (options.outputdir, options.inputdir))

        # FIXME: This section should be replaced in a future change to use the
        # med2image ChRIS plugin for converting the DCM image to a PNG.
        png_path = os.path.join(options.inputdir, 'PNG')
        for image_file in os.listdir(options.inputdir):
            filename, extension = os.path.splitext(image_file)
            if extension in ['.dcm']:
               ds = dcmread(os.path.join(options.inputdir, image_file))
               image = apply_voi_lut(ds.pixel_array, ds)
               rescaled = (np.maximum(image,0) / image.max()) * 255.0
               new_image = Image.fromarray(np.uint8(rescaled))
               image_path = os.path.join(png_path, filename)
               new_image.save(image_path+'.png')
        ###

        for filename in os.listdir(png_path):
            print('PNG created: %s' % filename)

        # FIXME: The avconv command does not create an mp4 currently. It errors
        # regarding the flags specified.
        # FIXME: This command relies on the images having a sequential naming
        # convention matching what is hard-coded here. This should be updated
        # to take any PNG files and apply a sequential naming convention
        # automatically.
        #cmd = ('/usr/local/bin/avconv', ' -f image2 -i ', png_path,
        #       '/%04d-*.png', options.outputdir, '/video.mp4')
        #sp.run(cmd, check=True)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
