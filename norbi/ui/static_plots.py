import matplotlib.pyplot as plt
import numpy as np

def inset_plot(df, offint=None, x1=None, x2=None, y1=None, y2=None):
    # min_y = df.iloc[:,1].min()  #find min y of representative trace

    left_cut_idx = df[df.iloc[:,0]>x1].index[0]
    try:
        right_cut_idx = df[df.iloc[:,0]>x2].index[0]
    except:
        right_cut_idx = df.tail(1).index.item()
    min_y = df.iloc[left_cut_idx:right_cut_idx,1:].min().min()

    max_y = df.iloc[:,1].max()  #find max y of representative trace

    if offint == None:
        offint = 0.02*(max_y-min_y)*(len(df.columns)-2)
    else:
        offint = offint

    if y1 == None:
        y1 = min_y
    else:
        y1 = y1

    if y2 == None:
        y2 = 0.15*(max_y-min_y)
    else:
        y2 = y2

    fig = plt.figure()

    ax1_shape = [0.2, 0.8, 2, 0.8]  # lt edge, top edge, w, h
    ax1 = fig.add_axes(ax1_shape)

    locs, labels = plt.xticks()  # Get the current locations and labels.
    plt.xticks(np.arange(0, 60, step=5))  # Set label locations.

    offset = offint*(len(df.columns)-2) 

    for i in range(len(df.columns)-1):
        ax1.plot(df.iloc[:,0],(df.iloc[:,(i+1)]+offset),label='rep'+ str(i+1))
        offset += offint

    legend = ax1.legend(loc='best', shadow=True, fontsize='medium')    

    ax1_inset_shape = [0.5, 0.5, 0.4, 0.8]  # lt edge, top edge, frac (w, h)
    axins = ax1.inset_axes(ax1_inset_shape)

    offset = offint*(len(df.columns)-2) 
    for i in range(len(df.columns) - 1):
        axins.plot(
            df.iloc[:, 0], (df.iloc[:, (i + 1)] + offset), label="rep" + str(i + 1)
        )
        offset += - offint

    x1, x2, y1, y2 = x1, x2, y1, y2  # sub region of the original image

    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    # axins.set_xticklabels('')
    # axins.set_yticklabels('')

    ax1.indicate_inset_zoom(axins)

    #     plt.savefig('plot4.png', dpi=300, bbox_inches='tight')

    plt.show()

    return
