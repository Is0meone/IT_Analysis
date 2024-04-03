import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ast
import re

import streamlit as st

import pickle
import json
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def recommend_technologies(user_skills, df, num_recommendations=2):
    # user_skills = set([skill.lower() for skill in user_skills])
    # tech_count = {}

    # for index, row in df.iterrows():
    #     used_techs = row['Used Technologies']
        
    #     if isinstance(used_techs, dict):
    #         for tech, level in used_techs.items():
    #             tech = tech.lower()
    #             if tech not in user_skills:
    #                 tech_count[tech] = tech_count.get(tech, 0) + 1

    # sorted_technologies = sorted(tech_count.items(), key=lambda x: x[1], reverse=True)
    # recommended_tech = [(tech, f"https://www.google.com/search?q={tech}+tutorial") 
    #                     for tech, count in sorted_technologies[:num_recommendations]]

    # return recommended_tech



    jobs_df = pd.read_csv('jobData.csv', on_bad_lines='skip')

    # Function to parse the 'Used Technologies' column
    def parse_technologies(tech_entry):
        if isinstance(tech_entry, str):
            # Handling the dictionary format
            if tech_entry.startswith('{'):
                try:
                    tech_dict = json.loads(tech_entry.replace("'", "\""))
                    return list(tech_dict.keys())
                except json.JSONDecodeError:
                    return []
            # Handling the comma-separated string format
            else:
                return tech_entry.split(',')
        return []

    # Applying the function to parse skills
    jobs_df['Skills'] = jobs_df['Used Technologies'].apply(parse_technologies)

    # Transforming the dataset into the right format
    te = TransactionEncoder()
    te_ary = te.fit(jobs_df['Skills']).transform(jobs_df['Skills'])
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Apply Association Rule Mining
    # Finding frequent itemsets
    frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)

    # Generating rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)  # Adjust min_threshold as needed

    # Extract and Analyze Rules
    # Filter and sort these rules based on metrics like lift, confidence, etc.
    # For example, to sort by confidence and lift:
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])

    # Filter rules where the antecedents contain any of the user inputs
    # Note: the antecedents in the rules DataFrame are of type frozenset, so we need to check accordingly
    filtered_rules = rules[rules['antecedents'].apply(lambda x: any(item in x for item in user_skills))]

    # Extract and rank recommended technologies (consequents)
    # We can rank by 'confidence', 'lift', or other metrics depending on your preference
    recommended_technologies = filtered_rules[['consequents', 'confidence', 'lift']].sort_values(by='confidence', ascending=False)
    recommended_technologies['consequents'] = recommended_technologies['consequents'].apply(iter_frozenset)

    return recommended_technologies[:num_recommendations]

def iter_frozenset(frozenset):
    return ', '.join([x for x in frozenset])

def predict_salary(user_input_technologies):
    column_names = []
    with open('column_names.txt', 'r') as file:
        for line in file:
            column_names.append(line.strip())  # Remove newline characters

    feature_vector = pd.Series(0, index=column_names)

    # Set the corresponding features to 1 based on user input
    for tech in user_input_technologies:
        if f'Used_{tech}' in feature_vector.index:
            feature_vector[f'Used_{tech}'] = 1

    with open('selector.pkl', 'rb') as file:
        selector = pickle.load(file)

    feature_vector_transformed = selector.transform(feature_vector.to_frame().T)
    loaded_model = pickle.load(open('salary_prediction_model.sav', 'rb'))
    predicted_salary_min = loaded_model.predict(feature_vector_transformed)

    print("Predicted Minimum Salary: {:.2f}".format(predicted_salary_min[0]))
    return round(predicted_salary_min[0], 2)



def parse_mixed_technologies(data):
    if isinstance(data, str):
        # Replace commas within parentheses with a placeholder
        data_with_placeholder = re.sub(r'\((.*?)\)', lambda x: x.group(0).replace(',', ';'), data)

        # Split the string by commas
        split_data = data_with_placeholder.split(', ')

        # Restore the original commas and strip whitespace
        parsed_data = [tech.replace(';', ',').strip() for tech in split_data]

        # Check if any item is a JSON-like dictionary
        for i, item in enumerate(parsed_data):
            try:
                # Attempt to parse as JSON
                tech_dict = json.loads(item.replace("'", "\""))
                if isinstance(tech_dict, dict):
                    # Replace the item with its keys
                    parsed_data[i] = list(tech_dict.keys())
            except json.JSONDecodeError:
                continue

        # Flatten the list in case of nested lists from JSON parsing
        return [item for sublist in parsed_data for item in (sublist if isinstance(sublist, list) else [sublist])]
    return []

FONT_SIZE = 18

def plot_recommendations(title, df):
    df_new = df.copy()

    # x_positions = np.arange(len(df_new['consequents']))

    plt.figure(figsize=(10, 6))
    plt.bar(df_new['consequents'], df_new['confidence'], color='skyblue', width=0.4)
    plt.xlabel('Technology')
    plt.ylabel('Confidence')
    plt.title(title)
    # plt.xticks(x_positions, df_new['consequents'], rotation=45, fontsize=FONT_SIZE)
    plt.xticks(df_new['consequents'], rotation=45, fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.ylim(0, 1)
    # plt.tight_layout()
    return plt


def parse_salary_range(salary_str):
    if salary_str != '-' and isinstance(salary_str, str):
        salary_range = salary_str.split()
        try:
            salary_range = [int(s) for s in salary_range if s.isdigit()]
            if len(salary_range) == 2:
                return tuple(salary_range)
            elif len(salary_range) == 1:
                return (salary_range[0], salary_range[0])
        except ValueError:
            return (np.nan, np.nan)
    return (np.nan, np.nan)

def safe_literal_eval(s):
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return None

def plot_graph1(title, df):
    plt.figure(figsize=(14, 8))
    plt.rcParams.update({'font.size': FONT_SIZE})  # Adjust as needed
    plt.title(title, fontsize=16)
    plt.xlabel('Salary', fontsize=FONT_SIZE)
    plt.ylabel('Job Position', fontsize=FONT_SIZE)
    plt.barh(df.index, df['Max Salary'], color='lightblue', label='Max Salary')
    plt.barh(df.index, df['Min Salary'], color='blue', label='Min Salary')
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.legend(fontsize=FONT_SIZE)
    plt.gca().invert_yaxis()  # Invert y-axis to display the highest salary at the top
    plt.tight_layout()
    return plt

def plot_graph2(title, df):
    plt.figure(figsize=(10, 6))
    plt.bar(df['Technology'], df['Count'], color='skyblue')
    plt.xlabel('Technology')
    plt.ylabel('Count')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.xticks(fontsize=FONT_SIZE)
    plt.yticks(fontsize=FONT_SIZE)
    plt.tight_layout()
    return plt
