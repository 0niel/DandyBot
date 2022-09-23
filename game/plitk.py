﻿import json
import importlib.resources
import tkinter as tk


def load_tileset(filename):
    tileset = json.loads(importlib.resources.read_text('game', filename))
    tileset["data"] = importlib.resources.read_binary('game', tileset["file"])
    return tileset


def get_tile_ppm(tileset, index):
    x = tileset["tile_width"] * (index % tileset["columns"])
    y = tileset["tile_height"] * (index // tileset["columns"])
    w = tileset["columns"] * tileset["tile_width"]
    data = bytes()
    for i in range(w * y + x, w * (y + tileset["tile_height"]) + x, w):
        data += tileset["data"][i * 3: i * 3 + tileset["tile_width"] * 3]
    return bytes("P6\n%d %d\n255\n" % (tileset["tile_width"],
                                       tileset["tile_height"]), "ascii") + data


class PliTk:
    def __init__(self, canvas, x, y, cols, rows, tileset, scale):
        self.canvas = canvas
        self.x, self.y = x, y
        self.tileset = tileset
        self.scale = scale
        self.tiles = []
        self.images = [
            tk.PhotoImage(data=get_tile_ppm(tileset, i)).zoom(scale)
            for i in range(tileset["size"])
        ]

        self.resize(cols, rows)

    def resize(self, cols, rows):
        self.cols, self.rows = cols, rows
        while self.tiles:
            self.canvas.delete(self.tiles.pop())
        for j in range(rows):
            for i in range(cols):
                self.tiles.append(self.canvas.create_image(
                    self.x + i * self.tileset["tile_width"] * self.scale,
                    self.y + j * self.tileset["tile_height"] * self.scale,
                    image=self.images[0], anchor="nw"))

    def set_tile(self, x, y, index):
        self.canvas.itemconfigure(
            self.tiles[self.cols * y + x], image=self.images[index]
        )
