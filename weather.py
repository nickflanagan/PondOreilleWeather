import argparse
import datetime
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
import os


def convert_to_datetime(datetime_str):
    try:
        return datetime.datetime.fromisoformat(datetime_str.replace('_', '-').replace('.', ' '))
    except ValueError:
        return False


def main(start, end):
    print(f"weather from {start} to {end}")
    files = []
    barometric_data = []
    for year in range(int(start.year), int(end.year) + 1):
        data_file = f"resources/Environmental_Data_Deep_Moor_{year}.txt"
        if os.path.isfile(data_file):
            files.append(data_file)
        else:
            print("Date out of range")
            exit(1)
    for file in files:
        with open(file, 'r') as f:
            f.readline()
            for line in f.readlines():
                dt = convert_to_datetime(line.split('\t')[0])
                if dt < start:
                    continue
                elif dt > end:
                    break
                else:
                    barometric_data.append([dt, line.split('\t')[2]])
    return barometric_data


def plot(bp_list):
    x = []
    y = []
    for point in bp_list:
        x.append(point[0])
        y.append(float(point[1]))

    # calculate slope value
    x_start = date2num(x[0])
    x_end = date2num(x[len(x)-1])
    y_start = y[0]
    y_end = y[len(y)-1]
    dy = y_end - y_start
    dt = x_end - x_start
    slope = dy / dt
    if slope > 0:
        slope_color = 'green'
    else:
        slope_color = 'red'

    plt.plot(x, y)
    plt.plot([x_start, x_end], [y_start, y_end], c=slope_color)
    plt.xlabel("Date/Time")
    plt.ylabel("Barometric Pressure (inHg)")
    plt.title("Slope = {0:.6f} inHg/day".format(slope), fontsize=10, fontweight='bold')
    plt.suptitle(f"{x[0]} --> {x[len(x)-1]}", fontsize=11)
    plt.gcf().autofmt_xdate()
    plt.gcf().canvas.set_window_title("Pond Oreille Barometric Pressure")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="Enter Start Date.Time (YYYY-MM-DD.HH:MM:SS")
    parser.add_argument("-e", "--end", help="Enter End Date.Time (YYYY-MM-DD.HH:MM:SS")
    args = parser.parse_args()
    start_date = args.start
    end_date = args.end

    if start_date and end_date:
        start_date = convert_to_datetime(start_date)
        end_date = convert_to_datetime(end_date)
    else:
        print("Enter start date and end date:")
        print("-s --start YYYY-MM-DD.HH:MM:SS")
        print("-e --end  YYYY-MM-DD.HH:MM:SS")
        exit(1)

    if not start_date or not end_date:
        print("Invalid date formats entered")
        exit(1)
    if start_date > end_date:
        print("Start date is > end date")
        print("Please use correct date ranges.")
        exit(1)
    barometric = main(start_date, end_date)

    plot(barometric)
