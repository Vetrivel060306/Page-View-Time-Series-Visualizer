import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df =pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')


# Clean data
df=df.loc[
                        (df['value'] >= df['value'].quantile(0.025)) &
                        (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    df_plot = df.copy()
    fig, ax = plt.subplots(figsize=(20, 6))
    ax.grid(c='blue', linestyle='--', linewidth=0.5)
    ax.plot(df_plot.index, df_plot['value'], c='red')
    ax.set_ylabel('Page Views')
    ax.set_xlabel('Date')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    df_bar = df.copy()
    df_bar = df_bar.reset_index()
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.month
    monthly_averages = df_bar.groupby(['year', 'month'])['value'].mean()
    df_monthly = monthly_averages.reset_index()

    # Create a new column with full month names for the legend
    df_monthly['Month_Name'] = df_monthly['month'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))

    # Ensure the months are sorted correctly for plotting and legend order
    # This creates a categorical type with a specific order
    month_order = [pd.to_datetime(str(m), format='%m').strftime('%B') for m in sorted(df_monthly['month'].unique())]
    df_monthly['Month_Name'] = pd.Categorical(df_monthly['Month_Name'], categories=month_order, ordered=True)

    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        x='year',  # Group on the x-axis by year
        y='value',  # Bar height is the average page view
        hue='Month_Name',  # Create separate bars and colors for each month
        data=df_monthly,  # The DataFrame to use
        ax=ax,  # Plot it on the Matplotlib Axes object
        palette='tab10'
    )

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    # Customize the legend title
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title='Months', loc='upper left')

    # Get the unique years for labels
    year_labels = df_monthly['year'].unique()

    # --- CORRECTION ---
    # Set ticks to be the positional index (0, 1, 2, 3) where the bars are drawn
    ax.set_xticks(np.arange(len(year_labels)))

    # Set the labels to be the actual year values (2016, 2017, etc.)
    ax.set_xticklabels(year_labels)

    plt.tight_layout()  # Adjust layout to prevent labels from overlapping

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

    # Repeat the same cleanup for draw_line_plot for safety


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(
        nrows=1, ncols=2,
        figsize=(15, 6),
        sharey=False
    )
    sns.boxplot(
        x="year",
        y="value",
        hue="year",
        data=df_box,
        ax=ax1,
        palette='tab10',
        legend=False
    )
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_ylabel('Page Views')
    ax1.set_xlabel('Year')

    sns.boxplot(
        x="month",
        y="value",
        hue='month',
        data=df_box,
        ax=ax2,
        palette='tab20',
        legend=False,
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_ylabel('Page Views')
    ax2.set_xlabel('Month')

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

