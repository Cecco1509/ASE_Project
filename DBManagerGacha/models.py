import datetime

class GachaItem:
    def __init__(self, gacha_id, name, image, rarity_percentage, description, created_at=None):
        self.gacha_id = gacha_id
        self.name = name
        self.image = image
        self.rarity_percentage = rarity_percentage
        self.description = description
        self.created_at = created_at or datetime.datetime.now()

    def to_dict(self):
        """Convert GachaItem to dictionary for easy JSON serialization."""
        return {
            "gacha_id": self.gacha_id,
            "name": self.name,
            "image": self.image,
            "rarity_percentage": self.rarity_percentage,
            "description": self.description,
            "created_at": self.created_at
        }
