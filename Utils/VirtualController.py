import random
import pydirectinput


class VirtualController(object):

	@staticmethod
	def left_click(x: float, y: float) -> None:
		""" Will execute a left mouse button click """

		offset: int = random.randint(-2, 2)
		pydirectinput.moveTo(int(x) - offset, int(y) - offset)
		pydirectinput.mouseDown()
		pydirectinput.mouseUp()

	@staticmethod
	def right_click(x: float, y: float) -> None:
		""" Will execute a right mouse button click """

		x, y = int(x), int(y)
		offset: int = random.randint(-2, 2)
		pydirectinput.moveTo(int(x) - offset, int(y) - offset)
		pydirectinput.mouseDown(button="right")
		pydirectinput.mouseUp(button="right")

	@staticmethod
	def press_f() -> None:
		""" Will press F """

		pydirectinput.press("f")

	@staticmethod
	def press_d() -> None:
		""" Will press D """

		pydirectinput.press("d")

	@staticmethod
	def press_e(x: float, y: float) -> None:
		""" Will press E """

		x, y = int(x), int(y)
		offset: int = random.randint(-2, 2)
		pydirectinput.moveTo(int(x) - offset, int(y) - offset)
		pydirectinput.press("e")
