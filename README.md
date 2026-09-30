# Job Market Skill Demand Tracker

## 1. Project Title
Job Market Skill Demand Tracker

## 2. Project Objective
To create a comprehensive, interactive Power BI dashboard that analyzes current job-market demand, identifies the most requested technical skills, compares job roles and locations, and evaluates salary and experience requirements in the Indian IT sector.

## 3. Problem Statement
Job seekers and career switchers often lack clear visibility into which technical skills are currently in highest demand, how compensation varies across locations, and the exact requirements for different job roles. This project aims to bridge that information gap by providing a data-driven tool to analyze real-world hiring trends, helping users make informed career and upskilling decisions.

## 4. Dataset Description
- **Source File**: `Data/job_market_data.csv`
- **Volume**: Over 1,000 unique job postings expanded into ~5,000 rows (job-skill combinations).
- **Domain**: Indian IT Job Market.
- **Key Columns**: Job ID, Title, Company, Location, Experience Level, Employment Type, Work Mode, Min/Max/Average Salary, Skill, Skill Category, Education, Posted Date.
- **Structure**: The data has one row per skill per job, allowing detailed analysis of skill demand. 

## 5. Data Cleaning Process
The raw data is processed using Power Query before building the dashboards:
- Removed empty/null values for critical fields or replaced them with "Unknown".
- Parsed dates and ensured `Posted_Date` is formatted correctly as a Date type.
- Handled missing numeric values (e.g., Application Count, Salaries) using average interpolation or replacing with 0.
- Cleaned Text (Trimmed whitespaces, capitalized Skill and Job Title names).

## 6. Data Model
A Star Schema is implemented for optimal performance:
- **Fact Table**: `FactJobs` (Contains quantitative data: Salaries, Application Counts, Job IDs).
- **Dimension Tables**: 
  - `DimJob` (Job_Title, Industry, Experience_Level)
  - `DimCompany` (Company, Company_Size)
  - `DimLocation` (Location, State, Work_Mode, Remote)
  - `DimSkill` (Skill, Skill_Category)
  - `DimDate` (Standard Date table linked to Posted_Date)
- **Relationships**: 1-to-Many relationships from all Dimensions to `FactJobs`.

## 7. DAX Measures
A robust set of DAX measures was created to support the visual analytics. These are stored in `DAX/dax_measures.txt`. Categories include:
- **Job Metrics**: Total Jobs, Total Companies, Average Salary
- **Skill Metrics**: Skill Demand, Top Skill, Skill Demand %
- **Trend Metrics**: Monthly Job Growth %, Skill Demand Growth %

## 8. Dashboard Descriptions
1. **Project Introduction**: A clean, professional cover page outlining the project's purpose and objectives without cluttering the screen with charts.
2. **Skill Demand Analysis**: Dedicated to understanding the top required skills, category breakdowns, and dynamic filtering to track a specific skill's prevalence.
3. **Job Role & Salary Analysis**: Focuses on compensation trends. Allows a user to select a job role (e.g., "Data Analyst") and immediately see the average salary, required experience, and top locations.
4. **Skill & Career Insights**: A highly interactive career-planning page. Users select a Role, Location, and Experience level to receive tailored insights (Top Skills, Salary, Job Counts).

## 9. Key Insights
- **Python and SQL** dominate the market for Data and Backend roles.
- **Remote** work mode impacts salary variance.
- **Senior level** roles command exponentially higher average salaries in hubs like Bangalore and Hyderabad.
- **Cloud (AWS/Azure)** and **DevOps** skills show significant salary premiums compared to traditional programming skills.

## 10. Tools Used
- **Power BI Desktop**: For data modeling, DAX, and visualization.
- **Power Query**: For ETL (Extract, Transform, Load) and data cleaning.
- **DAX**: For advanced calculations and dynamic metrics.
- **Python**: For generating the realistic synthetic dataset.

## 11. Future Improvements
- Integrate live web scraping (e.g., from LinkedIn or Indeed) to keep data constantly updated.
- Implement Machine Learning integration to forecast future skill trends.
- Add a "Resume Matcher" feature to compare user skills against top job demands.
