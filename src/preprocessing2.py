"""
Columnar operation function structure:

Inputs:
    column: list
    config: dict of parameters which will be required for the operation 

Output:
    column: list

Przykładowo:
def operacja(column: list, config: dict) -> list:
    '''Tu w komentarzu (trzy ciapki ' albo ") można podać co przyjmujemy w konfigu (pokaże się w podpowiedziach autocomplete)'''
    
    modified_col = [] <-- najlepiej tworzyć nową listę do której wrzucamy zmienione dane aby nie mutować oryginalnej kolumny w międzyczasie
    jakaś logika przetwarzająca
    return modified_col

---

Narazie trzymajmy wszystkie funkcje w jednym pliku (albo dwóch dopóki pracujemy jednocześnie).

Jeśli wyjdzie na to że niektóre operacje będą dosyć skomplikowane i będą potrzebować kilka funkcji pomocniczych
to sobie wydzielimy katalog src/preprocessing/ w którym każda operacja będzie w swoim pliku
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# dyskretyzacja zmiennych rzeczywistych na określoną liczbę przedziałów;
def discretize(column: list[float], num_col: int) -> list:
    data = pd.DataFrame({'column': column})
    discretized_column = pd.cut(data['column'], bins=num_col, labels=False)
    return discretized_column.to_list()


"""
    # Example usage:
    column_to_discretize = [1.5, 9.2, 8.0, 4.5, 5.8, 6.3, 7.1]
    num_bins = 3
    
    discretized_result = discretize_fixed_bins(column_to_discretize, num_bins)
    print(discretized_result)

"""


# zmiana przedziału wartości z oryginalnego <min; max> na przedział, którego zakres wartości poda użytkownik <a; b>
def discretize2(column: list[float], config: dict) -> list:
    # config = {'a': 0, 'b': 1}
    a = config['a']
    b = config['b']

    scale_factor = (b - a) / (max(column) - min(column))
    mapped_values = [a + scale_factor * (value - min(column)) for value in column]

    rounded_col = [round(value, 10) for value in
                   mapped_values]  # zaokrąglam wyniki do 10, nie potrzebnie ale do rozważenia

    return rounded_col


"""
    # Example usage:
    column_to_discretize = [1.5, 9.2, 3.0, 4.5, 5.8, 6.3, 7.1]
    config = {'a': 0, 'b': 1}
    
    discretized_result = discretize2(column_to_discretize, config)
    print(discretized_result)
"""


# wykres 2D (rozproszeń dwuwymiarowy) - zależność dwóch zmiennych, z możliwością wybrania opcji o zastosowaniu kolorów/znaczników do klas
def plot_2d(x, y, classes, colors=None, markers=None):
    if colors is None:
        colors = sns.color_palette("husl", n_colors=len(set(classes))) if classes else 'b'
    if markers is None:
        markers = ['o'] * len(set(classes)) if classes else 'o'

    data = {'x': x, 'y': y, 'class': classes}
    df = pd.DataFrame(data)

    sns.scatterplot(x='x', y='y', hue='class', data=df, palette=colors, style='class', markers=markers)

    plt.show()


"""
    # Example usage:
    x_values = [1.5, 2.2, 3.0, 4.5, 5.8, 6.3, 7.1]
    y_values = [2.0, 3.5, 1.8, 4.2, 5.1, 6.7, 7.5]
    class_labels = [1, 1, 1, 1, 0, 0, 0]
    class_colors = ['red', 'green']
    class_markers = ['o', '^','s']
    plot_2d(x_values, y_values, classes=class_labels, colors=class_colors, markers=class_markers)
"""


# histogram (zmienna dyskretna, zmienna ciągła - podanie liczby przedziałów)
def create_histogram_discrete(data, num_bins, discrete_data=True):
    if discrete_data:
        plt.hist(data, bins=num_bins, edgecolor='black', alpha=0.7, align='left')
        plt.title('Histogram (Discrete)')
    else:
        plt.hist(data, bins=num_bins, edgecolor='black', alpha=0.7)
        plt.title('Histogram (Continuous)')

    plt.xlabel('Values')
    plt.ylabel('Frequency')

    # Show the plot
    plt.show()


"""
    # Example usage for discrete data:
    
    discrete_data = np.random.randint(0, 10, size=100)  # Example: random discrete data
    num_bins_discrete = 10
    create_histogram_discrete(discrete_data, num_bins_discrete)
    
    continuous_data = np.random.randn(1000)  # Example: random continuous data
    num_bins_continuous = 20
    create_histogram_continuous(continuous_data, num_bins_continuous)
"""
