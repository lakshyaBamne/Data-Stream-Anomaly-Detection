import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count

class DataStream:
    """
        Class to represent a simulated data stream
    """

    def __init__(self, base_val=10, trend_slope=0.01, seasonal_period=50, noise_level=0.5, anomaly_level=1, anomaly_chance=0.05):
        """
            constructor
        """
        self.base_val = base_val
        self.trend_slope = trend_slope
        self.seasonal_period = seasonal_period
        self.noise_level = noise_level
        self.anomaly_level = anomaly_level
        self.anomaly_chance = anomaly_chance

        # initialize a generator object using the given values
        self.stream = self.stream_generator()
        self.xdata = []
        self.ydata = []
        self.curr_time = 1

    def baseline_trend(self, t):
        """
            Method which determines the underlying trend for the baseline value
            which may be linear, quadratic, exponential, etc
        """
        # linear trend
        return self.base_val + t*self.trend_slope 

    def seasonal_trend(self, t):
        """
            Method which determines the seasonal trend for the data
            this may be any periodic function which repeats exactly 1 complete cycle
            in the given seasonal period
        """
        # baseline value at this point in time
        bt = self.baseline_trend(t)

        # amplitude of the seasonal changes is taken as 10% of base value
        amp = max(1, 0.1*bt)

        return amp*np.sin(t*(2*np.pi/self.seasonal_period))
    
    def noise(self, t):
        """
            Method to generate random noise based on the standard normal distribution
        """
        # baseline value at this point in time
        bt = self.baseline_trend(t)

        return self.noise_level*bt*np.random.randn()

    def anomaly(self, t):
        """
            Method to generate anomay in the data with the specified chance
            -> anomalous value is generated as 50% of the baseline value in positive or negative direction
        """
        # baseline value at this point in time
        bt = self.baseline_trend(t)

        if np.random.random() < self.anomaly_chance:
            return np.random.choice([min(-1, -bt*abs(1-self.anomaly_level)), max(1, bt*abs(1-self.anomaly_level))])
        else:
            return 0
        
    def generate_data_point(self, t):
        """
            Method to generate a single data point having the 4 components
            -> baseline trend
            -> seasonal trend
            -> random noise
            -> anomaly
        """
        return self.baseline_trend(t) + self.seasonal_trend(t) + self.noise(t) + self.anomaly(t)
    
    def stream_generator(self):
        """
            generator method to generate a new value for the stream whenever required
        """
        while True:
            yield self.curr_time, self.generate_data_point(self.curr_time)
            self.curr_time += 1

    def visualize(self, total_frames=100, time_step=1000):
        """
            Function to visualize real time data generated using the created class
        """
        def animate(index):
            self.xdata.append(self.curr_time)
            self.ydata.append(self.generate_data_point(self.curr_time))

            self.curr_time += 1
            print(f"t={self.curr_time} f(t)={self.ydata[-1]}")

            plt.cla()
            plt.plot(self.xdata, self.ydata, marker='.', markersize=5, label=f"t={self.curr_time}")
            plt.legend(loc='upper left')
            plt.tight_layout()

        ani = FuncAnimation(plt.gcf(), animate, frames=range(total_frames), interval=time_step, repeat=False)
        plt.tight_layout()
        plt.show()

        plt.cla()
        plt.plot(self.xdata, self.ydata, marker='.', markersize=5, label=f"data till t={self.curr_time}")
        plt.tight_layout()
        plt.legend(loc='upper left')
        plt.show()
