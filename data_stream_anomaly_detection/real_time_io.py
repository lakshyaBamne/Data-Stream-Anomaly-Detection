"""
    Module contains some utility functions for input/output operations
    useful in the real time anomaly detection programs
"""
import time
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .data_stream import DataStream

def write_real_time_data(stream: DataStream, filename: str = "data.txt", time_period: int = 1000, total_writes: int = 10000) -> None:
    """
        Function writes new data into an external file after a specified time period
        we simply append the new data at the end of the file using commas (,) as separators
    """
    # first we need to clear the given file so that new data is generated
    if os.path.exists(filename):
        os.remove(filename)

    for i in range(total_writes):
        # write new data into the file
        with open(file=filename, mode='a') as f:
            t, ft = next(stream.stream)
            f.write(f"{t},{ft},\n")
            print(f"{t} {ft}")

        # wait for the time period to write new data
        time.sleep(time_period/1000)

    print(f"--- TOTAL WRITES COMPLETE ---")



