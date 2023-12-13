import time
from time import sleep

from PIL import Image

from OCR.Engine import OCREngine
from Player.SimpleSet9Player import SimpleSet9Player

champs = ["Cho'Gath", "Malzahar", "Kassadin", "Rek'Sai", "Vel'Koz", "Kai'Sa", "Bel'Veth", "Heimerdinger", "K'Sante"]


def benchmark():
	engine = OCREngine()
	engine.game_image = Image.open(r".\imgs\shot16.jpg")

	st = time.process_time()

	print("Orbs at: ", engine.get_random_drop_locations())
	print("Shop has: ", engine.get_shop())
	print("Gold: ", engine.get_gold())
	print("Round: ", engine.get_round())
	print("Regions: ", engine.get_regions())
	print("Vote locs: ", engine.get_vote_locations())
	print("Augments: ", engine.get_augments())
	print("Bench occupied: ", engine.get_bench_slots())
	print("Champ on details: ", engine.get_champ_from_details())

	et = time.process_time()
	res = et - st
	print('CPU Execution time:', res, 's')
	exit(0)


if __name__ == "__main__":
	player = SimpleSet9Player()
	# benchmark()

	while True:
		player.game_step()
		sleep(0.5)
