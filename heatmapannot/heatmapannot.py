import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.text as mpltext
import scipy as sp
import math

# gap: how far is the annotation from the previous annotation
# thick: how thick the annotation rectangle is
# feature: the representative values for the label 
# direction: "row" or "col"
def AddColorPatches(direction, ax, gap, thick, 
                    data = None, dataColumn = None, feature = None, colormap = None, palette = None):
    ticks = [l.get_text() for l in ax.get_yticklabels() if l.get_position()[0] >= -1e-3] if (direction == "row") else \
            [l.get_text() for l in ax.get_xticklabels() if l.get_position()[1] >= -1e-3] 
    palette = palette or "colorblind"
    
    tickFeature = {}
    featureRank = {}
    for t in ticks:
        tickFeature[t] = t
    if (feature is not None):
        for i, row in data.iterrows():
            tickFeature[ row[dataColumn] ] = row[feature]

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
        for i, t in enumerate(ticks):
            f = tickFeature[t]
            c = colormap[f]
            
            if (direction == "row"):
                x = left - gap - thick
                y = i 
            else:
                x = i
                y = bot + gap # Note that y is inversted
            
            width = thick if (direction == "row") else 1
            height = thick if (direction == "col") else 1
            ax.add_patch(patches.Rectangle([x, y], width, height, color=c))    
    
    # Update the ticks
    if (feature is not None):
        if (direction == "row"):
            locs = list(ax.get_xticks())
            labels = ax.get_xticklabels()
            labels.append( mpltext.Text(x = left - gap - thick / 2, y = labels[0].get_position()[1], 
                                   text=feature, horizontalalignment="center"))
            locs.append(left - gap - thick / 2)
            ax.set_xticks(locs, labels)
        else:
            locs = list(ax.get_yticks())
            labels = ax.get_yticklabels()
            labels.append( mpltext.Text(x = labels[0].get_position()[0], y = bot + gap + thick / 2, 
                                   text=feature, horizontalalignment="center"))
            locs.append(bot + gap + thick / 2)
            ax.set_yticks(locs, labels)            
            
    # Resize the plot
    if (direction == "row"):
        ax.set_xlim(left - gap - thick, right)
    else:
        ax.set_ylim(bot + gap + thick, top)
    return colormap


def AddLegend(colormap, title, idx, ax):
    legendPatches = []
    for f, c in colormap.items():
        legendPatches.append(patches.Patch(color=c, label=f))
        
    fig = ax.get_figure()
    #renderer = fig.canvas.get_renderer()
    
    figRight = fig.bbox.transformed(fig.transFigure.inverted()).get_points()[1][0]
    #xAnchor =  ax.bbox.transformed(ax.transData.inverted()).get_points()[1][0]
    xAnchor = figRight
    for a in fig.artists:
        right = a.get_tightbbox(renderer = \
                                fig.canvas.get_renderer()).transformed(fig.transFigure.inverted()).get_points()[1][0]
        if (right > xAnchor):
            xAnchor = right
    
    legendObject = fig.legend(handles = legendPatches, title = title, loc="center left", 
                             bbox_to_anchor=(xAnchor, 0.5))
    
    fig.add_artist(legendObject)

def AddHeatmapAnnot(data = None, heatmap_row = None, heatmap_col = None, gap=0.1, height=0.5,
                    row_features = None, col_features = None, 
                    row_colormaps = None, col_colormaps = None, row_palettes = None,
                    col_palettes = None, ax=None):
    ax = ax or plt.gca()
    #fig = ax.get_figure()
    #renderer = fig.canvas.get_renderer()
    
    legendIdx = 0 
    colormaps = []
    if (row_features or row_colormaps or row_palettes):
        for i, t in enumerate(row_features or row_colormaps or row_palettes):      
            feature = row_features[i] if (row_features is not None) else None
            colormap = row_colormaps[i] if (row_colormaps is not None) else None
            palette = row_palettes[i] if (row_palettes is not None) else None
            colormap = AddColorPatches("row", ax, gap, height, data, heatmap_row,
                                      feature=feature, colormap=colormap, palette=palette)
            AddLegend(colormap, feature, legendIdx, ax)
            legendIdx += 1
            colormaps.append(colormap)
            
        
    if (col_features or col_colormaps or col_palettes):
        for i, t in enumerate(col_features or col_colormaps or col_palettes):      
            feature = col_features[i] if (col_features is not None) else None
            colormap = col_colormaps[i] if (col_colormaps is not None) else None
            palette = col_palettes[i] if (col_palettes is not None) else None
            colormap = AddColorPatches("col", ax, gap, height, data, heatmap_col,
                                      feature=feature, colormap=colormap, palette=palette)
            AddLegend(colormap, feature, legendIdx, ax)
            legendIdx += 1
            colormaps.append(colormap)
            
    return colormaps
    
    