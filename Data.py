from dataclasses import dataclass


@dataclass
class GameWindow(object):
	"""Struct that contains information about the box to crop. Values are in percent."""
	x_start: float
	y_start: float
	x_end: float
	y_end: float

	# Transform percentage values to coordinates relative to game window size
	def coords(self, game_width: int, game_height: int) -> tuple[float, float, float, float]:
		return (round(self.x_start * game_width / 100),
		        round(self.y_start * game_height / 100),
		        round(self.x_end * game_width / 100),
		        round(self.y_end * game_height / 100))

	def to_screen_coords(self, coords: tuple[float, float], game_width: int, game_height: int) -> tuple[float, float]:
		return (round(coords[0] + game_width * (self.x_start / 100)),
		        round(coords[1] + game_height * (self.y_start / 100)))


BENCH_HEALTH_POS: list[GameWindow] = [
	GameWindow(19.218, 57.592, 24.583, 70.092),  # 0
	GameWindow(25.260, 57.592, 30.625, 70.092),  # 1
	GameWindow(31.302, 57.592, 36.666, 70.092),  # 2
	GameWindow(37.916, 57.592, 42.760, 70.092),  # 3
	GameWindow(43.958, 57.592, 49.323, 70.092),  # 4
	GameWindow(50.000, 57.592, 55.364, 70.092),  # 5
	GameWindow(56.041, 57.592, 61.406, 70.092),  # 6
	GameWindow(62.083, 57.592, 67.448, 70.092),  # 7
	GameWindow(68.125, 57.592, 73.489, 70.092),  # 8
]


BENCH_LOC: list[GameWindow] = [
	GameWindow(22.135, 71.944, 22.135, 71.944),
	GameWindow(28.229, 71.944, 28.229, 71.944),
	GameWindow(34.271, 71.944, 34.271, 71.944),
	GameWindow(40.521, 71.944, 40.521, 71.944),
	GameWindow(46.458, 71.944, 46.458, 71.944),
	GameWindow(52.604, 71.944, 52.604, 71.944),
	GameWindow(58.750, 71.944, 58.750, 71.944),
	GameWindow(64.791, 71.944, 64.791, 71.944),
	GameWindow(70.781, 71.944, 70.781, 71.944),
]

BOARD_BOX: GameWindow = GameWindow(22, 12, 75, 72)

# This list goes from bottom left (0) to top right (27)
BOARD_LOC: list[GameWindow] = [
	GameWindow(30.260, 60.278, 30.260, 60.278),
	GameWindow(36.823, 60.278, 36.823, 60.278),
	GameWindow(43.698, 60.278, 43.698, 60.278),
	GameWindow(50.312, 60.278, 50.312, 60.278),
	GameWindow(56.823, 60.278, 56.823, 60.278),
	GameWindow(63.646, 60.278, 63.646, 60.278),
	GameWindow(70.260, 60.278, 70.260, 60.278),

	GameWindow(27.708, 52.870, 27.708, 52.870),
	GameWindow(34.375, 52.870, 34.375, 52.870),
	GameWindow(40.416, 52.870, 40.416, 52.870),
	GameWindow(47.031, 52.870, 47.031, 52.870),
	GameWindow(53.229, 52.870, 53.229, 52.870),
	GameWindow(59.739, 52.870, 59.739, 52.870),
	GameWindow(66.406, 52.870, 66.406, 52.870),

	GameWindow(31.719, 45.741, 31.719, 45.741),
	GameWindow(37.656, 45.741, 37.656, 45.741),
	GameWindow(43.802, 45.741, 43.802, 45.741),
	GameWindow(50.104, 45.741, 50.104, 45.741),
	GameWindow(56.354, 45.741, 56.354, 45.741),
	GameWindow(62.396, 45.741, 62.396, 45.741),
	GameWindow(68.646, 45.741, 68.646, 45.741),

	GameWindow(29.011, 39.167, 29.011, 39.167),
	GameWindow(35.052, 39.167, 35.052, 39.167),
	GameWindow(41.198, 39.167, 41.198, 39.167),
	GameWindow(47.239, 39.167, 47.239, 39.167),
	GameWindow(53.073, 39.167, 53.073, 39.167),
	GameWindow(59.271, 39.167, 59.271, 39.167),
	GameWindow(65.156, 39.167, 65.156, 39.167),
]

