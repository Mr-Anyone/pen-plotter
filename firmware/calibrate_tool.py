import numpy as np 
from sympy import Matrix

# l1: 12 cm
# l2: 13 cm

if __name__ == "__main__":
    trial_one_angle_one = 10 * np.pi / 180
    trial_one_angle_two = 10 * np.pi / 180
    x1 = 26-0.5
    y1 = 10.5

    m = Matrix([
        [np.cos(trial_one_angle_one), np.cos(trial_one_angle_two + trial_one_angle_one), x1],
        [np.sin(trial_one_angle_one), np.sin(trial_one_angle_two + trial_one_angle_one), y1],
    ])

    print("Length One Length Two, Offset One Offset Two")
    print(m.rref())