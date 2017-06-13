"""
This module holds classes related to images.
A strong focus is given to ITK images and numpy arrays.
"""
import SimpleITK as sitk
import numpy as np
from typing import Tuple


class ImageProperties:
    """
    Represents ITK image properties.
    Also refer to itk::simple::Image::CopyInformation.
    """

    def __init__(self, image: sitk.Image):
        """
        Initializes a new instance of the ImageInformation class.

        :param image: The image.
        """
        self.size = image.GetSize()
        self.origin = image.GetOrigin()
        self.spacing = image.GetSpacing()
        self.direction = image.GetDirection()
        self.dimensions = image.GetDimension()
        self.number_of_components_per_pixel = image.GetNumberOfComponentsPerPixel()

    def is_two_dimensional(self) -> bool:
        """
        Determines whether the image is two-dimensional.

        :return: True if the image is two-dimensional; otherwise, False.
        :rtype: bool
        """
        return self.dimensions == 2

    def is_three_dimensional(self) -> bool:
        """
        Determines whether the image is three-dimensional.

        :return: True if the image is three-dimensional; otherwise, False.
        :rtype: bool
        """
        return self.dimensions == 3

    def is_vector_image(self) -> bool:
        """
        Determines whether the image is a vector image.

        :return: True for vector images; False for scalar images.
        :rtype: bool
        """
        return self.number_of_components_per_pixel > 1

    def __str__(self):
        """
        Gets a nicely printable string representation.

        :return: String representation.
        :rtype: str
        """
        return 'ImageProperties:\n' \
               ' size:                           {self.size}\n' \
               ' origin:                         {self.origin}\n' \
               ' spacing:                        {self.spacing}\n' \
               ' direction:                      {self.direction}\n' \
               ' dimensions:                     {self.dimensions}\n' \
               ' number_of_components_per_pixel: {self.number_of_components_per_pixel}\n' \
            .format(self=self)


class NumpySimpleITKImageBridge:
    """
    A numpy to SimpleITK bridge, which provides static methods to convert between numpy array and SimpleITK image.
    """

    @staticmethod
    def convert(array: np.ndarray, properties: ImageProperties) -> sitk.Image:
        """
        Converts a numpy array to a SimpleITK image.

        :param array: The image as numpy array. The shape can be either:
            - shape=(n,), where n = total number of voxels
            - shape=(n,v), where n = total number of voxels and v = number of components per pixel (vector image)
            - shape=(<reversed image size>), what you get from itk.GetArrayFromImage
        :type array: np.ndarray
        :param properties: The image information.
        :type properties: ImageProperties
        :return: The SimpleITK image.
        :rtype: sitk.Image
        """

        if not array.shape == properties.size[::-1]:
            # we need to reshape the array

            if not properties.is_vector_image() and array.ndim != 1:
                raise ValueError("array needs to be one-dimensional")

            if properties.is_vector_image() and array.ndim != 2:
                raise ValueError("array needs to be two-dimensional")

            # reshape array
            if not properties.is_vector_image():
                array = array.reshape(properties.size[::-1])
            else:
                array = array.reshape((properties.size[::-1] + (properties.number_of_components_per_pixel, )))

        image = sitk.GetImageFromArray(array)
        image.SetOrigin(properties.origin)
        image.SetSpacing(properties.spacing)
        image.SetDirection(properties.direction)

        return image

    @staticmethod
    def convert_to_vector_image(array: np.ndarray, properties: ImageProperties) -> sitk.Image:
        """
        Converts a two-dimensional numpy array to a SimpleITK vector image with the properties of a scalar image.

        :param array: The image as numpy two-dimensional array, e.g. shape=(4181760,2).
        :type array: np.ndarray
        :param properties: The image properties (scalar image; otherwise use convert()).
        :type properties: ImageProperties
        :return: The SimpleITK image. 
        :rtype: sitk.Image
        """

        if array.ndim != 2:
            raise ValueError("array needs to be two-dimensional")

        array = array.reshape((properties.size[::-1] + (array.shape[1], )))

        image = sitk.GetImageFromArray(array)
        image.SetOrigin(properties.origin)
        image.SetSpacing(properties.spacing)
        image.SetDirection(properties.direction)

        return image


class SimpleITKNumpyImageBridge:
    """
    A SimpleITK to numpy bridge, which provides static methods to convert between SimpleITK image and numpy array.
    """

    @staticmethod
    def convert(image: sitk.Image) -> Tuple[np.ndarray, ImageProperties]:
        """
        Converts an image to a numpy array and an ImageProperties class.

        :param image: The image.
        :type image: sitk.Image
        :return: (array, properties): The image as numpy array and the image properties as ImageProperties.
        :rtype: Tuple[np.ndarray, ImageProperties]
        """

        return sitk.GetArrayFromImage(image), ImageProperties(image)