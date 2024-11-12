from time import sleep
from typing import Any, List, Optional

from Data import BENCH_LOC, BOARD_LOC
from OCR.Engine import OCREngine
from Utils.VirtualController import VirtualController


def at_stages(rounds: List[str]):
	class Decorator:
		def __init__(self, fn):
			self.fn = fn

		def __set_name__(self, owner, name):
			owner._at_stage_funcs.append((rounds, self.fn))

			setattr(owner, name, self.fn)

	return Decorator


class BasePlayer(object):

	champs = ["Blitzcrank", "Seraphine", "Galio", "Nunu", "Vex", "Veigar", "Nami", "Taric", "Norra"]

	_at_stage_funcs = []

	augments: list[str] = []
	bench: list[Optional[str]] = [None] * 9
	board: list[Optional[str]] = [None] * 28

	cur_round: str = None
	gold: int = 0
	health: int = 0
	level: int = 0

	def __init__(self) -> None:
		self.engine: OCREngine = OCREngine()

	def on_shop_update(self) -> None:
		""" Called when there is an update to the shop """

		shop = self.engine.get_shop()

	def on_drops_found(self, drops: List[tuple[float, float]]) -> None:
		""" Called when there are drops on the board """

		while len(drops) > 0:
			print("Getting drop at: ", drops[0])
			x, y = self.engine.game_cap.get_screen_position(drops[0])
			VirtualController.right_click(*self.engine.game_cap.get_screen_position((x, y)))
			sleep(0.5)

			# We get a new image and drops due to some drops being close together and can be caught close to others
			# This can be done more efficiently by combining drop locations that are X close to others
			self.engine.get_game_image()
			drops = self.engine.get_random_drop_locations()

	@at_stages(["2-4", "3-4", "4-4", "5-4", "6-4", "7-4"])
	def at_carousel(self) -> None:
		print("At a carousel...")

	def on_round_change(self, cur_round: str) -> None:
		""" Called when the round changes """

		sleep(0.7)
		self.engine.get_game_image()
		self.update_stats()

		print("Now at round: ", cur_round)

		for rounds, func in self._at_stage_funcs:
			if cur_round in rounds:
				func(self)

		drops = self.engine.get_random_drop_locations()
		if len(drops) > 0:
			self.on_drops_found(drops)

		self.on_shop_update()

	def game_step(self) -> None:
		""" Executes a game engine step, will get a screenshot of the game and OCR/Match """

		if not self.engine.get_game_image():
			return

		# Check for new round and call round_change if it is a new one
		temp_round = self.engine.get_round()
		if temp_round != self.cur_round:
			self.cur_round = temp_round
			self.on_round_change(temp_round)

		self.update_stats()

	def update_stats(self) -> None:
		""" Updates health, gold and level from engine """
		tmp_gold = self.engine.get_gold()
		if tmp_gold:
			self.gold = tmp_gold
		self.health = self.engine.get_health()
		self.level = self.engine.get_level()

	def get_champs_on_bench(self, wait=True) -> None:
		""" Will go through all bench slots, if occupied gets champ from slot """

		if wait:
			sleep(2)
		self.engine.get_game_image()
		bench_slots = self.engine.get_bench_slots()

		for index, occupied in enumerate(bench_slots):
			if occupied and self.bench[index] is not None:
				continue

			if occupied:
				self.bench[index] = self.get_champion_on_bench(index)
			else:
				self.bench[index] = None

		for index, champ in enumerate(self.bench):
			if champ not in self.champs and champ is not None:
				print("Selling bench champ: ", champ)
				self.sell_bench_champion(index)

		# VirtualController.left_click(10, 10)  # Put mouse on IDLE position
		print("Bench: ", self.bench)

	def get_champion_on_bench(self, index: int) -> Optional[str]:
		""" Will return a champion from the given bench index """

		x, y, _, _ = BENCH_LOC[index].coords(self.engine.game_image.width, self.engine.game_image.height)
		VirtualController.right_click(x, y)

		self.engine.get_game_image()
		champion = self.engine.get_champ_from_details()
		return champion

	def sell_bench_champion(self, index: int) -> None:
		""" Will sell the champion on the bench index slot """

		x, y, _, _ = BENCH_LOC[index].coords(self.engine.game_image.width, self.engine.game_image.height)
		VirtualController.press_e(x, y)

		self.bench[index] = None

	def move_champion_to_board(self, bench_index: int, board_index: int) -> None:
		""" Moves a champion from bench to board """

		if not self.bench[bench_index]:
			return

		print(f"Moving {self.bench[bench_index]} to board position {board_index}")

		x, y, _, _ = BENCH_LOC[bench_index].coords(self.engine.game_image.width, self.engine.game_image.height)
		VirtualController.left_click(x, y)

		sleep(0.1)

		x, y, _, _ = BOARD_LOC[board_index].coords(self.engine.game_image.width, self.engine.game_image.height)
		VirtualController.left_click(x, y)

		self.board[board_index] = self.bench[bench_index]
		self.bench[bench_index] = None
