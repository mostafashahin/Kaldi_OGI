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
#Uttid 2 digits, check docs/all.map for scripted
#Uttid is xx for spontaneous speech

import pandas as pd
import numpy as np
import glob, sys
from os.path import join, isfile, splitext, basename, normpath
import argparse
import re

#There are different type of noise tags in the OGI trans files see https://catalog.ldc.upenn.edu/docs/LDC2006S35/labeling.pdf for details.
#Here each tag converted to a noise symbole, the dictionary has the tag as key and tuple with two symbol values, when connected to a word and when not connected.

dNoiseTag2Symb = {
        "<asp>"  : ('',''), #heavily aspirated p, t, or k or puff at end of word
        "<beep>" : ('',''), #a beep sound
        "<blip>" : ('',''), #temp signal blip signal goes completely silent for a period
        "<bn>"   : ('','NSN'), #Background noise
        "<br>"   : ('','NSN'), #breathing noise
        "<bs>"   : ('','SN'), #background speech
        "<cough>": ('','NSN'), # cough sound
        "<ct>"   : ('','NSN'), # a clear throat
        "<fp>"   : ('','SN'), #generic filled pause/false start
        "<lau>"  : ('',''), # ??
        "<laugh>": ('LAU','LAU'), #laughter
        "<ln>"   : ('','NSN'), # line noise
        "<long>" : ('',''), #elongated word
        "<ls>"   : ('','NSN'), #lip smack
        "<n>"    : ('',''), # ??
        "<nitl>" : ('','')

        }
#TODO:Let function takes file names strings not file objects and open it as append
def get_scripted(sOGIDir, fTxt, fUtt2Spk, fWavScp, sSpkrList='', lVerf = [1,2,4], lGrades = [0,1,2,3,4,5,6,7,8,9,10]):
    
    #Regular Expression to normalize the text
    p = re.compile('([\w]+)[,"\'.](\s)')

    sDocsDir = join(sOGIDir,'docs')
    print(sSpkrList)
    if isfile(sSpkrList):#Load list of selected speakers 
        with open(sSpkrList) as flSpkrList:
            lSelectSpkrs = flSpkrList.read().splitlines()
        print(lSelectSpkrs[0], len(lSelectSpkrs))
    else:
        lSelectSpkrs = None
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
    if lSelectSpkrs != None:
        lSpkrs = [splitext(basename(sPath))[0][:5] for sPath in aPaths]
        lInxSelcSpkrs = [i for i in range(len(lSpkrs)) if lSpkrs[i] in lSelectSpkrs]
        aPaths = aPaths[lInxSelcSpkrs]
    for sPath in aPaths:
        sRecId = splitext(basename(sPath))[0]
        sUttId = sRecId #Each recording contains one segment
        sSpkId = sRecId[:5]
        sTransId = sRecId[5:7].upper()
        sWavAbsPath = normpath(join(sDocsDir,sPath))
        aTransMask = dfMap.id==sTransId
        if not aTransMask.any():
            print('Invalid Trans ID:%s in Utt %s' % (sWavAbsPath,sTransId))
            continue
        sTrans = dfMap.trans[dfMap.id==sTransId].iloc[0].upper()
        sTrans = p.sub(r'\1\2',sTrans)
        print(sSpkId+'-'+sUttId, sTrans, file=fTxt)
        print(sSpkId+'-'+sUttId, sSpkId, file=fUtt2Spk)
        print(sSpkId+'-'+sUttId, sWavAbsPath, file=fWavScp)
    #print(dfVer.path.values,file=fOutFile)
    return

def get_spont(sOGIDir, fTxt, fUtt2Spk, fWavScp, sSpkrList='', lVerf = [1,2,4], lGrades = [0,1,2,3,4,5,6,7,8,9,10]):
    #1- get all trans files that match spkids, 2- Make sure each trans has wav file,
    #3- loop on trans files, 4- Treat the noise tags, 5- treat the [] remove what between them, 
    Get_basename = lambda s : splitext(basename(s))[0]
    Get_SpkrID = lambda s : splitext(basename(s))[0][:5]
    sTransDir = join(sOGIDir,'trans/spontaneous')
    sWavDir = join(sOGIDir,'speech/spontaneous')
    
    #Get all trans & wav files
    lTransFiles = np.asarray(glob.glob(join(sTransDir,'**/*.txt'),recursive=True))
    lWavFiles = np.asarray(glob.glob(join(sWavDir,'**/*.wav'),recursive=True))
    
    #Find wav files that have trans files 
    lValidFiles = np.intersect1d(np.asarray(list(map(Get_basename,lWavFiles))),np.asarray(list(map(Get_basename,lTransFiles))),return_indices=True)
    
    #Update files
    lWavFiles = lWavFiles[lValidFiles[1]]
    lTransFiles = lTransFiles[lValidFiles[2]]

    #Get files of selected speakers
    if isfile(sSpkrList):#Load list of selected speakers
        with open(sSpkrList) as flSpkrList:
            lSelectSpkrs = flSpkrList.read().splitlines()
        print(lSelectSpkrs[0], len(lSelectSpkrs))
        lSelectedFilesMap = np.in1d(list(map(Get_SpkrID,lWavFiles)),lSelectSpkrs)
        lWavFiles = lWavFiles[lSelectedFilesMap]





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
    parser.add_argument('-r','--read', help='Use this option to enable processing scripted (read) part of the OGI data', dest='process_read_data', action='store_true',default=False)
    parser.add_argument('-s','--spontaneous', help='Use this option to enable processing of spontaneous part of the data', dest='process_spontaneous_data', action='store_true', default=False)
    parser.add_argument('-l', '--spkrl', help='The file contains list of selected speakers', dest='spkrl', type=str, default='')
    parser.add_argument('-v', '--verify', help='The list of selected verification codes', dest='ver', action=str2list, default=[1,2,4])
    parser.add_argument('-g', '--grade', dest='grd', help='The list of kids grads to be included', action=str2list, default=list(range(0,11)))
    return parser.parse_args()

if __name__ == '__main__':
    args = ArgParser()
    sOGIDir, sTxt, sUtt2Spk, sWavScp = args.OGI_Dir, args.Text_File, args.Utterance_to_Speakers_File, args.Wav_Scp_File
    sSpkrList = args.spkrl
    lVerf = args.ver
    lGrades = args.grd
    with open(sTxt,'a') as fTxt, open(sUtt2Spk,'a') as fUtt2Spk, open(sWavScp,'a') as fWavScp:
        if args.process_read_data:
            get_scripted(sOGIDir, fTxt, fUtt2Spk, fWavScp, sSpkrList=sSpkrList, lVerf = lVerf, lGrades = lGrades)
        if args.process_spontaneous_data:




    



