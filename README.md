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
import seaborn as sns

#load "flights" dataset
df = sns.load_dataset("flights")
monthToSeason = {"Jan":"Winter", "Feb":"Winter", "Mar":"Spring", "Apr":"Spring", "May":"Spring",
                "Jun":"Summer", "Jul":"Summer", "Aug":"Summer", "Sep":"Fall", "Oct":"Fall", "Nov":"Fall",
                "Dec":"Winter"}
df["season"] = df["month"].map(monthToSeason)
df["leap"] = df["year"].map(lambda x: x%4==0)
heatmapdf = df.pivot("month", "year", "passengers")

sns.heatmap(heatmapdf)
heatmapannot.AddHeatmapAnnot(data=df, heatmap_row="month", heatmap_col="year",
                            row_features = ["season"], col_features = ["leap"],
                            row_palettes = ["bright"], col_colormaps = [{True:"r", False:"b"}])
plt.tight_layout()
```

Other examples can be found in dev.ipynb.

### Requirements
+ Python >= 3.6
+ seaborn >= 0.9
+ matplotlib >= 2.2.2
+ scipy >= 1.1.0

