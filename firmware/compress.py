import numpy as np
# redraw path to only use 500 points instead of how every many points it requires
def calculate_distance(x1, y1, x2, y2):
     return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def distance_distribut(all_x, all_y):
    total_length = 0
    for i in range(1, len(all_x), 1):
        previous_x = all_x[i - 1]
        previous_y = all_y[i - 1]
        length = calculate_distance(previous_x, previous_y, all_x[i], all_y[i])
        total_length += length 
    
    print(f"The total length is {total_length}")
    length_delta = total_length / 500 
    new_x = [all_x[0]]
    new_y = [all_y[0]]
    i = 1
    
    while  i < len(all_x): 
        if calculate_distance(all_x[i], all_y[i], new_x[-1], new_y[-1]) >  length_delta:
            new_x.append(all_x[i])
            new_y.append(all_y[i])

        i += 1 
    
    print(f"There are: {len(new_x)}  points")
    return new_x, new_y

def even_distribute(all_x, all_y):
    delta_x = (len(all_x) - 1) / 500
    new_x = []
    new_y = []
    for i in range(500):
        index = int(i * delta_x)
        new_x.append(all_x[index])
        new_y.append(all_y[index])
    return new_x, new_y


def compress_paths(all_x, all_y, is_even_distribute=True): 
    # calculate the total length 
    if is_even_distribute: 
        return even_distribute(all_x, all_y)
    # distance distribute
    return distance_distribut(all_x, all_y)