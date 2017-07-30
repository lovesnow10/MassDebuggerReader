import DetectorModel
import DetectorReader
import DatabaseHelper
import sys
import os


def Worker(app):
    for i in xrange(1000):
        cmd = raw_input('[%i] ' % (i))
        if cmd == 'exit' or cmd == 'Exit' or cmd == 'EXIT':
            break
        tmp = cmd.split(' ')[0]
        if tmp in app.FuncListNoArg:
            func = getattr(app, tmp)
            func()
        elif tmp in app.FuncList1Arg:
            arg = cmd.split(' ')[1]
            func = getattr(app, tmp)
            func(arg)
        else:
            print 'Command %s not available, please check.\
            Use "Help" to see all available commands' % (tmp)
            continue

        print ''


def main(DBpath):
    app = DetectorReader.DetectorReader(DBpath)
    app.Initialize()

    Worker(app)

    app.Finalise()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Please specify DataBase file!'
        sys.exit(-1)
    main(sys.argv[1])
