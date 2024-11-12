import random
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

class VirtualController:
    # Controller-Objekte für Maus und Tastatur
    mouse = MouseController()
    keyboard = KeyboardController()

    @staticmethod
    def left_click(x: float, y: float) -> None:
        """ Führt einen linken Mausklick aus """
        offset = random.randint(-2, 2)
        VirtualController.mouse.position = (x + offset, y + offset)
        VirtualController.mouse.click(Button.left)

    @staticmethod
    def right_click(x: float, y: float) -> None:
        """ Führt einen rechten Mausklick aus """
        offset = random.randint(-2, 2)
        VirtualController.mouse.position = (x + offset, y + offset)
        VirtualController.mouse.click(Button.right)

    @staticmethod
    def press_f() -> None:
        """ Drückt die Taste F """
        VirtualController.keyboard.press('f')
        VirtualController.keyboard.release('f')

    @staticmethod
    def press_d() -> None:
        """ Drückt die Taste D """
        VirtualController.keyboard.press('d')
        VirtualController.keyboard.release('d')

    @staticmethod
    def press_e(x: float, y: float) -> None:
        """ Bewegt die Maus und drückt die Taste E """
        offset = random.randint(-2, 2)
        VirtualController.mouse.position = (x + offset, y + offset)
        VirtualController.keyboard.press('e')
        VirtualController.keyboard.release('e')
