# State
# Este patrón es particularmente efectivo en juegos y 
# otras aplicaciones con múltiples modos o estados, 
#donde el comportamiento del programa varía significativamente 
#dependiendo del estado actual. En tu implementación, el patrón State 
#facilita la gestión de diferentes modos de juego, como jugar y el estado 
#de "game over", manteniendo el código organizado y facilitando la adición 
#de nuevos estados en el futuro si fuera necesario.

from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft

# Obtiene la instancia de configuración del juego
config = Settings.getInstance()

# Clase para manejar la renderización de texto en el juego Tetris
class Text:
    ''' Clase para renderizar texto en el juego Tetris. '''

    def __init__(self, app) -> None:
        ''' Inicializa la clase Text con la aplicación principal y la fuente '''
        self.app = app
        self.font = ft.Font(config.FONT_PATH)

    def get_color(self) -> tuple:
        ''' Devuelve un color basado en el tiempo para efectos dinámicos '''
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def render_text(self, text, position, fgcolor, size, bgcolor='black') -> None:
        ''' Render texto en pantalla '''
        self.font.render_to(self.app.screen, position, text=text, fgcolor=fgcolor, size=size, bgcolor=bgcolor)

    def draw_text(self, text, position, fgcolor, size, bgcolor='black') -> None:
        ''' Dibuja texto en la pantalla con los parámetros especificados '''
        self.font.render_to(self.app.screen, position, text=text, fgcolor=fgcolor, size=size, bgcolor=bgcolor)

# Métodos para dibujar diferentes textos en la pantalla (Tetris, next, score, etc.)
    def draw_tetris_text(self) -> None:
        ''' Dibuja el texto Tetris en la pantalla '''
        position = (config.WIN_W * 0.595, config.WIN_H * 0.02)
        self.draw_text('TETRIS', position, fgcolor=self.get_color(), size=config.TILE_SIZE * 1.65)

    def draw_next_text(self) -> None:
        ''' Draws the "next" text on the screen '''
        position = (config.WIN_W * 0.65, config.WIN_H * 0.22)
        self.draw_text('next', position, fgcolor='orange', size=config.TILE_SIZE * 1.4)

    def draw_score_text(self) -> None:
        ''' Dibuja el texto 'next' en la pantalla '''
        position = (config.WIN_W * 0.64, config.WIN_H * 0.67)
        self.draw_text('score', position, fgcolor='orange', size=config.TILE_SIZE * 1.4)

    def draw_score_value(self) -> None:
        ''' Dibuja el valor de la puntuación en la pantalla '''
        position = (config.WIN_W * 0.64, config.WIN_H * 0.8)
        self.draw_text(f'{self.app.tetris.score}', position, fgcolor='white', size=config.TILE_SIZE * 1.8)

    def draw(self) -> None:
        ''' Dibuja el estado actual del juego '''
        self.draw_tetris_text()
        self.draw_next_text()
        self.draw_score_text()
        self.draw_score_value()


# Definición de los estados
# Clase base para los estados del juego Tetris
class TetrisState:
    ''' Clase base para los estados del juego Tetris '''

    def handle_input(self, tetris, event) -> None:
        ''' Maneja la entrada del usuario en el juego '''
        pass

    def update(self, tetris) -> None:
        ''' Actualiza el estado del juego '''
        pass

    def draw(self, tetris) -> None:
        ''' Dibuja el estado del juego '''
        pass

class PlayingState(TetrisState):
    ''' Representa el estado de juego en Tetris '''

    def handle_input(self, tetris, event) -> None:
        ''' Maneja la entrada del usuario en el estado de juego '''
        key_actions = {
            pg.K_LEFT: lambda: tetris.tetromino.move(direction="left"),
            pg.K_RIGHT: lambda: tetris.tetromino.move(direction="right"),
            pg.K_UP: tetris.tetromino.rotate,
            pg.K_DOWN: lambda: setattr(tetris, 'speed_up', True)
        }

        if event.type == pg.KEYDOWN and event.key in key_actions:
            key_actions[event.key]()


    def update(self, tetris) -> None:
        ''' Actualiza PlayingState '''
        trigger = [tetris.app.anim_trigger, tetris.app.fast_anim_trigger][tetris.speed_up]
        if trigger:
            tetris.check_full_lines()
            tetris.tetromino.update()
            tetris.check_tetromino_landing()
            tetris.get_score()
        tetris.sprite_group.update()

    def draw(self, tetris) -> None:
        ''' Dibuja PlayingState '''
        tetris.draw_grid()
        tetris.sprite_group.draw(tetris.app.screen)


class GameOverState(TetrisState):
    ''' Representa estado Game Over del juego de Tetris '''

    def update(self, tetris) -> None:
        ''' Actualiza GameOverState '''
        pg.time.wait(1000)
        tetris.__init__(tetris.app)  # Reiniciar el juego


# Clase principal Tetris con el patrón State
class Tetris:
    ''' Inicializa la clase Tetris '''

    def __init__(self, app) -> None:
        ''' Inicializa la clase Tetris '''
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = [[0 for x in range(config.FIELD_W)] for y in range(config.FIELD_H)]
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

        # Inicializar el estado actual
        self.state = PlayingState()

    def get_score(self) -> None:
        ''' Actualiza puntaje '''
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def check_full_lines(self) -> None:
        ''' Verifica y limpia líneas completa '''
        rows_to_clear = []

        for y in range(config.FIELD_H - 1, -1, -1):
            if sum(map(bool, self.field_array[y])) == config.FIELD_W:
                rows_to_clear.append(y)

        for row in rows_to_clear:
            self.clear_line(row)

    def clear_line(self, row) -> None:
        ''' Limpia una línea específica en el array del campo'''
        for x in range(config.FIELD_W):
            self.field_array[row][x].alive = False
            self.field_array[row][x] = 0

        self.move_blocks_down(row)

        self.full_lines += 1

    def move_blocks_down(self, cleared_row) -> None:
        ''' Mueve hacia abajo una fila los bloques que están sobre la fila limpiada '''
        for y in range(cleared_row, 0, -1):
            for x in range(config.FIELD_W):
                self.field_array[y][x] = self.field_array[y - 1][x]

                if self.field_array[y][x]:
                    self.field_array[y][x].pos = config.vec(x, y)


    def put_tetromino_blocks_in_array(self) -> None:
        ''' Agrega los bloques del tetromino al arreglo del campo '''
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def is_game_over(self) -> bool:
        ''' Verifica si el juego ha terminado '''
        return self.tetromino.blocks[0].pos.y == config.INIT_POS_OFFSET[1]

    def check_tetromino_landing(self) -> None:
        ''' Verifica si el tetromino ha aterrizado '''
        if self.tetromino.landing:
            if self.is_game_over():
                self.state = GameOverState()  # Cambiar al estado de Game Over
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, event) -> None:
        ''' Controla el juego basado en la entrada '''
        self.state.handle_input(self, event)

    def update(self) -> None:
        ''' Actualiza el estado del juego'''
        self.state.update(self)

    def draw(self) -> None:
        ''' Dibuja el estado actual del juego '''
        self.state.draw(self)

    def draw_grid(self) -> None:
        ''' Dibuja la cuadrícula en la pantalla  '''
        for x in range(config.FIELD_W):
            for y in range(config.FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x * config.TILE_SIZE, y * config.TILE_SIZE, config.TILE_SIZE, config.TILE_SIZE), 1)
