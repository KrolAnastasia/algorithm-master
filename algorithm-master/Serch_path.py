import os
import re
def Search_path(const):
    derectory = []
    file = []
    for i in range(len(os.listdir(const))):
        derectory.append(os.listdir(const)[i])
        for y in range(len(os.listdir(f'{const}/{os.listdir(const)[i]}'))):

            file.append(const +
                            "/" + derectory[i] +
                            "/" + os.listdir(f'{const}/{os.listdir(const)[i]}')[y])
    return (file)