ROUND_BOX: GameWindow = GameWindow(39.94791667, 0.9259259259, 45.3125, 2.87037037)
ROUND_POS_1: GameWindow = GameWindow(50, 0, 100, 100)
ROUND_POS_2: GameWindow = GameWindow(0, 0, 50, 100)

CAROUSEL_ROUND: list[str] = ["2-4", "3-4", "4-4", "5-4", "6-4", "7-4"]

PVE_ROUND: list[str] = ["1-3", "1-4", "2-7", "3-7", "4-7", "5-7", "6-7", "7-7"]

PVP_ROUND: list[str] = ["2-1", "2-2", "2-3", "2-5", "2-6",
                        "3-1", "3-2", "3-3", "3-5", "3-6",
                        "4-1", "4-2", "4-3", "4-5", "4-6",
                        "5-1", "5-2", "5-3", "5-5", "5-6",
                        "6-1", "6-2", "6-3", "6-5", "6-6",
                        "7-1", "7-2", "7-3", "7-5", "7-6"]

ROUNDS: set[str] = {"1-1", "1-2", "1-3", "1-4",
                    "2-1", "2-2", "2-3", "2-4", "2-5", "2-6", "2-7",
                    "3-1", "3-2", "3-3", "3-4", "3-5", "3-6", "3-7",
                    "4-1", "4-2", "4-3", "4-4", "4-5", "4-6", "4-7",
                    "5-1", "5-2", "5-3", "5-4", "5-5", "5-6", "5-7",
                    "6-1", "6-2", "6-3", "6-4", "6-5", "6-6", "6-7",
                    "7-1", "7-2", "7-3", "7-4", "7-5", "7-6", "7-7"}

ROUND_WHITELIST: str = "0123456789-"

GOLD_BOX: GameWindow = GameWindow(45.3125, 81.75925926, 47.91666667, 84.16666667)
GOLD_WHITELIST: str = "0123456789"

REGIONS_POS: list[GameWindow] = [
	GameWindow(3.28, 30.83, 13.64, 34.72),
	GameWindow(3.28, 39.26, 13.64, 43.06),
	GameWindow(3.28, 47.60, 13.64, 51.38),
]
REGIONS_LOC: list[GameWindow] = [
	GameWindow(1.67, 31.94, 1.67, 31.94),
	GameWindow(1.67, 40.74, 1.67, 40.74),
	GameWindow(1.67, 48.70, 1.67, 48.70),
]
REGION_AUGMENT_LOC: GameWindow = GameWindow(26.041, 32.407, 26.041, 32.407)
REGION_AUGMENT_POS: GameWindow = GameWindow(34.375, 26.388, 44.010, 31.481)

PORTALS: list[str] = [
    # Prelude Portals
    "Golden Prelude",
    "Prismatic Prelude",

    # Gala Portals
    "Golden Gala",
    "Prismatic Party",

    # Finale Portals
    "Golden Finale",
    "Prismatic Finale",

    # Ascending Augments
    "Ascending Augments",

    # Champion Portals
    "3-Cost Champion",
    "Champion Duplicator",
    "3 Champions",
    "Upgraded Champion",
    "Champion Delivery",
    "Champion Conference",

    # Item Portals
    "Artifact Anvil",
    "Component Anvils",
    "Completed Anvil",
    "Radiant Item",
    "Support Anvil",
    "Tactician's Crown",
    "Anvil Buffet",
    "Make 'Em Cook",

    # Gold Portals
    "Pot of Gold",
    "Item Payout",
    "Gold Subscription",
    "Gold Opener",

    # Unique Portals
    "Scuttle Puddle",
    "Spatula",
    "Trainer Golems",
    "Radiant Blessing",
    "Loot Subscription",
    "Loaded Carousels",
    "Crab Rave",
    "Frying Pan",

    # Default Portals
    "No portal this game",

    # Charm Portals
    "Overachievers",
    "Castfest"
]

