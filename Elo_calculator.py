import numpy as np
import pandas as pd
import math
from datetime import date

#  Load the data into separate dataframes
Miecz = pd.read_csv("..\Dane Liga\Liga Zawo 2023 - Walki_Miecz.csv")
Szabla = pd.read_csv("..\Dane Liga\Liga Zawo 2023 - Walki_Szabla.csv")
Kuklerz = pd.read_csv("..\Dane Liga\Liga Zawo 2023 - Walki_Kuklerz.csv")
#  Create a list of dataframes for processing
tabelki = [Miecz, Szabla, Kuklerz]

#  Define the categories corresponding to the dataframes
categories = ["Miecz", "Szabla", "Kuklerz"]

# This function calculates the probability of win by a fencer given his elo rating

def exp_result(f1, f2):
    res = 1 / (1 + math.pow(10, (f2 - f1) / 400))
    return [np.round(res, 3), 1 - np.round(res, 3)]


# This function calculates changes in elo given fencers elo before bout, and k factor
# (as of now there is only one type of competition so k will be held constatnt)

def calculate_elo(w_elo, l_elo):
    k = 10
    wer, ler = exp_result(w_elo, l_elo)

    n_elo_w = w_elo + k * (1 - wer)
    n_elo_l = l_elo + k * (0 - ler)
    return n_elo_w, n_elo_l


# This function uses exp_result function and calculete_elo to allow users to check their win prob against oponent and
# possible Elo changes after the bout


def check_outcome(f1, f2):
    f1_c_rating = current_elo[f1]
    f2_c_rating = current_elo[f2]

    ex_1, ex_2 = exp_result(f1_c_rating, f2_c_rating)

    new_f1_rating_w, new_f2_rating_l = calculate_elo(f1_c_rating, f2_c_rating)
    new_f2_rating_w, new_f1_rating_l = calculate_elo(f2_c_rating, f1_c_rating)

    f1_change_w = new_f1_rating_w - f1_c_rating
    f1_change_l = new_f1_rating_l - f1_c_rating
    f2_change_w = new_f2_rating_w - f2_c_rating
    f2_change_l = new_f2_rating_l - f2_c_rating

    print(f"Win possibility for {f1} is {ex_1:.2f}", f"While for {f2} it is {ex_2:.2f}")
    print(f"If {f1} wins, their Elo change is +{f1_change_w:.2f} and {f2} Elo change is {f1_change_l:.2f}")
    print(f"If {f2} wins, their Elo change is +{f2_change_w:.2f} and {f1} Elo change is {f2_change_l:.2f}")


#  Loop through each category's dataframe
processed_dataframes = {}  #  Dictionary to store processed dataframes for each category
rankings_dataframes = {}    #  Dictionary to store ranking data frames for each category
Elo_history_dataframes = {}  #  Dictionary to store elo history data frames for each category

for df, category in zip(tabelki, categories):
    df = df.drop(labels=0, axis=0)
    df = df.dropna()
    df = df.drop(columns=["Trafienia Wygranego", "Trafienia Przegranego", "Duble", "Numer Ligi", "Maks punktów",
                          "Trafienia W. Znorm.", "Trafienia P. Znorm", "Duble Znorm."])
    print(f"Processing {category} data:")
    print(df.head())

    processed_dataframes[category] = df

for category, df in processed_dataframes.items():
    current_elo = {}
    rankings = []

    for idx, row in df.iterrows():
        winner = row['Wygrany']
        looser = row['Przegrany']

        if winner not in current_elo:
            current_elo[winner] = 1200
        if looser not in current_elo:
            current_elo[looser] = 1200

        w_elo = current_elo[winner]
        l_elo = current_elo[looser]
        n_elo_w, n_elo_l = calculate_elo(w_elo, l_elo)

        current_elo[winner] = n_elo_w
        current_elo[looser] = n_elo_l

        df.loc[idx, 'Elo_w_after'] = n_elo_w
        df.loc[idx, 'Elo_l_after'] = n_elo_l
        df.loc[idx, 'Elo_w_before'] = w_elo
        df.loc[idx, 'Elo_l_before'] = l_elo

    rankings.append(df.copy())  #  Append a copy of the DataFrame

    Elo_history_dataframes[category] = pd.concat(rankings, ignore_index=True)

    #  Create the ranking dataframe for the category
    category_ranking = pd.DataFrame.from_dict(current_elo, orient='index')
    category_ranking = category_ranking.set_axis(["Elo"], axis=1)
    category_ranking = category_ranking.sort_values(["Elo"], ascending=False)
    category_ranking = category_ranking.reset_index()
    category_ranking.index = category_ranking.index + 1
    category_ranking = category_ranking.set_axis(["Fencer", "Elo"], axis=1)

    rankings_dataframes[category] = category_ranking
    elo_history = pd.concat(rankings, ignore_index=True)

    #  Save the ranking to a file
    ranking_filename = f"Ranking_{category}_{date.today()}.txt"
    category_ranking.to_csv(ranking_filename, index=False)

    print(f"Saved {category} ranking to {ranking_filename}")

    #  Save the history to a file
    history_filename = f"History_{category}.txt"
    Elo_history_dataframes[category].to_csv(history_filename, index=False)

    print(f"Saved {category} history to {history_filename}")
    