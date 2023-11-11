heatmapannot
======

### What is it?
A Python package to add heatmap annotations on plots generated with Seaborn. 

### Installation

1. Clone the [GitHub repo](https://github.com/mourisl/heatmapannot), e.g. with `git clone https://github.com/mourisl/heatmapannot`.
2. Run "python setup.py install" to install heatmapannot.

I will try to add heatmapannot to PyPi in future.

### Usage
Here is an example:

```
import matplotlib.pyplot as plt
import seaborn as sns
from heatmapannot import heatmapannot

#load "flights" dataset
df = sns.load_dataset("flights")

# Add some features to month and year
monthToSeason = {"Jan":"Winter", "Feb":"Winter", "Mar":"Spring", "Apr":"Spring", "May":"Spring",
                "Jun":"Summer", "Jul":"Summer", "Aug":"Summer", "Sep":"Fall", "Oct":"Fall", "Nov":"Fall",
                "Dec":"Winter"}
monthToDays = {"Jan":31, "Feb":28, "Mar":31, "Apr":30, "May":31,
                "Jun":30, "Jul":31, "Aug":31, "Sep":30, "Oct":31, "Nov":30,
                "Dec":31}
df["season"] = df["month"].map(monthToSeason)
df["days"] = df["month"].map(monthToDays)
df["leap"] = df["year"].map(lambda x: x%4==0)
heatmapdf = df.pivot("month", "year", "passengers")

# Plot the heatmap
sns.heatmap(heatmapdf)
heatmapannot.AddHeatmapAnnot(data=df, heatmap_row="month", heatmap_col="year",
                            row_features = ["season", "days"], col_features = ["leap"],
                            row_palettes = ["bright", "dark"], col_colormaps = [{True:"r", False:"b"}])
plt.tight_layout()
```

AddHeatmapAnnot function takes the "data" as the dataframe for the pivot dataframe for heatmap. It assumes the x- and y-tick labels are the values in the "heatmap_row" and "heatmap_col" column. The features parameters specify map the tick labels to other features (e.g. the season of a month) through hthe input dataframe. row_features and col_features are lists, so you can add multiple annotations. The first feature in the list will be drawn first and is closer to the heatmap. The color for the annotation box is controled by palettes and user-defined colormaps (from feature to color). It is assumed that the color list is of the same length as the feature list. If you need to mix palettes and colormaps, you can put "None" as a place holder.  

Examples can be found in [example.ipynb](https://github.com/mourisl/heatmapannot/blob/main/example.ipynb).

### Requirements
+ Python >= 3.6
+ seaborn >= 0.9
+ matplotlib >= 2.2.2
+ scipy >= 1.1.0

