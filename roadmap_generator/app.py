from flask import Blueprint, render_template, request
import os
import json

from roadmap_generator.roadmap_data import career_roadmaps, career_skills
from roadmap_generator.ai_text_generator import generate_ai_text
from roadmap_generator.weekly_plan_generator import (
    generate_weekly_plan,
    generate_monthly_summaries,
    generate_skill_confidence_change
)
from roadmap_generator.final_verdict_generator import generate_final_verdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

roadmap_bp = Blueprint(
    "roadmap",
    __name__,
    url_prefix="/roadmap",
    template_folder="templates",
    static_folder="static"
)

@roadmap_bp.route("/")
def index():
    # looks for templates/roadmap/index.html
    return render_template(
        "roadmap/index.html",
        careers=career_skills.keys(),
        career_skills=json.dumps(career_skills)
    )

@roadmap_bp.route("/generate", methods=["POST"])
def generate():
    career = request.form["career"]
    skills = career_skills[career]

    user_scores = {}
    total = 0
    for key in skills:
        score = int(request.form.get(f"skill_{key}", 5))
        user_scores[key] = score
        total += score

    avg_score = round(total / len(skills), 2)

    if avg_score >= 7.5:
        duration = "3"
        roadmap = {"3 Months": career_roadmaps[career]["short_term"]}
    elif avg_score >= 5:
        duration = "6"
        roadmap = {"6 Months": career_roadmaps[career]["mid_term"]}
    else:
        duration = "12"
        roadmap = career_roadmaps[career]

    ai_roadmap = {}
    for phase, categories in roadmap.items():
        ai_roadmap[phase] = {}
        for category, items in categories.items():
            ai_roadmap[phase][category] = []
            for item in items:
                ai_roadmap[phase][category].append({
                    "title": item,
                    "description": generate_ai_text(
                        career, phase, category, item, avg_score
                    )
                })

    weekly_plan = generate_weekly_plan(career, duration, ai_roadmap, user_scores)
    monthly_summaries = generate_monthly_summaries(career, weekly_plan, user_scores)
    skill_confidence = generate_skill_confidence_change(user_scores, duration)

    final_verdict = generate_final_verdict(
        career, total, avg_score, skill_confidence, skills
    )

    return render_template(
        "roadmap/result.html",
        career=career,
        roadmap=ai_roadmap,
        avg_score=avg_score,
        duration=duration,
        weekly_plan=weekly_plan,
        monthly_summaries=monthly_summaries,
        skill_confidence=skill_confidence,
        final_verdict=final_verdict,
        skills=skills,
        user_scores=user_scores
    )
