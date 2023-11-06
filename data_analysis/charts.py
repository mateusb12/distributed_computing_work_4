import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_analysis.csv_merger import get_csv_folder


def get_merged_file() -> pd.DataFrame:
    path = get_csv_folder() / "merged.csv"
    return pd.read_csv(path)


def english_to_portuguese_y_label(term: str) -> str:
    term_table = {"Median Response Time": "Mediana do Tempo de Resposta (ms)",
                  "Average Response Time": "Média do Tempo de Resposta (ms)",
                  "95%": "Percentil 95%"}
    return term_table[term]


def plot_language_charts(input_dataframe: pd.DataFrame, feature: str = "Median Response Time"):
    feature_portuguese_y_label = english_to_portuguese_y_label(feature)
    disabled_cache_group = input_dataframe[input_dataframe['Cache'] == 'disabled']
    disabled_cache_grouped = disabled_cache_group.groupby(['Cache', 'Language', 'Users'])[feature].mean().reset_index()

    enabled_cache_group = input_dataframe[input_dataframe['Cache'] == 'enabled']
    enabled_cache_grouped = enabled_cache_group.groupby(['Language', 'Users'])[feature].mean().reset_index()
    enabled_cache_grouped['Cache'] = 'enabled'

    plt.figure(figsize=(14, 7))

    ax1 = plt.subplot(1, 2, 1)
    sns.barplot(x='Users', y=feature, hue='Language', data=disabled_cache_grouped, palette='muted',
                edgecolor='black', errorbar=None, zorder=3)
    plt.title('Cache Desabilitado')
    plt.xlabel('Número de Usuários')
    plt.ylabel(feature_portuguese_y_label)
    plt.legend(title='Linguagem')
    ax1.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)

    ax2 = plt.subplot(1, 2, 2)
    sns.barplot(x='Users', y=feature, hue='Language', data=enabled_cache_grouped, palette='muted',
                edgecolor='black', errorbar=None, zorder=3)
    plt.title('Cache Habilitado')
    plt.xlabel('Número de Usuários')
    plt.ylabel(feature_portuguese_y_label)
    plt.legend(title='Linguagem')
    ax2.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)
    plt.tight_layout()
    plt.show()


def plot_cache_impact(input_dataframe: pd.DataFrame, feature: str = "Median Response Time"):
    feature_portuguese_label = english_to_portuguese_y_label(feature)
    grouped_data = input_dataframe.groupby(['Cache', 'Language', 'Users'])[feature].mean().reset_index()

    plt.figure(figsize=(14, 7))

    plt.subplot(1, 2, 1)
    python_data = grouped_data[grouped_data['Language'] == 'python']
    sns.barplot(x='Users', y=feature, hue='Cache',
                data=python_data, palette='Set1', edgecolor='black', errorbar=None, zorder=3)
    plt.title('Impacto do Cache no Python')
    plt.xlabel('Número de Usuários')
    plt.ylabel(feature_portuguese_label)
    plt.legend(title='Configuração Cache')
    plt.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)

    plt.subplot(1, 2, 2)
    ruby_data = grouped_data[grouped_data['Language'] == 'ruby']
    sns.barplot(x='Users', y=feature, hue='Cache',
                data=ruby_data, palette='Set2', edgecolor='black', errorbar=None, zorder=3)
    plt.title('Impacto do Cache no Ruby')
    plt.xlabel('Número de Usuários')
    plt.ylabel(feature_portuguese_label)
    plt.legend(title='Configuração Cache')
    plt.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.7, zorder=0)

    plt.tight_layout()
    plt.show()


def __main():
    df = get_merged_file()
    plot_language_charts(df, feature="Median Response Time")
    plot_cache_impact(df, feature="Median Response Time")


if __name__ == '__main__':
    __main()
