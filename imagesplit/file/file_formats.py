# coding=utf-8
"""
Support multiple imaging formats

Author: Tom Doel
Copyright UCL 2017

"""
from imagesplit.file.metaio_reader import MetaIoFile
from imagesplit.file.tiff_file_reader import TiffFileReader
from imagesplit.file.vol_reader import VolFile


class FormatFactory(object):
    """Return required factory for image file formats"""

    # File format constants
    METAIO_FORMAT = "mhd"
    TIFF_FORMAT = "tiff"
    VOL_FORMAT = "vol"

    _factories = {METAIO_FORMAT: MetaIoFile,
                  VOL_FORMAT: VolFile,
                  TIFF_FORMAT: TiffFileReader}

    @classmethod
    def get_factory(cls, format_string):
        """Get the file factory for this format"""

        format_string = cls.simplify_format(format_string)
        if format_string in cls._factories:
            return cls._factories[format_string]
        else:
            raise ValueError("Unknown file format: " + format_string)

    @classmethod
    def extension_to_format(cls, file_extension):
        """Get the format name for this file"""

        # Remove leading and trailing spaces and leading period if it exists
        ext = file_extension.lower().strip().lstrip('.')

        if ext == "mhd" or ext == "mha":
            return cls.METAIO_FORMAT

        elif ext == "vge":
            return cls.VOL_FORMAT

        elif ext == "tif" or ext == "tiff":
            return cls.TIFF_FORMAT

        else:
            raise ValueError("Unknown file format: " + file_extension)

    @classmethod
    def simplify_format(cls, format_name):
        """Get the standard format name for a format name which should be
        standard but may have been modified"""

        # Remove leading and trailing spaces and leading period if it exists
        name = format_name.lower().strip().lstrip('.')

        if name == "mhd" or name == "mha":
            return cls.METAIO_FORMAT

        elif name == "vge" or name == "vol":
            return cls.VOL_FORMAT

        elif name == "tif" or name == "tiff":
            return cls.TIFF_FORMAT

        else:
            raise ValueError("Unknown file format: " + format_name)

    @classmethod
    def get_extension_for_format(cls, file_format):
        """Returns the output file extension for this file format"""

        file_format = cls.simplify_format(file_format)
        if file_format == "mhd":
            return ".mhd"
        elif file_format == "tiff":
            return ".tiff"

        else:
            raise ValueError("Format " + file_format + " not supported")
