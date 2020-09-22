from django.shortcuts import render
import pandas as pd
import json

# Read json file
globalMap = pd.read_json(
    'https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')


# globalMap = pd.read_json('/static/firstUI/world-population-density.json')

# globalMap_data = open('/static/firstUI/world-population-density.json')
# globalMap_data_clean = json.load(globalMap_data)
# globalMap = json.dumps(globalMap_data_clean)
# globalMap_data.close()

# Create your views here.


def indexPage(request):
    confirmedGlobal = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', encoding='utf-8', na_values=None)

    overallCount = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    barPlotData = confirmedGlobal[['Country/Region', confirmedGlobal.columns[-1]]].groupby(
        'Country/Region').sum().sort_values(by=confirmedGlobal.columns[-1], ascending=False)
    barPlotData = barPlotData.reset_index()
    barPlotData.columns = ['Country/Region', 'values']
    barPlotData = barPlotData.sort_values(by='values', ascending=False)
    # countryNames = barPlotData['Country/Region'].values.tolist()
    # countsVal = barPlotData['values'].values.tolist()
    # dataForMap = mapDataCal(barPlotData, countryNames)

    # print("time_series_covid19_deaths_global..")
    covid19_deaths_global = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv', encoding='utf-8', na_values=None)
    overalldeathCount = covid19_deaths_global[covid19_deaths_global.columns[-1]].sum()
    barPlotDeathData = covid19_deaths_global[['Country/Region', covid19_deaths_global.columns[-1]]].groupby(
        'Country/Region').sum().sort_values(by=covid19_deaths_global.columns[-1], ascending=False)
    barPlotDeathData = barPlotDeathData.reset_index()
    barPlotDeathData.columns = ['Country/Region', 'values']
    barPlotDeathData = barPlotDeathData.sort_values(
        by='values', ascending=False)

    barPlotData = barPlotData.merge(barPlotDeathData, left_on='Country/Region',
                                    right_on='Country/Region')
    barPlotData.columns = ['Country/Region', 'valuesx', 'valuesy']

    barPlotData.loc[barPlotData['Country/Region']
                    == 'US', 'Country/Region'] = 'United States'
    barPlotData.loc[barPlotData['Country/Region'] ==
                    'Russia', 'Country/Region'] = 'Russian Federation'

    barPlotData.loc[barPlotData['Country/Region'] ==
                    'Iran', 'Country/Region'] = 'Iran, Islamic Rep.'

    barPlotData.loc[barPlotData['Country/Region'] ==
                    'Egypt', 'Country/Region'] = 'Egypt, Arab Rep.'

    barPlotData.loc[barPlotData['Country/Region'] ==
                    'Yemen', 'Country/Region'] = 'Yemen, Rep.'

    barPlotData.loc[barPlotData['Country/Region'] ==
                    'Venezuela', 'Country/Region'] = 'Venezuela, RB'

    barPlotData.loc[barPlotData['Country/Region'] ==
                    'Congo (Brazzaville)', 'Country/Region'] = 'Congo, Dem. Rep.'

    barPlotData.loc[barPlotData['Country/Region'] ==
                    'Congo (Kinshasa)', 'Country/Region'] = 'Congo, Rep.'

    barPlotData.loc[barPlotData['Country/Region'] ==
                    'Korea, South', 'Country/Region'] = 'Korea, Rep.'

    countryNames = barPlotData['Country/Region'].values.tolist()
    countsVal = barPlotData['valuesx'].values.tolist()
    deathcountsVal = barPlotData['valuesy'].values.tolist()
    dataForMap = mapDataCal(barPlotData, countryNames)
    # print("dataForMap: ", dataForMap)

    # dataForMap = mapDataCal(barPlotDeathData, countryNames)
    print("countsVal", countsVal)

    context = {'overallCount': overallCount, 'countryNames': countryNames,
               'countsVal': countsVal, 'deathcountsVal': deathcountsVal, 'overalldeathCount': overalldeathCount, 'deathcountsVal': deathcountsVal,
               'dataForMap': dataForMap}

    return render(request, 'firstUI/index.html', context)


def mapDataCal(barPlotData, countryNames):
    dataForMap = []
    for i in countryNames:
        try:
            tempdf = globalMap[globalMap['name'] == i]
            temp = {}
            temp["code3"] = list(tempdf['code3'].values)[0]
            temp["name"] = i
            temp["value"] = barPlotData[barPlotData['Country/Region']
                                        == i]['valuesx'].sum()
            temp['code'] = list(tempdf['code'].values)[0]
            dataForMap.append(temp)
        except:
            pass
    return dataForMap
