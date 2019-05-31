#!/usr/bin/env python3

#The main directory of the OGI data should contains docs directory

#The verification codes:
#1 Good: Only the target word is said.
#2 Maybe: Target word is present, but there's other junk in the file.
#3 Bad: Target word is not said.
#4 Puff: Same as good, but w/ an air puff.

#The naming convention:
#ks000820 --> ks[1gradeid][2spkcode][2uttid]0
#gradeid: K --> 0,b 
#         1 --> 1,c 
#         2 --> 2,d 
#         3 --> 3,e 
#         4 --> 4,f 
#         5 --> 5,g 
#         6 --> 6,h 
#         7 --> 7,i 
#         8 --> 8,j 
#         9 --> 9,k 
#         10 --> a,l 

#Uttid 2 digits, check docs/all.map

import pandas as pd
import numpy as np
import glob, sys
from os.path import join, isfile, splitext, basename, normpath
import argparse

def get_scripted(sOGIDir, fTxt, fUtt2Spk, fWavScp, lVerf = [1,2,4], lGrades = [0,1,2,3,4,5,6,7,8,9,10]):
    sDocsDir = join(sOGIDir,'docs')
    dfMap = pd.read_csv(join(sDocsDir,'all.map'),sep=' ',names=['id','trans'])
    aVerFiles = np.asarray([join(sOGIDir,'docs',str(i).zfill(2)+'-verified.txt') for i in lGrades],dtype=str) #The ver files exist in the docs directory as 00-verified.txt, 01-verified.txt, ....
    aIsFile = np.asarray([isfile(f) for f in aVerFiles],dtype=bool) #Check that all ver files are exist
    if not np.all(aIsFile):
        print('Missing Files: ',' '.join(aVerFiles[~aIsFile]))
        return
    #Read ver files
    aDataFrames = (pd.read_csv(f,sep=' ',names=['path','ver']) for f in aVerFiles) 
    dfVer = pd.concat(aDataFrames,ignore_index=True)
    dfVer.path[dfVer.ver.isin(lVerf)]
    aPaths = dfVer.path.values
    for sPath in aPaths:
        sRecId = splitext(basename(sPath))[0]
        sUttId = sRecId #Each recording contains one segment
        sSpkId = sRecId[:5]
        sTransId = sRecId[5:7].upper()
        sWavAbsPath = normpath(join(sDocsDir,sPath))
        aTransMask = dfMap.id==sTransId
        if not aTransMask.any():
            print('Invalid Trans ID:%s in Utt %s' % (sWavAbsPath,sTransId))
            return
        sTrans = dfMap.trans[dfMap.id==sTransId].iloc[0].upper()
        print(sSpkId+'-'+sUttId, sTrans, file=fTxt)
        print(sUttId, sSpkId, file=fUtt2Spk)
        print(sSpkId+'-'+sUttId, sWavAbsPath, file=fWavScp)
    #print(dfVer.path.values,file=fOutFile)
    return

class str2list(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(str2list, self).__init__(option_strings, dest, **kwargs)
    def parse_str(self,text):
        r = []
        for p in text.split(','):
            if '-' in p:
                s, e = [int(i) for i in p.split('-')]
                r.extend(range(s,e+1))
            else:
                r.append(int(p))
        return r
    def __call__(self, parser, namespace, values, option_string=None):
        #print('%r %r %r' % (namespace, values, option_string))
        setattr(namespace, self.dest, self.parse_str(values))

def ArgParser():
    parser = argparse.ArgumentParser(description='This code for creating Kaldi files for OGI Kids dataset', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('OGI_Dir',  help='The path to the main directory of OGI data', type=str)
    parser.add_argument('Text_File',  help='The path to the text file with <UttID> <Trans>', type=str)
    parser.add_argument('Utterance_to_Speakers_File',  help='The path to the Utterance to Speaker mapping file', type=str)
    parser.add_argument('Wav_Scp_File',  help='The path to the file contains list of wav files <RecID> <wavfile>', type=str)
    parser.add_argument('-v', '--verify', help='The list of selected verification codes', dest='ver', action=str2list, default=[1,2,4])
    parser.add_argument('-g', '--grade', dest='grd', help='The list of kids grads to be included', action=str2list, default=list(range(0,11)))
    return parser.parse_args()

if __name__ == '__main__':
    args = ArgParser()
    sOGIDir, sTxt, sUtt2Spk, sWavScp = args.OGI_Dir, args.Text_File, args.Utterance_to_Speakers_File, args.Wav_Scp_File
    lVerf = args.ver
    lGrades = args.grd
    with open(sTxt,'w') as fTxt, open(sUtt2Spk,'w') as fUtt2Spk, open(sWavScp,'w') as fWavScp:
        get_scripted(sOGIDir, fTxt, fUtt2Spk, fWavScp, lVerf = lVerf, lGrades = lGrades)




    



