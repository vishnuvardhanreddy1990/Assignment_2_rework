import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def retrieve_data():
    
    '''

    RECIEVING DATA

    '''
    
    # Assuming you have your data stored in a CSV file named 'data.csv'
    data = pd.read_csv('worldbank_climate_change_data.csv')
    
    # Clean up the dataframe
    data = data.rename(columns={'country': 'Country', 'date': 'Year'})
    
    return data


def process_data(filename):
    
    '''
    PROCESSING DATA
    
    '''
    
    df = pd.read_csv(filename)
    df.dropna(inplace=True)

    # Transpose the dataframe to have years as columns
    df_years = df.pivot(index='Country', columns='Year')

    # Transpose the dataframe again to have countries as columns
    df_countries = df.pivot(index='Year', columns='Country')

    # Clean up the transposed dataframes
    df_years.columns = df_years.columns.droplevel()
    df_countries.columns = df_countries.columns.droplevel()

    return df_years, df_countries


def save_data(data, filename):
    
    # Save the data to a CSV file
    data.to_csv(filename, index=False)


def plot_time_series(data, x, y, hue=None, title=None, xlabel=None, ylabel=None):
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=data, x=x, y=y, hue=hue)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    

def plot_bar_chart(data, x, y, hue=None, title=None, xlabel=None, ylabel=None):
    
    '''
    BAR PLOT
    '''
    plt.figure(figsize=(8, 6))
    sns.barplot(data=data, x=x, y=y, hue=hue)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.show()


def plot_scatter(data, x, y, title=None, xlabel=None, ylabel=None):
    
    '''
    SCATTER PLOT
    '''
    plt.scatter(data[x], data[y])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def plot_heatmap(data, title=None):
    
    '''
    HEATMAP
    '''
    corr_matrix = data.corr()
    sns.heatmap(corr_matrix, cmap='YlGnBu', annot=True)
    plt.title(title)
    plt.show()


def analyze_data(filename):
    
    '''
    ANALYSING DATA
    '''
    
    df = pd.read_csv(filename)
    df.dropna(inplace=True)

    # Select countries
    countries = ['United States', 'United Kingdom', 'China', 'India', 'Russia',
                 'Brazil', 'South Africa']
    df = df[df['Country'].isin(countries)]

    # Plot CO2 emissions for United States
    df_US = df[df['Country'] == 'United States'][::-1]
    plot_time_series(df_US, 'Year', 'CO2 emissions (kt)', 
                     title='CO2 Emissions for United States')
    
    plot_time_series(df_US, 'Year', 'Energy use per capita (kg of oil equivalent)',
                     title='Energy Use per Capita for United States')
    
    plot_time_series(df_US, 'Year', 'GDP (current US$)', title='GDP for United States')
    
    plot_scatter(df_US, 'GDP (current US$)', 'CO2 emissions (kt)', 
                 title='CO2 Emissions vs GDP for United States')
    
    plot_bar_chart(df_US, 'Year', 'Population, total', 
                   title='Population Trend over the Years')

    # Plot correlation heatmap
    plot_heatmap(df, title='Correlation Heatmap')

    # Calculate correlation coefficients between CO2 emissions and energy use per capita for each country
    corr_by_country = df.groupby('Country')[['CO2 emissions (kt)', 
         'Energy use per capita (kg of oil equivalent)']].corr().iloc[0::2, -1]
    
    print(corr_by_country)

    # Plot 5-Year average of CO2 emissions by country
    df['Year'] = pd.to_datetime(df['Year'])
    grouped = df.groupby(['Country', 
        pd.Grouper(key='Year', freq='1Y')])['CO2 emissions (kt)'].mean().reset_index()
   
    grouped = grouped.set_index('Year').groupby('Country').resample('5Y').mean().reset_index()

    plt.figure(figsize=(8, 6))
    sns.barplot(data=grouped, x='Country', y='CO2 emissions (kt)', hue='Year')
    plt.title('5-Year Average of CO2 Emissions by Country')
    plt.xlabel('Year')
    plt.ylabel('CO2 Emissions (kt)')

    handles, labels = plt.gca().get_legend_handles_labels()
    new_labels = [label.split('T')[0] for label in labels]
    plt.legend(handles, new_labels)
    plt.xticks(rotation=45)
    plt.show()

    df_china = df[df['Country'] == 'China']

    plt.figure(figsize=(8, 6))
    sns.lineplot(data=df, x='Year', y='GDP (current US$)', hue='Country')
    plt.xlabel('Year')
    plt.title('GDP over Time')
    plt.show()

# Define the indicator codes for the data we want to retrieve
indicator_codes = {
    'EN.ATM.CO2E.KT': 'CO2 emissions (kt)',
    'EG.USE.PCAP.KG.OE': 'Energy use per capita (kg of oil equivalent)',
    'NY.GDP.MKTP.CD': 'GDP (current US$)',
    'SP.POP.TOTL': 'Population, total',
}

data = retrieve_data()

# Analyze the data
analyze_data('worldbank_climate_change_data.csv')

