# coding=utf-8
import time

import numpy as np


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


def algorithm_1(video_sizes, endpoint_latencies, latency_diffs, video_requests):
    number_deleted_max = E  # hand waving criterion!
    video_allocation = np.zeros((C, V))

    # # TODO select smaller video if efficiency is equivalent
    # print("video_max_efficient:\n {}".format(video_max_efficient))
    # cache_sizes = np.dot(video_allocation, video_sizes)
    # video_sizes_stretched = np.tile(video_sizes, (C, 1))
    # selected_video_sizes = np.choose(video_max_efficient, video_sizes_stretched.T)
    # print("selected_video_sizes:\n {}".format(selected_video_sizes))
    # cache_video_fits = cache_capacity_max - cache_sizes >= selected_video_sizes
    # print("videos_fit:\n {}".format(cache_video_fits))
    #
    # video_allocation[cache_video_fits, video_allocation] = 1
    number_deleted = 0
    for i in range(0, V):
        latency_pot_win = np.dot(video_requests.T, latency_diffs)
        # print("latency_pot_win:\n {}".format(latency_pot_win))
        # find global most efficient video
        video_max_efficient_idx = latency_pot_win.argmax()
        video_max_efficient = np.unravel_index(video_max_efficient_idx, latency_pot_win.shape)
        current_video_idx = video_max_efficient[0]
        current_cache_idx = video_max_efficient[1]

        if latency_pot_win[current_video_idx, current_cache_idx] == 0:
            break

        relevant_endpoint_idxs = np.nonzero(latency_diffs[:, current_cache_idx])
        for relevant_endpoint_idx in relevant_endpoint_idxs:
            video_requests[relevant_endpoint_idx, current_video_idx] = 0
        # calculate space
        video_allocation[current_cache_idx, current_video_idx] = 1
        cache_sizes = np.dot(video_allocation, video_sizes)
        if cache_sizes[current_cache_idx] > cache_capacity_max:
            number_deleted += 1
            # print("latency_pot_win:\n {}".format(latency_pot_win))
            video_allocation[current_cache_idx, current_video_idx] = 0
            if number_deleted > number_deleted_max:
                break

    return video_allocation


def output(video_allocation, outputname):
    global C
    summation = np.sum(video_allocation, axis=1)
    used_cache_number = np.size(np.nonzero(summation))
    with open(outputname, 'w') as out:
        out.writelines(str(used_cache_number) + "\n")
        for cache_idx in range(0, C):
            str_out = np.array_str(np.nonzero(video_allocation[cache_idx, :])[0])
            str_out = str_out.replace('\n', '')
            str_out = str_out[1:-1]
            if (str_out != ''):
                out.writelines(str(cache_idx) + " " + str_out + "\n")
    return


def main():
    V = 1  # (1 ≤ V ≤ 10000) - the number of videos
    E = 1  # (1 ≤ E ≤ 1000) - the number of endpoints
    R = 1  # (1 ≤ R ≤ 1000000) - the number of request descriptions
    C = 1  # (1 ≤ C ≤ 1000) - the number of cache servers
    cache_capacity_max = 1  # (1 ≤ X ≤ 500000) - the capacity of each cache server in megabyte

    name = "kittens"
    filename = name + ".in"
    outputname = name + ".out"

    start_time = time.time()
    [video_sizes, endpoint_latencies, latency_diffs, video_requests] = read_file(filename)
    print("Reading took {} seconds".format(time.time() - start_time))
    print("V, E, R, C, X :", V, E, R, C, cache_capacity_max)
    print("video_sizes: {}".format(video_sizes))
    print("endpoint_latencies:\n {}".format(endpoint_latencies))
    print("latency_diffs:\n {}".format(latency_diffs))
    print("video_requests:\n {}".format(video_requests))

    video_allocation = algorithm_1(video_sizes, endpoint_latencies, latency_diffs, video_requests)
    np.save(name + "-video_allocation", video_allocation)

    output(video_allocation, outputname)

    print("video_requests:\n {}".format(video_requests))
    print("video_allocation:\n {}".format(video_allocation))


if __name__ == "__main__":
    main()
