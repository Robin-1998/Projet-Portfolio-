from app.models.race import Race
from app.models.character import Character
from app.models.history import History
from app.models.image_post import ImagePost

from app import db

class PortfolioFacade:
# -------------------------RACES-----------------------------------------------

    def get_all_races(self):
        return Race.query.all()

    def get_race(self, race_id):
        race = Race.query.get(race_id)
        if not race:
            raise ValueError(f"Race avec id {race_id} introuvable.")
        return race

# -------------------------CHARACTERS------------------------------------------

    def get_all_characters(self):
        return Character.query.all()

    def get_character(self, character_id):
        character = Character.query.get(character_id)
        if not character:
            raise ValueError(f"Character avec id {character_id} introuvable.")
        return character

# -------------------------EVENTS------------------------------------------

    def get_all_histories(self):
        return History.query.all()

    def get_history(self, history_id):
        history = History.query.get(history_id)
        if not history:
            raise ValueError(f"History avec id {history_id} introuvable.")
        return history


# -------------------------SEARCH------------------------------------------

    def search_all(self, query):
        if not query:
            return {"error": "Aucun terme de recherche fourni"}

        characters = Character.query.filter(Character.name.ilike(f"%{query}%")).all()
        races = Race.query.filter(Race.name.ilike(f"%{query}%")).all()
        history = History.query.filter(History.name.ilike(f"%{query}%")).all()
        #places = Place.query.filter(Place.name.ilike(f"%{query}%")).all()
        image_post = ImagePost.query.filter(ImagePost.title.ilike(f"%{query}%")).all()

        return {
            "query": query,
            "results": {
                "characters": [c.to_dict() for c in characters],
                "races": [r.to_dict() for r in races],
                "history": [h.to_dict() for h in history],
                #"places": [i.to_dict() for p in places],
                "image_post": [i.to_dict() for i in image_post]
            }
        }
