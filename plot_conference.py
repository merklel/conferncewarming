import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import scipy.interpolate.ndgriddata as griddata
import matplotlib.tri as tri
import numpy as np


HEATMAP=True


def plot_conference(df_match, venue,title, CONFERENCE,total_co2, world_conf_venues):

	n_paper = len(df_match)

    fig, (ax) = plt.subplots(nrows=1, figsize=(20,10))

    ax = plt.axes(projection=ccrs.PlateCarree())


    for index, row in df_match.iterrows():
        plt.scatter(row['lng'], row['lat'], color='green', transform=ccrs.PlateCarree())
        plt.plot([row['lng'], venue['lon']], [row['lat'], venue['lat']],
                 color='gray', linestyle='--',
                 transform=ccrs.PlateCarree(),
                 )

    # Plot Venue
    plt.scatter(venue['lon'], venue['lat'],linewidths=15,color='red', transform=ccrs.PlateCarree())

    # Heatmap
    colormap = ""
    if HEATMAP:
        colormap = "_colormap"
        X = world_conf_venues['lng']
        Y = world_conf_venues['lat']
        Z = world_conf_venues['co2']
        xi = np.linspace(min(X), max(X))
        yi = np.linspace(min(Y), max(Y))

        # Perform linear interpolation of the data (x,y)
        # on a grid defined by (xi,yi)
        triang = tri.Triangulation(X, Y)
        interpolator = tri.LinearTriInterpolator(triang, Z)
        Xi, Yi = np.meshgrid(xi, yi)
        zi = interpolator(Xi, Yi)


        cntr1 = plt.contourf(xi,yi,zi, 10,transform=ccrs.PlateCarree())
        fig.colorbar(cntr1, ax=ax)

    ax.coastlines()
    ax.set_global()
    plt.title(title + ": "+venue['name'] + ", Total $CO_2$: "+ str(round(total_co2,2)) + " Tons. " + "$CO_2$ per person: " + str(round(total_co2/n_paper,2)) + " Tons.")

    '''
    plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
             color='gray', linestyle='--',
             transform=ccrs.PlateCarree(),
             )'''

    # Save the plot by calling plt.savefig() BEFORE plt.show()
    plt.savefig('results/{}_{}_{}{}.pdf'.format(CONFERENCE, venue['name'], title,colormap))
    plt.savefig('results/{}_{}_{}{}.png'.format(CONFERENCE, venue['name'], title,colormap))

    plt.show()