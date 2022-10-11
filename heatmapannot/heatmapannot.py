import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.text as mpltext
import math

# gap: how far is the annotation from the previous annotation
# thick: how thick the annotation rectangle is
# feature: the representative values for the label 
# direction: "row" or "col"
# anchor: -1: add the annotation to the negative side of the axis; 1 to the positive side
def AddColorPatches(direction, ax, gap, thick, anchor, ticks, shift = 0,
                    data = None, dataColumn = None, feature = None, colormap = None, palette = None):
    #ticks = [l.get_text() for l in ax.get_yticklabels() if l.get_position()[1] >= -1e-3] if (direction == "row") else \
    #        [l.get_text() for l in ax.get_xticklabels() if l.get_position()[0] >= -1e-3] 
    palette = palette or "colorblind"

    tickFeature = {}
    featureRank = {}
    for t in ticks:
        tickFeature[t] = t
    if (feature is not None):
        tickFeature = {}
        for i, row in data.iterrows():
            tickFeature[ str(row[dataColumn]) ] = row[feature]

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
    
    invertx = False
    inverty = False
    if (bot > top):
        bot, top = top, bot
        inverty = True
    if (left > right):
        left, right = right, left
        invertx = True
    
    for i, t in enumerate(ticks):
        f = tickFeature[t]
        c = colormap[f]

        if (direction == "row"):
            if (anchor == -1):
                x = left - gap - thick
            else: 
                x = right + gap 
            y = i + shift
        elif (direction == "col"):
            x = i + shift          
            if (anchor == -1):
                y = bot - gap - thick
            else:
                y = top + gap
        else:
            print("Unkown direction=%s"%(direction))
            return

        width = thick if (direction == "row") else 1
        height = thick if (direction == "col") else 1
        ax.add_patch(patches.Rectangle([x, y], width, height, color=c))    
    
    # Update the ticks
    if (feature is not None):
        if (direction == "row"):
            locs = list(ax.get_xticks())
            labels = ax.get_xticklabels()
            
            x = left - gap - thick / 2
            if (anchor == 1):
                x = right + gap + thick / 2
                
            labels.append( mpltext.Text(x = x, y = labels[0].get_position()[1], 
                                   text=feature, horizontalalignment="center"))
            locs.append(x)
            ax.set_xticks(locs, labels)
        else:
            locs = list(ax.get_yticks())
            labels = ax.get_yticklabels()
            y = top + gap + thick / 2
            if (anchor == -1):
                y = bot - gap - thick / 2
                
            labels.append( mpltext.Text(x = labels[0].get_position()[0], y = y, 
                                   text=feature, horizontalalignment="center"))
            locs.append(y)
            ax.set_yticks(locs, labels)            
            
    # Resize the plot
    if (direction == "row"):
        if (anchor == -1):
            ax.set_xlim(left - gap - thick, right)
        else:
            ax.set_xlim(left, right + gap + thick)
    else:
        if (anchor == -1):
            ax.set_ylim(bot - gap - thick, top)
        else:
            ax.set_ylim(bot, top + gap + thick)
            
    if (invertx):
        left, right = ax.get_xlim()
        ax.set_xlim(right, left)
    else:
        bot, top = ax.get_ylim()
        ax.set_ylim(top, bot)
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
    
def AdjustAxes(ax, align, heatmap_orig_lim, heatmap_new_lim):
    lim = ()
    if (align == "row"):
        lim = ax.get_ylim()
    elif (align == "col"):
        lim = ax.get_xlim()
    else:
        print("Unknown align=%s"%(align))
    
    scale = (lim[1] - lim[0]) / (heatmap_orig_lim[1] - heatmap_orig_lim[0])
    newlim = [0, 0]
    for i in [0, 1]:
        newlim[i] = lim[i] + scale * (heatmap_new_lim[i] - heatmap_orig_lim[i]) 

    if (align == "row"):
        ax.set_ylim(newlim)
    elif (align == "col"):
        ax.set_xlim(newlim)        
        
    return lim, tuple(newlim) 

def AddHeatmapAnnot(data = None, heatmap_row = None, heatmap_col = None, gap=0.1, height=0.5,
                    row_features = None, col_features = None, 
                    row_colormaps = None, col_colormaps = None, 
                    row_palettes = None, col_palettes = None, 
                    row_anchors = None, col_anchors = None,
                    row_align_shift = 0, col_align_shift = 0,
                    hide_legends = None, ax=None):
    ax = ax or plt.gca()
    fig = ax.get_figure()
    #renderer = fig.canvas.get_renderer()
    left, right = ax.get_xlim()
    bot, top = ax.get_ylim()
    
    xticks = [l.get_text() for l in ax.get_xticklabels()]
    yticks = [l.get_text() for l in ax.get_yticklabels()]   
    
    needCanvasDraw = True
    
    for t in xticks + yticks:
        if (len(t) > 0):
            needCanvasDraw = False
            break
        
    # This command is very IMPORTANT to put the ticks on the plot,
    # so heatmapannot can track the labels
    if (needCanvasDraw):
        fig.canvas.draw()
        xticks = [l.get_text() for l in ax.get_xticklabels()]
        yticks = [l.get_text() for l in ax.get_yticklabels()]  
        
    legendIdx = 0 
    colormaps = []
    if (row_features or row_colormaps or row_palettes):
        for i, t in enumerate(row_features or row_colormaps or row_palettes):      
            feature = row_features[i] if (row_features is not None) else None
            colormap = row_colormaps[i] if (row_colormaps is not None) else None
            palette = row_palettes[i] if (row_palettes is not None) else None
            anchor = row_anchors[i] if (row_anchors is not None) else -1
            colormap = AddColorPatches("row", ax, gap, height, anchor, yticks, row_align_shift, data, heatmap_row, 
                                      feature=feature, colormap=colormap, palette=palette)
            if (not hide_legends or legendIdx not in hide_legends):
                AddLegend(colormap, feature, legendIdx, ax)
        
            legendIdx += 1
            colormaps.append(colormap)
            
        
    if (col_features or col_colormaps or col_palettes):
        for i, t in enumerate(col_features or col_colormaps or col_palettes):      
            feature = col_features[i] if (col_features is not None) else None
            colormap = col_colormaps[i] if (col_colormaps is not None) else None
            palette = col_palettes[i] if (col_palettes is not None) else None
            anchor = col_anchors[i] if (col_anchors is not None) else 1
            colormap = AddColorPatches("col", ax, gap, height, anchor, xticks, col_align_shift, data, heatmap_col,
                                      feature=feature, colormap=colormap, palette=palette)
            if (not hide_legends or legendIdx not in hide_legends):
                AddLegend(colormap, feature, legendIdx, ax)
                
            legendIdx += 1
            colormaps.append(colormap)
    newLeft, newRight = ax.get_xlim()
    newBot, newTop = ax.get_ylim()
    return colormaps, (left, right), (bot, top), (newLeft, newRight), (newBot, newTop)
    
    