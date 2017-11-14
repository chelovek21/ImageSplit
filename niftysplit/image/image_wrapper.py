# coding=utf-8
"""A wrapper for a multi-dimensional image with an origin offset"""

import numpy as np


class SmartImage(object):
    """Image wrapper which converts between Axes"""

    def __init__(self, start, size, image, transformer):
        self._size = size
        self._start = start
        self.image = image
        self._transformer = transformer

    def transform_to_global(self):
        """Returns a partial image using the specified global coordinates"""

        if self.image is None:
            raise ValueError("Image has not been created")

        transformed_origin, transformed_size = self._transformer.to_global(
            self._start, self._size)
        transformed_image = \
            self._transformer.image_to_global(self.image)

        return ImageWrapper(origin=transformed_origin, image=transformed_image)

    def coords_to_global(self):
        """Returns a partial image using the specified global coordinates"""

        transformed_origin, transformed_size = self._transformer.to_global(
            self._start, self._size)

        return transformed_origin, transformed_size

    def set_sub_image(self, sub_image):
        """Replaces part of the image with the corresponding subimage"""

        if self.image is None:
            self.image = np.zeros(shape=self._size,
                                  dtype=sub_image.image.dtype)

        global_subimage = sub_image.transform_to_global()
        local_subimage = self._transformer.image_to_local(global_subimage.image)

        global_start, global_size = sub_image.coords_to_global()
        start, size = self._transformer.to_local(global_start, global_size)

        start_indices = np.array(start)
        end_indices = np.add(start_indices, np.array(size))
        if np.any(np.less(start_indices, np.zeros_like(start_indices))) \
                or np.any(np.greater(end_indices, self._size)):
            raise ValueError("Subimage is not contained within the main image")
        selector = tuple([slice(start, end) for start, end in
                          zip(start_indices, end_indices)])
        self.image[selector] = local_subimage


class ImageWrapper(object):
    """Multi-dimensional image array with an origin"""

    def __init__(self, origin, image_size=None, image=None):
        self.origin = origin
        if image is not None:
            self.size = list(np.shape(image))
        else:
            self.size = image_size
        self.image = image

    def get_sub_image(self, start, size):
        """Returns the corresponding subimage"""

        start_indices = np.subtract(start, self.origin)
        end_indices = np.add(start_indices, np.array(size))
        if np.any(np.less(start_indices,
                          np.zeros_like(start_indices))) \
                or np.any(np.greater(end_indices, self.size)):
            raise ValueError("Subimage is not contained within the main image")
        selector = tuple([slice(start, end) for start, end in
                          zip(start_indices, end_indices)])
        return ImageWrapper(origin=start, image=self.image[selector])

    def set_sub_image(self, sub_image):
        """Replaces part of the image with the corresponding subimage"""

        if self.image is None:
            self.image = np.zeros(shape=self.size, dtype=sub_image.image.dtype)
        start_indices = np.subtract(sub_image.origin, self.origin)
        end_indices = np.add(start_indices, np.array(sub_image.size))
        if np.any(np.less(start_indices, np.zeros_like(start_indices))) \
                or np.any(np.greater(end_indices, self.size)):
            raise ValueError("Subimage is not contained within the main image")
        selector = tuple([slice(start, end) for start, end in
                          zip(start_indices, end_indices)])
        self.image[selector] = sub_image.image
