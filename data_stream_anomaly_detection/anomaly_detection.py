import os
import time
import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .data_stream import DataStream

class AnomalyDetection:
    """
        Class represents the anomaly detection algorithm customized by the user
    """

    def __init__(self, filename="data.txt", anomaly_log="anomaly.txt" ,global_window=1000, total_reads=1000, local_window=100, time_period=1000, point_tolerance=3):
        """
            Constructor
        """
        self.filename = filename
        self.anomaly_log = anomaly_log
        self.global_window = global_window
        self.local_window = local_window
        self.time_period = time_period
        self.total_reads = total_reads

        self.anomaly_tag = []
        self.xdata = []
        self.ydata = []
        self.prev_len = 0

        # some variables to determine tolerance for the anomaly detection
        self.point_tolerance = point_tolerance

        # some parameters for the local window are stored as class variables
        self._lmean = 0
        self._lvar = 0
        self._lsd = 0

        # other initialization tasks
        if os.path.exists(self.anomaly_log):
            os.remove(self.anomaly_log)

    def update_stream_data(self):
        """
            Method to update new data from the stream
        """
        with open(file=self.filename, mode='r') as f:
            lines = f.readlines()
            if len(lines) > self.prev_len:
                # new information is present
                for line in lines[self.prev_len:]:
                    line_data = list(map(float, line.split(',')[:-1]))
                    self.xdata.append(int(line_data[0]))
                    self.ydata.append(line_data[1])
                    self.anomaly_tag.append(False)
                    self.prev_len += 1

                print(f"new data added : {self.xdata[-1]} {self.ydata[-1]} {self.prev_len}")

                # update the data in the local window according to the new information
                self.update_local_window()

            else:
                # new information not present
                pass

    def point_anomaly(self):
        """
            Method to detect the point anomaly using data in the local window only
        """
        if self.ydata[-1]<=self._lmean-self._lsd*self.point_tolerance or self.ydata[-1]>=self._lmean+self._lsd*self.point_tolerance:
            # point anomaly detected
            return True
        else:
            # no point anomaly detected
            return False

    def report_anomaly(self):
        """
            Method to report the last added point as anomolous and write it to a log file
        """
        print(f"[ANOMALY DETECTED] : {self.xdata[-1]} {self.ydata[-1]}")
        with open(self.anomaly_log, mode='a') as f:
            f.write(f"{self.xdata[-1]},{self.ydata[-1]},\n")

    def update_local_window(self):
        """
            Method to check if the new data is point anomolous or not
            If it is, report and log and remove it from the data
            Else update the local window parameters with the new data point included
        """
        if self.prev_len > self.local_window:
            # there is enough data for 1 complete local window
            # check if the newly added point is point anomaly
            if self.point_anomaly():
                self.anomaly_tag[-1] = True
                self.report_anomaly()
            else:

                irem = -self.local_window-1
                iadd = -1

                self._lmean = self._lmean - (self.ydata[irem]/self.local_window) + (self.ydata[iadd]/self.local_window)
                self._lvar = self._lvar - ( (self.ydata[irem]-self._lmean)**2/(self.local_window-1) ) + ( (self.ydata[iadd]-self._lmean)**2/(self.local_window-1) )
                self._lsd = math.sqrt(self._lvar)

        else:
            # there is not enough data for 1 complete local window
            self._lmean += self.ydata[-1]/self.local_window
            self._lvar += (self.ydata[-1]-self._lmean)**2/(self.local_window-1)
            self._lsd = math.sqrt(self._lvar)

    def visualize(self):
        """
            Function to visualize the data stream from the external file
        """
        def animate(i):
            # update the stream data before drawing any frame
            self.update_stream_data()

            plt.cla()

            # plot the data points
            plt.plot(self.xdata[:-self.local_window], self.ydata[:-self.local_window], marker='.', markersize=5, label=f"global window")
            plt.plot(self.xdata[-self.local_window:], self.ydata[-self.local_window:], marker='.', markersize=5, color="orange", label=f"local window")
            for pid in range(self.prev_len):
                if self.anomaly_tag[pid]:
                    plt.plot(self.xdata[pid], self.ydata[pid], marker="*", markersize=5, color="red")

            # plot some metrics for point anomaly detection
            plt.axhline(self._lmean+self._lsd*self.point_tolerance, xmin=0, xmax=self.xdata[-1], color="yellow", label=f"{self.point_tolerance}sd")
            plt.axhline(self._lmean, xmin=0, xmax=self.xdata[-1], color="yellow", label="lw mean")
            plt.axhline(self._lmean-self._lsd*self.point_tolerance, xmin=0, xmax=self.xdata[-1], color="yellow", label=f"-{self.point_tolerance}sd")

            plt.legend(loc='upper left')
            plt.tight_layout()


        ani = FuncAnimation(plt.gcf(), animate, frames=range(self.total_reads), interval=self.time_period, repeat=False)
        plt.tight_layout()
        plt.show()

        plt.cla()
        # plot the data points
        plt.plot(self.xdata[:-self.local_window], self.ydata[:-self.local_window], marker='.', markersize=5, label=f"before local window")
        plt.plot(self.xdata[-self.local_window:], self.ydata[-self.local_window:], marker='.', markersize=5, color="orange", label=f"inside local window")
        for pid in range(self.prev_len):
            if self.anomaly_tag[pid]:
                plt.plot(self.xdata[pid], self.ydata[pid], marker="*", markersize=5, color="red")

        plt.legend(loc='upper left')
        plt.tight_layout()
        plt.show()
    

