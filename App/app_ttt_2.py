import streamlit as st
import pandas as pd
import re

from app_utils import recommend_technologies, parse_salary_range, \
    predict_salary, \
    safe_literal_eval, plot_graph1, plot_graph2, \
    plot_recommendations


# Page functions
def home():
    left_column, right_column = st.columns([1, 1])

    with left_column:
        st.title("IT Career Recommender")
        st.subheader("Discover common tech pairs in job descriptions. We don't track trends or offer personalization. Let's explore synergies together!")
        if st.button("Try out"):
            st.session_state.page = "recommender"

    with right_column:
        st.image("An office scene.png", use_column_width=True)

def recommender():
    file_path = 'jobData.csv'
    job_data_df = pd.read_csv(file_path, on_bad_lines='skip')
    job_data_df['Used Technologies'] = job_data_df['Used Technologies'].apply(safe_literal_eval)
    expanded_tech_df = pd.json_normalize(job_data_df['Used Technologies'])
    full_df = job_data_df.join(expanded_tech_df)

    st.title("Recommender")
    user_input = st.text_input('Enter your technologies, separated by commas (e.g., Python, Java, SQL)')
    num_recommendations = st.number_input('Enter the number of recommendations you want', min_value=1, max_value=10, value=2)

    if st.button('Get Recommendations'):
        user_skills = [skill.strip() for skill in user_input.split(',')]
        recommendations = recommend_technologies(user_skills, full_df, num_recommendations=int(num_recommendations))
        st.info('Recommendations are derived from common pairings in \
                technologies found in job descriptions up to 2023', icon="ℹ️")

        if len(recommendations) == 0:
            file_path = 'jobData.csv'
            job_data_df = pd.read_csv(file_path, on_bad_lines='skip')

            job_data_df['Used Technologies'] = job_data_df['Used Technologies'].apply(safe_literal_eval)
            tech_count = {}

            for tech_dict in job_data_df['Used Technologies']:
                if isinstance(tech_dict, dict):
                    for tech in tech_dict.keys():
                        tech_count[tech] = tech_count.get(tech, 0) + 1

            tech_count_df = pd.DataFrame(list(tech_count.items()), columns=['Technology', 'Count'])
            tech_count_df = tech_count_df.sort_values(by='Count', ascending=False)
            top_tech_count_df = tech_count_df.head(10)

            st.warning('We are unable to give accurate recommendations, however here are some of the \
                       most popular technologies you might want to consider:', icon="⚠️")
            title = 'Top 10 Technologies by Frequency in Job Data'
            st.subheader(title)
            fig = plot_graph2(title, top_tech_count_df)
        else:
            fig = plot_recommendations('Recommendations', recommendations)
        st.pyplot(fig)

        for tech in recommendations['consequents']:
            tech_encoded = re.sub(r'\s+', '', tech)
            search_link = f"https://www.google.com/search?q={tech_encoded}+tutorial"
            st.markdown(f"- {tech}: [Search for Tutorials]({search_link})")
        
        st.info('Results based on current market trends and user skills. \
                Results based on statistics, consider your interests and goals when choosing technology', icon="ℹ️")


    st.markdown("---")
    
    st.write("Are you satisfied with the recommendations?")

    _, left_column_YES, right_column_NO, _ = st.columns(4)

    with left_column_YES:
        st.button('YES')
    
    with right_column_NO:
        st.button('NO')

    feedback = st.text_area("Is there anything that would increase your trust to this recommendation? Your opinion here:", height=150)

    if st.button('Submit Feedback'):
        st.success("Thank you for your feedback!")

def salary_prediction():
    st.title("Salary Prediction")
    user_input = st.text_input('Enter your technologies, separated by commas (e.g., Python, Java, SQL)')
    
    if st.button('Predict Salary'):
        user_skills = [skill.strip() for skill in user_input.split(',')]
        st.write('Monthly minimum salary that you can expect based on your skills:')
        st.markdown(f'### {predict_salary(user_skills)} zł')
        st.write('Results are based on current market trends.')

def it_trends():
    file_path = 'jobData.csv'
    job_data_df = pd.read_csv(file_path, on_bad_lines='skip')

    st.title("IT Trends")
    
    # Create two columns for the graphs
    col1, col2 = st.columns(2)

    # Display the first graph in the first column
    job_data_df['Min Salary'], job_data_df['Max Salary'] = zip(*job_data_df['Salary'].apply(parse_salary_range))
    salary_range_by_position = job_data_df.groupby('Position')[['Min Salary', 'Max Salary']].mean()
    top_salary_ranges = salary_range_by_position.sort_values(by='Max Salary', ascending=False).head(10)

    with col1:
        title = 'Top 10 Jobs with Salary Ranges'
        st.subheader(title)
        fig1 = plot_graph1(title, top_salary_ranges)
        st.pyplot(fig1)

    # Display the second graph in the second column
    job_data_df['Used Technologies'] = job_data_df['Used Technologies'].apply(safe_literal_eval)
    tech_count = {}

    for tech_dict in job_data_df['Used Technologies']:
        if isinstance(tech_dict, dict):
            for tech in tech_dict.keys():
                tech_count[tech] = tech_count.get(tech, 0) + 1

    tech_count_df = pd.DataFrame(list(tech_count.items()), columns=['Technology', 'Count'])
    tech_count_df = tech_count_df.sort_values(by='Count', ascending=False)
    top_tech_count_df = tech_count_df.head(10)

    with col2:
        title = 'Top 10 Technologies by Frequency in Job Data'
        st.subheader(title)
        fig2 = plot_graph2(title, top_tech_count_df)
        st.pyplot(fig2)

def top_nav():
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])  # Adjust the column ratio as needed
    with col1:
        if st.button("IT Career"):
            st.session_state.page = "home"
    with col2:
        if st.button("Recommender"):
            st.session_state.page = "recommender"
    with col3:
        if st.button("IT Trends"):
            st.session_state.page = "it_trends"
    with col4:
        # Dropdown for language selection
        selected_language = st.selectbox('Select Language', ['English', 'Polish', 'French'], index=0)
        # You can use the selected language to do something like translation or other logic
    st.markdown("---")

def recommender_nav():
    col1, col2 = st.columns([1, 1])  # Adjust the column ratio as needed
    with col1:
        if st.button("Technology Recommender"):
            st.session_state.subpage = "recommender"
    with col2:
        if st.button("Salary Prediction"):
            st.session_state.subpage = "salary_prediction"
    st.markdown("---")

# Main app logic
def main():
    # Initialize the session state
    if 'page' not in st.session_state:
        st.session_state.page = "home"

    top_nav()  # Display the navigation at the top

    # Page display logic
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "recommender":
        recommender_nav()  # Display the second navbar for "Recommender" page
        if 'subpage' not in st.session_state:
            st.session_state.subpage = "recommender"  # Default subpage when on Recommender
        if st.session_state.subpage == "recommender":
            recommender()
        elif st.session_state.subpage == "salary_prediction":
            salary_prediction()
    elif st.session_state.page == "it_trends":
        it_trends()

if __name__ == "__main__":
    main()
