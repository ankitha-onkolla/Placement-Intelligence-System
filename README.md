
# Placement Intelligence System (PlacementIQ)

## Project Overview
Placement Intelligence System is a web-based application that analyses student resumes and identifies skills required for different job roles.

It helps students understand their skill gaps, predict placement readiness, receive job recommendations, and follow a learning roadmap.

## Objectives
- Analyse student resumes.
- Extract technical skills automatically.
- Calculate job skill-match percentage.
- Identify missing skills.
- Predict placement readiness.
- Generate a skill development roadmap.
- Recommend suitable job roles.

## Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Testing
- Pytest

### DevOps
- Git
- GitHub
- Jenkins

## Main Features

1. Resume Upload (PDF and DOCX)
2. Automatic Skill Extraction
3. Job Skill Match Analysis
4. Placement Readiness Prediction
5. Missing Skills Identification
6. Skill Development Roadmap
7. Job Role Recommendations

## Supported Job Roles
- Python Developer
- Data Analyst
- Web Developer
- Data Scientist

## Project Structure

```text
Placement-Intelligence-System/
│
├── app.py
├── templates/
│   └── dashboard.html
├── uploads/
├── tests/
│   └── test_app.py
├── Jenkinsfile
├── requirements.txt
└── README.md
```

## How to Run the Project

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Flask Application

```bash
python app.py
```

### Step 3: Open in Browser

```text
http://127.0.0.1:5000
```

### Step 4: Run Automated Tests

```bash
python -m pytest tests -v
```

## Jenkins Integration

This project uses Jenkins for Continuous Integration (CI).

Pipeline activities:
1. Download source code from GitHub.
2. Install project dependencies.
3. Execute automated tests using Pytest.
4. Display build results.

**Latest Test Result:** 7 Tests Passed

**Jenkins Build Status:** SUCCESS

## Expected Output

The application generates:
- Resume skill analysis report.
- Job skill-match percentage.
- Placement readiness status.
- Missing skills and learning recommendations.
- Skill development roadmap.
- Recommended job roles.

## Future Enhancements
- Machine Learning-based placement prediction.
- Student and recruiter login.
- Placement statistics dashboard.
- Real-time job recommendations.
- Advanced resume analysis.

## Important Note
This is a rule-based educational prototype. Placement readiness is calculated using predefined skill matching rules. It is not a trained machine learning placement model and does not guarantee employment.

## Developed By
**Onkolla Ankitha**

B.Tech - Computer Science and Engineering (Data Science)
