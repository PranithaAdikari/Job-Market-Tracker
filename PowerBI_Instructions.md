# Power BI Implementation Guide: Job Market Skill Demand Tracker

Follow these step-by-step instructions to build the Power BI `.pbix` file from the provided CSV dataset.

## PART 1: Importing and Transforming Data (Power Query)

1. Open Power BI Desktop.
2. Click **Get Data** > **Text/CSV**.
3. Select `Job_Market_Skill_Demand_Tracker/Data/job_market_data.csv`.
4. Click **Transform Data** to open Power Query Editor.

### Data Cleaning Steps
1. **Handle Missing Values**: 
   - Right-click the `Salary_Min` column > Replace Values > `null` (or blank) to `0`. Repeat for `Salary_Max`, `Average_Salary`, and `Application_Count`.
2. **Correct Data Types**:
   - Ensure `Average_Salary`, `Salary_Min`, `Salary_Max`, `Application_Count`, `Experience_Min`, `Experience_Max` are set to **Whole Number**.
   - Ensure `Posted_Date` is set to **Date**.
   - Ensure all other categorical columns are set to **Text**.
3. **Remove Duplicates (If Any)**:
   - It is important to understand that in this dataset, a single `Job_ID` will appear on multiple rows if that job requires multiple skills (e.g., one row for Python, another for SQL). 
   - Therefore, **do NOT** simply select the `Job_ID` column and remove duplicates, as that will accidentally delete valuable skill data.
   - Instead, we only want to remove identical, full-row duplicates. To do this:
     - Click anywhere inside the data preview table.
     - Press `Ctrl + A` on your keyboard to select all columns simultaneously (the headers will highlight).
     - In the Home tab on the ribbon, click **Remove Rows** > **Remove Duplicates** (or right-click any column header and select Remove Duplicates). This guarantees only exact 100% identical rows are dropped.

### Creating the Star Schema Models
We will create dimension tables by referencing the main query.
1. Right-click the `job_market_data` query and rename it to `FactJobs`.
2. **Create DimJob**:
   - Right-click `FactJobs` > **Reference**. Rename to `DimJob`.
   - Select `Job_Title`, `Industry`, `Experience_Level`, `Employment_Type`.
   - Right-click the column headers > **Remove Other Columns**.
   - Select all remaining columns > **Remove Duplicates**. Add an Index Column (Job_ID_FK).
3. **Create DimSkill**:
   - Right-click `FactJobs` > **Reference**. Rename to `DimSkill`.
   - Select `Skill`, `Skill_Category`. Remove Other Columns. Remove Duplicates.
4. **Create DimLocation**:
   - Reference `FactJobs` > Rename to `DimLocation`.
   - Select `Location`, `State`. Remove Other Columns. Remove Duplicates.
5. **Create DimCompany**:
   - Reference `FactJobs` > Rename to `DimCompany`.
   - Select `Company`, `Company_Size`. Remove Other Columns. Remove Duplicates.
