import sys
# Import functions
from request_elevation import *
from generate_maps import *
from file_manager import *
from geocoder import *
from static_map import *
# Import for plots
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import axes3d
# Import global variables
import maps
import plot
import keys

# I/O Interface
print("Welcome on Fluss 0.1")
new = input("Download a new map? [y, n]")

if new == 'y':
    sure = input(
        '''Downloading a new map may take a minute,
           are you sure you want to continue? [y, n]''')
    if sure == 'y':
        if keys.elevation_API_key != "" and keys.staticmap_API_key != "":
            # Create a new map
            address = input("Enter an address (i.e uniersity of lausanne):")
            size = input("Enter the size of the map in km (i.e 4):")
            res = input("Enter the resolution per km (i.e 5):")
            # Geocode the address
            lat, lng = get_coordinates(address)
            # Add the address to the database
            id = add_location(address, lat, lng, size, res)
            print("LOADING ...")
            # Download elevation map WARNING: takes time
            download_elevations(lat, lng, size, res, id)
            # Download a satellite picture of the area
            download_map_sat(lat, lng, id)
            # Read the result of the download
            maps.read_map(id, address)
        else:
            print(
                "Keys not found. Please, set the API keys in the file keys.py")
            sys.exit()

if new == "n" or sure == "n":
    # Choose among exisiting map
    print("Choose a map:")
    # Show existing map in the database
    show_infos()
    # Ask for index
    req = input("Enter an index: ")
    # Get informations of the map through index
    try:
        id, address, size, res = get_info_from_index(req)
    except:
        print("Invalid index")
        sys.exit()
    # Read the result of the choice
    maps.read_map(id, address)

# Declaration
global sea_level

# Initialize plots
plot.set_parameters()
min_alt = maps.elevation.min().min()
max_alt = maps.elevation.max().max()
step = int((max_alt - min_alt) / 200)

# Set the slider
# Draw slider area
axSlider1 = plt.axes([0.1, 0.05, 0.8, 0.05])
plt.subplots_adjust(left=0.1, bottom=0.15)
# Create the slider
slider1 = Slider(axSlider1, 'level:', valmin=min_alt,
                 valmax=max_alt-1, valstep=step)
# Define slider behaviour
slider1.on_changed(update)

# Maps generation
# Show 2d map
generate_elevation_map(address, id, 0, plot.show_img)
plt.show()

# Show 3d map
generate_map_3d(maps.sea_level, size, res)
plt.show()
