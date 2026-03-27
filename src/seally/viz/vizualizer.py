from typing import Tuple
import numpy as np
import pygame
from seally.common.grid_cell import GridCell
from seally.common.path import Path
from seally.env.gridmap import GridMap

class Visualizer2D:
    def __init__(self):
        pygame.init()
        self.tile_size = 64
        self.padding = 40
        self.bg_color = (245, 240, 232)
        self.border_color = (180, 178, 172)
        self.grid_color = (210, 208, 200)
        self.path_color = (29, 158, 117)
        self.clock = pygame.time.Clock()
        self.running = False
        self.screen = None

    def _init_screen(self, env: GridMap):
        screen_w = env.x_dim * self.tile_size + self.padding * 2
        screen_h = env.y_dim * self.tile_size + self.padding * 2
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption("Seally")

    def _build_map_surface(self, env: GridMap) -> pygame.Surface:
        grey_map = np.where(env.map == 0, 240, 60).astype(np.uint8)
        rgb_map = np.zeros((*grey_map.shape, 3), dtype=np.uint8)
        rgb_map[..., 0] = grey_map
        rgb_map[..., 1] = grey_map
        rgb_map[..., 2] = grey_map
        rgb_map[env.map > 0] = [50, 47, 44]

        surf = pygame.transform.scale(
            pygame.surfarray.make_surface(rgb_map.transpose(1, 0, 2)),
            (env.x_dim * self.tile_size, env.y_dim * self.tile_size)
        )
        for x in range(env.x_dim):
            pygame.draw.line(surf, self.grid_color,
                             (x * self.tile_size, 0),
                             (x * self.tile_size, env.y_dim * self.tile_size))
        for y in range(env.y_dim):
            pygame.draw.line(surf, self.grid_color,
                             (0, y * self.tile_size),
                             (env.x_dim * self.tile_size, y * self.tile_size))
        return surf

    def _draw_border(self, env: GridMap):
        border_rect = pygame.Rect(
            self.padding - 2,
            self.padding - 2,
            env.x_dim * self.tile_size + 4,
            env.y_dim * self.tile_size + 4
        )
        pygame.draw.rect(self.screen, self.border_color, border_rect, width=2, border_radius=4)

    def _draw_path(self, path_cells: list):
        for cell in path_cells:
            rect = pygame.Rect(
                self.padding + cell.x * self.tile_size + 2,
                self.padding + cell.y * self.tile_size + 2,
                self.tile_size - 4,
                self.tile_size - 4
            )
            pygame.draw.rect(self.screen, self.path_color, rect, border_radius=6)

    def _draw_start_goal(self, start, goal):
        for cell, color in [(start, (55, 138, 221)), (goal, (216, 90, 48))]:
            if cell:
                rect = pygame.Rect(
                    self.padding + cell.x * self.tile_size + 2,
                    self.padding + cell.y * self.tile_size + 2,
                    self.tile_size - 4,
                    self.tile_size - 4
                )
                pygame.draw.rect(self.screen, color, rect, border_radius=6)

    def run_visualization(self, path: Path, env: GridMap):
        self._init_screen(env)
        map_surf = self._build_map_surface(env)
        path_cells = list(path)
        start = path_cells[0] if path_cells else None
        goal  = path_cells[-1] if path_cells else None

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.bg_color)
            self.screen.blit(map_surf, (self.padding, self.padding))
            self._draw_border(env)
            self._draw_path(path_cells)
            self._draw_start_goal(start, goal)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()


class InteractiveVisualizer2D(Visualizer2D):
    def __init__(self, planner):
        super().__init__()
        self.planner = planner
        self.source = None
        self.goal = None
        self.path_cells = []

    def _screen_to_cell(self, mouse_pos: Tuple[int, int], env: GridMap):
        x = (mouse_pos[0] - self.padding) // self.tile_size
        y = (mouse_pos[1] - self.padding) // self.tile_size
        cell = GridCell(x, y)
        if env.in_bounds(cell) and not env.is_occupied(cell):
            return cell
        return None

    def _try_plan(self):
        if self.source and self.goal:
            try:
                path = self.planner.compute_path(self.source, self.goal)
                self.path_cells = list(path)
            except Exception:
                self.path_cells = []

    def _draw_instructions(self):
        font = pygame.font.SysFont("monospace", 13)
        if not self.source:
            msg = "Left click to set source"
        elif not self.goal:
            msg = "Left click to set goal"
        else:
            msg = "Right click to reset"
        surf = font.render(msg, True, (120, 115, 105))
        self.screen.blit(surf, (self.padding, self.padding // 4))

    def run_visualization(self, env: GridMap):
        self._init_screen(env)
        map_surf = self._build_map_surface(env)

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        cell = self._screen_to_cell(event.pos, env)
                        if cell:
                            if not self.source:
                                self.source = cell
                            elif not self.goal:
                                self.goal = cell
                                self._try_plan()

                    elif event.button == 3:
                        self.source = None
                        self.goal = None
                        self.path_cells = []

            self.screen.fill(self.bg_color)
            self.screen.blit(map_surf, (self.padding, self.padding))
            self._draw_border(env)
            self._draw_path(self.path_cells)
            self._draw_start_goal(self.source, self.goal)
            self._draw_instructions()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()