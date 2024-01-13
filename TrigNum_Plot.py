import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Code Plots Number of Triggers per Channel For a Single Wavelength

df = pd.read_csv("C:\\Users\\lzvio\\OneDrive\\Desktop\\LArS_Run1\\60tin_1800A-0_2023-07-10_15-49-38.csv")

category = Counter(df['ChannelID'])
plt.figure()
plt.scatter(category.keys(), category.values())
plt.show()