import os
import json
import logging
import google.generativeai as genai
from django.conf import settings
from quiz.models import Quiz, Question

logger = logging.getLogger(__name__)

# Try to load API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        config_path = os.path.join(settings.BASE_DIR, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                api_key = config_data.get("GEMINI_API_KEY")
    except Exception:
        pass

if api_key:
    genai.configure(api_key=api_key)

LEVEL_DESCRIPTIONS = {
    'BEGINNER': "Basic recall and simple comprehension. Simple language. Test whether the student remembers key facts and definitions from the material.",
    'INTERMEDIATE': "Application and analysis. Require the student to apply concepts, compare ideas, and explain relationships — not just recall.",
    'ADVANCED': "Evaluation, synthesis, and critical thinking. Ask about edge cases, implications, real-world applications, and nuanced understanding requiring deep mastery."
}

def generate_quiz_for_material(material, level):
    if not api_key:
        logger.error("GEMINI_API_KEY is not set. Cannot generate quiz.")
        return False
        
    prompt = f"""You are an expert educational quiz generator.

Generate exactly 10 multiple-choice questions from the study material below.

Subject: {material.subject.name}
Topic / Title: {material.title}
Difficulty Level: {level}
Level Guidance: {LEVEL_DESCRIPTIONS[level]}

Study Material:
\"\"\"
{material.content}
\"\"\"

Rules:
- Each question must have exactly 4 answer options (A, B, C, D)
- Only one option is correct per question
- Questions must only be based on the provided material above
- Include a brief explanation for why the correct answer is right
- correctAnswer is 0-indexed: 0 = A, 1 = B, 2 = C, 3 = D

Return ONLY a valid JSON array. No markdown formatting, no code fences, no preamble, no extra text.

[
  {{
    "question": "...",
    "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
    "correctAnswer": 2,
    "explanation": "..."
  }}
]"""

    try:
        model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})
        response = model.generate_content(prompt)
        
        raw_text = response.text.strip()
        
        # Strip markdown codes if still present
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        json_data = json.loads(raw_text.strip())
        
        # Cleanup any existing quiz for this level/material
        Quiz.objects.filter(material=material, level=level).delete()
        
        quiz = Quiz.objects.create(material=material, level=level)
        
        for q_data in json_data:
            Question.objects.create(
                quiz=quiz,
                question_text=q_data['question'],
                option_a=q_data['options'][0],
                option_b=q_data['options'][1],
                option_c=q_data['options'][2],
                option_d=q_data['options'][3],
                correct_index=q_data['correctAnswer'],
                explanation=q_data.get('explanation', '')
            )
            
        return True
        
    except Exception as e:
        logger.error(f"Quiz generation failed for {material.title} ({level}): str({e})")
        return False

def generate_all_levels(material):
    # Generates three quizzes for the 3 levels iteratively
    for level in ['BEGINNER', 'INTERMEDIATE', 'ADVANCED']:
        generate_quiz_for_material(material, level)
