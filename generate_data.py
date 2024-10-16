"""
    Python script to generate new data according to the simulated data stream and
    write it into an external text file which can be read by another program
"""
import data_stream_anomaly_detection as ds

st = ds.DataStream(base_val=10, trend_slope=0.02, seasonal_period=50, noise_level=0.1, anomaly_level=2, anomaly_chance=0.05)
ds.write_real_time_data(st)

