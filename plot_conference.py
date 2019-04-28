import cartopy.crs as ccrs
import matplotlib.pyplot as plt



def plot_conference(df_match, venue,title, CONFERENCE,total_co2):

    ax = plt.axes(projection=ccrs.PlateCarree())




    for index, row in df_match.iterrows():
        plt.scatter(row['lng'], row['lat'], color='green', transform=ccrs.PlateCarree())
        plt.plot([row['lng'], venue['lon']], [row['lat'], venue['lat']],
                 color='gray', linestyle='--',
                 transform=ccrs.PlateCarree(),
                 )

    # Plot Venue
    plt.scatter(venue['lon'], venue['lat'],linewidths=15,color='red', transform=ccrs.PlateCarree())

    ax.coastlines()
    ax.set_global()
    plt.title(title + ": "+venue['name'] + ", Total CO2: "+ str(round(total_co2,2)) + " Tons")

    '''
    plt.plot([ny_lon, delhi_lon], [ny_lat, delhi_lat],
             color='gray', linestyle='--',
             transform=ccrs.PlateCarree(),
             )'''

    # Save the plot by calling plt.savefig() BEFORE plt.show()
    plt.savefig('results/{}_{}_{}.pdf'.format(CONFERENCE, venue['name'], title))
    plt.savefig('results/{}_{}_{}.png'.format(CONFERENCE, venue['name'], title))

    plt.show()