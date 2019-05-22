import matplotlib.pyplot as plt


def set_parameters():
    """Set global parameters for plots.
    """
    # Declaration
    global show_img
    global fig
    global ax
    # Set whether to show the satellite image (True) or not (False)
    show_img = False
    fig, ax = plt.subplots()
    # Set the hatches
    plt.rcParams['hatch.color'] = 'r'
    plt.rcParams['hatch.linewidth'] = 0.3
