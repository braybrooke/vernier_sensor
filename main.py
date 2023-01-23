import math
import csv

# z1 = worm starts
# z2 = worm teeth
# z3 = spur 1 teeth
# z4 = spur 2 teeth

#  create function to set range limits for all variables
def create_library():
    """Function to create library of gear ratios to be analysed. Set limits by setting limit variables within function"""
    worm_starts_limits = [1, 6]
    worm_wheel_teeth_limits = [5, 31]
    spur_gear1_teeth_limits = [7, 31]
    spur_gear2_teeth_limits = [7, 31]

    # Create list of integers between limits. Each entry of range represents a
    # number of gear teeth
    worm_starts_range = list(range(worm_starts_limits[0], worm_starts_limits[1]))
    worm_wheel_teeth_range = list(
        range(worm_wheel_teeth_limits[0], worm_wheel_teeth_limits[1])
    )
    spur_gear1_teeth_range = list(
        range(spur_gear1_teeth_limits[0], spur_gear1_teeth_limits[1])
    )
    spur_gear2_teeth_range = list(
        range(spur_gear2_teeth_limits[0], spur_gear2_teeth_limits[1])
    )

    # Create empty lists to be filled in nested loops
    worm_start_list = []
    worm_wheel_teeth_list = []
    spur_gear1_teeth_list = []
    spur_gear2_teeth_list = []

    # Loop over all combinations of gear teeth to create design space
    for worm_start in worm_starts_range:
        for worm_wheel_teeth in worm_wheel_teeth_range:
            for spur_gear1_teeth in spur_gear1_teeth_range:
                for spur_gear2_teeth in spur_gear2_teeth_range:
                    worm_start_list.append(worm_start)
                    worm_wheel_teeth_list.append(worm_wheel_teeth)
                    spur_gear1_teeth_list.append(spur_gear1_teeth)
                    spur_gear2_teeth_list.append(spur_gear2_teeth)

    # return lists representing the design space
    return (
        worm_start_list,
        worm_wheel_teeth_list,
        spur_gear1_teeth_list,
        spur_gear2_teeth_list,
    )


#  Create function to calculate total gear ratio
def calc_gear_ratios(z1, z2, z3, z4):
    """Calculate gear ratios from given gear teeth selection"""
    gear1_ratio = z1 / z2
    gear2_ratio = z4 / z3
    total_ratio = gear1_ratio * gear2_ratio

    return gear1_ratio, gear2_ratio, total_ratio


def gcd_float(a, b):
    """GCD functon for floating point numbers. In-built Python function only
    accepts integers so had to create my own, stolen from Stack Overflow."""

    if a < b:
        return gcd_float(b, a)

    # base case
    if abs(b) < 0.001:
        return a
    else:
        return gcd_float(b, a - math.floor(a / b) * b)


#  Create function to calculate LCM
def calc_lcm(x, y):
    """Calculates the lowest common multiple using the GCD"""
    return abs(x * y) // gcd_float(x, y)


#  Function to give total rotations:
def calc_total_rotations(z1, z2, z3, z4):
    """Calculates the total possible rotations able to be sensed absolutely by
    a given gear ratio combination"""

    gear_ratios = calc_gear_ratios(z1, z2, z3, z4)
    total_rotations = calc_lcm((360 / gear_ratios[0]), (360 / gear_ratios[2])) / 360

    return total_rotations, gear_ratios[2]


def 


def main():
    # Create gear library by running function
    gear_library = create_library()

    # Create empty lists to be filled by loop
    z1_output = []
    z2_output = []
    z3_output = []
    z4_output = []
    total_rotations_output = []
    total_ratio_output = []

    # Loop over entire design space, running the total rotation function to
    # calculate the number of absolute rotations possible. If beow required 74,
    # discard the design.
    for z1, z2, z3, z4 in zip(*gear_library):
        total_rotation = calc_total_rotations(z1, z2, z3, z4)
        if total_rotation[0] >= 89:
            z1_output.append(z1)
            z2_output.append(z2)
            z3_output.append(z3)
            z4_output.append(z4)
            total_rotations_output.append(total_rotation[0])
            total_ratio_output.append(total_rotation[1])

    # Oganise data ready for output. Header and data lists ready for .csv conversion
    headers = ["z1", "z2", "z3", "z4", "total rotations", "total_ratio"]
    data = [
        z1_output,
        z2_output,
        z3_output,
        z4_output,
        total_rotations_output,
        total_ratio_output,
    ]

    # zip function reorganises the data list into rows for the csv. Takes
    # lists representing columns and converts into lists for each row.
    rows = zip(*data)

    # csv.writer function creates teh csv in the format we need. First the
    # header row written to file, then we loop over all rows writing them
    # to file.
    with open("vernier_output_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    main()
