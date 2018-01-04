# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:42:21 2017

@author: Lenovo
"""
import pyaudio
import numpy as np 
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter
#from pyqt5 import QtGui,QtCore
import pyqtgraph as pg
class Visualization(object):
    """docstring for Visualization"""
    def __init__(self):
        # super(Visualization, self).__init__()
        # self.arg = arg
        
        MultipleLocator(1000)
        FormatStrFormatter('%1.1f')

        win = pg.GraphicsWindow(title='麦克风测试')
        stringaxis = pg.AxisItem(orientation='bottom')
        plot = win.addPlot(axisItems={'bottom': stringaxis}, title='麦克风功能测试')
        label = pg.TextItem()
        plot.addItem(label)
        plot.showGrid(x=True, y=True, alpha=0.5)
        plot.setLabel(axis='left')
        plot.setLabel(axis='bottom', text='time (seconds)')
        plot.setXRange(0.1,0.185)
        plot.setYRange(-5000,5000)
        
        while(win.isVisible()):
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            RECORD_SECONDS = 0.2
            
            p = pyaudio.PyAudio()
            
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
            
            #print("Begin recording")
            
            frames = []
            
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            #print("End recording")
            
            stream.stop_stream()
            stream.close()
            #p.terminate()
            wave_data = np.fromstring(b''.join(frames), dtype=np.short)
            
            # 绘制波形准备工作：左右声道分离
            wave_data.shape = -1, 2  
            wave_data = wave_data.T
            time = np.arange(0, len(wave_data[0])) * (1.0 / RATE)

            #http://blog.51cto.com/6230973/2052761
            # app = pg.QtGui.QApplication([]) #首先实例化一个QT实例
            #stringaxis.setTicks([time, wave_date[1]])
            plot.clear()
            # plot.plotItem.legend.items = []
            plot.plot(x=time[::10], y=wave_data[0][::10], pen='r', size=0.01)#, symbolBrush=(255, 0, 0))
            plot.plot(x=time[::10], y=wave_data[1][::10], pen='g', size=0.01)#, symbolBrush=(0, 255, 0))
            pg.QtGui.QApplication.processEvents()

            #可视化
            #左声道设置
            #ax1 = pl.subplot(211)
            #ax1.yaxis.set_major_locator(ymajorLocator)
            #ax1.yaxis.set_major_formatter(ymajorFormatter)
            #ax1.yaxis.grid(True, which='major')
            #pl.ylim(ymin = -5000, ymax = 5000)
            #ax1.plot(time, wave_data[0])
            #右声道设置
            #ax2 = pl.subplot(212)
            #ax2.yaxis.set_major_locator(ymajorLocator)
            #ax2.yaxis.set_major_formatter(ymajorFormatter)
            #ax2.yaxis.grid(True, which='major')
            #pl.ylim(ymin = -5000, ymax = 5000)
            #ax2.plot(time, wave_data[1])
            #现实上0.1秒录入声音的波形
            #pl.xlabel("time (seconds)")
            # pl.show()
            #pl.savefig('1.jpeg')

            #label = QLabel(self)
            #pixmap = QPixmap('1.jpeg')
            #label.setPixmap(pixmap)
            #self.resize(pixmap.width(),pixmap.height())

            # img_open = Image.open('1.png')
            # img_png = ImageTk.PhotoImage(img_open)
            # label_img = Tkinter.Label(root, image=img_png)
            # label_img.pack()
