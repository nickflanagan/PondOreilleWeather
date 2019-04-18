import argparse
import datetime


def convert_to_datetime(datetime_str):
    try:
        return datetime.datetime.fromisoformat(datetime_str.replace('_', '-').replace('.', ' '))
    except ValueError:
        return datetime.datetime.now()


def main(start, end):
    print(f"weather from {start} to {end}")
    files = []
    barometric_data = {}
    for year in range(int(start.year), int(end.year)+1):
        files.append(f"resources/Environmental_Data_Deep_Moor_{year}.txt")
    for file in files:
        with open(file, 'r') as f:
            header = f.readline()
            for line in f.readlines():
                dt = convert_to_datetime(line.split('\t')[0])
                if dt < start:
                    continue
                elif dt > end:
                    break
                else:
                    #barometric_data[dt.strftime("%Y-%m-%d %H:%M:%S")] = line.split('\t')[2]
                    barometric_data[dt] = line.split('\t')[2]
    return barometric_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="Enter Start Date.Time (YYYY-MM-DD.HH:MM:SS")
    parser.add_argument("-e", "--end", help="Enter End Date.Time (YYYY-MM-DD.HH:MM:SS")
    args = parser.parse_args()
    start_arg = args.start
    end_arg = args.end

    start = convert_to_datetime(start_arg)
    end = convert_to_datetime(end_arg)
    barometric = main(start, end)

    for key, value in barometric.items():
        print(f"{key.strftime('%Y-%m-%d %H:%M:%S')}  {value}")
