file_template = f"""
/*
THIS FILE IS AUTO GENERATED
*/
"""

import numpy as np

# export file in the following command 
# [[theta one, theta two, theta one, theta two]]
# [lines] thetas

l1 = 12
l2 = 13 

def convert_theta_into_servo_theta():
    pass

def convert_x_y_into_theta(x, y):
    # return in degree 
    if np.abs((x**2 + y**2 - l1**2  - l2**2 )/(2*l1*l2)) >= 1:
        print(x, y)
        raise Exception

    theta_two = np.arccos((x**2 + y**2 - l1**2  - l2**2 )/(2*l1*l2)) 
    theta_one = np.arctan(y/x) - np.arctan(l2*np.sin(theta_two)/(l1 + l2*np.cos(theta_two)))
    
    # front and back motor
    return 90 - theta_one * 180/np.pi, theta_two * 180/np.pi

def draw_line(x1, y1, x2, y2): 
    sample_count = 100
    if x1 > x2: 
        tmp = x1
        x1 = x2 
        x2 = tmp

    if y1 > y2: 
        tmp = y1
        y1 = y2 
        y2 = tmp

    x = np.linspace(x1, x2, sample_count)
    y = np.linspace(y1, y2, sample_count)
    return x, y 
    
def export_as_string(x, y):
    result = []
    result_string = "char path [] = {"
    for i in range(len(x)):
        theta_one, theta_two = convert_x_y_into_theta(x[i], y[i])
        result.append((theta_one, theta_two))
        result_string += f"{theta_one},"
        if i == len(x) - 1:
            result_string += f"{theta_two}"
        else:
            result_string += f"{theta_two},"

    result_string += '};'
    return result_string

def draw_box(bottom_left_x, bottom_left_y, width, height):
    x1, y1 = draw_line(bottom_left_x, bottom_left_y, bottom_left_x + width, bottom_left_y)
    x2, y2 = draw_line(bottom_left_x + width, bottom_left_y, bottom_left_x + width, bottom_left_y + height)
    x3, y3 = draw_line(bottom_left_x +width, bottom_left_y + height, bottom_left_x, bottom_left_y + height)
    x4, y4 = draw_line(bottom_left_x , bottom_left_y + height, bottom_left_x , bottom_left_y )
    return np.concatenate([x1, x2, x3, x4], axis=0), np.concatenate([y1,  y2 , y3 , y4], axis=0) 

def write_to_file(file, x, y):
    file_template = f"""#ifndef PATH_H\n#define PATH_H\n"""
    file_template += export_as_string(x, y)
    file_template += "\n#endif"
    with open(file, "w") as f:
        f.write(file_template)

if __name__ == "__main__":
    x, y = draw_box(5, 3, 12, 12)
    write_to_file("firmware/path.h", x, y )
    #genereate_test_path()
