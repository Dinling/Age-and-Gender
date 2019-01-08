import pickle
import random

import cv2 as cv
import numpy as np
from torch.utils.data import Dataset

from config import *


class AGDataset(Dataset):
    """
    A PyTorch Dataset class to be used in a PyTorch DataLoader to create batches.
    """

    def __init__(self, split):
        with open(pickle_file, 'rb') as file:
            samples = pickle.load(file)

        self.samples = samples

    def __getitem__(self, i):
        # Remember, the Nth caption corresponds to the (N // captions_per_image)th image
        sample = self.samples[i]
        full_path = sample['full_path']
        # Read images
        img = cv.imread(full_path)
        img = cv.resize(img, (image_h, image_w))
        img = img.transpose(2, 0, 1)
        assert img.shape == (3, image_h, image_w)
        assert np.max(img) <= 255
        img = torch.FloatTensor(img / 255.)

        age = sample['age']
        gender = sample['gender']

        return img, age, gender

    def __len__(self):
        return len(self.samples)


if __name__ == "__main__":
    with open(pickle_file, 'rb') as file:
        samples = pickle.load(file)

    samples = random.sample(samples, 10)

    for i, sample in enumerate(samples):
        full_path = sample['full_path']
        age = sample['age']
        gender = sample['gender']
        face_loc = sample['face_location']
        print(gender, age, full_path, face_loc)
        img = cv.imread(full_path)
        print(i)
        print(img.shape)
        img = img[face_loc[1]:face_loc[3], face_loc[0]:face_loc[2]]
        cv.imwrite('images/{}_img.jpg'.format(i), img)
