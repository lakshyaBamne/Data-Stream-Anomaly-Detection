import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import data_stream_anomaly_detection as ds

anomaly_detector = ds.AnomalyDetection(global_window=500, local_window=100, total_reads=1000, point_tolerance=1.5)
anomaly_detector.visualize()


