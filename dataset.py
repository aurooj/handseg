import os

import numpy as np
import PIL.Image
import torch
from torch.utils import data
import pdb
import random
import cv2


class MyClsTestData(data.Dataset):
    """
    load images for testing
    root: director/to/images/
            structure:
            - root
                - images (images here)
                - masks (ground truth)
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    def __init__(self, root, transform=True, hflip=False, vflip=False, crop=False):
        super(MyClsTestData, self).__init__()
        self.root = root
        self.is_transform = transform
        self.is_hflip = hflip
        self.is_vflip = vflip
        self.is_crop = crop
        neg_root = os.path.join(self.root, '0')
        pos_root = os.path.join(self.root, '1')
        neg_names = os.listdir(neg_root)
        pos_names = os.listdir(pos_root)

        neg_img_names = []
        pos_img_names = []
        for i, name in enumerate(neg_names):
            if not name.endswith('.jpg'):
                continue
            neg_img_names.append(
                os.path.join(neg_root, name)
            )
        for i, name in enumerate(pos_names):
            if not name.endswith('.jpg'):
                continue
            pos_img_names.append(
                os.path.join(pos_root, name)
            )
        self.labels = [0] * len(neg_img_names) + [1] * len(pos_img_names)
        self.img_names = neg_img_names + pos_img_names

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, index):
        # load image
        img_file = self.img_names[index]
        img = PIL.Image.open(img_file)
        img = np.array(img, dtype=np.uint8)
        if len(img.shape) < 3:
            img = np.stack((img, img, img), 2)
        if img.shape[2] > 3:
            img = img[:, :, :3]
        gt = self.labels[index]
        if self.is_crop:
            H = int(0.9 * img.shape[0])
            W = int(0.9 * img.shape[1])
            H_offset = random.choice(range(img.shape[0] - H))
            W_offset = random.choice(range(img.shape[1] - W))
            H_slice = slice(H_offset, H_offset + H)
            W_slice = slice(W_offset, W_offset + W)
            img = img[H_slice, W_slice, :]
        if self.is_hflip and random.randint(0, 1):
            img = img[:, ::-1, :]
        if self.is_vflip and random.randint(0, 1):
            img = img[::-1, :, :]
        img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)

        if self.is_transform:
            img, gt = self.transform(img, gt)
            return img, gt
        else:
            return img, gt

    def transform(self, img, gt):
        img = img.astype(np.float64) / 255
        img -= self.mean
        img /= self.std
        img = img.transpose(2, 0, 1)
        # img = torch.from_numpy(img).float()
        #
        # gt = torch.LongTensor(gt)
        return img, gt


class MyClsData(data.Dataset):
    """
    load images for testing
    root: director/to/images/
            structure:
            - root
                - images (images here)
                - masks (ground truth)
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    def __init__(self, root, transform=True, hflip=False, vflip=False, crop=False):
        super(MyClsData, self).__init__()
        self.root = root
        self.is_transform = transform
        self.is_hflip = hflip
        self.is_vflip = vflip
        self.is_crop = crop
        neg_root = os.path.join(self.root, '0')
        pos_root = os.path.join(self.root, '1')
        pos_root2 = os.path.join(self.root, 'images')
        neg_names = os.listdir(neg_root)
        pos_names = os.listdir(pos_root)
        pos_names2 = os.listdir(pos_root2)

        neg_img_names = []
        pos_img_names = []
        for i, name in enumerate(neg_names):
            if not name.endswith('.jpg'):
                continue
            neg_img_names.append(
                os.path.join(neg_root, name)
            )
        for i, name in enumerate(pos_names):
            if not name.endswith('.jpg'):
                continue
            pos_img_names.append(
                os.path.join(pos_root, name)
            )
        for i, name in enumerate(pos_names2):
            if not name.endswith('.jpg'):
                continue
            pos_img_names.append(
                os.path.join(pos_root2, name)
            )
        self.labels = [0] * len(neg_img_names) + [1] * len(pos_img_names)
        self.img_names = neg_img_names + pos_img_names

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, index):
        # load image
        img_file = self.img_names[index]
        img = PIL.Image.open(img_file)
        img = np.array(img, dtype=np.uint8)
        if len(img.shape) < 3:
            img = np.stack((img, img, img), 2)
        if img.shape[2] > 3:
            img = img[:, :, :3]
        gt = self.labels[index]
        if self.is_crop:
            H = int(0.9 * img.shape[0])
            W = int(0.9 * img.shape[1])
            H_offset = random.choice(range(img.shape[0] - H))
            W_offset = random.choice(range(img.shape[1] - W))
            H_slice = slice(H_offset, H_offset + H)
            W_slice = slice(W_offset, W_offset + W)
            img = img[H_slice, W_slice, :]
        if self.is_hflip and random.randint(0, 1):
            img = img[:, ::-1, :]
        if self.is_vflip and random.randint(0, 1):
            img = img[::-1, :, :]
        img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)

        if self.is_transform:
            img, gt = self.transform(img, gt)
            return img, gt
        else:
            return img, gt

    def transform(self, img, gt):
        img = img.astype(np.float64) / 255
        img -= self.mean
        img /= self.std
        img = img.transpose(2, 0, 1)
        # img = torch.from_numpy(img).float()
        #
        # gt = torch.LongTensor(gt)
        return img, gt


