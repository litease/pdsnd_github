import time
import pandas as pd
import numpy as np

# set_option to show all columns in output, necessary for raw data not to be truncated
# https://stackoverflow.com/a/49189503/5494666
pd.set_option('display.max_columns', None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all months" to apply no month filter
        (str) day - name of the day of week to filter by, or "all days" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Which city are you interested in? You can choose between: 'Chicago', 'New York' or 'Washington'")
    city = str(input().lower())
    
    #check that city exists in Dictionary
    while city not in CITY_DATA.keys():
            print('Oops, ', city , 'doesn\'t seem to be a city that I know. Remember, you can choose between Chicago, New York or Washington. Please try again!')
            city = str(input().lower())
    
    # Get user input for month (all, january, february, ... , june)
    print("Great! You choose {}. Would you like to filter by month?".format(city.title()))
    filter_by_month = str(input().lower())
    
    while not (filter_by_month == 'yes' or filter_by_month == 'no'):
        print('Seems that I didn\'t get that... Would you like to filter by month? Please type yes or no.')
        filter_by_month = str(input().lower())
                
    if filter_by_month == 'yes':
        print("Which month would you like to see? I have data for January through to June.")
        month = str(input().lower())
        #declare available months for input
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        while month not in months:
            print("Hmm... Seems that I don't have any data for that month. You can choose between January, February, March, April, May or June.")
            month = str(input().lower())
        else:
            print("Great! You choose {}".format(month.title()))
    else:
        month = 'all months'
    
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    print("Ok, last question! Would you like to filter by a specific day of the week?")
    filter_by_day = str(input().lower())
    
    while not (filter_by_day == 'yes' or filter_by_day == 'no'):
        print('Seems that I didn\'t get that... Would you like to filter by day? Please type yes or no.')
        filter_by_day = str(input().lower())

    # Declare available days for input
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    if filter_by_day == 'yes':
        print("Which day would you like to filter by? Type in the full name, e.g. Monday, Tuesday")
        day = str(input().title())
        while day not in days:
            print("Hmm... Seems that is not a correct day. Type in the full name, e.g. Monday, Tuesday")
            month = str(input().lower())
    else:
        day = 'all days'
    print("Ok, I will look at {} in {} for {}. Let's go!".format(city.title(), month.title(), day))
     
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all months" to apply no month filter
        (str) day - name of the day of week to filter by, or "all days" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    
    # filter by month if applicable
    if month != 'all months':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # convert month name to index position, add one for January = 1
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all days':
        # filter by day of week to create the new dataframe 
        
        #Week start on Monday = 0
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        #Convert days into integer position
        day = days.index(day.title())

        #filter data frame for day of week
        df = df.loc[df['day_of_week'] == day]
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month_name = months[int(most_common_month)-1]
    print('The most common month is', most_common_month_name)


    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    #Week start on Monday = 0
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    most_common_day_name = days[int(most_common_day)-1]
    print('The most common day is', most_common_day_name)


    # Display the most common start hour
    # Find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station is', most_popular_start_station)

    # TO DO: display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station is', most_popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    # Concatenate most frequent combination of start and end station, and then split by comma to create a list
    most_popular_route = (df['Start Station'] + ',' + df['End Station']).mode()[0].split(',')
    
    # Get start and end station by index 0 and 1
    print('The most popular route is starting at', most_popular_route[0], 'and ending at', most_popular_route[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    
    minutes = int(total_travel_time / 60)
    hours = int(minutes / 60)
    days = int(hours / 24)
    hours = hours - days * 24
    minutes = minutes - (hours * 60 + days * 60 * 24)
    seconds = int(total_travel_time - (minutes * 60 + hours * 60 * 60 + days * 60 * 60 * 24))

    print("Total travel time for all trips together is {} days, {} hours, {} minutes and {} seconds.".format(days, hours, minutes, seconds))

    # TO DO: display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    minutes = int(average_travel_time / 60)
    seconds = int(average_travel_time - minutes * 60)
    print("Average travel time is {} minutes and {} seconds.".format(minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """
    Displays statistics on bikeshare users.
    
    Input:
    Takes df and city as input. city is used to determine if the data has all necessary columns, e.g. Washington does not have Gender
    and Birth Year, therefore exclude this anlaysis from the logic.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # Output the result into a frame by using <code>.to_frame()</code>, removing the dtype section. See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_frame.html, https://stackoverflow.com/questions/35523635/extract-values-in-pandas-value-counts#comment58737580_35523820
    print(df['User Type'].value_counts().to_frame('User Type Count'))

    # Check if not Washington, as Washington does not store Gender, Birth Year
    if city != 'washington':
        # TO DO: Display counts of gender

        # Output the result into a frame by using <code>.to_frame()</code>, removing the dtype section. See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_frame.html, https://stackoverflow.com/questions/35523635/extract-values-in-pandas-value-counts#comment58737580_35523820
        print(df['Gender'].value_counts().to_frame('Gender Count'))

        # TO DO: Display earliest, most recent, and most common year of birth
        oldest_rider = int(df['Birth Year'].min())
        youngest_rider = int(df['Birth Year'].max())
        most_common_age = int(df['Birth Year'].mode())

        print('The oldest rider was born in', oldest_rider)
        print('The youngest rider was born in', youngest_rider)
        print('The year of birth with most riders is', most_common_age)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(df):
    '''
    Asks the user if they want to see first five rows of data. User can continue to view five rows of data until break.

    Input: Asks user if they want to see first five rows
    Output: None

    '''
    ans = input("Would you like to see the first five rows? Write yes or press Enter. Type no to exit.\n")
    row = int(0)

    while  ans == 'yes' or ans == '':
        print('Showing you row', row + 1, 'to row', row + 5, '\n\n', df[row:row + 5])
        row += 5
        ans = input("\nPress Enter to see the next five rows. Type no to exit.\n")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()