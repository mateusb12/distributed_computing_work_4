import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_analysis.csv_merger import get_csv_folder


def get_merged_file() -> pd.DataFrame:
    path = get_csv_folder() / "merged.csv"
    return pd.read_csv(path)


def plot_charts(input_dataframe: pd.DataFrame):
    disabled_cache_group = input_dataframe[input_dataframe['Cache'] == 'disabled']
    disabled_cache_grouped = disabled_cache_group.groupby(['Cache', 'Language', 'Users'])[
        'Median Response Time'].mean().reset_index()

    enabled_cache_group = input_dataframe[input_dataframe['Cache'] == 'enabled']
    enabled_cache_grouped = enabled_cache_group.groupby(['Language', 'Users'])[
        'Median Response Time'].mean().reset_index()
    enabled_cache_grouped['Cache'] = 'enabled'

    plt.figure(figsize=(14, 7))

    ax1 = plt.subplot(1, 2, 1)
    sns.barplot(x='Users', y='Median Response Time', hue='Language', data=disabled_cache_grouped, palette='muted',
                edgecolor='black', errorbar=None, zorder=3)
    plt.title('Cache Desabilitado')
    plt.xlabel('Número de Usuários')
    plt.ylabel('Tempo Médio de Resposta (ms)')
    plt.legend(title='Linguagem')
    ax1.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)

    ax2 = plt.subplot(1, 2, 2)
    sns.barplot(x='Users', y='Median Response Time', hue='Language', data=enabled_cache_grouped, palette='muted',
                edgecolor='black', errorbar=None, zorder=3)
    plt.title('Cache Habilitado')
    plt.xlabel('Número de Usuários')
    plt.ylabel('Tempo Médio de Resposta (ms)')
    plt.legend(title='Linguagem')
    ax2.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)
    plt.tight_layout()
    plt.show()



def plot_cache_impact(input_dataframe: pd.DataFrame):
    # Group the data by 'Cache', 'Language', and 'Users', then calculate the average median response time
    grouped_data = input_dataframe.groupby(['Cache', 'Language', 'Users'])['Median Response Time'].mean().reset_index()

    # Set up the figure for plotting
    plt.figure(figsize=(14, 7))

    # Subplot for the impact of caching on Python
    plt.subplot(1, 2, 1)
    python_data = grouped_data[grouped_data['Language'] == 'python']
    sns.barplot(x='Users', y='Median Response Time', hue='Cache',
                 data=python_data, palette='Set1', edgecolor='black', errorbar=None)
    plt.title('Impacto do Cache no Python')
    plt.xlabel('Número de Usuários')
    plt.ylabel('Tempo de Resposta Médio (ms)')
    plt.legend(title='Configuração Cache')
    plt.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)

    # Subplot for the impact of caching on Ruby
    plt.subplot(1, 2, 2)
    ruby_data = grouped_data[grouped_data['Language'] == 'ruby']
    sns.barplot(x='Users', y='Median Response Time', hue='Cache',
                 data=ruby_data, palette='Set2', edgecolor='black', errorbar=None)
    plt.title('Impacto do Cache no Ruby')
    plt.xlabel('Número de Usuários')
    plt.ylabel('Tempo de Resposta Médio (ms)')
    plt.legend(title='Configuração Cache')
    plt.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)

    # Adjust the layout and display the plots
    plt.tight_layout()
    plt.show()


def __main():
    df = get_merged_file()
    plot_charts(df)
    plot_cache_impact(df)


if __name__ == '__main__':
    __main()
