# This is a sample Python script.
from itertools import count
from shlex import split


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
from itertools import chain

def decode():
    prev_dial = 50
    dial = 50
    zeros = 0
    zeros_clicks = 0
    with open("test.txt") as file:
        #code = file.readline()
        for line in file:
            direction = (1 if line[0] == "R" else -1)
            number = int(line[1:])
            #code = file.readline()
            rotation = direction * number
            print("rotation", rotation)
            dial += rotation
            print("dial", dial)
            temp = abs(dial) // 100
            print("temp", temp)

            if dial < 0 and prev_dial != 0:
                zeros_clicks += 1
                zeros_clicks += temp
            elif dial > 100:
                zeros_clicks += temp


            dial %= 100
            print("dial mod", dial)
            if dial == 0:
                zeros += 1
                zeros_clicks += 1
            prev_dial = dial
            print("zeros_clicks", zeros_clicks)
        print(zeros)
        print(zeros_clicks)


def lock_sim():
    dial = 50
    zeros_clicks = 0
    with open("code.txt") as file:
        for line in file:
            direction = (1 if line[0] == "R" else -1)
            number = int(line[1:])
            rotation = direction * number
            while rotation != 0:
                rotation -= direction
                dial -= direction
                #print("dial", dial)
                dial %= 100
                if dial == 0:
                    zeros_clicks += 1
    print("zeros_clicks", zeros_clicks)