AUGMENTS_POS: list[GameWindow] = [
	GameWindow(22.031, 47.222, 35.156, 53.888),
	GameWindow(43.489, 47.222, 56.562, 53.888),
	GameWindow(64.114, 47.222, 78.437, 53.888),
]

AUGMENTS_LOC: list[GameWindow] = [
	GameWindow(28.593, 41.203, 28.593, 41.203),
	GameWindow(49.739, 41.203, 49.739, 41.203),
	GameWindow(71.093, 41.203, 71.093, 41.203)
]

AUGMENTS_ROLL_ONE: GameWindow = GameWindow(28.750, 80.092, 28.750, 80.092)
AUGMENTS_ROLL_TWO: GameWindow = GameWindow(50.000, 80.092, 50.000, 80.092)
AUGMENTS_ROLL_THREE: GameWindow = GameWindow(71.093, 80.092, 71.093, 80.092)

AUGMENTS_NAME_WHITELIST: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'&+!1234567890 "

AUGMENTS_HERO: set[str] = {
    "Balanced Budget",
    "Balanced Budget II",
    "Balanced Budget III",
    "Battle Ready",
    "Battle Ready II",
    "Battle Ready III",
    "Big Grab Bag",
    "Ascension",
    "Knowledge Download I",
    "Knowledge Download II",
    "Knowledge Download III",
    "Final Ascension",
    "Large Forge",
    "Masterful Job",
    "Medium Forge",
    "Job Well Done",
    "Money!",
    "Money Money!",
    "Money Money Money!",
    "Partial Ascension",
    "Rolling For Days I",
    "Rolling For Days II",
    "Rolling For Days III",
    "Small Forge",
    "Job's Done",
    "Teaming Up I",
    "Teaming Up II",
    "Teaming Up III",
    "Tiny Power I",
    "Tiny Power II",
    "Tiny Power III",
    "Well-Earned Comforts I",
    "Well-Earned Comforts II",
    "Well-Earned Comforts III",
    "Final Grab Bag",
    "Final Grab Bag II",
    "Urf's Grab Bag",
    "Giant Grab Bag",
    "Gotta Go Fast!",
    "Gotta Go Fast! II",
    "Gotta Go Fast!!! III",
    "Item Grab Bag I",
    "Item Grab Bag II",
    "Item Grab Bag III",
    "It Pays To Learn",
    "It Pays to Learn II",
    "It Pays to Learn III",
    "AFK",
    "Caretaker's Ally",
    "Caretaker's Favor",
    "Caretaker's Chosen",
    "Branching Out",
    "Buried Treasures I",
    "Buried Treasures II",
    "Buried Treasures III",
    "Cutting Corners",
    "Spoils of War I",
    "Spoils of War II",
    "Spoils of War III",
    "Jeweled Lotus III",
    "Hedge Fund",
    "Shopping Spree",
    "Jeweled Lotus II",
    "Patient Study",
    "Jeweled Lotus I",
    "Living Forge",
    "Latent Forge",
    "Level Up!",
    "Metabolic Accelerator",
    "On a Roll",
    "One Twos Three",
    "Pandora's Items",
    "Pandora's Items II",
    "Pandora's Box",
    "Portable Forge",
    "Pumping Up I",
    "Pumping Up II",
    "Pumping Up III",
    "Rich Get Richer",
    "Stars are Born",
    "Starter Kit",
    "Tiniest Titan",
    "Tiny Titans",
    "Ancient Archives I",
    "Ancient Archives II",
    "Trade Sector",
    "Transfusion I",
    "Transfusion II",
    "Transfusion III",
    "Tiny Grab Bag",
    "Training Reward",
    "Training Reward II",
    "Training Reward III"
}

