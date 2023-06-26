import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import re

def bar_graph(df):

    bar_data = df.sort_values('Overall')[-5:]
    bar_data = bar_data[['Company', 'Flavor', 'Aroma', 'Sweetness', 'Aftertaste']]

    categories = ['Flavor', 'Aroma', 'Sweetness', 'Aftertaste']
    colors = ['#86BBD8', '#F6AE2D', '#F26419']

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

    for i, c in enumerate(categories):
        row = i // 2
        col = i % 2
        ax = axes[row, col]
        
        data = bar_data[['Company', c]] # Gets the values of the category divided by company
        
        sns.barplot(data=data, x=np.arange(len(bar_data)), y=c, hue='Company', dodge=False, ax=ax, palette=colors)
        
        ax.set_xticks([]) # Removes x label
        ax.set_ylabel(c)
        
        ax.set_title(c, weight='bold')
        ax.set_ylim((0, 20))
        
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, title='Company')

        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2, p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')
        
    plt.tight_layout()
    plt.show()

def _clean(date_str):
    pattern = r'(\d+)(st|nd|rd|th)'
    match = re.search(pattern, date_str)
    if match:
        number = match.group(1)
        return date_str.replace(match.group(), number)
    else:
        return date_str

def convert_date(date_str):
    clean = date_str.apply(_clean)
    return pd.to_datetime(clean, format='%B %d, %Y')

def line_graph(df):
    company = df.sort_values('Overall').iloc[-1]['Company']
    line_data = df[df['Company'] == company][['Company', 'Overall', 'Grading Date']] # Filters all registers of the overall best company's coffee over time
    
    # Converting 'Grading Date' field to Date
    line_data['Grading Date'] = convert_date(line_data['Grading Date'])
    
    # Removing duplicates, that is, two different types of coffee that were graded on the same day. The coffee with overall best quality is kept.
    line_data = line_data.sort_values('Overall', ascending=False)
    line_data = line_data.drop_duplicates('Grading Date', keep='first')
    line_data = line_data.sort_values('Grading Date') # Sorting the values based on the grading date

    plt.figure(figsize=(7, 5))

    sns.lineplot(data=line_data, x='Grading Date', y='Overall', linewidth=2, marker='o', color='#AD2831')

    for x, y in zip(line_data['Grading Date'], line_data['Overall']):
        plt.annotate(format(y, '.2f'), (x, y), ha='center', va='bottom', xytext=(0, 5), textcoords='offset points')

    plt.title(f'{company} Coffee Quality', weight='bold')
    plt.xlabel('Grading Date')
    plt.ylabel('Overall Quality')

    plt.ylim(line_data['Overall'].min() - 0.5, line_data['Overall'].max() + 0.5)

    plt.show()

if __name__ == '__main__':
    df = pd.read_csv('df_arabica_clean.csv')
    bar_graph(df)
    # line_graph(df)