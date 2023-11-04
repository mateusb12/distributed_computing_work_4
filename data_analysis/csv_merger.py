import os
from pathlib import Path
import pandas as pd
from shutil import move


def get_csv_folder():
    return Path(os.path.dirname(os.path.realpath(__file__))).parent / "test_results"


def merge_csv_files():
    folder_path = get_csv_folder()
    all_folder_files = os.listdir(folder_path)
    all_csv_files = [item for item in all_folder_files if item.endswith(".csv")]
    df_pot = []
    for file in all_csv_files:
        raw_cache, raw_language, raw_users = file[:-4].split("+")
        dataframe = pd.read_csv(folder_path / file)
        cache = raw_cache.split("_")[-1]
        language = raw_language.split("_")[-1]
        users = int(raw_users.split("_")[0])
        dataframe["Cache"] = cache
        dataframe["Language"] = language
        dataframe["Users"] = users
        df_pot.append(dataframe)
    mega_df = pd.concat(df_pot)
    mega_df.to_csv(folder_path / "merged.csv", index=False)
    csv_pool_path = folder_path / 'csv_pool'
    if not csv_pool_path.exists():
        csv_pool_path.mkdir()

    # Move all the original csv files to the new 'csv_pool' folder
    for file in all_csv_files:
        move(str(folder_path / file), str(csv_pool_path / file))


def __main():
    merge_csv_files()
    return


if __name__ == '__main__':
    __main()