def id_validation():
    invalid_ids = []
    with open("ids.txt") as file:
        id_ranges = file.read().split(',')
        print("id_ranges", id_ranges)
        for id_range in id_ranges:
            id_range = id_range.split("-")
            print("id_range", id_range)
            for i in range(int(id_range[0]), int(id_range[1]) + 1):
                i_str = str(i)
                #if len(i_str) % 2 == 0:
                #    if i_str[:len(i_str)//2] == i_str[len(i_str)//2:]:
                #        invalid_ids.append(i)
                #print(i)
                for j in range(1, (len(i_str)//2)+1):
                    if len(i_str) % j == 0:
                        digit_seq = i_str[:j]
                        #print("digit_seq", digit_seq)
                        #print(i_str.count(digit_seq))
                        #print("j", j)
                        if i_str.count(digit_seq) * j == len(i_str):
                            invalid_ids.append(i)
                            #print("invalid_ids", invalid_ids)
                            break

    print("invalid_ids", invalid_ids)
    print("sum", sum(invalid_ids))


def jolting_it():
    with open("power_banks.txt") as power_banks:
        joltages = 0
        for line in power_banks:
            bank = line.strip("\n")
            print("bank", bank, len(bank))
            idx1 = 0
            idx2 = 1
            if int(bank[idx2]) > int(bank[idx1]):
                idx1 = idx2
                idx2 += 1
            for battery_idx in range(2, len(bank)-1):
                if int(bank[battery_idx]) > int(bank[idx1]):
                    idx1 = battery_idx
                    idx2 = battery_idx + 1
                    #print("new 1 and 2:", idx1, idx2)
                elif int(bank[battery_idx]) > int(bank[idx2]):
                    idx2 = battery_idx
                    #print("new 2:", idx2)
            if int(bank[-1]) > int(bank[idx2]):
                idx2 = len(bank)-1
            print("indices", idx1, idx2, "values", bank[idx1], bank[idx2])
            joltages += 10 * int(bank[idx1]) + int(bank[idx2])
        print("joltages", joltages)

def jolting_it_more():
    with open("power_banks.txt") as power_banks:
        joltages = 0
        for line in power_banks:
            bank = line.strip("\n")
            print("bank", bank, len(bank))
            idx_lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            for i in range(len(idx_lst)):
                for battery_idx in range(idx_lst[i], len(bank) - len(idx_lst) + 1 + i):
                    if int(bank[battery_idx]) > int(bank[idx_lst[i]]):
                        idx_lst[i] = battery_idx

                if i != len(idx_lst)-1:
                    idx_lst[i+1] = idx_lst[i] + 1

            print("indices", idx_lst)
            print("values", "".join([bank[i] for i in idx_lst]))
            joltages += int("".join([bank[i] for i in idx_lst]))
        print("joltages", joltages)

def paper_rolls(overwrite:list[list]=None):
    with open("paper_shelve.txt") as shelve:
        padded_shelve = []  # np.ndarray([])
        if overwrite is None:
            row = shelve.readline().strip("\n")
            padded_shelve.append('.' + "".join(['.' for i in range(len(row))]) + '.')
            #np.append(padded_shelve, '.' + "".join(['.' for i in range(len(row))]) + '.')
            padded_shelve.append('.' + row + '.')
            #np.append(padded_shelve, '.' + row + '.')
            for line in shelve:
                row = line.strip("\n")
                padded_shelve.append('.' + row + '.')

            padded_shelve.append('.' + "".join(['.' for i in range(len(row))]) + '.')
        else:
            padded_shelve = overwrite


        movable_rolls = 0
        for i in range(1, len(padded_shelve) - 1):
            row = padded_shelve[i]
            print(row)
            for j in range(1, len(row) - 1):
                space = row[j]
                #print(space)
                if space == '@':
                    neighborhood = [padded_shelve[i + idx1][j + idx2] for idx1 in range(-1, 2) for idx2 in range(-1, 2)]#[padded_shelve[i - 1][j - 1], padded_shelve[i][j - 1], padded_shelve[i + 1][j - 1]]
                    #print("n", neighborhood)
                    neighborhood_roll_num = neighborhood.count('@') - 1 + neighborhood.count('X')
                    if neighborhood_roll_num < 4:
                        new_row = list(row)
                        new_row[j] = 'X'
                        #print("row new", new_row)
                        row = "".join(new_row)
                        movable_rolls += 1
            padded_shelve[i] = row
        print("movable_rolls", movable_rolls)
        print("padded_shelve", padded_shelve)
        return padded_shelve, movable_rolls

def paper_rolls_transport():
    padded_shelve, movable_rolls = paper_rolls()
    final_moves = movable_rolls
    while movable_rolls > 0:
        for i in range(1, len(padded_shelve) - 1):
            row = padded_shelve[i]
            new_row = list(row)
            for j in range(1, len(row) - 1):
                if new_row[j] == 'X':
                    new_row[j] = '.'
            padded_shelve[i] = "".join(new_row)
        print("padded_shelve clean", padded_shelve)
        padded_shelve, movable_rolls = paper_rolls(overwrite=padded_shelve)
        final_moves += movable_rolls
    print("final_moves", final_moves)


def fridge_check():
    with open("fridge.txt") as fridge:
        ranges, inventory = [], []
        line = fridge.readline()
        while line != "\n":
            ranges.append(line.strip("\n").split("-"))
            line = fridge.readline()

        for line in fridge:
            inventory.append(line.strip("\n"))
        print("inventory", inventory)

        fresh_count = 0
        for id in inventory:
            for r in ranges:
                if int(r[0]) <= int(id) <= int(r[1]):
                    fresh_count += 1
                    print(id, r)
                    break
    print("fresh_count", fresh_count)


def fridge_check2():
    with open("fridge.txt") as fridge:
        ranges = []
        line = fridge.readline()
        while line != "\n":
            r = line.strip("\n").split("-")
            r[0] = int(r[0])
            r[1] = int(r[1])
            ranges.append(r)
            line = fridge.readline()
        #range_min = min(list(chain(*ranges)))
        #for r in ranges:
        #    r[0] -= range_min
        #    r[1] -= range_min
        print("ranges", ranges)
        fresh_count = 0
        #fresh_ids = set()
        entry_removed = True
        while entry_removed:
            entry_removed = False
            i = 0
            while i < len(ranges):
                j = i + 1
                while j < len(ranges):
                    if ranges[j][0] <= ranges[i][0] <= ranges[j][1] \
                        or ranges[j][0] <= ranges[i][1] <= ranges[j][1] \
                        or (ranges[i][0] <= ranges[j][0] and ranges[j][1] <= ranges[i][1]):

                        if int(ranges[j][0]) <= int(ranges[i][0]) <= int(ranges[j][1]):
                            ranges[i][0] = ranges[j][0]
                        if int(ranges[j][0]) <= int(ranges[i][1]) <= int(ranges[j][1]):
                            ranges[i][1] = ranges[j][1]
                        ranges.pop(j)
                        entry_removed = True
                    j += 1
                i += 1
            print("ranges", ranges)

        for r in ranges:
            fresh_count += r[1] - r[0] + 1
    print("fresh_count", fresh_count)

def nachhilfe():
    with open("homework.txt") as homework:
        lines = homework.read()#.split("\n")
        print("lines", lines.count("\n"))
        lines = lines.split("\n")
        print("lines", len(lines))
        print(lines[0])
        for i in range(len(lines)):
            line = lines[i].split(" ")
            while True:
                try:
                    line.remove('')
                except ValueError:
                    break
            lines[i] = line

        print("lines", lines)
        print("lines", len(lines))

        results = []
        for i in range(len(lines[0])):
            result = 0
            if lines[-1][i] == '+':
                for j in range(len(lines) - 1):
                    result += int(lines[j][i])
            elif lines[-1][i] == '*':
                result += 1
                for j in range(len(lines) - 1):
                    result *= int(lines[j][i])
            results.append(result)

        print("results", results)
        print("result", sum(results))







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #lock_sim()
    #id_validation()
    #jolting_it()
    #jolting_it_more()
    #paper_rolls()
    #paper_rolls_transport()
    #fridge_check()
    #fridge_check2()
    nachhilfe()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
