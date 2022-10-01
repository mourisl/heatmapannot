heatmapannot
======

### What is it?
A Python package to add heatmap annotations on plots generated with Seaborn. 

### Installation

1. Clone the [GitHub repo](https://github.com/mourisl/pvalannot), e.g. with `git clone https://github.com/mourisl/heatmapannot`.
2. Copy "heatmapannot" folder to your project folder.

I will try to add pvalannot to PyPi in future.

### Usage
Here is a minimal example:

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

Other examples can be found in dev.ipynb.

### Requirements
+ Python >= 3.6
+ seaborn >= 0.9
+ matplotlib >= 2.2.2
+ scipy >= 1.1.0

