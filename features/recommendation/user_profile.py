
class UserProfile:

    def __init__(
        self,
        skills,
        work_life_balance=70,
        culture_values=70,
        career_opp=70,
        comp_benefits=70
    ):
        if isinstance(skills, str):
            skills = skills.split(",")

        self.skills = {
            skill.strip().lower()
            for skill in skills
            if skill.strip()
        }

        self.preferences = {
            "work_life_balance": work_life_balance,
            "culture_values": culture_values,
            "career_opp": career_opp,
            "comp_benefits": comp_benefits
        }

        for attribute, value in self.preferences.items():
            if not isinstance(value, (int, float)) or not 0 <= value <= 100:
                raise ValueError(
                    f"{attribute} must be between 0 and 100."
                )

    def get_preferences(self):
        return self.preferences

    def get_skills(self):
        return self.skills