AUGMENTS_SILVER: set[str] = {
    "AFK",
    "All Natural I",
    "Army Building",
    "Bastion Heart",
    "Blood Money",
    "Bronze Ticket",
    "Bruiser Heart",
    "Buried Treasures I",
    "Challenger Heart",
    "Cybernetic Bulk I",
    "Deadeye Heart",
    "Demacia Heart",
    "Branching Out",
    "Gunner Heart",
    "Invoker Heart",
    "Ionia Heart",
    "Iron Assets",
    "JACKPOT!",
    "Juggernaut Heart",
    "Jeweled Lotus I",
    "Long Distance Pals",
    "Latent Forge",
    "Missed Connections",
    "Noxus Heart",
    "One, Twos, Three",
    "One, Two, Five!",
    "Pandora's Bench",
    "Pandora's Items",
    "Cybernetic Leech I",
    "Pumping Up I",
    "Recombobulator",
    "Red Buff",
    "Risky Moves",
    "Rogue Heart",
    "Shadow Isles Heart",
    "Shurima Heart",
    "Silver Spoon",
    "Slayer Heart",
    "Social Distancing I",
    "Sorcerer Heart",
    "Spoils of War I",
    "Harmacist I",
    "Healing Orbs I",
    "Component Buffet",
    "Tiny Titans",
    "Transfusion I",
    "Unified Resistance I",
    "Unburdened I",
    "Inconsistency",
    "Young and Wild and Free",
    "Zaun Heart"
}

AUGMENTS_GOLD: set[str] = {
    "A Cut Above",
    "Adrenaline Rush",
    "All Natural II",
    "All That Shimmers",
    "Bastion Crest",
    "Buried Treasures II",
    "Defensive Dash",
    "Built Different II",
    "Capricious Forge",
    "Challenger Crest",
    "Loving Invocation",
    "Chemtech Enhancements",
    "Contagion",
    "Bruiser Crest",
    "Cybernetic Bulk II",
    "Cybernetic Leech II",
    "Deadeye Crest",
    "Demacia Crest",
    "Demonflare",
    "Double Trouble II",
    "Early Education",
    "Petricite Shackles",
    "Endurance Training",
    "Escort Quest",
    "Freljord Heart",
    "Gargantuan Resolve",
    "Glacial Breeze",
    "Gunner Crest",
    "Harmacist II",
    "Haunted Shell",
    "Healing Orbs II",
    "Idealism",
    "Impromptu Inventions",
    "Indomitable Will",
    "Infusion",
    "Invoker Crest",
    "Ionia Crest",
    "Jeweled Lotus",
    "Juggernaut Crest",
    "Frequent Flyer",
    "Know Your Enemy",
    "Library Card",
    "Last Stand",
    "Patient Study II",
    "Long Distance Pals II",
    "Mana Burn",
    "Martyr",
    "Medium-End Shopping",
    "Metabolic Accelerator",
    "Morning Light",
    "Multicaster Heart",
    "Not Today",
    "Noxus Crest",
    "Magic Wand",
    "Overcharged Manafont",
    "Pandora's Items II",
    "Perfected Repetition",
    "Piltover Heart",
    "Portable Forge",
    "Pumping Up II",
    "Ravenous Hunter",
    "Return on Investment",
    "Rich Get Richer",
    "Rich Get Richer+",
    "Riftwalk",
    "Rogue Crest",
    "Salvage Bin",
    "Scoped Weapons",
    "Sentinel's Spirit",
    "Shadow Isles Crest",
    "Shimmering Inventors",
    "Shoplifting",
    "Shurima Crest",
    "Shurima's Legacy",
    "Silver Ticket",
    "Slayer Crest",
    "Slayer's Resolve",
    "Sleight of Hand",
    "Social Distancing II",
    "Sorcerer Crest",
    "Dueling Gunners",
    "Spoils of War II",
    "Stars are Born",
    "Strategist Heart",
    "Stellacorn's Blessing",
    "Suppressing Fire",
    "Tactical Superiority",
    "Targon Heart",
    "The Boss",
    "Three's a Crowd",
    "Three's Company",
    "Tons of Stats!",
    "Titanic Strength",
    "Total Domination",
    "Trade Sector",
    "Transfusion II",
    "Two Healthy",
    "Unified Resistance II",
    "Unburdened II",
    "Winds of War"
}

