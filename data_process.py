#!/usr/bin/env python
# coding: utf-8



import csv
import os

with open("privamov.clean.60s","r") as file_read:
    line = file_read.readline()
    while line:
        line = line.split()
        id = line[0]
        with open("data"+id+".csv", "a", newline = "") as file:
            writer = csv.writer(file, delimiter=',')
            if os.stat("data"+id+".csv").st_size == 0:
                writer.writerow(["id","timestamp","longitude","latitude"])

            writer.writerow(line)

            line = file_read.readline()
        












