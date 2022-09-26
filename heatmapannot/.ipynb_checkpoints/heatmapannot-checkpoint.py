import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import scipy as sp
import math

# x: the dataColumn for the ticks
# feature: the representative values for the label 
# direction: "row" or "col"
def AddColorPatches(data, direction, ax, dataColumn = None, feature = None, colormap = None, palette = None):
    ticks = [l.get_text() for l in ax.get_yticklabels() if l.get_position()[0] >= -1e-3] if (direction == "row") else \
            [l.get_text() for l in ax.get_xticklabels() if l.get_position()[1] >= -1e-3] 
    palette = palette or "colorblind"
    
    tickFeature = {}
    featureRank = {}
    for t in ticks:
        tickFeature[t] = t
    if (feature is not None):
        for row in data.iterrows():
            tickFeature[ row[dataColumn] ] = feature
    for i, t in enumerate(ticks):
        f = tickFeature[t]
        if (f not in featureRank):
            featureRank[f] = len(featureRank)
            
    if (colormap == None):
        colors = sns.color_palette(palette, len(featureRank))
        colormap = {}
        for f, c in zip([f for f in sorted(featureRank.keys(), 
                                           key=lambda x:featureRank[x])], 
                        colors):
            colormap[f] = c
    
    # Draw the colors
    bot, top = ax.get_ylim()
    left, right = ax.get_xlim()
    for i, t in enumerate(ticks):
        if (direction == "row"):
            x = left - 1 
            y = 0
        else: 
            x = 0
            y = bot + 1  # Note that the y-axis is inverted
        for i, t in enumerate(ticks):
            f = tickFeature[t]
            c = colormap[f]
            
            if (direction == "row"):
                x = left - 1
                y = i
            else:
                x = i
                y = bot

            ax.add_patch(patches.Rectangle([x, y], 1, 1, color=c, clip_on=False))    
    
    if (direction == "row"):
        ax.set_xlim(left - 1, right)
    else:
        ax.set_ylim(bot + 1, top)
    return colormap


def AddHeatmapAnnot(data = None, heatmap_row = None, heatmap_col = None, 
                    row_features = None, col_features = None, 
                    row_colormaps = None, col_colormaps = None, row_palettes = None,
                    col_palettes = None, ax=None):
    ax = ax or plt.gca()
    #fig = fig or ax.get_figure()
    #renderer = fig.canvas.get_renderer()
    
    if (row_features or row_colormaps or row_palettes):
        for i, t in enumerate(row_features or row_colormaps or row_palettes):      
            feature = row_features[i] if (row_features is not None) else None
            colormap = row_colormaps[i] if (row_colormaps is not None) else None
            palette = row_palettes[i] if (row_palettes is not None) else None
            colormap = AddColorPatches(data, "row", ax, heatmap_row,
                                      feature=feature, colormap=colormap, palette=palette)
        
    if (col_features or col_colormaps or col_palettes):
        for i, t in enumerate(col_features or col_colormaps or col_palettes):      
            feature = col_features[i] if (col_features is not None) else None
            colormap = col_colormaps[i] if (col_colormaps is not None) else None
            palette = col_palettes[i] if (col_palettes is not None) else None
            colormap = AddColorPatches(data, "col", ax, heatmap_row,
                                      feature=feature, colormap=colormap, palette=palette)
    
    