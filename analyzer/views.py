from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MatchRequestSerializer, MatchResponseSerializer
from linkedin_scraper import Person, actions
from selenium import webdriver
import re
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import cohere
import logging
from django.shortcuts import render


def index(request):
    return render(request, "calculate_match.html")


def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text.lower())  # Remove punctuation and convert to lowercase
    tokens = text.split()
    tokens = [word for word in tokens if word not in ENGLISH_STOP_WORDS]  # Remove stopwords
    return tokens


def extract_keywords(text):
    tokens = preprocess_text(text)
    return Counter(tokens)


def calculate_match_score(profile_keywords, jd_keywords, weights):
    total_score = 0
    total_possible_score = 0

    for section, profile_section_keywords in profile_keywords.items():
        matches = sum((jd_keywords & profile_section_keywords).values())
        total_score += matches * weights[section]
        total_possible_score += len(profile_section_keywords) * weights[section]

    return total_score / total_possible_score if total_possible_score > 0 else 0


def get_profile_data(linkedin_url, email, password):
    driver = webdriver.Chrome()
    try:
        actions.login(driver, email, password)
        person = Person(linkedin_url, driver=driver)
        profile_data = {
            "name": person.name,
            "about": person.about,
            "experience": " ".join(
                [f"{exp.position_title} at {exp.institution_name} ({exp.from_date} - {exp.to_date})" for exp in person.experiences]
            ) if isinstance(person.experiences, list) else "",
            "education": " ".join(
                [f"{edu.degree} from {edu.institution_name} ({edu.from_date} - {edu.to_date})" for edu in person.educations]
            ) if isinstance(person.educations, list) else "",
            "interest": " ".join(person.interests) if isinstance(person.interests, list) else "",
            "accomplishment": " ".join(person.accomplishments) if isinstance(person.accomplishments, list) else "",
        }
        return profile_data
    finally:
        driver.quit()


class AdvancedCulturalFitAnalyzer:
    def __init__(self, api_key: str, company_values: list):
        self.client = cohere.Client(api_key)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.company_values = company_values

        # Predefined evaluation criteria
        self.evaluation_criteria = [
            "Leadership Potential",
            "Innovation Mindset",
            "Collaborative Skills",
            "Adaptability",
            "Cultural Alignment",
            "Problem-Solving Approach",
            "Ethical Standards",
        ]

    def generate_comprehensive_prompt(self, candidate_data):
        profile_sections = "\n".join([
            f"{key.upper()}: {str(value)}"
            for key, value in candidate_data.items()
            if value and str(value).strip()
        ])

        return f"""
        Advanced Cultural Fit and Potential Analysis

        Company Core Values: {' | '.join(self.company_values)}

        Candidate Comprehensive Profile:
        {profile_sections}

        Detailed Analysis Requirements:
        1. Comprehensive Cultural Alignment Score (0-100)
        2. Depth Analysis for Each Evaluation Criterion:
           {', '.join(self.evaluation_criteria)}
        3. Predictive Team Integration Potential
        4. Skill-Value Synergy Assessment
        5. Potential Growth Trajectory
        6. Unique Value Proposition

        Provide a nuanced, multi-dimensional, data-driven assessment with:
        - Specific quantitative scoring
        - Qualitative insights
        - Actionable recommendations
        """

    def analyze_candidate(self, candidate_data):
        try:
            prompt = self.generate_comprehensive_prompt(candidate_data)
            response = self.client.generate(
                model='command-xlarge-nightly',
                prompt=prompt,
                max_tokens=1000,
                temperature=0.3,
                k=0,
                p=0.75
            )
            analysis_text = response.generations[0].text.strip()
            alignment_score = self._extract_alignment_score(analysis_text)
            detailed_evaluation = self._parse_detailed_evaluation(analysis_text)
            return {
                'overall_alignment_score': alignment_score,
                'detailed_evaluation': detailed_evaluation,
                'full_analysis': analysis_text
            }
        except Exception as e:
            self.logger.error(f"Candidate Analysis Error: {e}")
            return {
                'error': str(e)
            }

    def _extract_alignment_score(self, analysis_text):
        match = re.search(r'Cultural Alignment Score[: ]*(\d+)', analysis_text, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    def _parse_detailed_evaluation(self, analysis_text):
        evaluation = {}
        for criterion in self.evaluation_criteria:
            pattern = rf'{criterion}[:\s]*(.+?)(?=\n\n|$)'
            match = re.search(pattern, analysis_text, re.IGNORECASE | re.DOTALL)
            if match:
                evaluation[criterion] = match.group(1).strip()
        return evaluation


# API View to calculate match score and cultural fit analysis
class MatchScoreAndCulturalFitAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate input data
        serializer = MatchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

        linkedin_url = serializer.validated_data["linkedin_url"]
        job_description = serializer.validated_data["job_description"]

        email = settings.EMAIL
        password = settings.PASSWORD
        api_key = settings.COHERE_API_KEY

        # Extract company values from the request payload
        company_values = request.data.get("company_values", "").split("\n")
        company_values = [value.strip() for value in company_values if value.strip()]

        if not company_values:
            return Response({"error": "Company values cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch LinkedIn profile data
        try:
            profile_data = get_profile_data(linkedin_url, email, password)
        except Exception as e:
            return Response(
                {"error": f"Error fetching LinkedIn profile: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Process job description and calculate match score
        jd_keywords = extract_keywords(job_description)
        profile_keywords = {
            "about": extract_keywords(profile_data["about"]),
            "experience": extract_keywords(profile_data["experience"]),
            "education": extract_keywords(profile_data["education"]),
            "interest": extract_keywords(profile_data["interest"]),
            "accomplishment": extract_keywords(profile_data["accomplishment"]),
        }
        section_weights = {"about": 2, "experience": 3, "education": 2, "interest": 1, "accomplishment": 1}
        match_score = calculate_match_score(profile_keywords, jd_keywords, section_weights)

        # Cultural fit analysis
        analyzer = AdvancedCulturalFitAnalyzer(api_key=api_key, company_values=company_values)
        cultural_analysis = analyzer.analyze_candidate(profile_data)

        # Serialize the response data
        response_data = {
            "name": profile_data["name"],
            "match_score": f"{match_score * 100:.2f}",
            "cultural_fit_analysis": cultural_analysis,
        }
        response_serializer = MatchResponseSerializer(response_data)

        return render(request, "analysis_result.html", response_data)

