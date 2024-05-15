# Imports
import numpy as np
np.warnings.filterwarnings('ignore')
import pandas as pd
from pyearth import Earth
from matplotlib import pyplot
    
# Inputs
# Slope height (m)
h = 30
# Slope angle (degrees)
a = 30
# Depth of top of stratum at top of slope (m)
s1 = 3
# Thickness of stratum
s2 = 3
# Soil 1 friction (degrees)
f1 = 30
# Soil 2 friction (degrees)
f2 = 20
# Cohesion (kPa)
c = 0.1

# Read data
data = pd.read_csv('Embodied Carbon Data.csv')
df = pd.DataFrame(data)
df2 = df.dropna()

X = df[["h","a","s1","s2","f1","f2"]]
X2 = df2[["h","a","s1","s2","f1","f2"]]
y1 = df["ec1"]
y2 = df2["ec2"]
y3 = df["ec3"]
y4 = df["ec4"]

# Fit models for each technique
model1 = Earth()
model2 = Earth()
model3 = Earth()
model4 = Earth()

model1.fit(X,y1)
model2.fit(X2,y2)
model3.fit(X,y3)
model4.fit(X,y4)

# Print results
print("Regrading = ", model1.predict([[h,a,s1,s2,f1,f2]]), "kgCO2e/m")
print("Soil nailing = ", model2.predict([[h,a,s1,s2,f1,f2]]), "kgCO2e/m")
print("Gabion wall = ", model3.predict([[h,a,s1,s2,f1,f2]]), "kgCO2e/m")
print("Concrete anchored wall =", model4.predict([[h,a,s1,s2,f1,f2]]), "kgCO2e/m")


