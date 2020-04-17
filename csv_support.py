import csv
import random
from Task import Task

def generate(_n: int, _w: int, _s: int, output_file: str) -> None:
    """
    Generates a csv file with n objects
    :param _n: maximum number of objects
    :param _w: maximum capacity of the knapsack
    :param _s: maximum size of the knapsack
    :param output_file: name of the file
    :return: None
    """
    w_threshold: int = 10 * int(_w / _n)
    s_threshold: int = 10 * int(_s / _n)

    # csv file handle
    with open(output_file, 'w', newline='') as csvfile:
        output_csv = csv.writer(csvfile, delimiter=',', quotechar='|')

        # write first line
        output_csv.writerow((_n, _w, _s))

        # random seed
        random.seed()
        total_w_i = 0
        total_s_i = 0
        for _i in range(_n):
            # item is a tuple of (w_i, s_i, c_i)
            w_i = random.randint(1, w_threshold - 1)
            s_i = random.randint(1, s_threshold - 1)
            c_i = random.randint(1, _n - 1)
            total_w_i += w_i
            total_s_i += s_i
            item = w_i, s_i, c_i
            output_csv.writerow(item)


def read(input_file: str) -> Task:
    """
    Reads a csv file and converts it to a Task
    :param input_file: Name of the file
    :return: Task
    """
    # csv file handle
    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        # https://stackoverflow.com/a/60011999
        _n, _w, _s = next(reader)
        # print('n', n, 'w', w, 's', s)

        # https://stackoverflow.com/a/33549711
        list_of_items = [(int(row[0]), int(row[1]), int(row[2])) for row in reader]
        # print(list_of_items)

        return Task(int(_n), int(_w), int(_s), list_of_items)

if __name__ == "__main__":
    filename: str = "output.csv"
    n: int = 1000
    w: int = 10000
    s: int = 10000
    generate(n, w, s, filename)