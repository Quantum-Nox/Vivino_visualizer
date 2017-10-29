#!/usr/bin/env python
__author__ = "Leonardo Disilvestro"

# https://console.developers.google.com/apis/dashboard
import pandas as pd
import numpy as np
import googlemaps
import pycountry
from geocode_results_saved import data
from CONFIG import googlemapsClientKey

# coding=utf-8
import plotter

gmaps = googlemaps.Client(key=googlemapsClientKey)

df = pd.read_csv('/home/leo/PycharmProjects/Wine/db_leo', sep='^')


# df.sort_values(by='Winery')

def pre_process_the_data(df):
    columns_to_be_dropped = ['Scan location', 'Drinking window', 'Food pairing']
    df.drop(columns_to_be_dropped, axis=1, inplace=True)

    df = df[pd.notnull(df['Winery'])]
    df = df[pd.notnull(df['Region'])]

    wine_cellar = [(i, df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2],
                    df.iloc[i, 3], df.iloc[i, 4], df.iloc[i, 5],
                    pycountry.countries.get(name=df.iloc[i, 4]).alpha_3, df.iloc[i, 12], df.iloc[i, 2]) for i in
                   range(len(df))]

    wine_cellar_dictionary = {}
    for item in wine_cellar:
        wine_cellar_dictionary[item[1]] = item[0], item[2], item[3], item[4], item[5], item[6], item[7], item[8]

    return wine_cellar_dictionary


def geo_coding(wine_cellar_dictionary):
    geocode_results = {}
    print('Obtaining the coordinates ...')
    for prod in wine_cellar_dictionary:
        print(prod)
        geocode_results[prod] = gmaps.geocode(prod,
                                              components={
                                                  wine_cellar_dictionary[prod][4]: wine_cellar_dictionary[prod][6]})
    print('Locations acquired!')
    return geocode_results


def check_geo_consistency(wine_cellar_dictionary, geocode_results):
    print('Checking for consistency ... ')
    for prod in wine_cellar_dictionary:
        if geocode_results[prod]:
            if geocode_results[prod][0]['formatted_address'].split()[-1] != wine_cellar_dictionary[prod][4]:
                print(prod)
                print(geocode_results[prod][0]['formatted_address'].split()[-1], wine_cellar_dictionary[prod][6])
                _temp = gmaps.geocode(wine_cellar_dictionary[prod][4])
                geocode_results[prod] = _temp


def location(wine_cellar_dictionary, geocode_results):
    meta_wine = [(name, geocode_results[name][0]['geometry']['location']['lat'],
                  geocode_results[name][0]['geometry']['location']['lng'],
                  wine_cellar_dictionary[name][1]) for name in geocode_results if geocode_results[name]]
    latitude = []
    longitude = []
    winery = []
    wineName = []
    for element in meta_wine:
        winery.append(element[0])
        latitude.append(element[1])
        longitude.append(element[2])
        wineName.append(element[3])
    data = {
        'lat': latitude,
        'lon': longitude,
        'Winery': winery,
        'wineName': wineName
    }
    return data


def data_charts(wine_cellar_dictionary):
    variety = []
    country = []
    for element in wine_cellar_dictionary:
        variety.append(wine_cellar_dictionary[element][7])
        country.append(wine_cellar_dictionary[element][4])
    country = list(set([(x, country.count(x)) for x in country]))
    variety = list(set([(x, variety.count(x)) for x in variety]))

    data_country = {
        'country_names': [name[0] for name in sorted(country)],
        'country_counts': [name[1] for name in sorted(country)],
    }
    total_country = float(np.array(data_country['country_counts']).sum())
    data_country['percentage'] = [str(round((name[1] / total_country), 4) * 100) + "%" for name in sorted(country)]

    data_types = {
        'variety_names': [name[0] for name in sorted(variety)],
        'variety_counts': [name[1] for name in sorted(variety)],
    }
    total_types = float(np.array(data_types['variety_counts']).sum())
    data_types['percentage'] = [str(round((name[1] / total_types), 4) * 100) + "%" for name in sorted(variety)]
    return data_country, data_types


def data_years(wine_cellar_dictionary):
    vintage = []
    for element in wine_cellar_dictionary:
        vintage.append(wine_cellar_dictionary[element][2])
        vintage_cleaned = list(np.nan_to_num(vintage))
    vintage = list(set([(x, vintage_cleaned.count(x)) for x in vintage_cleaned]))
    vintage_dic = {
        'vintage_years': [str(name[0]) for name in sorted(vintage)],
        'vintage_count': [(name[1]) for name in sorted(vintage)],
    }
    total = float(np.array(vintage_dic['vintage_count']).sum())
    vintage_dic['percentage'] = [str(round((name[1] / total), 4) * 100) + "%" for name in sorted(vintage)]
    return vintage_dic


wineDictionary = pre_process_the_data(df)
# geoResults = geo_coding(wineDictionary)
geoResults = data
# check_geo_consistency(wineDictionary, geoResults)
data_map = location(wineDictionary, geoResults)
data_charts = data_charts(wineDictionary)
data_vintage = data_years(wineDictionary)
plotter.plot_all(data_charts[0], data_charts[1], data_vintage, data_map)
