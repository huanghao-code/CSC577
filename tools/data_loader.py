import torch
from torch.utils.data import Dataset, DataLoader

import csv
import h5py
import numpy as np
from pathlib import Path

import pdb

# transform video ResNet features into a pytorch dataset 
class FeatureData(Dataset):
    """
    Args:
        fea_dir: a directory containing video ResNet features
    """
    def __init__(self, fea_dir):
        self.fea_dir = fea_dir
        #pdb.set_trace()
        self.fea_list = list(self.fea_dir.iterdir())

    # return num of video features (equal to num of videos)
    def __len__(self):
        return len(self.fea_list)

    def __getitem__(self, index):
        fea_file = self.fea_list[index]
        with h5py.File(fea_file, 'r') as f: # for each video feature
            video_feature = torch.Tensor(np.array(f['pool5']))
            f.close()

        return video_feature

# generate feature loader according to the given feature directory
def feature_loader(fea_dir, mode = 'train'):
    #pdb.set_trace()
    if mode.lower() == 'train':
        return DataLoader(FeatureData(fea_dir), batch_size = 1)
    elif mode.lower() == 'test':
        return DataLoader(FeatureData(fea_dir), batch_size = 1)
    else:
        raise "No such mode!"

# load ground-truth file
def gt_loader(gt_dir):
    gt = []
    with open(str(gt_dir) + '/gt.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            row_arr = []
            for i in range(len(row)):
                elem = int(row[i].strip())
                row_arr.append(elem)
            gt.append(row_arr)
        f.close()

    return gt
