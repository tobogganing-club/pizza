# coding=utf-8
import time

import numpy as np

V = 1  # (1 ≤ V ≤ 10000) - the number of videos
E = 1  # (1 ≤ E ≤ 1000) - the number of endpoints
R = 1  # (1 ≤ R ≤ 1000000) - the number of request descriptions
C = 1  # (1 ≤ C ≤ 1000) - the number of cache servers
cache_capacity_max = 1  # (1 ≤ X ≤ 500000) - the capacity of each cache server in megabyte


def read_file(filename):
    # write into global variables
    global V, E, R, C, cache_capacity_max
    # open file read only
    with open(filename, 'r') as file:
        # read first line with general information
        header = file.readline()
        header2 = file.readline()
        # remove linebreak '\n' and split numbers
        header = header.rstrip('\n').split(' ')
        header2 = header2.rstrip('\n').split(' ')
        # save in global variable
        [V, E, R, C, cache_capacity_max] = map(int, header)
        video_sizes = np.array(header2, dtype=int)

        # create arrays
        endpoint_latencies = np.zeros(E, dtype=int)
        latency_diffs = np.zeros((E, C), dtype=int)
        video_requests = np.zeros((E, V), dtype=int)

        for endpoint_idx in range(0, E):
            line = file.readline()
            [datacenter_latency, caches] = map(int, line.rstrip('\n').split(' '))
            endpoint_latencies[endpoint_idx] = datacenter_latency
            for i in range(0, caches):
                cache_latency_line = file.readline()
                [cache_idx, cache_latency] = map(int, cache_latency_line.rstrip('\n').split(' '))
                latency_diffs[endpoint_idx, cache_idx] = datacenter_latency - cache_latency
        for line in file:
            [video_idx, endpoint_idx, requests] = map(int, line.rstrip('\n').split(' '))
            video_requests[endpoint_idx, video_idx] = requests

    return [video_sizes, endpoint_latencies, latency_diffs, video_requests]


filename = "example-video.in"
[video_sizes, endpoint_latencies, latency_diffs, video_requests] = read_file(filename)

print("V, E, R, C, X :", V, E, R, C, cache_capacity_max)
print("video_sizes: {}".format(video_sizes))
print("endpoint_latencies:\n {}".format(endpoint_latencies))
print("latency_diffs:\n {}".format(latency_diffs))
print("video_requests:\n {}".format(video_requests))
