# coding=utf-8
"""Write multidimensional data line by line"""

from abc import ABCMeta, abstractmethod
import itertools
import numpy as np

from niftysplit.image.image_wrapper import ImageWrapper


class ImageFileReader(object):
    """Base class for writing data from source to destination"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_image(self, data_source):
        """Create and write out this file, using data from this image source"""
        pass


class LinearImageFileReader(ImageFileReader):
    """Base class for writing data from source to destination line by line"""

    def __init__(self, image_size):
        self.size = image_size

    @abstractmethod
    def write_line(self, start, image_line):
        """Write the next line of bytes to the file"""

    @abstractmethod
    def read_line(self, start, num_voxels):
        """Reads a line of bytes from the file"""
        pass

    @abstractmethod
    def close_file(self):
        """Close the file"""
        pass

    def read_image(self, start_local, size_local):
        """Read the specified part of the image"""

        # Compute coordinate ranges
        ranges = [range(st, st + sz) for st, sz in
                  zip(start_local, size_local)]

        # Exclude first coordinate and get others in reverse order
        ranges_to_iterate = ranges[:0:-1]

        # Initialise the output array only when we know the data tyoe
        combined_image = ImageWrapper(origin=start_local,
                                      image_size=size_local)

        # Iterate over each line (equivalent to multiple for loops)
        for start_points in itertools.product(*ranges_to_iterate):
            start = [start_local[0]] + list(reversed(start_points))
            size = np.ones_like(size_local)
            size[0] = size_local[0]

            # Read one image line from the file
            image_line = self.read_line(start, size[0])
            sub_image = ImageWrapper(origin=start,
                                     image=image_line.reshape(size))

            combined_image.set_sub_image(sub_image)

        return combined_image.image

    def write_image(self, data_source):
        """Create and write out this file, using data from this image source"""

        # Compute coordinate ranges
        ranges = [range(0, sz) for sz in self.size]

        # Exclude first two coordinates and get others in reverse order
        ranges_to_iterate = ranges[:1:-1]

        # Iterate over each line (equivalent to multiple for loops)
        for main_dim_size in itertools.product(*ranges_to_iterate):
            start = [0] * min(2, len(self.size)) + \
                    list(reversed(main_dim_size))

            # Size contains the first two dimensions and ones
            size = self.size[:2] + [1] * (len(self.size) - 2)

            # Read one image slice from the transformed source
            image_slice = data_source.read_image(start, size)

            # Write out the image data to the file
            for line in range(0, size[1] if len(size) > 1 else 1):
            # for line in ranges[1:1]:
                line_coords = (Ellipsis,) + (line,) + \
                              tuple(np.zeros_like(start)[2:])
                line_coords = line_coords[0:len(size)]
                out_start = start
                if len(start) > 1:
                    out_start[1] = line
                self.write_line(out_start, image_slice[line_coords])

        self.close_file()


class BlockImageFileReader(ImageFileReader):
    """Base class for writing data from source to destination as a  2d block"""

    @abstractmethod
    def save(self, image):
        """Write the image to the file"""

    @abstractmethod
    def load(self):
        """Reads an image from the file"""
        pass

    @abstractmethod
    def close_file(self):
        """Close the file"""
        pass

    def __init__(self, image_size):
        self.size = image_size

    def read_image(self, start_local, size_local):
        """Read the specified part of the image"""

        image_data = self.load()
        if image_data.shape != self.size:
            raise ValueError("Image is not the expected size")

        image = ImageWrapper(origin=np.zeros_like(start_local),
                             image=image_data)

        return image.get_sub_image(start_local, size_local).image

    def write_image(self, data_source):
        """Create and write out this file, using data from this image source"""

        image_data = data_source.read_image(np.zeros_like(self.size), self.size)
        self.save(image_data)
        self.close_file()
