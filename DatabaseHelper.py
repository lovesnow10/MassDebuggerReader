import sqlite3
import os
import sys
import DetectorModel


class DatabaseHelper(object):
    """docstring for DatabaseHelper."""

    def __init__(self, DBpath):
        super(DatabaseHelper, self).__init__()
        self.DBpath = DBpath
        self.isNew = False

    def Initialize(self):
        self.CheckCreated()
        if self.isNew:
            print 'DataBaseHelper: You are creating a new DB file,'
        else:
            print 'DataBaseHelper: You are using a existing DB file.'

        self.DataBase = sqlite3.connect(self.DBpath)
        self.Cursor = self.DataBase.cursor()

    def CheckCreated(self):
        self.isNew = os.path.isfile(self.DBpath)

    def CreateDB(self, physVol, detMod):
        print 'DataBaseHelper: Table will be dropped if already exists'
        self.Cursor.execute('''DROP TABLE IF EXISTS DETECTOR''')
        self.Cursor.execute('''CREATE TABLE IF NOT EXISTS DETECTOR
        (ROWID      INTEGER PRIMARY KEY AUTOINCREMENT,
        PHYSNAME    TEXT    NOT NULL,
        ID          INT     NOT NULL,
        LOGINAME    TEXT    NOT NULL,
        SHAPE       TEXT    NOT NULL,
        MATERIAL    TEXT    NOT NULL,
        MASS        REAL    NOT NULL,
        VOLUME      REAL    NOT NULL,
        DENSITY     REAL    NOT NULL,
        PAR1        REAL,
        PAR2        REAL,
        PAR3        REAL,
        CATEGORY    TEXT    NOT NULL,
        MOTHER      TEXT);''')

        file_phys = open(physVol)
        lns = file_phys.readlines()

        for line in lns:
            line = line.strip()
            vals = line.split('\t')
            physName = vals[0]
            Index = int(vals[1])
            logiName = vals[2]
            Shape = vals[7]
            Material = vals[8]
            Mass = float(vals[9])
            Volume = float(vals[10])
            Density = float(vals[11])
            Par1 = float(vals[12])
            Par2 = float(vals[13])
            Par3 = float(vals[14])
            Category = detMod.GetDetType(physName, logiName)
            Mother = detMod.Mother[Category]

            self.Cursor.execute('''INSERT INTO DETECTOR VALUES
            (NULL , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?);''',
                                (physName, Index, logiName, Shape, Material,
                                 Mass, Volume,
                                 Density, Par1, Par2, Par3, Category, Mother))
        self.DataBase.commit()
        print 'DataBaseHelper: DB created.'
