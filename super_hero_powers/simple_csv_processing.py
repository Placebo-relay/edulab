"""
Analyze dataset:
    
    Count heroes per each ability
    Get top-10 pairs of abilities
    Count abilities per each hero

License: MIT License
"""

from itertools import combinations
import pandas as pd
import streamlit as st

# Load the data from the CSV file into a pandas DataFrame
data = pd.read_csv(
    "super_hero_powers/super_hero_powers.csv",
    true_values=["True"],
    false_values=["False"],
)

# Dropping names for heroes per each ability count
abilities_data = data.drop("hero_names", axis=1)

# Saving to CSV
abilities_data.sum().to_csv(
    "heroes_per_ability.csv",
    header=["ability_total"],
    index_label="ability_name",
)

# Getting combinations
ability_combinations = list(combinations(abilities_data.columns, 2))

# Pairs to dictionary
ability_pair_counts = {}
for pair in ability_combinations:
    pair_name = f"{pair[0]} & {pair[1]}"
    pair_count = (abilities_data[pair[0]] & abilities_data[pair[1]]).sum()
    ability_pair_counts[pair_name] = pair_count

# Freeing some memory
# del abilities_data

# Reading top-10 from dictionary
top_10_ability_pairs = pd.Series(ability_pair_counts).nlargest(10)

# Getting top-10 ability pairs to CSV
top_10_ability_pairs.to_csv(
    "top_10_ability_pairs.csv",
    header=["ability_pair_total"],
    index_label="ability_pair",
)

top_10_ability_pairs.index = ['ability_pair', 'ability_pair_count']
    
# Getting abilitues per each hero count
data["ability_count"] = data.iloc[:, 1:].sum(axis=1)

# Saving abilities_per_hero_count.csv
data[["hero_names", "ability_count"]].to_csv(
    "abilities_per_hero_count.csv", index=False
)

# Create the Streamlit app
st.title('Superhero Powers Analysis')

# Display the original CSV data
st.header('Original Superhero Powers Data')
original_data = pd.read_csv(
    "super_hero_powers/super_hero_powers.csv",
    true_values=["True"],
    false_values=["False"],
)

original_data["hero_abilities"] = original_data.iloc[:, 1:].apply(
    lambda x: ", ".join(x.index[x]), axis=1
)

original_data["ability_count"] = data["ability_count"]

st.dataframe(
    original_data[["hero_names", "ability_count", "hero_abilities"]],
    hide_index=True,
    column_config={
        "hero_names": "Hero",
        "ability_count": st.column_config.NumberColumn(
            "Ability count",
            help="Number of abilities that hero has",
            format="%d 💪",
        ),
        "hero_abilities": "Ability list",
    },
)

# Display the top 10 ability pairs
st.write("## Top 10 Ability Pairs:")
st.dataframe(
    top_10_ability_pairs,
    column_config={
        "": "Power-pair",
        "0": st.column_config.NumberColumn(
            "Power-pair count",
            help="Number of heroes with these two powers",
            format="%d 🦸‍♂️",
        ),
    },
)

# Allow users to download the top 10 ability pairs as a CSV file
st.markdown("### ⬇️Download Top 10 Ability Pairs as CSV")
csv = top_10_ability_pairs.to_csv()
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='top_10_ability_pairs.csv',
    mime='text/csv'
)

# Display the abilities per hero count
st.write("## 🦸‍♂️Heroes per Ability Count:")
st.dataframe(
    abilities_data.sum(),
    column_config={
        "": "Ability",
        "0": st.column_config.NumberColumn(
            "Power-pair count",
            help="Number of heroes with this power",
            format="%d 🦸‍♂️",
        ),
    },
)

# Allow users to download the abilities per hero count as a CSV file
st.markdown("### ⬇️Download Heroes per Ability as CSV")
csv = data[["hero_names", "ability_count"]].to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='heroes_per_ability.csv',
    mime='text/csv'
)

# Display the abilities per hero count
st.write("## 💪Abilities per Hero Count:")
st.dataframe(
    data[["hero_names", "ability_count"]],
    hide_index=True,
    column_config={
        "hero_names": "Hero",
        "ability_count": st.column_config.NumberColumn(
            "Ability count",
            help="Number of abilities that hero has",
            format="%d 💪",
        ),
    },
)
# Allow users to download the abilities per hero count as a CSV file
st.markdown("### ⬇️Download Abilities per Hero Count as CSV")
csv = data[["hero_names", "ability_count"]].to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='abilities_per_hero_count.csv',
    mime='text/csv'
)