class MyBoxPixData(data.Dataset):
    """
    load images for testing
    root: director/to/images/
            structure:
            - root
                - images (images here)
                - pix (pixel ground truth)
                - box (box ground truth)
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    def __init__(self, root, transform=True, hflip=False, vflip=False, crop=False, source=''):
        super(MyBoxPixData, self).__init__()
        self.root = root
        self.is_transform = transform
        self.is_hflip = hflip
        self.is_vflip = vflip
        self.is_crop = crop
        img_root = os.path.join(self.root, 'images')
        pix_root = os.path.join(self.root, 'pix')
        box_root = os.path.join(self.root, 'box')
        pix_names = os.listdir(pix_root)
        box_names = os.listdir(box_root)
        self.img_names = []
        self.gt_names = []
        self.names = []
        for i, name in enumerate(pix_names):
            if not name.endswith('.png'):
                continue
            self.img_names.append(
                os.path.join(img_root, name[:-4] + '.jpg')
            )
            self.gt_names.append(
                os.path.join(pix_root, name[:-4] + '.png')
            )
        for i, name in enumerate(box_names):
            if not name.endswith('.png'):
                continue
            self.img_names.append(
                os.path.join(img_root, name[:-4] + '.jpg')
            )
            self.gt_names.append(
                os.path.join(box_root, name[:-4] + '.png')
            )
        self.flags = ['pix']*len(pix_names) + ['box']*len(box_names)
        if 'pix' == source:
            self.img_names = self.img_names[:len(pix_names)]
            self.gt_names = self.gt_names[:len(pix_names)]
            self.flags = self.flags[:len(pix_names)]
        elif 'box' == source:
            self.img_names = self.img_names[-len(box_names):]
            self.gt_names = self.gt_names[-len(box_names):]
            self.flags = self.flags[-len(box_names):]

    def __len__(self):
        return len(self.gt_names)

    def __getitem__(self, index):
        # load image
        img_file = self.img_names[index]
        img = PIL.Image.open(img_file)
        img = np.array(img, dtype=np.uint8)
        if len(img.shape) < 3:
            img = np.stack((img, img, img), 2)
        if img.shape[2] > 3:
            img = img[:, :, :3]

        gt_file = self.gt_names[index]
        gt = PIL.Image.open(gt_file)
        gt = np.array(gt, dtype=np.int32)
        gt[gt != 0] = 1
        flag = self.flags[index]
        if 'pix' == flag and self.is_crop:
            H = int(0.9 * img.shape[0])
            W = int(0.9 * img.shape[1])
            H_offset = random.choice(range(img.shape[0] - H))
            W_offset = random.choice(range(img.shape[1] - W))
            H_slice = slice(H_offset, H_offset + H)
            W_slice = slice(W_offset, W_offset + W)
            img = img[H_slice, W_slice, :]
            gt = gt[H_slice, W_slice]
        if 'pix' == flag and self.is_hflip and random.randint(0, 1):
            img = img[:, ::-1, :]
            gt = gt[:, ::-1]
        if 'pix' == flag and self.is_vflip and random.randint(0, 1):
            img = img[::-1, :, :]
            gt = gt[::-1, :]
        img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)
        gt = cv2.resize(gt, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)

        if self.is_transform:
            img, gt = self.transform(img, gt)
            return img, gt
        else:
            return img, gt

    def transform(self, img, gt):
        img = img.astype(np.float64) / 255
        img -= self.mean
        img /= self.std
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).float()

        gt = torch.from_numpy(gt)
        return img, gt


class MyClsBoxPixData(data.Dataset):
    """
    load images for testing
    root: director/to/images/
            structure:
            - root
                - images (images here)
                - pix (pixel ground truth)
                - box (box ground truth)
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    def __init__(self, root, transform=True, hflip=False, vflip=False, crop=False, source=''):
        super(MyClsBoxPixData, self).__init__()
        self.root = root
        self.is_transform = transform
        self.is_hflip = hflip
        self.is_vflip = vflip
        self.is_crop = crop
        img_root = os.path.join(self.root, 'images')
        pix_root = os.path.join(self.root, 'pix')
        box_root = os.path.join(self.root, 'box')
        pos_root = os.path.join(self.root, '1')
        neg_root = os.path.join(self.root, '0')
        pix_names = os.listdir(pix_root)
        box_names = os.listdir(box_root)
        pos_names = os.listdir(pos_root)
        neg_names = os.listdir(neg_root)
        self.img_names = []
        self.gt_names = []
        self.names = []
        for i, name in enumerate(pix_names):
            if not name.endswith('.png'):
                continue
            self.img_names.append(
                os.path.join(img_root, name[:-4] + '.jpg')
            )
            self.gt_names.append(
                os.path.join(pix_root, name[:-4] + '.png')
            )
        for i, name in enumerate(box_names):
            if not name.endswith('.png'):
                continue
            self.img_names.append(
                os.path.join(img_root, name[:-4] + '.jpg')
            )
            self.gt_names.append(
                os.path.join(box_root, name[:-4] + '.png')
            )
        for i, name in enumerate(pos_names):
            if not name.endswith('.jpg'):
                continue
            self.img_names.append(
                os.path.join(pos_root, name[:-4] + '.jpg')
            )
            self.gt_names.append(
                os.path.join(pos_root, name[:-4] + '.jpg')
            )
        for i, name in enumerate(neg_names):
            if not name.endswith('.jpg'):
                continue
            self.img_names.append(
                os.path.join(neg_root, name[:-4] + '.jpg')
            )
            self.gt_names.append(
                os.path.join(neg_root, name[:-4] + '.jpg')
            )
        self.flags = ['pix']*len(pix_names) + ['box']*len(box_names) + ['pos']*len(pos_names) + ['neg']*len(neg_names)
        # only pixel annotations
        if 'pix' == source:
            self.img_names = self.img_names[:len(pix_names)]
            self.gt_names = self.gt_names[:len(pix_names)]
            self.flags = self.flags[:len(pix_names)]
        # only box annotations
        elif 'box' == source:
            self.img_names = self.img_names[len(pix_names):len(box_names)]
            self.gt_names = self.gt_names[len(pix_names):len(box_names)]
            self.flags = self.flags[len(pix_names):len(box_names)]
        # pixel and box annotations
        elif 'seg' == source:
            self.img_names = self.img_names[:len(pix_names)+len(box_names)]
            self.gt_names = self.gt_names[:len(pix_names)+len(box_names)]
            self.flags = self.flags[:len(pix_names)+len(box_names)]

    def __len__(self):
        return len(self.gt_names)

    def __getitem__(self, index):
        # load image
        img_file = self.img_names[index]
        img = PIL.Image.open(img_file)
        img = np.array(img, dtype=np.uint8)
        if len(img.shape) < 3:
            img = np.stack((img, img, img), 2)
        if img.shape[2] > 3:
            img = img[:, :, :3]
        flag = self.flags[index]
        if 'pix' == flag or 'box' == flag:
            gt_file = self.gt_names[index]
            gt = PIL.Image.open(gt_file)
            gt = np.array(gt, dtype=np.int32)
            gt[gt != 0] = 1
            if 'pix' == flag and self.is_crop:
                H = int(0.9 * img.shape[0])
                W = int(0.9 * img.shape[1])
                H_offset = random.choice(range(img.shape[0] - H))
                W_offset = random.choice(range(img.shape[1] - W))
                H_slice = slice(H_offset, H_offset + H)
                W_slice = slice(W_offset, W_offset + W)
                img = img[H_slice, W_slice, :]
                gt = gt[H_slice, W_slice]
            if 'pix' == flag and self.is_hflip and random.randint(0, 1):
                img = img[:, ::-1, :]
                gt = gt[:, ::-1]
            if 'pix' == flag and self.is_vflip and random.randint(0, 1):
                img = img[::-1, :, :]
                gt = gt[::-1, :]
        elif 'neg' == flag:
            gt = np.zeros((img.shape[0], img.shape[1]), dtype=np.int32)
        else:
            # label=2 for positive images. Will generate labels while training
            gt = np.ones((img.shape[0], img.shape[1]), dtype=np.int32)*2
        img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)
        gt = cv2.resize(gt, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)

        if self.is_transform:
            img, gt = self.transform(img, gt)
            return img, gt
        else:
            return img, gt

    def transform(self, img, gt):
        img = img.astype(np.float64) / 255
        img -= self.mean
        img /= self.std
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).float()

        gt = torch.from_numpy(gt)
        return img, gt


