# coding=utf-8
"""Factory for creating file objects fod different file types"""

from niftysplit.file.metaio_reader import MetaIoFile


class FileFactory(object):
    """Create objects for handling file input and output"""

    def __init__(self, file_handle_factory):
        self._file_handle_factory = file_handle_factory
        self._metaio_factory = None

    def create_read_file(self, subimage_descriptor):
        """Create a class for reading"""

        data_format = subimage_descriptor.file_format.lower()
        if data_format == "mhd":
            return MetaIoFile.create_read_file(subimage_descriptor,
                                               self._file_handle_factory)
        else:
            raise ValueError("Format " + data_format + " not supported")

    def create_write_file(self, subimage_descriptor):
        """Create a class for writing"""

        data_format = subimage_descriptor.file_format.lower()
        if data_format == "mhd":
            return MetaIoFile.create_write_file(subimage_descriptor,
                                                self._file_handle_factory)
        else:
            raise ValueError("Format " + data_format + " not supported")

    @staticmethod
    def get_extension_for_format(file_format):
        """Returns the file extension for this file format"""
        file_format = file_format.lower()
        if file_format == "mhd":
            return ".mhd"

        else:
            raise ValueError("Format " + file_format + " not supported")
