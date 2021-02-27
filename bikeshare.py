#!/usr/bin/env python

import time
import pandas as pd
import numpy as np

#Dictionary to convert number of day of week to strings
DAY_OF_WEEK = {0: 'Monday',
               1: 'Tuesday',
               2: 'Wednesday',
               3: 'Thursday',
               4: 'Friday',
               5: 'Saturday',
               6: 'Sunday'}

#Dictionary to convert number of month to strings
MONTHS = {1: 'January',
          2: 'February',
          3: 'March',
          4: 'April',
          5: 'May',
          6: 'June',
          7: 'July',
          8: 'August',
          9: 'September',
          10: 'October',
          11: 'November',
          12: 'December'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter a city:')
        if city.lower() in ['washington', 'dc', 'd.c.', 'washinghton dc', 'washington d.c.',
                            'new york city', 'nyc', 'n.y.c', 'new york', 'chicago']:
            break
        else:
            print('Sorry, the current options are Washington DC, New York City, and Chicago')
            
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = int(input('Choose a month (1-12, or 0 to ignore date filtering):'))
            if month > 0 and month < 13:
                break
            elif month == 0:
                month = 'all'
                day = 'all'
                break
            else:
                print('Sorry, There are only 12 months in a year!')
        except:
            print('That\'s not a valid number!')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        if month == 'all':
            print('No Date Filter')
            break
        try:
            if month == 2:
                day = int(input('Choose a day (1-28, or 0 to ignore the day filter):'))
                if day > 0 and day < 29:
                    break
                elif day == 0:
                    day = 'all'
                    break
                else:
                    print('There are only 28 days in February! (There is no leap year data)')
            elif month in [1, 3, 5, 7, 8, 10, 12]:
                day = int(input('Choose a day (1-31, or 0 to ignore the day filter)):'))
                if day > 0 and day < 32:
                    break
                elif day == 0:
                    day = 'all'
                    break
                else:
                    print('The maximum days in a month is 31!')
            else:
                day = int(input('Choose a day (1-30, or 0 to ignore the day filter)):'))
                if day > 0 and day < 31:
                    break
                elif day == 0:
                    day = 'all'
                    break
                else:
                    print('The maximum days in your selected month is 30!')
        except:
            print('That\'s not a valid number!')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nImporting Data...\n')
    
    if city.lower() in ['washington', 'dc', 'd.c.', 'washinghton dc', 'washington d.c.']:
        df = pd.read_csv('washington.csv')
    elif city.lower() in ['new york city', 'nyc', 'n.y.c', 'new york']:
        df = pd.read_csv('new_york_city.csv')
    elif city.lower() in ['chicago']:
        df = pd.read_csv('chicago.csv')
    
    
    # Next two lines run very slow for DC (~50s total), no issues for NYC or Chicago (both ~1s total)
    # This doesn't seem to be an issue on the Udacity workspace, but on Jupiter on my machine it was
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    if type(month).__name__ == 'int' and type(day).__name__ == 'int':
        start_day = pd.to_datetime('2017-'+str(month)+'-'+str(day))
        end_day = pd.to_datetime('2017-'+str(month)+'-'+str(day+1))
        print('\nReturning data for select day in select city.')
        df = df.loc[(df['Start Time']>start_day) & (df['Start Time']<end_day)]
    elif type(month).__name__ == 'int' and type(day).__name__ == 'str':
        start_day = pd.to_datetime('2017-'+str(month)+'-'+str(1))
        end_day = pd.to_datetime('2017-'+str(month+1)+'-'+str(1))
        print('\nReturning data for select month in select city.')
        df = df.loc[(df['Start Time']>start_day) & (df['Start Time']<end_day)]
    else:
        print('\nReturning all data for the selected city.')
    
    data_sample = input('\nWould you like to see a data sample? Enter yes or no.\n')
    if data_sample.lower() in ['yes', 'y',  'ye', 'yse']:
        sample_index = 0
        while True:        
            print('Lines {0} through {1} of data:\n'.format(sample_index, sample_index+4))
            print(df.iloc[sample_index:sample_index+5])
            sample_index += 5
            data_sample = input('\nWould you like more data to view? Enter yes or no.\n')
            if data_sample.lower() not in ['y', 'yes', 'ye', 'yse']:
                break
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if type(month).__name__ == 'int':
        print('You selected to filter on a specific month. Therefore, no monthly statistics are availiable.')
    else:
        cmn_str = 'The most common month to rent is {0}.'
        print(cmn_str.format(MONTHS[df['Start Time'].dt.month.mode()[0]]))

    # TO DO: display the most common day of week
    if type(day).__name__ == 'int':
        print('You selected to filter on a specific day. Therefore, no daily statistics are availiable.')       
    else:
        cdy_str = 'The most common day to rent is {0}.'
        print(cdy_str.format(DAY_OF_WEEK[df['Start Time'].dt.dayofweek.mode()[0]]))
        
    # TO DO: display the most common start hour
    chr_str = 'The most common hour to start a rental is {0}:00.'
    print(chr_str.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    com_ss = df.groupby(['Start Station'])['Start Time'].count().sort_values(ascending=False).head(1)
    print('The most common start station is {0} with {1:,} trip starts.'.format(com_ss.idxmax(),com_ss.max()))
    
    # display most commonly used end station
    com_es = df.groupby(['End Station'])['Start Time'].count().sort_values(ascending=False).head(1)
    print('The most common end station is {0} with {1:,} trip completions.'.format(com_es.idxmax(),com_es.max()))
    
    # display most frequent combination of start station and end station trip
    com_rt = df.groupby(['Start Station', 'End Station'])['Start Time'].count().sort_values(ascending=False).head(1)
    print('The most common route is {0} to {1} with {2:,} trips.'.format(com_rt.idxmax()[0],com_rt.idxmax()[1],com_rt.max()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tt_string = 'The cumulative travel time for the selected location and timeframe was {:,.2f} days'
    print(tt_string.format(df['Trip Duration'].sum() / 86400))

    # display mean travel time
    mt_string = 'The average travel time for the selected location and timeframe was {:,.2f} hours'
    print(mt_string.format(df['Trip Duration'].mean() / 3600))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    usr_typ_cnt = df.groupby(['User Type'])['Start Time'].count()
    try:
        print('There were {0:,} use(s) by customers in your city and time range.'.format(usr_typ_cnt['Customer']))
    except:
        print('There were no use(s) by customers in your city and time range.')
    try:
        print('There were {0:,} use(s) by subscribers in your city and time range.'.format(usr_typ_cnt['Subscriber']))
    except:
        print('There were no use(s) by subscribers in your city and time range.')
    try:
        print('There were {0:,} use(s) by dependents in your city and time range.'.format(usr_typ_cnt['Dependent']))
    except:
        print('There were no use(s) by dependents in your city and time range.')
    
    # Display counts of gender
    try:
        gender = df['Gender']
        male_string = '\nThere were {0:,} uses by males in the selected city in the selected timeframe.'
        fmale_string = 'There were {0:,} uses by females in the selected city in the selected timeframe.'
        nan_string = 'There were {0:,} uses by undisclosed gender users in the selected city in the selected timeframe.'
        print(male_string.format(gender.str.contains('Male').value_counts()[True]))
        print(fmale_string.format(gender.str.contains('Female').value_counts()[True]))
        print(nan_string.format(gender.isnull().sum().sum()))
    except:
        print("\nSorry, no gender data for this city.")
    # Display earliest, most recent, and most common year of birth
    try:
        dob = df['Birth Year'].dropna(axis = 0)
        erl_string = '\nThe earliest birth year a bike was used under is {0:.0f}.'
        lts_string = 'The latest birth year a bike was used under is {0:.0f}.'
        com_string = 'The most common birth year a bike was used under is {0:.0f}.'
        print(erl_string.format(dob.min()))
        print(lts_string.format(dob.max()))
        print(com_string.format(dob.mode()[0]))
    except:
        print("\nSorry, no birth year data for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y', 'ye', 'yse']:
            break


if __name__ == "__main__":
	main()