class MyData(data.Dataset):
    """
    load images for testing
    root: director/to/images/
            structure:
            - root
                - images (images here)
                - masks (ground truth)
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    def __init__(self, root, transform=True, hflip=False, vflip=False, crop=False):
        super(MyData, self).__init__()
        self.root = root
        self.is_transform = transform
        self.is_hflip = hflip
        self.is_vflip = vflip
        self.is_crop = crop
        img_root = os.path.join(self.root, 'images')
        gt_root = os.path.join(self.root, 'masks')
        file_names = os.listdir(gt_root)
        self.img_names = []
        self.map_names = []
        self.gt_names = []
        self.names = []
        for i, name in enumerate(file_names):
            if not name.endswith('.png'):
                continue
            self.img_names.append(
                os.path.join(img_root, name[:-4] + '.jpg')
            )
            self.gt_names.append(
                os.path.join(gt_root, name[:-4] + '.png')
            )
            self.names.append(name[:-4])

    def __len__(self):
        return len(self.gt_names)

    def __getitem__(self, index):
        # load image
        img_file = self.img_names[index]
        img = PIL.Image.open(img_file)
        img = np.array(img, dtype=np.uint8)

        gt_file = self.gt_names[index]
        gt = PIL.Image.open(gt_file)
        gt = np.array(gt, dtype=np.int32)
        gt[gt != 0] = 1
        if self.is_crop:
            H = int(0.9 * img.shape[0])
            W = int(0.9 * img.shape[1])
            H_offset = random.choice(range(img.shape[0] - H))
            W_offset = random.choice(range(img.shape[1] - W))
            H_slice = slice(H_offset, H_offset + H)
            W_slice = slice(W_offset, W_offset + W)
            img = img[H_slice, W_slice, :]
            gt = gt[H_slice, W_slice]
        if self.is_hflip and random.randint(0, 1):
            img = img[:, ::-1, :]
            gt = gt[:, ::-1]
        if self.is_vflip and random.randint(0, 1):
            img = img[::-1, :, :]
            gt = gt[::-1, :]
        img = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)
        gt = cv2.resize(gt, dsize=(256, 256), interpolation=cv2.INTER_NEAREST)

        if self.is_transform:
            img, gt = self.transform(img, gt)
            return img, gt
        else:
            return img, gt

    def transform(self, img, gt):
        img = img.astype(np.float64) / 255
        img -= self.mean
        img /= self.std
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).float()

        gt = torch.from_numpy(gt)
        return img, gt


class MyTestData(data.Dataset):
    """
    load images for testing
    root: director/to/images/
            structure:
            - root
                - images (images here)
                - masks (ground truth)
    """
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    def __init__(self, root, transform=True):
        super(MyTestData, self).__init__()
        self.root = root
        self._transform = transform

        img_root = os.path.join(self.root, 'images')
        file_names = os.listdir(img_root)
        self.img_names = []
        self.names = []
        for i, name in enumerate(file_names):
            if not name.endswith('.jpg'):
                continue
            self.img_names.append(
                os.path.join(img_root, name[:-4] + '.jpg')
            )
            self.names.append(name[:-4])

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, index):
        # load image
        img_file = self.img_names[index]
        img = PIL.Image.open(img_file)
        img_size = img.size
        img = img.resize((256, 256))
        img = np.array(img, dtype=np.uint8)
        if self._transform:
            img = self.transform(img)
            return img, self.names[index], img_size
        else:
            return img, self.names[index], img_size

    def transform(self, img):
        img = img.astype(np.float64) / 255
        img -= self.mean
        img /= self.std
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).float()
        return img