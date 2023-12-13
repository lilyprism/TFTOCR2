import time

import dxcam
import numpy as np
import win32con
import win32gui
from numpy import ndarray


class WindowCapture:
	w: int = 0
	h: int = 0
	hwnd = None
	cropped_x: int = 0
	cropped_y: int = 0
	offset_x: int = 0
	offset_y: int = 0
	rect = [0, 0, 0, 0]
	camera = None

	def __init__(self, window_name: str):
		self.window_name: str = window_name

	def try_get_window(self) -> bool:
		""" Tries to get the window given the name and returns whether it was successful """

		# find the handle for the window we want to capture
		tmp = win32gui.FindWindow(None, self.window_name)

		self.hwnd = tmp
		if not self.hwnd:
			return False

		# get the window size
		window_rect = win32gui.GetWindowRect(self.hwnd)
		self.rect = window_rect
		self.w = window_rect[2] - window_rect[0]
		self.h = window_rect[3] - window_rect[1]

		# set the cropped coordinates offset, so we can translate screenshot
		# images into actual screen positions
		self.offset_x = window_rect[0] + self.cropped_x
		self.offset_y = window_rect[1] + self.cropped_y

		if not self.camera:
			self.focus_window()
			self.camera = dxcam.create(region=self.rect)

		return True

	def focus_window(self) -> None:
		""" Focus the Window, bringing forward """
		win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
		win32gui.SetForegroundWindow(self.hwnd)

	def get_screen_position(self, pos) -> tuple[int, int]:
		""" Returns the screen position given the position inside the window """
		return pos[0] + self.offset_x, pos[1] + self.offset_y

	def get_screenshot(self) -> ndarray:
		""" Gets a screenshot of the Window """
		img = self.camera.grab()

		while img is None:
			img = self.camera.grab()
			time.sleep(0.1)

		# Drop the alpha channel
		img = img[..., :3]

		# Convert to contiguous array
		img = np.ascontiguousarray(img)

		return img

	@staticmethod
	def list_windows() -> None:
		""" Lists all windows """
		def winEnumHandler(hwnd, ctx):
			if win32gui.IsWindowVisible(hwnd):
				print(hex(hwnd), win32gui.GetWindowText(hwnd))

		win32gui.EnumWindows(winEnumHandler, None)
