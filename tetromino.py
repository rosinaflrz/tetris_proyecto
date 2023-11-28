# Composite Pattern
# Cada Tetromino es una agrupación de varios Block. 
# Esta relación es una forma simplificada del patrón Compuesto, 
# donde Tetromino actúa como el componente compuesto y cada Block 
# como un componente hoja.

from abc import ABC, abstractmethod
import pygame as pg
from settings import Settings
import random

config = Settings.getInstance()

class Component(ABC):
    ''' Clase abstracta para los componentes del juego '''

    @abstractmethod
    def draw(self) -> None:
        ''' Dibuja el componente a ser implementado '''
        pass

    @abstractmethod
    def is_collide(self, pos) -> bool:
        ''' Verifica si el componente colisiona con otro componente '''
        pass

    @abstractmethod
    def move(self, direction) -> None:
        ''' Mueve el componente '''
        pass

    @abstractmethod
    def update(self) -> None:
        ''' Actualiza el componente a ser implementado por las subclases '''
        pass

class Block(Component, pg.sprite.Sprite):
    ''' Clase concreta para los bloques del juego '''

    def __init__(self, tetromino, pos) -> None:
        ''' Inicializa la clase Block '''
        super().__init__(tetromino.tetris.sprite_group)
        self.tetromino = tetromino
        self.pos = config.vec(pos) + config.INIT_POS_OFFSET
        self.next_pos = config.vec(pos) + config.NEXT_POS_OFFSET
        self.alive = True

        self._initialize_graphics()

    def _initialize_graphics(self) -> None:
        ''' Inicializa los gráficos del bloque '''
        self.image = self.tetromino.image
        self.rect = self.image.get_rect()

        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0

    def sfx_end_time(self) -> bool:
        ''' Verifica si el tiempo de efecto ha terminado '''
        if self.tetromino.tetris.app.anim_trigger:
            self.cycle_counter += 1
            return self.cycle_counter > self.sfx_cycles

        return False

    def sfx_run(self) -> None:
        ''' Ejecuta el efecto en el bloque '''
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    def is_alive(self) -> None:
        ''' Verifica si el bloque está vivo y ejecuta el efecto si no lo está '''
        if not self.alive and not self.sfx_end_time():
            self.sfx_run()
        elif not self.alive:
            self.kill()

    def rotate(self, pivot_pos) -> None:
        ''' Rota el bloque '''
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self) -> None:
        ''' Establece la posición del bloque '''
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * config.TILE_SIZE

    def draw(self) -> None:
        ''' Dibuja el bloque '''
        self.is_alive()
        self.set_rect_pos()

    def is_collide(self, pos) -> bool:
        ''' Verifica si el bloque colisiona con otro bloque '''
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < config.FIELD_W and y < config.FIELD_H and (
                y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True

    def move(self, direction) -> None:
        ''' Mueve el bloque '''
        pass  # No se mueve

    def update(self):
        ''' Actualiza el bloque '''
        self.draw()


class Tetromino(Component):
    ''' Clase concreta para los tetrominos del juego '''

    def __init__(self, tetris, current=True) -> None:
        ''' Inicializa la clase Tetromino '''
        self.tetris = tetris
        self.shape = random.choice(list(config.TETROMINOES.keys()))
        self.image = random.choice(tetris.app.images)
        self.blocks = [Block(self, pos) for pos in config.TETROMINOES[self.shape]]
        self.landing = False
        self.current = current

    def rotate(self) -> None:
        ''' Rota el tetromino '''
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

    def is_collide(self, block_positions) -> bool:
        ''' Verifica si el tetromino colisiona con otro tetromino '''
        return any(map(Block.is_collide, self.blocks, block_positions))

    def move(self, direction) -> None:
        ''' Mueve el tetromino '''
        move_direction = config.MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    def draw(self) -> None:
        ''' Dibuja el tetromino '''
        for block in self.blocks:
            block.draw()

    def update(self) -> None:
        ''' Actualiza el tetromino '''
        self.move(direction='down')