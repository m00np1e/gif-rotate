from util import *
import numpy as np
import cv2


class ImageTransformer(object):
    # perspective transformation class for image with shape (height, width, #channels)
    def __init__(self, image_path, shape):
        self.image_path = image_path
        self.image = load_image(image_path, shape)
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.num_channels = self.image.shape[2]

    # wrapper for rotating an image
    def rotate_along_axis(self, theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0):
        # Get radius of rotation along 3 axes
        rtheta, rphi, rgamma = get_rad(theta, phi, gamma)
        # get ideal focal length on z-axis
        d = np.sqrt(self.height ** 2 + self.width ** 2)
        self.focal = d / (2 * np.sin(rgamma) if np.sin(rgamma) != 0 else 1)
        dz = self.focal
        # get projection matrix
        mat = self.get_M(rtheta, rphi, rgamma, dx, dy, dz)
        return cv2.warpPerspective(self.image.copy(), mat, (self.width, self.height))

    # get perspective projection matrix
    def get_M(self, theta, phi, gamma, dx, dy, dz):
        w = self.width
        h = self.height
        f = self.focal
        # projection 2D to 3D matrix
        A1 = np.array([[1, 0, -w / 2],
                       [0, 1, -h / 2],
                       [0, 0, 1],
                       [0, 0, 1]])
        # rotation matrices around the x, y, and z axis
        RX = np.array([[1, 0, 0, 0],
                       [0, np.cos(theta), -np.sin(theta), 0],
                       [0, np.sin(theta), np.cos(theta), 0],
                       [0, 0, 0, 1]])
        RY = np.array([[np.cos(phi), 0, -np.sin(phi), 0],
                       [0, 1, 0, 0],
                       [np.sin(phi), 0, np.cos(phi), 0],
                       [0, 0, 0, 1]])
        RZ = np.array([[np.cos(gamma), -np.sin(gamma), 0, 0],
                       [np.sin(gamma), np.cos(gamma), 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        # composed rotation matrix with (RX, RY, RZ)
        R = np.dot(np.dot(RX, RY), RZ)
        # translation matrix
        T = np.array([[1, 0, 0, dx],
                      [0, 1, 0, dy],
                      [0, 0, 1, dz],
                      [0, 0, 0, 1]])
        # projection 3D to 2D matrix
        A2 = np.array([[f, 0, w / 2, 0],
                       [0, f, h / 2, 0],
                       [0, 0, 1, 0]])
        # final transformation matrix
        return np.dot(A2, np.dot(T, np.dot(R, A1)))