AUGMENTS_PRISMATIC: set[str] = {
    "Endless Horde",
    "Endless Horde+",
    "Ancient Archives II",
    "Bastion Crown",
    "Binary Airdrop",
    "Birthday Present",
    "Bruiser Crown",
    "Buried Treasures III",
    "Built Different III",
    "Challenger Crown",
    "Cruel Pact",
    "Cybernetic Bulk III",
    "Cybernetic Leech III",
    "Deadeye Crown",
    "Demacia Crown",
    "Double Trouble III",
    "Final Reserves",
    "Freljord Soul",
    "Gifts From Above",
    "Golden Ticket",
    "Jeweled Lotus III",
    "Gunner Crown",
    "Harmacist III",
    "Hedge Fund",
    "Hedge Fund+",
    "Hedge Fund++",
    "High End Sector",
    "Invoker Crown",
    "Ionia Crown",
    "Level Up!",
    "Living Forge",
    "Lucky Gloves",
    "March of Progress",
    "Wellness Trust",
    "Multicaster Soul",
    "Noxus Crown",
    "Pandora's Box",
    "Phreaky Friday",
    "Phreaky Friday +",
    "Piltover Soul",
    "Pumping Up III",
    "Radiant Relics",
    "Rogue Crown",
    "Roll The Dice",
    "Shadow Isles Crown",
    "Shurima Crown",
    "Slayer Crown",
    "Social Distancing III",
    "Sorcerer Crown",
    "Spoils of War III",
    "Starter Kit",
    "Strategist Soul",
    "Tactician's Tools",
    "Targon Soul",
    "Think Fast",
    "Tiniest Titan",
    "Transfusion III",
    "Void Soul",
    "Wandering Trainer",
    "What The Forge",
    "Zaun Crown",
    "The Golden Egg",
    "Cursed Crown",
    "Unleashed Arcana",
    "Impenetrable Bulwark",
    "Blinding Speed"
}

AUGMENTS = AUGMENTS_HERO.union(AUGMENTS_SILVER, AUGMENTS_GOLD, AUGMENTS_PRISMATIC)

SHOP_BOX: GameWindow = GameWindow(25.05208333, 96.2037037, 76.875, 99.07407407)
CHAMP_NAME_POS: list[GameWindow] = [
	GameWindow(0.3015075377, 16.12903226, 12.06030151, 77.41935484),
	GameWindow(20.50251256, 16.12903226, 32.16080402, 77.41935484),
	GameWindow(40.90452261, 16.12903226, 52.46231156, 77.41935484),
	GameWindow(61.10552764, 16.12903226, 71.55778894, 77.41935484),
	GameWindow(81.20603015, 16.12903226, 91.65829146, 77.41935484)
]
CHAMP_NAME_WHITELIST: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'& "
BUY_LOCATIONS: list[GameWindow] = [
	GameWindow(29.94, 91.85, 29.94, 91.85),
	GameWindow(40.36, 91.85, 40.36, 91.85),
	GameWindow(50.78, 91.85, 50.78, 91.85),
	GameWindow(61.20, 91.85, 61.20, 91.85),
	GameWindow(71.61, 91.85, 71.61, 91.85),
]

