import sys
import pygame
import numpy as np
import cv2
from enum import Enum

class Camera:
    def __init__(self, screen, size: tuple[int, int], resolution: tuple[int, int]):
        self.size = size
        self.resolution = resolution
        self.screen = screen

