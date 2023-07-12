import os
launch = int(input("輸入一個整數來開啓游戲 (0 = easy, 1 = normal, 2 = Hard): "))
if launch == 0:
    os.system('start Easy.py')
if launch == 1:
    os.system('start Normal.py')
if launch == 2:
    os.system('start Difficult.py')