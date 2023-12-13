import collections
from time import sleep
from typing import List

from Data import AUGMENTS_LOC, BUY_LOCATIONS, CAROUSEL_ROUND, CHAMPIONS, REGIONS_LOC, REGION_AUGMENT_LOC
from Player.BasePlayer import BasePlayer, at_stages
from Utils.VirtualController import VirtualController


class SimpleSet9Player(BasePlayer):

	region_augment = ""


	def on_shop_update(self) -> None:
		shop = self.engine.get_shop()

		for index, champ in enumerate(shop):
			if champ not in self.champs:
				continue

			cost = CHAMPIONS.get(champ, {}).get("Gold", 999)
			if not self.gold >= cost:
				continue

			if None not in self.bench and not (self.bench.count(champ) >= 2 or shop.count(champ) >= 2):
				continue

			print("Buying: ", champ)
			x, y, _, _ = BUY_LOCATIONS[index].coords(self.engine.game_image.width, self.engine.game_image.height)
			VirtualController.left_click(*self.engine.game_cap.get_screen_position((x, y)))

			self.gold -= cost

			for i, slot in enumerate(self.bench):
				if slot is None:
					self.bench[i] = champ
					break

			self.get_champs_on_bench()

	def on_round_change(self, cur_round: str) -> None:
		super().on_round_change(cur_round)

		# Don't reroll if we are in carousel
		# TODO: Implement a CLASS that controls the economics of the game instead
		#  of doing it like this so we can have different type of "playstyles"
		if cur_round in CAROUSEL_ROUND:
			return

		self.get_champs_on_bench()

		if self.level >= 9 or self.health <= 25:
			while self.gold >= 52 or (self.health <= 25 and self.gold >= 6):
				VirtualController.press_d()
				self.engine.get_game_image()
				self.update_stats()
				self.on_shop_update()

		elif self.level >= 5 and self.gold >= 4:
			VirtualController.press_f()

			while self.gold >= 32:
				VirtualController.press_d()
				self.engine.get_game_image()
				self.update_stats()
				self.on_shop_update()
		else:
			while self.gold >= 24:
				VirtualController.press_f()
				self.gold -= 4

	@at_stages(["1-1"])
	def region_stage(self) -> None:
		""" Region Voting Stage """

		regions = self.engine.get_regions()

		print("Regions: ", regions)
		print("Choosing region: ", regions[0])

		x, y, _, _ = REGIONS_LOC[0].coords(self.engine.game_image.width, self.engine.game_image.height)
		VirtualController.left_click(*self.engine.game_cap.get_screen_position((x, y)))
		sleep(1.7)

		self.engine.get_game_image()
		vote_locs = self.engine.get_vote_locations()
		if len(vote_locs) > 0:
			loc = vote_locs[0]
			VirtualController.left_click(*self.engine.game_cap.get_screen_position((loc[0], loc[1])))

	@at_stages(["1-2"])
	def first_pve(self) -> None:
		# First round has some delay to it
		sleep(2)

		x, y, _, _ = REGION_AUGMENT_LOC.coords(self.engine.game_image.width, self.engine.game_image.height)
		VirtualController.right_click(*self.engine.game_cap.get_screen_position((x, y)))

		self.engine.get_game_image()
		self.region_augment = self.engine.get_region_augment()
		print("Region Augments is: ", self.region_augment)

		self.get_champs_on_bench(wait=False)

		self.move_champion_to_board(0, 25)

	def on_drops_found(self, drops: List[tuple[float, float]]) -> None:
		super().on_drops_found(drops)

		self.get_champs_on_bench()

	@at_stages(["2-1", "3-2", "4-2"])
	def at_augment_round(self) -> None:
		# First augment legend animation delay
		sleep(3)

		self.engine.get_game_image()
		augments = self.engine.get_augments()

		if len(augments) <= 0:
			print("Error reading augments from game...")
			return

		# TODO: Implement augment choosing logic
		index = 0
		print("Choosing: ", augments[index], "From: ", augments)

		x, y, _, _ = AUGMENTS_LOC[index].coords(self.engine.game_image.width, self.engine.game_image.height)
		VirtualController.left_click(*self.engine.game_cap.get_screen_position((x, y)))

		self.augments.append(augments[index])
		sleep(1.5)

		self.engine.get_game_image()
		self.update_stats()

	@at_stages(["2-5", "3-5", "4-5", "5-5", "6-5", "7-5"])
	def after_carousel(self) -> None:
		# self.get_champs_on_bench()
		pass
