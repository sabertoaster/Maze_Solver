PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": {"Login": (40, 40), "Menu": (80, 80), "Play": (80, 80), "Leaderboard": (80, 80), "Settings": (80, 80)}, # 12 cells column, 8 cells row
    "scenes": ["Login", "Menu", "Play", "Leaderboard", "Settings"],
    "initial_pos": {"Login": (12, 12), "Menu": (11, 2), "Play": (0, 0), "Leaderboard": (0, 0), "Settings": (0, 0)}  # need adjusting
}

FPS = 60