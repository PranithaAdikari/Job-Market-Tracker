import os
import csv
import random
import uuid
from datetime import datetime, timedelta

# Create directories
base_dir = "Job_Market_Skill_Demand_Tracker"
dirs = ["Data", "Documentation", "DAX", "Screenshots"]
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# Generate Dataset
jobs = [
    "Data Analyst", "Data Scientist", "Software Developer", "Full Stack Developer",
    "Backend Developer", "Frontend Developer", "Java Developer", "Python Developer",
    "Machine Learning Engineer", "AI Engineer", "Cloud Engineer", "DevOps Engineer",
    "Cybersecurity Analyst", "Database Administrator", "Business Analyst",
    "Power BI Developer", "UI/UX Designer"
]
companies = [f"Company_{chr(65+i)}{chr(65+j)}" for i in range(26) for j in range(10)]
locations_states = {
    "Hyderabad": "Telangana", "Bangalore": "Karnataka", "Chennai": "Tamil Nadu",
    "Pune": "Maharashtra", "Mumbai": "Maharashtra", "Delhi": "Delhi",
    "Noida": "Uttar Pradesh", "Gurugram": "Haryana", "Kolkata": "West Bengal",
    "Kochi": "Kerala", "Ahmedabad": "Gujarat", "Visakhapatnam": "Andhra Pradesh"
}
industries = ["IT Services", "Finance", "Healthcare", "E-commerce", "EdTech", "FinTech"]
employment_types = ["Full-time", "Contract", "Part-time"]
work_modes = ["On-site", "Hybrid", "Remote"]
company_sizes = ["1-50", "51-200", "201-500", "501-1000", "1000+"]

skills_db = {
    "Python": "Programming", "Java": "Programming", "JavaScript": "Programming",
    "SQL": "Database", "Excel": "Data Tools", "Power BI": "Data Visualization",
    "Tableau": "Data Visualization", "React": "Web Development", "Node.js": "Web Development",
    "HTML": "Web Development", "CSS": "Web Development", "C++": "Programming",
    "C": "Programming", "AWS": "Cloud", "Azure": "Cloud", "Google Cloud": "Cloud",
    "Docker": "DevOps", "Kubernetes": "DevOps", "Git": "Version Control",
    "MongoDB": "Database", "MySQL": "Database", "PostgreSQL": "Database",
    "Machine Learning": "AI/ML", "Deep Learning": "AI/ML", "TensorFlow": "AI/ML",
    "PyTorch": "AI/ML", "NLP": "AI/ML", "Data Analysis": "Analytics",
    "Data Visualization": "Analytics", "Cybersecurity": "Security"
}

job_role_skills = {
    "Data Analyst": ["SQL", "Excel", "Power BI", "Tableau", "Python", "Data Analysis", "Data Visualization"],
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Data Analysis"],
    "Software Developer": ["Java", "Python", "C++", "C", "Git", "SQL"],
    "Full Stack Developer": ["JavaScript", "React", "Node.js", "HTML", "CSS", "MongoDB", "SQL", "Git"],
    "Backend Developer": ["Python", "Java", "Node.js", "SQL", "MySQL", "PostgreSQL", "AWS", "Docker"],
    "Frontend Developer": ["JavaScript", "React", "HTML", "CSS", "Git"],
    "Machine Learning Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "AWS", "Azure"],
    "Cloud Engineer": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Python"],
    "DevOps Engineer": ["AWS", "Docker", "Kubernetes", "Git", "Python", "Azure"],
    "Power BI Developer": ["Power BI", "SQL", "Excel", "Data Visualization", "Data Analysis"],
    "UI/UX Designer": ["HTML", "CSS", "JavaScript", "React"], 
    "Java Developer": ["Java", "SQL", "Git", "MySQL"],
    "Python Developer": ["Python", "SQL", "Git", "PostgreSQL", "AWS"],
    "Cybersecurity Analyst": ["Cybersecurity", "Python", "AWS", "SQL"],
    "Database Administrator": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "AWS"],
    "Business Analyst": ["Excel", "SQL", "Data Analysis", "Power BI"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP"]
}

data = []
start_date = datetime.now() - timedelta(days=365)

for _ in range(1200): # ~1200 unique jobs
    job_id = f"JOB-{uuid.uuid4().hex[:8].upper()}"
    job_title = random.choice(jobs)
    company = random.choice(companies)
    loc = random.choice(list(locations_states.keys()))
    state = locations_states[loc]
    industry = random.choice(industries)
    
    exp_min = random.randint(0, 8)
    exp_max = exp_min + random.randint(2, 5)
    
    if exp_min == 0:
        exp_lvl = "Entry Level"
    elif exp_min <= 3:
        exp_lvl = "Junior"
    elif exp_min <= 7:
        exp_lvl = "Mid Level"
    else:
        exp_lvl = "Senior"
        
    emp_type = random.choice(employment_types)
    work_mode = random.choice(work_modes)
    remote = "Yes" if work_mode == "Remote" else "No"
    
    base_sal = 300000 + (exp_min * 150000)
    sal_min = base_sal + random.randint(-50000, 100000)
    sal_max = sal_min + random.randint(100000, 500000)
    avg_sal = (sal_min + sal_max) / 2
    
    edu = random.choice(["Bachelor's", "Master's", "PhD", "Any Graduate"])
    posted_date = start_date + timedelta(days=random.randint(0, 365))
    app_count = random.randint(5, 500)
    job_desc = f"Looking for a {job_title} at {company}."
    comp_size = random.choice(company_sizes)
    
    job_skills_pool = job_role_skills.get(job_title, list(skills_db.keys()))
    num_skills = random.randint(3, 6)
    job_skills = random.sample(job_skills_pool, min(num_skills, len(job_skills_pool)))
    
    for skill in job_skills:
        skill_cat = skills_db[skill]
        row = {
            "Job_ID": job_id,
            "Job_Title": job_title,
            "Company": company,
            "Location": loc,
            "State": state,
            "Industry": industry,
            "Experience_Min": exp_min,
            "Experience_Max": exp_max,
            "Experience_Level": exp_lvl,
            "Employment_Type": emp_type,
            "Work_Mode": work_mode,
            "Salary_Min": sal_min,
            "Salary_Max": sal_max,
            "Average_Salary": avg_sal,
            "Skill": skill,
            "Skill_Category": skill_cat,
            "Education": edu,
            "Posted_Date": posted_date.strftime("%Y-%m-%d"),
            "Application_Count": app_count,
            "Job_Description": job_desc,
            "Remote": remote,
            "Company_Size": comp_size
        }
        
        # Introduce some missing values realistically
        # 2% of salaries missing
        # 5% missing Application Count
        if random.random() < 0.02:
            row["Salary_Min"] = ""
            
        if random.random() < 0.05:
            row["Application_Count"] = ""
            
        data.append(row)

csv_path = os.path.join(base_dir, 'Data', 'job_market_data.csv')
fieldnames = [
    "Job_ID", "Job_Title", "Company", "Location", "State", "Industry", 
    "Experience_Min", "Experience_Max", "Experience_Level", "Employment_Type", 
    "Work_Mode", "Salary_Min", "Salary_Max", "Average_Salary", "Skill", 
    "Skill_Category", "Education", "Posted_Date", "Application_Count", 
    "Job_Description", "Remote", "Company_Size"
]

with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"Generated {len(data)} rows and saved to {csv_path}")
