import time
import calendar
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_cities = ['chicago','new york city','washington']
    valid_month_filts = ['january','february','march','april','may','june','all']
    valid_day_filts = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        user_input_city = input('Please enter city: ' )
        city = user_input_city.lower()
        if city not in valid_cities:
            print('City Not Found- Please Enter a Valid City(Chicago,New York City or Washington): \n')
            continue
        else: 
            print('City Found! \n')
            break

            
    # get user input for month (all, january, february, ... , june)
    while True:
        user_input_month = input('Please enter Month(from January to June) or all: ')
        month = user_input_month.lower()
        if month not in valid_month_filts:
            print('Please enter a valid month \n')
            continue
        else: 
            print('Filtering for {}....'.format(month))
            break 
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True: 
        user_input_day = input('Please enter day or all: ')
        day = user_input_day.lower()
        if day not in valid_day_filts:
            print('Please enter a valid day of the week: \n')
            continue
        else: 
            print('Filtering for {}....'.format(day))
            break
    

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
   # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    # print(df)
    return df 


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    df['month'] = df['month'].apply(lambda x: calendar.month_name[x])
    most_common_month = df.month.mode()[0]

    # # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday
    df['day'] = df['day'].apply(lambda x: calendar.day_name[x])
    most_common_day = df['day'].mode()[0]

    # # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('The most common month of travel is: {}'.format(most_common_month))
    print('The most common day of travel is: {}'.format(most_common_day))
    print('The most common hour of travel is: {}'.format(most_common_hour))

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display top 5 most commonly used start station
    most_common_start_stations = df['Start Station'].value_counts().nlargest(5)

    # display top 5 most commonly used end station
    most_common_end_stations = df['End Station'].value_counts().nlargest(5)

    # display most frequent combination of start station and end station trip
    most_common_trip_combo = df.groupby(['Start Station','End Station']).size().idxmax()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print('The top 5 most common starting locations are \n{}'.format(most_common_start_stations))
    print('-'*40)
    print('The top 5 most common end locations are \n{}'.format(most_common_end_stations))
    print('-'*40)
    print('The most common Start/End Location Combo is \n{}'.format(most_common_trip_combo))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_duration_sum = df['Trip Duration'].sum()
    total_travel_time = dt.timedelta(seconds=(int(trip_duration_sum)))

    # display mean travel time
    avg_travel_time_secs = df['Trip Duration'].mean()
    avg_travel_time = dt.timedelta(seconds=(int(avg_travel_time_secs)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('The total travel time during the selected period is: \n {}'.format(total_travel_time))
    print('The mean travel time during the selected period is: \n {}'.format(avg_travel_time))

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('This is a breakdown of user types: \n{}'.format(user_type_count))

    print('-'*40)
    # Display counts of gender
    try:
        gender_type_count = df['Gender'].value_counts()
        print('This is a breakdown of user genders: \n{}'.format(gender_type_count))
    except KeyError: 
        print('Gender data not available for selected city')
    

    print('-'*40)

    # Display earliest, most recent, and most common year of birth
    try: 
        earliest_birth_year = int(df['Birth Year'].min())
        print('Earliest Birth Year: {}'.format(earliest_birth_year))
        latest_birth_year = int(df['Birth Year'].max())
        print('Latest Birth Year: {}'.format(latest_birth_year))
        most_common_birth_year = int(df['Birth Year'].mode())
        print('Most Common Birth Year: {}'.format(most_common_birth_year))
    except KeyError:
        print('Birth Year data not available for selected city')
    
    
    print('-'*40)

def data_viewer(df):
    "Asks user if they would like view data (yes or no) returns: if yes, displays 5 rows of data (sorted by descending trip duration length) at a time until user says no "
    
    view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no: ')
    
    start_loc = 0
    end_loc = 5
    while (view_data == 'yes'):
        print(df.iloc[start_loc:end_loc:1])
        start_loc += 5
        end_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display == 'yes':
            continue
        else:
            break           

    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_viewer(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()