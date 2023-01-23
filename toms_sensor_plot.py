import numpy as np
import matplotlib.pyplot as plt

"""This script takes a set of gear ratios and plots the sensor outputs"""


def calc_ratios(z1, z2, z3, z4):
    """calculate ratios from gear teeth"""
    worm_ratio = z1 / z2
    total_ratio = worm_ratio * (z4 / z3)

    return worm_ratio, total_ratio


def create_data_to_plot(worm_ratio, spur_ratio, total_turns):
    """Create data tobe plotted.Takes gear ratios and total turns and projects
    sensor output across this range"""
    angle_range = range(total_turns * 360)
    worm_angle = []
    spur_angle = []

    for angle in angle_range:
        worm_angle_temp = angle * worm_ratio
        spur_angle_temp = angle * spur_ratio

        # Conditional statements needed to reset sensor outputs once 360
        # degrees is reached
        if worm_angle_temp >= 360:
            worm_angle.append(worm_angle_temp % 360)
        else:
            worm_angle.append(worm_angle_temp)

        if worm_angle_temp >= 360:
            spur_angle.append(spur_angle_temp % 360)
        else:
            spur_angle.append(spur_angle_temp)

    # Calculate the difference between sensor 1 and sensor 2
    angle_offset = np.array(spur_angle) - np.array(worm_angle)
    total_turn_plt = np.array(angle_range) / 360

    # Converts list to array so I can use the in-built numpy mask functions.
    # Mask functions hide data in the array for plotting.
    worm_angle_array = np.array(worm_angle)
    spur_angle_array = np.array(spur_angle)

    # Run conditional masking on the data to hide the reset lines from the plot
    worm_mask = np.ma.masked_where(np.gradient(worm_angle_array) < 0, worm_angle)
    worm_mask_inv = np.ma.masked_where(np.gradient(worm_angle_array) > 0, worm_angle)
    spur_mask = np.ma.masked_where(np.gradient(spur_angle_array) < 0, spur_angle)
    spur_mask_inv = np.ma.masked_where(np.gradient(spur_angle_array) > 0, spur_angle)

    return (
        worm_mask,
        worm_mask_inv,
        worm_angle_array,
        spur_mask,
        spur_mask_inv,
        spur_angle_array,
        angle_offset,
        total_turn_plt,
    )


def create_plots(
    worm_mask, worm_mask_inv, spur_mask, spur_mask_inv, angle_offset, total_turn_plt
):
    #  Plot data
    fig, axs = plt.subplots(2, sharex=True)
    axs[0].plot(total_turn_plt, worm_mask, label="Sensor 1", color="orange")
    axs[0].plot(total_turn_plt, worm_mask_inv, color="grey", linestyle="dotted")

    axs[0].plot(total_turn_plt, spur_mask, label="Sensor 2", color="blue")
    axs[0].plot(total_turn_plt, spur_mask_inv, color="grey", linestyle="dotted")

    plt.xlabel("Total Motor Shaft Rotations")
    plt.xticks([0, 15, 30, 45, 60, 75])
    axs[0].set_ylabel("Sensor Output [degrees]")
    axs[0].legend()

    # Plot offset in angle between worm and spur
    # mask vertical portions of line
    offset_mask = np.ma.masked_where(abs(np.gradient(angle_offset)) > 10, angle_offset)
    offset_mask_inv = np.ma.masked_where(
        abs(np.gradient(angle_offset)) < 10, angle_offset
    )

    # plot data
    axs[1].plot(total_turn_plt, offset_mask, label="offset")
    axs[1].plot(
        total_turn_plt, offset_mask_inv, label="offset", color="grey", linestyle=":"
    )
    axs[1].set_ylabel("(Sensor1 Output) - (Sensor2 Output) [degrees]")
    plt.show()

    # offset_mask_upper_line = np.ma.masked_where(offset_mask > -100, offset_mask)
    # slope, intercept = np.polyfit(total_turn_plt, offset_mask_upper_line, 1)
    # print(slope)


def simulate_error(error_degrees, worm_angle, spur_angle):
    worm_error = worm_angle + error_degrees
    spur_error = spur_angle - error_degrees
    angle_offset_error = spur_error - worm_error

    return angle_offset_error


def calculate_error(offset_angle, offset_angle_error, total_turns):
    total_degrees = total_turns * 360
    masked_offset_angle = np.ma.masked_where(offset_angle < 0, offset_angle)
    masked_offset_angle_error = np.ma.masked_where(
        offset_angle_error < 0, offset_angle_error
    )

    slope1, intercept1 = np.ma.polyfit(total_degrees, masked_offset_angle, 1)
    slope_error, intercept_error = np.ma.polyfit(
        total_turns, masked_offset_angle_error, 1
    )

    x_intercept1 = -intercept1 / slope1
    x_intercept_error = -intercept_error / slope_error

    test_line = slope1 * total_degrees + intercept1

    plt.plot(total_degrees, masked_offset_angle)
    plt.plot(total_degrees, test_line)
    plt.title("this one")
    plt.show()

    return x_intercept1 - x_intercept_error


def plot_offset(angle_offset, angle_offset_error, total_turns):
    plt.plot(total_turns, angle_offset)
    plt.plot(total_turns, angle_offset_error)
    plt.show()


def main():
    # plot data
    z1 = 5
    z2 = 15
    z3 = 30
    z4 = 7
    total_rotations = 90

    worm_ratio, spur_ratio = calc_ratios(z1, z2, z3, z4)
    (
        worm_mask,
        worm_mask_inv,
        worm_angle_array,
        spur_mask,
        spur_mask_inv,
        spur_angle_array,
        angle_offset,
        total_turn_plt,
    ) = create_data_to_plot(worm_ratio, spur_ratio, total_rotations)

    angle_offset_error = simulate_error(0.5, worm_angle_array, spur_angle_array)

    plot_offset(angle_offset, angle_offset_error, total_turn_plt)

    create_plots(
        worm_mask, worm_mask_inv, spur_mask, spur_mask_inv, angle_offset, total_turn_plt
    )

    error = calculate_error(angle_offset, angle_offset_error, total_turn_plt)
    print(error)


if __name__ == "__main__":
    main()
