from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import bluetooth

win = pg.GraphicsWindow()
win.setWindowTitle('Project RADAR: UDOO Neo Accelerometer Data')


server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 12

server_sock.bind(("", port))  # Bind Client's Socket
server_sock.listen(1)

client_sock, address = server_sock.accept()
print "Accepted connection from ", address

raw = 0
l = [None]*1000  # Init List

p1 = win.addPlot()
p1.setLabel('bottom', 'Time', 's')
p1.setLabel('left', 'ACC_X (m/s^2)')
p1.setYRange(-16000, 16000)
curve1 = p1.plot()
data1 = [0]
ptr1 = 0


def update1():
    global curve1, data1, ptr1, l
    data1[:-1] = data1[1:]
    data1.append(l[0])
    xdata = np.array(data1[:-1], dtype='int32')
    ptr1 += 1
    curve1.setData(xdata, pen='g')
    curve1.setPos(ptr1, 0)


win.nextRow()
p2 = win.addPlot()
p2.setLabel('bottom', 'Time', 's')
p2.setLabel('left', 'ACC_Y (m/s^2)')
p2.setYRange(-16000, 16000)
curve2 = p2.plot()
data2 = [0]
ptr2 = 0


def update2():
    global curve2, data2, ptr2, l
    data2[:-1] = data2[1:]
    data2.append(l[1])
    xdata = np.array(data2[:-1], dtype='int32')
    ptr2 += 1
    curve2.setData(xdata, pen='y')
    curve2.setPos(ptr2, 0)


win.nextRow()
p3 = win.addPlot()
p3.setLabel('bottom', 'Time', 's')
p3.setLabel('left', 'ACC_Z (m/s^2)')
p3.setYRange(-16000, 16000)
curve3 = p3.plot()
data3 = [0]
ptr3 = 0


def update3():
    global curve3, data3, ptr3, l
    data3[:-1] = data3[1:]
    data3.append(l[2])
    xdata = np.array(data3[:-1], dtype='int32')
    ptr3 += 1
    curve3.setData(xdata, pen='r')
    curve3.setPos(ptr3, 0)


# update all plots
def update():
    global raw, l
    raw = client_sock.recv(1024)
    raw = raw[1:-1]  # Drop the square braces
    try:
        l = map(int, raw.split(','))  # String to Integer List
    except ValueError as e:
        raw = client_sock.recv(1024)
        raw = raw[1:-1]  # Drop the square braces
        l = map(int, raw.split(','))  # String to Integer List
        print e

    update1()
    update2()
    update3()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

client_sock.close()
server_sock.close()
