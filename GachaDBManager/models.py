from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app import db
from enum import Enum

class GachaSource(Enum):
    ROLL = 1
    AUCTION = 2
    UNKNOWN = 3

class Gacha(db.Model):
    __tablename__ = 'gacha'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    image: Mapped[str]
    rarityPercent: Mapped[float]
    description: Mapped[str]
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'rarityPercent': self.rarityPercent
        }
        

class GachaCollection(db.Model):
    __tablename__ = 'gachaCollection'
    id: Mapped[int] = mapped_column(primary_key=True)
    gachaId: Mapped[int] = mapped_column(ForeignKey("gacha.id"))
    userId: Mapped[int]
    timestamp: Mapped[datetime]
    source: Mapped[GachaSource]
    def to_dict(self):
        return {
            'id': self.id,
            'gachaId': self.gachaId,
            'userId': self.userId,
            'timestamp': self.timestamp,
            'source': self.source.name
        }

gacha_items = [
    {"name": "Kuriboh", "description": "An adorable monster that defends you in battles.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/a/a4/Kuriboh.png", "rarityPercent": 24.75},
    {"name": "Winged Kuriboh", "description": "A winged version of Kuriboh with extra defense abilities.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/e/e4/WingedKuriboh.png", "rarityPercent": 24.75},
    {"name": "Baby Dragon", "description": "A small dragon with potential to grow stronger.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/7/79/BabyDragon.png", "rarityPercent": 12.5},
    {"name": "Giant Soldier of Stone", "description": "A giant made of stone that stands as a solid defense.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/8/80/GiantSoldierofStone.png", "rarityPercent": 12.5},
    {"name": "Mystical Elf", "description": "A sorceress with high defensive power.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/d/d6/MysticalElf.png", "rarityPercent": 5.0},
    {"name": "Celtic Guardian", "description": "An elf warrior that strikes with swift attacks.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/7/76/CelticGuardian.png", "rarityPercent": 5.0},
    {"name": "Man-Eater Bug", "description": "A nasty bug that destroys one monster upon flipping.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/5/55/ManEaterBug.png", "rarityPercent": 2.5},
    {"name": "Feral Imp", "description": "A beast with surprising power in battles.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/2/23/FeralImp.png", "rarityPercent": 2.5},
    {"name": "Harpie Lady", "description": "A bird-like warrior with swift attacks.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/7/7b/HarpieLady.png", "rarityPercent": 1.5},
    {"name": "Swordsman of Landstar", "description": "A humble swordsman with determination.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/c/c8/SwordsmanofLandstar.png", "rarityPercent": 1.5},
    {"name": "Spirit of the Harp", "description": "A spirit that brings harmony and high defense.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/e/e4/SpiritoftheHarp.png", "rarityPercent": 1.25},
    {"name": "Silver Fang", "description": "A wolf with sharp fangs for quick strikes.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/8/8f/SilverFang.png", "rarityPercent": 1.25},
    {"name": "Battle Ox", "description": "A beast-warrior that packs a punch in battle.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/8/8f/BattleOx.png", "rarityPercent": 0.975},
    {"name": "Armed Ninja", "description": "A stealthy ninja that flips the battle in your favor.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/4/4c/ArmedNinja.png", "rarityPercent": 0.975},
    {"name": "Dark Blade", "description": "A warrior who has mastered the blade.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/8/8d/DarkBlade.png", "rarityPercent": 0.75},
    {"name": "Luster Dragon", "description": "A shiny dragon that dazzles the battlefield.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/a/a8/LusterDragon.png", "rarityPercent": 0.75},
    {"name": "Penguin Soldier", "description": "A strategic penguin that bounces enemies back to hand.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/1/11/PenguinSoldier.png", "rarityPercent": 0.5},
    {"name": "Dragon Zombie", "description": "A dragon that rose from the dead with reduced power.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/9/9f/DragonZombie.png", "rarityPercent": 0.5},
    {"name": "Rogue Doll", "description": "A mystical doll with unpredictable attacks.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/d/db/RogueDoll.png", "rarityPercent": 0.25},
    {"name": "Time Wizard", "description": "A wizard that manipulates time to change battles.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/4/41/TimeWizard.png", "rarityPercent": 0.25},
    {"name": "Thousand Dragon", "description": "The elder form of Baby Dragon after time travel.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/4/42/ThousandDragon.png", "rarityPercent": 0.025},
    {"name": "The Shadow Who Controls the Dark", "description": "A sinister shadow with hidden power.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/a/ac/ShadowWhoControlsDark.png", "rarityPercent": 0.025},
    ]