6. **Create DimDate**:
   - Create a blank query and generate a Date table covering the min and max `Posted_Date`. 
   - (Alternatively, you can just use Power BI's Auto Date/Time, or write a DAX Date table later).
7. **Apply & Close**: Click **Close & Apply**.

## PART 2: Data Modeling
1. Go to the **Model View** in Power BI.
2. Create relationships by dragging and dropping:
   - `DimJob[Job_Title]` to `FactJobs[Job_Title]` (1 to Many).
   - `DimSkill[Skill]` to `FactJobs[Skill]` (1 to Many).
   - `DimLocation[Location]` to `FactJobs[Location]` (1 to Many).
   - `DimCompany[Company]` to `FactJobs[Company]` (1 to Many).
3. Ensure all relationships are Active and Single cross-filter direction (except where specific DAX requires Both).

## PART 3: DAX Measures
1. Go to the **Data View** or **Report View**.
2. Click **New Measure** and copy-paste each formula from `DAX/dax_measures.txt`.
3. Put all measures into a dedicated Measure Table (Create Table > `_Measures = { BLANK() }`) for a clean layout.

## PART 4: Dashboard Construction

*Note: Use a light background (e.g., `#F3F4F6`), professional blue/neutral palettes, and rounded corners for visuals.*

### Page 1: Project Introduction
- **Visuals**: No charts or data visuals.
- **Text Box 1 (Title)**: "JOB MARKET SKILL DEMAND TRACKER" (Large, Bold, Blue).
- **Text Box 2 (Purpose)**: 
  *The Job Market Skill Demand Tracker analyzes job-market data to identify the skills that are most frequently requested by employers. It helps users understand current skill demand, popular job roles, salary trends, hiring locations, and experience requirements...*
- **Text Box 3 (Objectives)**: Bullet list of project objectives.
- **Buttons**: Create a navigation menu at the top or left (Overview | Skills | Jobs & Salary | Career Insights) using blank Buttons with Action = Page Navigation.

### Page 2: Skill Demand Analysis
- **KPI Cards**: Top Skill, Total Skills, Total Jobs.
- **Visual 1 (Top 10 Demanded Skills)**: Bar Chart. Axis = `DimSkill[Skill]`, Values = `[Skill Demand]`. Filter Top N = 10.
- **Visual 2 (Skill Demand by Category)**: Donut Chart. Legend = `DimSkill[Skill_Category]`, Values = `[Skill Demand]`.
- **Visual 3 (Average Salary by Skill)**: Column Chart. Axis = `DimSkill[Skill]`, Values = `[Average Salary]`.
- **Visual 4 (Skill Demand Trend)**: Line Chart. Axis = `DimDate[Month]`, Values = `[Skill Demand]`.
- **Visual 5 (Summary Table)**: Matrix/Table. Columns: `Skill`, `Job Count` (Total Jobs measure), `Demand %`, `Average Salary`.
- **Slicers**: `Skill Category`, `Location`.

### Page 3: Job Role & Salary Analysis
- **Slicer**: `DimJob[Job_Title]`. (Set to Dropdown).
- **Visual 1 (Average Salary by Job Role)**: Bar Chart. Axis = `DimJob[Job_Title]`, Values = `[Average Salary]`.
- **Visual 2 (Salary by Experience Level)**: Column Chart. Axis = `DimJob[Experience_Level]`, Values = `[Average Salary]`.
- **Visual 3 (Top Hiring Locations)**: Map or Filled Map. Location = entire dashboards
`DimLocation[Location]`, Size/Bubble = `[Total Jobs]`.
- **Visual 4 (Top Skills for Role)**: Bar Chart. Axis = `DimSkill[Skill]`, Values = `[Skill Demand]`.
- **Visual 5 (Salary Range)**: Table. Columns: `Job Title`, `Min Salary`, `Max Salary`, `Average Salary`.

### Page 4: Skill & Career Insights
- **Slicers**: `DimJob[Job_Title]`, `DimLocation[Location]`, `DimJob[Experience_Level]`.
- **Visual 1 (Required Skills)**: Treemap. Category = `DimSkill[Skill]`, Values = `[Skill Demand]`.
- **Visual 2 (Location Demand)**: Bar Chart. Axis = `DimLocation[Location]`, Values = `[Total Jobs]`.
- **Visual 3 (Dynamic Insight Text)**: Use the "Smart Narrative" visual or a DAX measure returning text like: 
  `[Top Skill] & " is one of the most frequently requested skills for " & SELECTEDVALUE(DimJob[Job_Title], "various positions") & "."`
- **Visual 4 (Experience vs Salary Scatter)**: Scatter Chart. X-Axis = `[Experience_Min]`, Y-Axis = `[Average Salary]`, Details = `DimJob[Job_Title]`.

## PART 5: Finishing Touches
- Sync slicers where appropriate.
- Configure Tooltips on all charts for better user experience.
- Ensure cross-filtering works intuitively.
- Add a "Reset Filters" button using Bookmarks.