CHAMPIONS: dict[str, dict[str, int]] = {
	"Ashe"        : {"Gold": 1, "Board Size": 1},
	"Blitzcrank"  : {"Gold": 1, "Board Size": 1},
	"Elise"       : {"Gold": 1, "Board Size": 1},
	"Jayce"       : {"Gold": 1, "Board Size": 1},
	"Lillia"      : {"Gold": 1, "Board Size": 1},
	"Nomsy"       : {"Gold": 1, "Board Size": 1},
	"Poppy"       : {"Gold": 1, "Board Size": 1},
	"Seraphine"   : {"Gold": 1, "Board Size": 1},
	"Soraka"      : {"Gold": 1, "Board Size": 1},
	"Twitch"      : {"Gold": 1, "Board Size": 1},
	"Warwick"     : {"Gold": 1, "Board Size": 1},
	"Ziggs"       : {"Gold": 1, "Board Size": 1},
	"Zoe"         : {"Gold": 1, "Board Size": 1},

	"Ahri"        : {"Gold": 2, "Board Size": 1},
	"Akali"       : {"Gold": 2, "Board Size": 1},
	"Galio"       : {"Gold": 2, "Board Size": 1},
	"Kassadin"    : {"Gold": 2, "Board Size": 1},
	"Kog'Maw"     : {"Gold": 2, "Board Size": 1},
	"Neeko"       : {"Gold": 2, "Board Size": 1},
	"Nilah"       : {"Gold": 2, "Board Size": 1},
	"Nunu"        : {"Gold": 2, "Board Size": 1},
	"Rumble"      : {"Gold": 2, "Board Size": 1},
	"Shyvana"     : {"Gold": 2, "Board Size": 1},
	"Swain"       : {"Gold": 2, "Board Size": 1},
	"Zilean"      : {"Gold": 2, "Board Size": 1},

	"Bard"        : {"Gold": 3, "Board Size": 1},
	"Ezreal"      : {"Gold": 3, "Board Size": 1},
	"Hecarim"     : {"Gold": 3, "Board Size": 1},
	"Hwei"        : {"Gold": 3, "Board Size": 1},
	"Jinx"        : {"Gold": 3, "Board Size": 1},
	"Katarina"    : {"Gold": 3, "Board Size": 1},
	"Mordekaiser" : {"Gold": 3, "Board Size": 1},
	"Shen"        : {"Gold": 3, "Board Size": 1},
	"Taric"       : {"Gold": 3, "Board Size": 1},
	"Vex"         : {"Gold": 3, "Board Size": 1},
	"Wukong"      : {"Gold": 3, "Board Size": 1},
	"Veigar"      : {"Gold": 3, "Board Size": 1},

	"Fiora"       : {"Gold": 4, "Board Size": 1},
	"Gwen"        : {"Gold": 4, "Board Size": 1},
	"Kalista"     : {"Gold": 4, "Board Size": 1},
	"Karma"       : {"Gold": 4, "Board Size": 1},
	"Nami"        : {"Gold": 4, "Board Size": 1},
	"Nasus"       : {"Gold": 4, "Board Size": 1},
	"Olaf"        : {"Gold": 4, "Board Size": 1},
	"Rakan"       : {"Gold": 4, "Board Size": 1},
	"Ryze"        : {"Gold": 4, "Board Size": 1},
	"Tahm Kench"  : {"Gold": 4, "Board Size": 1},
	"Varus"       : {"Gold": 4, "Board Size": 1},

	"Briar"       : {"Gold": 5, "Board Size": 1},
	"Camille"     : {"Gold": 5, "Board Size": 1},
	"Diana"       : {"Gold": 5, "Board Size": 1},
	"Milio"       : {"Gold": 5, "Board Size": 1},
	"Morgana"     : {"Gold": 5, "Board Size": 1},
	"Norra"       : {"Gold": 5, "Board Size": 1},
	"Smolder"     : {"Gold": 5, "Board Size": 1},
	"Xerath"      : {"Gold": 5, "Board Size": 1},
}

CHAMPION_DETAILS_NAME: GameWindow = GameWindow(89, 30, 97, 32)
