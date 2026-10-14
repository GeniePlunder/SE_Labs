"""
GameEngine: owns the frog and all vehicles, and runs one frame's worth
of game logic.

Game states:
  playing   - normal play, arrow keys move the frog
  hit       - frog was just hit; it flashes in place for a moment so the
              player can see what happened, then respawns (or game over)
  game_over - no lives left; only R works
  won       - frog reached the goal; only R works

Each attempt (a new game, or a respawn after losing a life) gets a
30-second countdown. Running out of time costs a life, exactly like
being hit.
"""

import math
import random

import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS, GOAL_ROW, ROAD_ROWS, START_ROW, CELL_SIZE, WIDTH, HEIGHT,
)

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]   # one entry per road row, alternating direction

FPS = 60                 # must match clock.tick() in main.py
STARTING_LIVES = 3
TIME_LIMIT_SECONDS = 30
TIME_LIMIT_FRAMES = TIME_LIMIT_SECONDS * FPS
LOW_TIME_SECONDS = 5     # timer turns red at or below this
HIT_PAUSE_FRAMES = 45    # ~0.75 s at 60 FPS: how long the hit is shown before respawn
HIT_BLINK_FRAMES = 6     # frog alternates colour every 6 frames while hit

STATE_PLAYING = "playing"
STATE_HIT = "hit"
STATE_GAME_OVER = "game_over"
STATE_WON = "won"


class GameEngine:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """Full restart (R key): new frog, new vehicles, all state reset."""
        self._build_entities()
        self.lives = STARTING_LIVES
        self.score = 0
        self.state = STATE_PLAYING
        self.hit_timer = 0
        self.time_left = TIME_LIMIT_FRAMES
        self.fail_reason = ""

    def _build_entities(self):
        start_col = GRID_COLS // 2
        self.frog = Frog(
            col=start_col, row=START_ROW,
            start_col=start_col, start_row=START_ROW,
            cols=GRID_COLS, start_row_limit=START_ROW,
        )
        frog_x_range = (start_col * CELL_SIZE, start_col * CELL_SIZE + CELL_SIZE)

        self.vehicles = []
        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]
            vehicle_width = 40 if i % 2 == 0 else 70   # mix of cars and wider trucks
            spacing = 300
            count = 2

            # Try a few random phases and keep the first one that doesn't
            # already overlap the frog's starting column - guarantees a
            # safe first lane instead of leaving it to chance.
            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True
                for n in range(count):
                    offset = phase + n * spacing
                    x = offset if speed > 0 else WIDTH - offset - vehicle_width
                    positions.append(x)
                    if not (x + vehicle_width <= frog_x_range[0] or x >= frog_x_range[1]):
                        safe = False
                if safe:
                    break

            for x in positions:
                self.vehicles.append(Vehicle(x=x, row=row, width=vehicle_width,
                                              height=CELL_SIZE - 8, speed=speed))

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.reset_game()
            return
        if self.state != STATE_PLAYING:
            return  # no hopping while hit, after game over, or after a win

        if key == pygame.K_UP:
            self.frog.move(0, -1)
        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)
        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)
        else:
            return
        # Check every cell the frog lands on, not just where it ends up
        # this frame - otherwise two quick hops in one frame could skip
        # a vehicle or step onto and off the goal unnoticed.
        self._check_frog()

    def update(self):
        for v in self.vehicles:
            v.update(road_width_px=WIDTH)

        if self.state == STATE_PLAYING:
            self.time_left -= 1
            self._check_frog()   # vehicles moved, so re-check even if the frog didn't
            if self.state == STATE_PLAYING and self.time_left <= 0:
                self.lose_life("Time's up!")

        elif self.state == STATE_HIT:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                if self.lives > 0:
                    self.frog.reset()
                    self.time_left = TIME_LIMIT_FRAMES   # new attempt, fresh 30 s
                    self.state = STATE_PLAYING
                else:
                    self.state = STATE_GAME_OVER   # frog stays where it was hit

    def _check_frog(self):
        """Collision first, then goal. Only called while playing."""
        if check_collision(self.frog, self.vehicles):
            self.lose_life("Splat!")
        elif self.frog.row == GOAL_ROW:
            self._win()

    def lose_life(self, reason):
        """One failed attempt (hit by a vehicle or out of time)."""
        self.lives -= 1
        self.fail_reason = reason
        self.state = STATE_HIT
        self.hit_timer = HIT_PAUSE_FRAMES

    def _win(self):
        self.score += 1          # runs once: state leaves PLAYING immediately
        self.frog.reset()
        self.state = STATE_WON

    def draw(self, surface, font):
        from game import renderer

        frog_color = renderer.COLOR_FROG
        if self.state == STATE_HIT:
            blink_on = (self.hit_timer // HIT_BLINK_FRAMES) % 2 == 0
            frog_color = renderer.COLOR_FROG_HIT if blink_on else renderer.COLOR_TEXT
        elif self.state == STATE_GAME_OVER:
            frog_color = renderer.COLOR_FROG_HIT

        renderer.draw_scene(surface, self.frog, self.vehicles, frog_color)
        renderer.draw_text(surface, font, f"Lives: {self.lives}   Score: {self.score}", (10, 14))

        seconds_left = max(0, math.ceil(self.time_left / FPS))
        time_color = renderer.COLOR_TEXT
        if self.state == STATE_PLAYING and seconds_left <= LOW_TIME_SECONDS:
            time_color = renderer.COLOR_TIME_LOW
        renderer.draw_text(surface, font, f"Time: {seconds_left:2d}", (WIDTH - 110, 14), time_color)
        renderer.draw_text(surface, font, "Arrow keys to move. R to restart.", (10, HEIGHT - 24))

        if self.state == STATE_HIT:
            renderer.draw_banner(surface, font, self.fail_reason)
        elif self.state == STATE_GAME_OVER:
            renderer.draw_banner(surface, font, "Game Over - press R to restart")
        elif self.state == STATE_WON:
            renderer.draw_banner(surface, font, "You Won! - press R to play again")