![Django](https://img.shields.io/badge/Django-5.x-green)  ![Python](https://img.shields.io/badge/Python-3.9%2B-blue)  ![Selenium](https://img.shields.io/badge/Selenium-4.x-orange)  ![Cohere API](https://img.shields.io/badge/Cohere%20API-AI%20Powered-blueviolet)   ![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)  ![Status](https://img.shields.io/badge/Status-In%20Development-blue)  


# RightSwipe - LinkedIn Profile & Job Match Analyzer

A one-stop tool for HR that evaluates a candidate's LinkedIn profile against a job description, calculating a match score and providing a detailed cultural fit analysis based on the company's core cultural values. The application uses advanced text processing techniques and AI-powered insights to assess alignment with company values.

---

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)

---

## Features

- **LinkedIn Profile Parsing**: Automatically fetches data (about, experience, education, interests, accomplishments) from a LinkedIn profile.
- **Job Description Analysis**: Extracts keywords and evaluates match score based on the job description.
- **Cultural Fit Analysis**: Uses AI to provide a comprehensive evaluation based on company values and predefined criteria.
- **Match Score Calculation**: Generates a percentage score indicating how well the candidate fits the job requirements.
- **User-Friendly Interface**: Input forms and result pages are cleanly designed for an intuitive experience.

---

## Demo

### Home Page
- A simple form where users can input:
  - LinkedIn profile URL
  - Job description
  - Company values

### Results Page
- Displays:
  - Candidate's name
  - Match score (percentage)
  - Cultural fit analysis with:
    - Overall alignment score
    - Evaluation of criteria such as leadership, innovation, collaboration, etc.
    - Full textual analysis

---

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/linkedin-job-match-analyzer.git
   cd linkedin-job-match-analyzer
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   Create a `.env` file in the project directory and add the following:
   ```env
   EMAIL=your_linkedin_email
   PASSWORD=your_linkedin_password
   COHERE_API_KEY=your_cohere_api_key
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Usage

1. Enter the **LinkedIn Profile URL**, **Job Description**, and **Company Values** on the home page form.
2. Submit the form to calculate the match score and cultural fit analysis.
3. View the detailed results on the analysis page.

---

## Technologies Used

- **Backend**:
  - Django
  - Django REST Framework
- **Web Scraping**:
  - [LinkedIn Scraper]([https://github.com/joeyism/linkedin_scraper/tree/master])
  - Selenium
- **AI Analysis**:
  - [Cohere API](https://cohere.ai)
- **Frontend**:
  - HTML
  - CSS (with modern frameworks for styling)
- **Database**:
  - SQLite (default Django database, can be replaced with PostgreSQL)
- **Others**:
  - Scikit-learn (for keyword extraction)
  - Collections (for text preprocessing)

---

## Project Structure

```
linkedin-job-match-analyzer/
├── linkedin_scraper/       # Handles LinkedIn profile scraping
├── templates/              # HTML templates for the UI
│   ├── calculate_match.html  # Input form page
│   └── analysis_result.html  # Results page
├── static/                 # Static assets (CSS, JS, images)
├── match/                  # Main app for processing match and analysis
│   ├── views.py            # View logic for rendering pages and processing input
│   ├── serializers.py      # API serializers for validating input/output
│   ├── urls.py             # Routes for the app
├── settings.py             # Django settings file
├── requirements.txt        # Python dependencies
├── manage.py               # Django's management script
└── README.md               # Project documentation
```

---

## Future Improvements

- Using React instead of Plain HTML, CSS for better User Experience
- Instead of web-scraping utilize Linkedin API for better results.
- Add OAuth-based LinkedIn authentication to avoid manual email/password entry.
- Implement caching for faster LinkedIn profile scraping.
- Provide a downloadable PDF of the analysis results.
- Support for additional profile sources (e.g., GitHub, personal websites).
