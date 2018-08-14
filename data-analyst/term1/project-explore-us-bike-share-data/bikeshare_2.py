import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for chicago, new york city, or washington: ").lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("Sorry, you entered an incorrect city, please try again.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to see data for (data is only avaiable for january through june)? Specify 'all' if you'd like to see every month: ").lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("Sorry, you entered an incorrect month, please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day of week would you like to see data for? Specify 'all' if you'd like to see every day: ").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("Sorry, you entered an incorrect day of week, please try again.")


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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month for travel is {}".format(MONTHS[df['Month'].mode()[0]-1].title()))

    # display the most common day of week
    print("The most common day of week for travel is {}".format(df['Day of Week'].mode()[0]))

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    print("The most common starting hour for travel is {} o\'clock".format(df['Start Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station is {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print("The most commonly used combination of start station and end station trip is {} to {}".format(combination[0], combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time was {} seconds".format(int(df['Trip Duration'].sum())))

    # display mean travel time
    print("The mean travel time per trip was {} seconds".format(int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    print(df.groupby(['User Type']).size())
    print("\n")

    # Display counts of gender
    try:
        print(df.groupby(['Gender']).size())
        print("\n")
    except KeyError:
        print("No gender data available")

    # Display earliest, most recent, and most common year of birth
    try:
        print("The earliest year of birth is {}, most recent year of birth is {}, and most common year of birth is {}".format(int(df['Birth Year'].min()) , int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])))
    except KeyError:
        print("Non birth year data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
