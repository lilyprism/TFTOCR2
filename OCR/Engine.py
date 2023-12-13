from difflib import SequenceMatcher
from typing import List, Optional
import requests
import urllib3
import cv2 as cv
import numpy as np
from PIL import Image
from imutils.object_detection import non_max_suppression
from numpy import ndarray
from tesserocr import PyTessBaseAPI

from Data import *
from OCR.Capturer import WindowCapture


class OCREngine(object):

	def __init__(self) -> None:
		self.tess_api: PyTessBaseAPI = PyTessBaseAPI(path="./tessdata", psm=7)
		self.game_image: Image = None
		self.game_cap: WindowCapture = WindowCapture("League of Legends (TM) Client")  # League of Legends (TM) Client

		# Disable requests warnings
		urllib3.disable_warnings()

		# Load matching images to memory
		self.MATCHING_IMAGES = {
			"gray_random_drop": cv.imread(r".\OCR\Matching\gray_random_drop.jpg", cv.IMREAD_GRAYSCALE),
			"blue_random_drop": cv.imread(r".\OCR\Matching\blue_random_drop.jpg", cv.IMREAD_GRAYSCALE),
			"vote"            : cv.imread(r".\OCR\Matching\vote.jpg", cv.IMREAD_GRAYSCALE),
			# "book": cv.imread(r".\OCR\Matching\book.jpg", cv.IMREAD_GRAYSCALE),
			# "anvil": cv.imread(r".\OCR\Matching\anvil.jpg", cv.IMREAD_GRAYSCALE),
		}

	def get_game_image(self) -> bool:
		""" Gets a screenshot of the game """
		if not self.get_level():
			return False

		if self.game_cap.try_get_window():
			self.game_image = Image.fromarray(self.game_cap.get_screenshot())
			self.game_image.save("debug.bmp")  # TODO: Add this only if DEBUG is active
			return True
		return False

	def get_round(self) -> Optional[str]:
		""" Returns the current round """

		image: Image = self.game_image.crop(ROUND_BOX.coords(self.game_image.width, self.game_image.height))
		cut_img: Image = image.crop(ROUND_POS_1.coords(image.width, image.height))

		round = self.recognize(cut_img, ROUND_WHITELIST)

		if round not in ROUNDS:
			cut_img: Image = image.crop(ROUND_POS_2.coords(image.width, image.height))
			round = self.recognize(cut_img, ROUND_WHITELIST)

		return round if round in ROUNDS else None

	def get_gold(self) -> Optional[int]:
		""" Returns current gold for tactician """

		image: Image = self.game_image.crop(GOLD_BOX.coords(self.game_image.width, self.game_image.height))

		try:
			return int(self.recognize(image, GOLD_WHITELIST))
		except ValueError:
			return None

	def get_shop(self) -> List[str]:
		""" Returns the list of champions in the shop if any """

		image: Image = self.game_image.crop(SHOP_BOX.coords(self.game_image.width, self.game_image.height))

		shop_champs: List[str] = []
		for champion_position in CHAMP_NAME_POS:
			champ_box: Image = image.crop(champion_position.coords(image.width, image.height))

			name: str = self.recognize(champ_box, CHAMP_NAME_WHITELIST)

			# Correct mistakes from OCR
			name = self.get_valid_champ(name)
			shop_champs.append(name)

		return shop_champs

	def get_regions(self) -> List[str]:
		""" Returns the list of regions """

		regions: List[str] = []
		for region in REGIONS_POS:
			region_box: Image = self.game_image.crop(region.coords(self.game_image.width, self.game_image.height))

			name: str = self.recognize(region_box, CHAMP_NAME_WHITELIST)

			# Correct mistakes from OCR
			name = self.get_valid_region(name)
			regions.append(name)

		return regions

	def get_random_drop_locations(self) -> List[tuple]:
		""" Returns a list of all locations (if any) of random drops """

		image: Image = self.game_image.crop(BOARD_BOX.coords(self.game_image.width, self.game_image.height))

		template1 = self.MATCHING_IMAGES.get("blue_random_drop")
		template2 = self.MATCHING_IMAGES.get("gray_random_drop")

		locs = self.match_template(image, template1) + self.match_template(image, template2)

		# Translate to screen coordinates since we crop the initial image
		locs = [BOARD_BOX.to_screen_coords(loc, self.game_image.width, self.game_image.height) for loc in locs]

		return locs

	def get_vote_locations(self) -> List[tuple]:
		""" Returns the location (if any) of vote button """

		template1 = self.MATCHING_IMAGES.get("vote")

		locs = self.match_template(self.game_image, template1)

		return locs

	def get_region_augment(self) -> str:
		""" Returns the current region augment """

		image: Image = self.game_image.crop(REGION_AUGMENT_POS.coords(self.game_image.width, self.game_image.height))
		region: str = self.recognize(image, CHAMP_NAME_WHITELIST)

		return self.get_valid_region(region)

	def get_augments(self) -> List[str]:
		""" Returns a list of augments on screen """

		augments: List[str] = []
		for augment in AUGMENTS_POS:
			augment_box: Image = self.game_image.crop(augment.coords(self.game_image.width, self.game_image.height))

			name: str = self.recognize(augment_box, AUGMENTS_NAME_WHITELIST)

			# Correct mistakes from OCR
			name = self.get_valid_augment(name)
			augments.append(name)

		return augments

	def get_champ_from_details(self) -> Optional[str]:
		""" Will return a champion (if any) from details window """

		image: Image = self.game_image.crop(CHAMPION_DETAILS_NAME.coords(self.game_image.width, self.game_image.height))

		name: str = self.recognize(image, CHAMP_NAME_WHITELIST)

		# Correct mistakes from OCR
		name = self.get_valid_champ(name)
		return name

	def get_bench_slots(self) -> list[bool]:
		""" Will return a list of booleans representing if its occupied """

		bench: list[bool] = []
		for pos in BENCH_HEALTH_POS:
			image: Image = self.game_image.crop(pos.coords(self.game_image.width, self.game_image.height))
			image_arr = np.array(image)

			if not (np.abs(image_arr - (0, 210, 5)) <= 25).all(axis=2).any():
				bench.append(False)
			else:
				bench.append(True)

		return bench

	@staticmethod
	def get_level() -> Optional[int]:
		""" Returns the level for the tactician """

		try:
			response = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', timeout=1, verify=False)
			return int(response.json()['activePlayer']['level'])
		except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, KeyError):
			return None

	@staticmethod
	def get_health() -> Optional[int]:
		""" Returns the health for the tactician """

		try:
			response = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', timeout=1, verify=False)
			return int(response.json()['activePlayer']['championStats']["currentHealth"])
		except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, KeyError):
			return None

	@staticmethod
	def get_valid_champ(champ_name: str) -> Optional[str]:
		""" Will return a champion name given the champion name partially correct """

		if champ_name in CHAMPIONS:
			return champ_name

		for champ in CHAMPIONS:
			if SequenceMatcher(a=champ, b=champ_name).ratio() >= 0.7:
				return champ
		return None

	@staticmethod
	def get_valid_region(region_name: str) -> Optional[str]:
		""" Will return a region name given the region name partially correct """

		if region_name in REGIONS:
			return region_name

		for region in REGIONS:
			if SequenceMatcher(a=region, b=region_name).ratio() >= 0.7:
				return region
		return None

	@staticmethod
	def get_valid_augment(augment_name: str) -> Optional[str]:
		""" Will return an augment name given the augment name partially correct """

		if augment_name in AUGMENTS:
			return augment_name

		for augment in AUGMENTS:
			if SequenceMatcher(a=augment, b=augment_name).ratio() >= 0.7:
				return augment
		return None

	@staticmethod
	def match_template(img: Image, template: ndarray, threshold=0.70) -> List[tuple]:
		""" Match a template image with the given image and return a list of locations """

		# Convert image from PIL to CV
		img = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)

		# Create HeatMap from template image matching
		heat_map = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)

		# Filter threshold
		(yCoords, xCoords) = np.where(heat_map >= threshold)

		# Perform non-maximum suppression.
		template_h, template_w = template.shape[:2]
		rects = []
		for (x, y) in zip(xCoords, yCoords):
			rects.append((x, y, x + template_w, y + template_h))
		pick: list = non_max_suppression(np.array(rects))

		# For Debugging purposes
		# TODO: Do this only in DEBUG
		for (startX, startY, endX, endY) in pick:
			cv.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)

		cv.imwrite('matches.png', img)

		return [((endX - startX) / 2 + startX, (endY - startY) / 2 + startY) for (startX, startY, endX, endY) in pick]

	def recognize(self, img: Image, whitelist: str = "") -> str:
		""" Tries to recognize text in the given image """

		if whitelist != "":
			self.tess_api.SetVariable("tessedit_char_whitelist", whitelist)

		# Convert Image to array so we can use CV
		arr = np.array(img)

		# Convert to grayscale
		arr = cv.cvtColor(arr, cv.COLOR_BGR2GRAY)

		# Apply thresholding
		arr = cv.threshold(arr, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

		pil_img = Image.fromarray(arr)
		# pil_img.show()

		self.tess_api.SetImage(pil_img)
		self.tess_api.Recognize()
		return self.tess_api.GetUTF8Text().replace("\n", "")
