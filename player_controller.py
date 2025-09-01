import json

class ChessPlayer:
    
    def __init__(self, surname, name, date_of_birth, elo):
        self.surname = surname
        self.name = name
        self.date_of_birth = date_of_birth
        self.elo = elo

    def to_dict(self):
        return {
            "surname": self.surname,
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "elo": self.elo
        }

    def save_to_json(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(self.to_dict())

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
