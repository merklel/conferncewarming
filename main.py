import pandas as pd
#from fuzzyset import FuzzySet
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import math
import plot_conference

flag_matching = False

# ICPS 2018 St. Petersburg
# CONFERENCE = "icps18.csv"
# VENUE = {'name':'St. Petersburg', 'lat':59.93863 , 'lon':30.31413}

# ITSC 2018 Maui
#CONFERENCE = "itsc18.csv"
#VENUE = {'name':'Maui, Hawaii', 'lat':20.798363 , 'lon':-156.331924} #20.798363, -156.331924

# ITSC17 Yokohama
# CONFERENCE = "itsc17.csv"
# VENUE = {'name':"Yokohama", 'lat':35.443707 , 'lon':139.638031} #35.443707, 139.638031.

CONFERENCE="icis18.csv"
VENUE={'name':'Singapore', 'lat':1.290270 , 'lon':103.851959} #1.290270	103.851959

# CONFERENCE="iros18.csv"
# VENUE={'name':'Madrid', 'lat':40.416775 , 'lon':-3.703790} #40.416775	-3.703790

# CONFERENCE="EVER2018.csv"
# VENUE = {"name": "Monte Carlo", 'lat':43.73976 , 'lon':7.42732} #43.73976, 7.42732

WORLDCITIES = "simplemaps_worldcities_basicv1.4/worldcities.csv"
AFFILIATION_MATCH = CONFERENCE +'_matched.csv'

# Assumptions
FACTOR_KM_FLIGHT_TO_g_CO2 = 285 # grams
FACTOR_KM_CAR_TO_g_CO2 = 72
FACTOR_KM_TRAIN_TO_g_CO2 = 14

DISTANCE_FLIGHT = 300


def compare_affiliation_worldcities(affiliation, df_worldcities):

    best_guess = {'score': 0, 'row': None, 'notfound':1}
    for row in df_worldcities.iterrows():
        city = row[1]['city_ascii']

        if isinstance(affiliation, str):
            affiliation = affiliation.split(';')[0]
            affiliation = affiliation.replace(' ',',')
            #affiliation = affiliation.replace(';', ',')
            aff_split_space = affiliation.split(',')


            for a in aff_split_space:

                # Method 2: fuzzywuzzy
                res = fuzz.ratio(a.strip(), city)/100

                if res != None:
                    if res > 0.7:
                        #print('circa match!')
                        #print(row[1]['city_ascii'])
                        #print(a)
                        #return row[1]
                        if res > best_guess['score']:
                            best_guess['score'] = res
                            best_guess['row'] = row[1]
                            best_guess['notfound'] = 0

    return best_guess

def latlon2km(lat1, lon1, lat2, lon2):
    r = 6372.8
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = (math.sin(dlat / 2))**2 + math.cos(lat1)* math.cos(lat2)* (math.sin(dlon / 2))**2
    c = 2 * math.asin(math.sqrt(a))
    d = r * c
    return d

def co2_for_confernce_venue(df_match, venue):

    df_match['co2'] = pd.Series()
    for index, row in df_match.iterrows():
        distance = latlon2km(row['lat'], row['lng'], venue['lat'], venue['lon'])

        if DISTANCE_FLIGHT > distance: # by train or car
            co2 = distance * FACTOR_KM_CAR_TO_g_CO2 * 2 # mal zwei wegen hin und zurück
        if distance >= DISTANCE_FLIGHT: #flight
            co2 = distance * FACTOR_KM_FLIGHT_TO_g_CO2 * 2 # mal zwei wegen hin und zurück

        #df_match['co2'].iloc[index] = co2
        df_match.loc[index, 'co2'] = co2

        #print('City: {}, Distance: {}, CO2: {}'.format(row['city'], distance, co2))

    print('Total CO2 Conference: {} Tonns. Venue: {}'.format(round(df_match['co2'].sum()/1000000,3), venue['name']))
    return {"total_co2": df_match['co2'].sum()/1000000, 'df_match': df_match}


# load conference
df_conference=pd.read_csv(CONFERENCE)


# load worldcities
df_worldcities = pd.read_csv(WORLDCITIES)

if flag_matching == True:
    # match affiliations with worldcities
    df_match = pd.DataFrame()
    c=1
    n=len(df_conference)
    for row in df_conference.iterrows():
        match = compare_affiliation_worldcities(row[1]['Author Affiliations'], df_worldcities)
        if match['notfound'] == 1:
            print("Could not resolve affiliations. Skipping...")
            print('Aff: {}'.format(row[1]['Author Affiliations']))
        else:
            print("Analysing {} of {}.".format(c, n))
            print('Score: {}. Best Guess: {}. Aff: {}'.format(match['score'], match['row']['city'], row[1]['Author Affiliations'].split(';')[0]))
            df_match = df_match.append(match['row'])
        c=c+1

    df_match.to_csv(AFFILIATION_MATCH)
else:
    df_match = pd.read_csv(AFFILIATION_MATCH)



# Calculate distances and co2 from the df_match for the original conference venue
co2_actual_venue = co2_for_confernce_venue(df_match, VENUE)['total_co2']


# Worldwide Optimization
min_co2=co2_actual_venue
min_venue = VENUE
df_worldcities_biggest = df_worldcities[df_worldcities['population']>1000000]
analysis_venue = co2_for_confernce_venue(df_match, VENUE)
c=1
n = len(df_worldcities_biggest)
world_conf_venues = pd.DataFrame(columns=['lng', 'lat', 'co2'])
for index, row in df_worldcities_biggest.iterrows():
    print('Analysing {} of {}.'.format(c, n))
    c=c+1
    venue={"name":row["city"], "lat":row["lat"],"lon":row["lng"]}
    conference = co2_for_confernce_venue(df_match, venue)
    world_conf_venues = world_conf_venues.append({'lng': venue['lon'], 'lat': venue['lat'], 'co2': conference['total_co2']}, ignore_index=True)

    co2 = conference['total_co2']
    if co2 < min_co2:
        min_co2 = co2
        min_venue = venue


    # if c>5:
    #    break


print('CO2 minimal venue: {}. CO2: {}'.format(min_venue['name'], min_co2))
plot_conference.plot_conference(conference['df_match'], VENUE,title='Original Location', CONFERENCE=CONFERENCE, total_co2 = analysis_venue['total_co2'], world_conf_venues=world_conf_venues)
plot_conference.plot_conference(conference['df_match'], min_venue, title='CO2 Optimal Location', CONFERENCE=CONFERENCE, total_co2 = min_co2, world_conf_venues=world_conf_venues)

