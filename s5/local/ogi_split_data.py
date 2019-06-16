import argparse
import pandas as pd
from glob import glob
from os.path import join, isdir
from utils.split_path import Split_Path

#This function should split the speakers in the OGI data into train, dev, test. Based on the determined portions.
def Split_Data(sOGIDir, fTest_Portion = 0.15, fDevel_Portion = 0.15, fTrain_Portion = 0.7):
    #TO DO: Check if 'docs' exist first and return with error 
    for sVerFile in glob(join(sOGIDir,'docs','*-verified.txt')):
        with open(sVerFile,'r') as f:
            lLines = f.read().splitlines()
            lSpkrs = set([Split_Path(l.split()[0])[-2] for l in lLines])

