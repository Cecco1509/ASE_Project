
mock_gacha_list = [
    {"id": 1, "name": "Kuriboh", "description": "An adorable monster that defends you in battles.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/a/a4/Kuriboh.png", "rarityPercent": 24.75},
    {"id": 2, "name": "Winged Kuriboh", "description": "A winged version of Kuriboh with extra defense abilities.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/e/e4/WingedKuriboh.png", "rarityPercent": 24.75},
    {"id": 3, "name": "Baby Dragon", "description": "A small dragon with potential to grow stronger.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/7/79/BabyDragon.png", "rarityPercent": 12.5},
    {"id": 4, "name": "Giant Soldier of Stone", "description": "A giant made of stone that stands as a solid defense.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/8/80/GiantSoldierofStone.png", "rarityPercent": 12.5},
    {"id": 5, "name": "Mystical Elf", "description": "A sorceress with high defensive power.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/d/d6/MysticalElf.png", "rarityPercent": 5.0},
    {"id": 6, "name": "Celtic Guardian", "description": "An elf warrior that strikes with swift attacks.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/7/76/CelticGuardian.png", "rarityPercent": 5.0},
    {"id": 7, "name": "Man-Eater Bug", "description": "A nasty bug that destroys one monster upon flipping.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/5/55/ManEaterBug.png", "rarityPercent": 2.5},
    {"id": 8, "name": "Feral Imp", "description": "A beast with surprising power in battles.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/2/23/FeralImp.png", "rarityPercent": 2.5},
    {"id": 9, "name": "Harpie Lady", "description": "A bird-like warrior with swift attacks.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/7/7b/HarpieLady.png", "rarityPercent": 1.5},
    {"id": 10, "name": "Swordsman of Landstar", "description": "A humble swordsman with determination.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/c/c8/SwordsmanofLandstar.png", "rarityPercent": 1.5},
    {"id": 11, "name": "Spirit of the Harp", "description": "A spirit that brings harmony and high defense.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/e/e4/SpiritoftheHarp.png", "rarityPercent": 1.25},
    {"id": 12, "name": "Silver Fang", "description": "A wolf with sharp fangs for quick strikes.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/8/8f/SilverFang.png", "rarityPercent": 1.25},
    {"id": 13, "name": "Battle Ox", "description": "A beast-warrior that packs a punch in battle.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/8/8f/BattleOx.png", "rarityPercent": 0.975},
    {"id": 14, "name": "Armed Ninja", "description": "A stealthy ninja that flips the battle in your favor.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/4/4c/ArmedNinja.png", "rarityPercent": 0.975},
    {"id": 15, "name": "Dark Blade", "description": "A warrior who has mastered the blade.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/8/8d/DarkBlade.png", "rarityPercent": 0.75},
    {"id": 16, "name": "Luster Dragon", "description": "A shiny dragon that dazzles the battlefield.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/a/a8/LusterDragon.png", "rarityPercent": 0.75},
    {"id": 17, "name": "Penguin Soldier", "description": "A strategic penguin that bounces enemies back to hand.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/1/11/PenguinSoldier.png", "rarityPercent": 0.5},
    {"id": 18, "name": "Dragon Zombie", "description": "A dragon that rose from the dead with reduced power.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/9/9f/DragonZombie.png", "rarityPercent": 0.5},
    {"id": 19, "name": "Rogue Doll", "description": "A mystical doll with unpredictable attacks.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/d/db/RogueDoll.png", "rarityPercent": 0.25},
    {"id": 20, "name": "Time Wizard", "description": "A wizard that manipulates time to change battles.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/4/41/TimeWizard.png", "rarityPercent": 0.25},
    {"id": 21, "name": "Thousand Dragon", "description": "The elder form of Baby Dragon after time travel.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/4/42/ThousandDragon.png", "rarityPercent": 0.025},
    {"id": 22, "name": "The Shadow Who Controls the Dark", "description": "A sinister shadow with hidden power.", 
     "image": "https://static.wikia.nocookie.net/yugioh/images/a/ac/ShadowWhoControlsDark.png", "rarityPercent": 0.025}
]

mock_gacha_collection_list = [
        {
            'id': 1,
            'gachaId': 1,
            'userId': 1,
            'timestamp': '2021-07-01T12:00:00',
            'source': 'ROLL'
        },
        {
            'id': 2,
            'gachaId': 2,
            'userId': 1,
            'timestamp': '2021-07-01T12:01:00',
            'source': 'AUCTION'
        },
        {
            'id': 3,
            'gachaId': 3,
            'userId': 2,
            'timestamp': '2021-07-01T12:02:00',
            'source': 'ROLL'
        }
    ]

mock_user_list = [
        {
            'id': 1,
            'authId': 101,
            'ingameCurrency': 1500.0,
            'profilePicture': 'profile1.png',
            'registrationDate': '2021-01-01T10:00:00',
            'status': 'ACTIVE'
        },
        {
            'id': 2,
            'authId': 102,
            'ingameCurrency': 3000.0,
            'profilePicture': 'profile2.png',
            'registrationDate': '2021-02-01T11:00:00',
            'status': 'ACTIVE'
        },
        {
            'id': 3,
            'authId': 103,
            'ingameCurrency': 0.0,
            'profilePicture': 'profile3.png',
            'registrationDate': '2021-03-01T12:00:00',
            'status': 'ACTIVE'
        }
    ]