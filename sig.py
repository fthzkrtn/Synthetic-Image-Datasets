#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Synthetic Image Dataset Generator
"""
from __future__ import print_function

from numpy.random import random
import skimage.transform as transform
import hashlib
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import skimage.io as io
from numpy.random import random
from matplotlib.patches import Rectangle


class SIG(object):
    """
    Synthetic Image Generator
    """

    def __init__(self):
        """:char"""

    @staticmethod
    def foreground_aug(fg):
        """
        Apply augmentations on the foreground.
        :param fg:
        :return:
        """
        # Random rotation, zoom, translation
        angle = np.random.randint(-10, 10) * (np.pi / 180.0)  # Convert to radians
        zoom = random() * 0.4 + 0.8  # Zoom in range [0.8,1.2)
        t_x = np.random.randint(0, int(fg.shape[1] / 3))
        t_y = np.random.randint(0, int(fg.shape[0] / 3))
        tform = transform.AffineTransform(scale=(zoom, zoom),
                                          rotation=angle,
                                          translation=(t_x, t_y))
        fg = transform.warp(fg, tform.inverse)
        if np.random.randint(0, 100) >= 50:
            fg = fg[:, ::-1]
        return fg

    @staticmethod
    def get_foreground_mask(fg):
        """
        Create a mask for this new foreground object
        :param fg:
        :return:
        """
        mask_new = fg.copy()[:, :, 0]
        mask_new[mask_new > 0] = 1
        return mask_new

    @staticmethod
    def compose(fg, mask, bg):
        """
        Compose entire image
        :param fg:
        :param mask:
        :param bg:
        :return:
        """
        # resize background
        bg = transform.resize(bg, fg.shape[:2])

        # Subtract the foreground area from the background
        bg = bg * (1 - mask.reshape(fg.shape[0], fg.shape[1], 1))

        # Finally, add the foreground
        composed_image = bg + fg
        return composed_image

    @staticmethod
    def generate_sig():
        # Random selection of background from the backgrounds folder
        bg_file = np.random.choice(os.listdir("./backgrounds/"))
        background = io.imread('./backgrounds/' + bg_file) / 255.0

        # Read the image
        img = io.imread('./dogSeg.jpg') / 255.0  # Cut out the foreground layer
        foreground = img.copy()
        foreground[foreground >= 0.9] = 0  # Setting surrounding pixels to zeroplt.axis('off')
        foreground_new = SIG.foreground_aug(foreground)
        mask_new = SIG.get_foreground_mask(foreground_new)
        composed_image = SIG.compose(foreground_new, mask_new, background)

        # Display the image
        plt.imshow(composed_image)
        plt.axis('off')
        # plt.show()
        ts = datetime.now().strftime("%Y%m%d%H%M%s")
        hsh = hashlib.sha256(ts.encode())
        plt.savefig("./pics/{}.jpg".format(hsh.hexdigest()))