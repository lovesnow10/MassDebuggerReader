import json
import os
import sys


class DetectorModel(object):
    """docstring for DetectorModel."""

    def __init__(self):
        super(DetectorModel, self).__init__()
        self.ModelJson = ("DetectorModel.json")
        self.DetList = []
        self.Mother = {}
        self.Daughter = {}
        self.Selection = {}
        self.auxSelection = {}
        self.Category = {}

    def Initialize(self):
        mJson = json.load(file(self.ModelJson))

        for det, content in mJson.items():
            det = det.encode()
            self.DetList.append(det)
            self.Category[det] = content['Category']
            self.Selection[det] = content['Sel']
            self.auxSelection[det] = content['auxSel']
            self.Mother[det] = content['Mother']
            if content['Mother'] in self.Daughter:
                self.Daughter[content['Mother']].append(det)
            else:
                self.Daughter[content['Mother']] = []
                self.Daughter[content['Mother']].append(det)

            print 'DetectorModel: Building detector %s done.' % (det)

    def GetDetType(self, physName, volName):
        if 'Pixel::' in physName:
            physName = physName[7:]
        if 'Pixel::' in volName:
            volName = volName[7:]
        for det in self.DetList:
            if self.Selection[det] in volName and \
             self.auxSelection[det] in physName:
                return self.Category[det]
        print 'DetectorModel: Cannot find detector %s!!!' % (physName)
        return 'None'

    def HasDet(self, det):
        return det in self.DetList
