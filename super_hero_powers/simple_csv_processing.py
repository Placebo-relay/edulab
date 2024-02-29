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
    pair_name = f"{pair[0]}_and_{pair[1]}"
    pair_count = (abilities_data[pair[0]] & abilities_data[pair[1]]).sum()
    ability_pair_counts[pair_name] = pair_count

# Freeing some memory
del abilities_data

# Reading top-10 from dictionary
top_10_ability_pairs = pd.Series(ability_pair_counts).nlargest(10)

# Getting top-10 ability pairs to CSV
top_10_ability_pairs.to_csv(
    "top_10_ability_pairs.csv",
    header=["ability_pair_total"],
    index_label="ability_pair",
)

# Getting abilitues per each hero count
data["ability_count"] = data.iloc[:, 1:].sum(axis=1)

# Saving abilities_per_hero_count.csv
data[["hero_names", "ability_count"]].to_csv(
    "abilities_per_hero_count.csv", index=False
)

# Create the Streamlit app
st.title('Superhero Powers Analysis')

# Display the top 10 ability pairs
st.write("Top 10 Ability Pairs:")
st.write(top_10_ability_pairs)

# Allow users to download the top 10 ability pairs as a CSV file
st.markdown("### Download Top 10 Ability Pairs as CSV")
csv = top_10_ability_pairs.to_csv()
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='top_10_ability_pairs.csv',
    mime='text/csv'
)

# Display the abilities per hero count
st.write("Abilities per Hero Count:")
st.write(data[["hero_names", "ability_count"]])

# Allow users to download the abilities per hero count as a CSV file
st.markdown("### Download Abilities per Hero Count as CSV")
csv = data[["hero_names", "ability_count"]].to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='abilities_per_hero_count.csv',
    mime='text/csv'
)
