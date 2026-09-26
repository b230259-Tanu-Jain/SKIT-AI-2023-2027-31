class UserProfile:

    def __init__(
        self,
        skills,
        work_life_balance=0,
        culture_values=0,
        career_opp=0,
        comp_benefits=0
    ):
        self.skills = {
            skill.strip().lower()
            for skill in skills
        }

        self.preferences = {
            "work_life_balance": work_life_balance,
            "culture_values": culture_values,
            "career_opp": career_opp,
            "comp_benefits": comp_benefits
        }

    def get_preferences(self):
        return self.preferences

    def get_skills(self):
        return self.skills