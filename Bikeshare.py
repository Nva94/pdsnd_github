import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!\n')
    city = ''
    month = ''
    day =''
    while city not in ('chicago', 'new york' , 'washington'):
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
    print()

    filters = ''
    while filters not in ('month', 'day','both','no'):
        filters = input('Would you like to filter the data by month, day, both or not? Enter month, day, both, or no\n').lower()
    print()

    if filters == 'month' or filters =='both':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        while month not in (months):
            month = input('Which month - January, February, March, April, May, or June?\n').lower()
    print()

    if filters == 'day' or filters == 'both':
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        while day not in (days):
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
    print()

    if filters == 'no':
        day , month = 'all','all'

    if day == '': day = 'all'
    if month == '' : month = 'all'

    print('-'*40)
    return city, month, day, filters


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def display_data(df):
    ''' return 5 row from the df'''
    view_data = ''
    while view_data not in ('yes','no'):
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?\n")
    if view_data != 'no':
        start_loc = 0
        continue_display = ''
        while continue_display != 'no':
            print(df.iloc[start_loc:start_loc+5])
            start_loc+=5
            continue_display= input("Do you wish to continue? type(yes/no)\n").lower()

    print('-'*40)

def time_stats(df , filters):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    if filters == 'no':
        print('No filter was selected.\n')
        print()
        common_month = months[df['month'].mode()[0]-1].title()
        common_day_of_week = df['day_of_week'].mode()[0]
        common_hour_of_day = df['hour'].mode()[0]

        print('The most common month: {}\n'.format(common_month))
        print('The most common day of week: {}\n'.format(common_day_of_week))
        print('The most common hour: {}\n'.format(common_hour_of_day))

    if filters == 'both':
        print('The data filtered by both month and day.\n')

        common_hour_of_day = df['hour'].mode()[0]
        month = months[df['month'].mode()[0]-1].title()
        day = df['day_of_week'].mode()[0]

        print('Month: {}\nDay: {}\n'.format( month ,day ))
        print('The most common hour: {}\n'.format(common_hour_of_day))

    if filters == 'month':

        print('The data filtered by month.\n')

        month = months[df['month'].mode()[0]-1]
        common_day_of_week = df['day_of_week'].mode()[0]
        common_hour_of_day = df['hour'].mode()[0]

        print('Month: {}\n'.format(month))
        print('The most common day of week: {}\nThe most common hour: {}\n'.format(common_day_of_week , common_hour_of_day))

    if filters == 'day':
        print('The data filtered by day.\n')

        day = df['day_of_week'].mode()[0]
        common_month = months[df['month'].mode()[0]-1].title()
        common_hour_of_day = df['hour'].mode()[0]

        print('Day: {}\n'.format(day))
        print('The most common month: {}\nThe most common hour: {}\n'.format(common_month , common_hour_of_day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most common start station: {}\n'.format(start_station))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most common end station: {}\n'.format(end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['combination']=df['Start Station'] +" and "+df['End Station']
    print('The most frequent combination of start station and end station trip: {}\n'.format(df['combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    count = df['Trip Duration'].count()
    total_sum = df['Trip Duration'].sum()
    mean =  df['Trip Duration'].mean()

    print('The total travel time: {}\nAverage total time: {}\nCount of travel time: {}\n'.format(total_sum ,mean, count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user type
    users = dict(df['User Type'].value_counts())
    print('Count of user type')
    for u, v in users.items():
        print('{}: {}'.format(u,v))
    # TO DO: Display counts of gender
    if 'Gender' in df:
        print('Count of each gender')
        gender = dict(df['Gender'].value_counts())
        for g, c in gender.items():
            print('{}: {}'.format(g,c))
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = max(df['Birth Year'])
        print('Earliest year of birth: {}'.format(int(earliest)))
        common_year = df['Birth Year'].mode()[0]
        print('Most common year of birth: {}'.format(common_year))




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, filters = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df, filters, city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
