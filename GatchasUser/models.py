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
    
    # TODO handle errors, return None if data is invalid, and handle it in other code
    @classmethod
    def from_dict(cls, data):
        """Create a GachaItem instance from a dictionary."""
        return cls(
            gacha_id=data.get("gacha_id"),
            name=data.get("name"),
            image=data.get("image"),
            rarity_percentage=data.get("rarity_percentage"),
            description=data.get("description"),
            created_at=data.get("created_at")
        )    

class GachaCollection:
    def __init__(self, id, gachaId, userId, source, timestamp=None):
        self.id = id
        self.gachaId = gachaId
        self.userId = userId
        self.source = source
        self.timestamp = timestamp or datetime.datetime.now()

    def to_dict(self):
        """Convert GachaCollection to dictionary for easy JSON serialization."""
        return {
            "id": self.id,
            "gachaId": self.gachaId,
            "userId": self.userId,
            "source": self.source,
            "timestamp": self.timestamp
        }
    
    # TODO handle errors, return None if data is invalid, and handle it in other code
    @classmethod
    def from_dict(cls, data):
        """Create a GachaCollection instance from a dictionary."""
        return cls(
            id=data.get("id"),
            gachaId=data.get("gachaId"),
            userId=data.get("userId"),
            source=data.get("source"),
            timestamp=data.get("timestamp"),
        )
