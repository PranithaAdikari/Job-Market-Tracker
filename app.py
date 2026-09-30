import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Set clean default theme for all charts
pio.templates.default = "plotly_white"

st.set_page_config(page_title="Job Market Skill Demand Tracker", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Data/job_market_data.csv")
    df['Posted_Date'] = pd.to_datetime(df['Posted_Date'])
    df['Month'] = df['Posted_Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

st.title("Job Market Skill Demand Tracker")

# Navigation
page = st.sidebar.radio("Navigation", ["Overview", "Skill Demand Analysis", "Job Role & Salary Analysis", "Skill & Career Insights"])

if page == "Overview":
    st.header("Project Introduction")
    st.write("The Job Market Skill Demand Tracker analyzes job-market data to identify the skills that are most frequently requested by employers. It helps users understand current skill demand, popular job roles, salary trends, hiring locations, and experience requirements.")
    
    st.subheader("Objectives")
    st.markdown("- Identify top skills in demand.\n- Understand salary trends across experience levels.\n- Analyze job roles and hiring locations.\n- Empower job seekers with actionable insights.")
    
elif page == "Skill Demand Analysis":
    st.header("Skill Demand Analysis")
    
    # KPIs
    top_skill = df['Skill'].value_counts().idxmax()
    total_skills = df['Skill'].nunique()
    total_jobs = df['Job_ID'].nunique()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Top Skill", top_skill)
    col2.metric("Total Unique Skills", total_skills)
    col3.metric("Total Jobs", total_jobs)
    
    # Slicers
    st.sidebar.header("Filters")
    categories = st.sidebar.multiselect("Skill Category", df['Skill_Category'].unique(), default=df['Skill_Category'].unique()[:2])
    locations = st.sidebar.multiselect("Location", df['Location'].unique(), default=df['Location'].unique()[:3])
    
    filtered_df = df[(df['Skill_Category'].isin(categories)) & (df['Location'].isin(locations))]
    
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        
        # Visual 1
        top_10 = filtered_df['Skill'].value_counts().nlargest(10).reset_index()
        top_10.columns = ['Skill', 'Demand']
        fig1 = px.bar(top_10, x='Skill', y='Demand', title='Top 10 Demanded Skills')
        col1.plotly_chart(fig1, use_container_width=True)
        
        # Visual 2
        category_counts = filtered_df['Skill_Category'].value_counts().reset_index()
        category_counts.columns = ['Skill Category', 'Demand']
        fig2 = px.pie(category_counts, names='Skill Category', values='Demand', hole=0.4, title='Skill Demand by Category')
        col2.plotly_chart(fig2, use_container_width=True)
        
        # Visual 3
        avg_sal = filtered_df.groupby('Skill')['Average_Salary'].mean().nlargest(10).reset_index()
        fig3 = px.bar(avg_sal, x='Skill', y='Average_Salary', title='Top 10 Paying Skills')
        col1.plotly_chart(fig3, use_container_width=True)
        
        # Visual 4
        trend = filtered_df.groupby(['Month']).size().reset_index(name='Demand')
        fig4 = px.line(trend, x='Month', y='Demand', title='Skill Demand Trend')
        col2.plotly_chart(fig4, use_container_width=True)
        
        # Table
        st.subheader("Summary Table")
        summary = filtered_df.groupby('Skill').agg(
            Job_Count=('Job_ID', 'nunique'),
            Average_Salary=('Average_Salary', 'mean')
        ).reset_index()
        st.dataframe(summary)
    else:
        st.warning("No data found for the selected filters.")

elif page == "Job Role & Salary Analysis":
    st.header("Job Role & Salary Analysis")
    
    jobs = st.sidebar.multiselect("Job Title", df['Job_Title'].unique(), default=df['Job_Title'].unique()[:5])
    
    if jobs:
        filtered_df = df[df['Job_Title'].isin(jobs)]
        
        col1, col2 = st.columns(2)
        
        # V1
        avg_sal_job = filtered_df.groupby('Job_Title')['Average_Salary'].mean().reset_index()
        fig1 = px.bar(avg_sal_job, x='Job_Title', y='Average_Salary', title='Average Salary by Job Role')
        col1.plotly_chart(fig1, use_container_width=True)
        
        # V2
        exp_sal = filtered_df.groupby('Experience_Level')['Average_Salary'].mean().reset_index()
        fig2 = px.bar(exp_sal, x='Experience_Level', y='Average_Salary', title='Salary by Experience Level')
        col2.plotly_chart(fig2, use_container_width=True)
        
        # V3
        loc_jobs = filtered_df.groupby('Location')['Job_ID'].nunique().reset_index(name='Total Jobs')
        fig3 = px.bar(loc_jobs, x='Location', y='Total Jobs', title='Top Hiring Locations')
        col1.plotly_chart(fig3, use_container_width=True)
        
        # Table
        st.subheader("Salary Range")
        sal_range = filtered_df.groupby('Job_Title').agg(
            Min_Salary=('Salary_Min', 'min'),
            Max_Salary=('Salary_Max', 'max'),
            Average_Salary=('Average_Salary', 'mean')
        ).reset_index()
        st.dataframe(sal_range)

elif page == "Skill & Career Insights":
    st.header("Skill & Career Insights")
    
    jobs = st.sidebar.multiselect("Job Title", df['Job_Title'].unique(), default=df['Job_Title'].unique()[:3])
    locs = st.sidebar.multiselect("Location", df['Location'].unique(), default=df['Location'].unique()[:3])
    exps = st.sidebar.multiselect("Experience Level", df['Experience_Level'].unique(), default=df['Experience_Level'].unique())
    
    filtered_df = df[(df['Job_Title'].isin(jobs)) & (df['Location'].isin(locs)) & (df['Experience_Level'].isin(exps))]
    
    if not filtered_df.empty:
        # Smart Narrative
        top_skill = filtered_df['Skill'].value_counts().idxmax() if not filtered_df['Skill'].empty else "N/A"
        job_text = ", ".join(jobs) if jobs else "various positions"
        st.info(f"💡 **Insight:** {top_skill} is one of the most frequently requested skills for {job_text}.")
        
        col1, col2 = st.columns(2)
        
        skill_counts = filtered_df['Skill'].value_counts().reset_index()
        skill_counts.columns = ['Skill', 'Demand']
        fig1 = px.treemap(skill_counts, path=['Skill'], values='Demand', title='Required Skills Treemap')
        col1.plotly_chart(fig1, use_container_width=True)
        
        fig4 = px.scatter(filtered_df, x='Experience_Min', y='Average_Salary', color='Job_Title', title='Experience vs Salary')
        col2.plotly_chart(fig4, use_container_width=True)
