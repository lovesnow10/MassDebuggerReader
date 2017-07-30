import os
import sys
import DetectorModel
import DatabaseHelper


class DetectorReader(object):
    """docstring for DetectorReader."""

    def __init__(self, DBpath):
        super(DetectorReader, self).__init__()
        self.DBpath = DBpath
        self.Model = None
        self.DB = None
        self.FuncListNoArg = ('PrintDetectorList', 'Help',
                              'GetSumMass')
        self.FuncList1Arg = ('CreateDataBase', 'GetNdet', 'PrintDetail')

    def Initialize(self):
        self.Model = DetectorModel.DetectorModel()
        self.DB = DatabaseHelper.DatabaseHelper(self.DBpath)

        self.Model.Initialize()
        self.DB.Initialize()

    def Finalise(self):
        self.DB.Cursor.close()
        self.DB.DataBase.close()

    def CreateDataBase(self, physVol):
        self.DB.CreateDB(physVol, self.Model)

    def PrintDetectorList(self):
        for det in self.Model.DetList:
            print('%-20s' % (det))

    def GetNdet(self, det):
        if not self.Model.HasDet(det):
            print 'DetectorReader: %s does not exist.' % (det)
            return
        self.DB.Cursor.execute('''
        SELECT * FROM DETECTOR WHERE CATEGORY = ?
        ''', (det,))

        print len(self.DB.Cursor.fetchall())

    def PrintDetail(self, det):
        if not self.Model.HasDet(det):
            print 'DetectorReader: %s does not exist.' % (det)
            return
        self.DB.Cursor.execute('''
        SELECT * FROM DETECTOR WHERE CATEGORY = ?
        ''', (det,))

        detList = self.DB.Cursor.fetchall()
        print ('''%-20s%-20s%-20s%-20s%-20s%-20s
        %-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s'''
               % ('RowID', 'PhysName', 'Index', 'LogiName',
                  'Shape', 'Material', 'Mass', 'Volume',
                  'Density', 'Par1', 'Par2', 'Par3', 'Category', 'Mother'))
        print '-----------------------'
        for row in detList:
            print ('''%-20s%-20s%-20s%-20s%-20s%-20s
            %-20s%-20s%-20s%-20s%-20s%-20s%-20s%-20s'''
                   % (row[0], row[1], row[2], row[3], row[4],
                      row[5], row[6], row[7], row[8], row[9],
                      row[10], row[11], row[12], row[13]))

    def GetSumMass(self):
        self.DB.Cursor.execute('''
        SELECT CATEGORY, SUM(MASS) FROM DETECTOR GROUP BY CATEGORY
        ''')
        detList = self.DB.Cursor.fetchall()
        print('%-20s%-20s' % ('Detector', 'Mass(g)'))
        print('-----------------------')
        for row in detList:
            print('%-20s%-20s' % (row[0], row[1]))

    def Help(self):
        print 'Following commands are available:'
        print '''
        * CreateDataBase physVol: Create data base using givin physVols file.
        '''
        print '''
        * PrintDetectorList: Print all detector
         categories in the DetectorModel.
        '''
        print '''
        * PrintDetail DETNAME: Print detailed detector
         information for a given category.
        '''
        print '''
        * GetNdet DETNAME: Get the quantity of detectors for a given category.
        '''
        print '''
        * GetSumMass: Show sum of mass for all categories.
        '''
        print '''
        * Help: Show this menu.
        '''
