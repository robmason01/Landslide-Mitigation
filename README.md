# Landslide-Mitigation
This repository contains material from my dissertation on the embodied carbon of landslide mitigation measures. The contents are as follows:
1. Embodied Carbon Calculator (.py) - Takes lists of input values and calculates the embodied carbon for four landslide mitigation techniques for every permutation of inputs. Run in HYRCAN console.
2. Embodied Carbon Data (.csv) - Large spreadsheet containing input and output values of the carbon calcualtor for every sample.
3. MARS Model (.py) - Creates a MARS model busing the embodied carbon data as training samples.

Prerquisites for running the code:
1. numpy
2. xlsxwriter
3. HYRCAN - download from http://www.geowizard.org/download_hyrcan.html
4. pandas
5. matplotlib
6. scikit-learn
7. pyearth - download from https://github.com/scikit-learn-contrib/py-earth
