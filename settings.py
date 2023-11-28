import pygame as pg

class Settings:
    ''' Clase Singleton para la configuración del juego '''
    # Este patrón garantiza que todas las partes del juego accedan 
    # a una sola instancia de la configuración, lo cual es importante 
    # para mantener la consistencia en las configuraciones del juego en todas partes.

    __instance = None

    @staticmethod
    def getInstance() -> __instance:
        ''' Devuelve la instancia de la clase Settings. Si no existe, la crea y la devuelve '''
        # Si no existe una instancia, se crea una nueva
        if Settings.__instance is None:
            Settings()
        return Settings.__instance
    
    def __init__(self) -> None:
        ''' Inicializa la clase Settings. Si ya existe, lanza una excepción '''
        # Asegurar que solo haya una instancia de la clase (patrón Singleton)
        if Settings.__instance is not None:
            raise Exception("La clase Settings es un singleton")
        else:
            Settings.__instance = self
            # Vector2 para operaciones de vectores
            self.vec = pg.math.Vector2
            # Configuraciones de juego
            self.FPS = 60
            self.FIELD_COLOR = (48, 39, 32)
            self.BG_COLOR = (24, 89, 117)

            # Rutas a los directorios de recursos
            self.SPRITE_DIR_PATH = 'assets/sprites'
            self.FONT_PATH = 'assets/font/FREAKSOFNATUREMASSIVE.ttf'

            # Intervalos de tiempo para animaciones (en milisegundos)
            self.ANIM_TIME_INTERVAL = 150
            self.FAST_ANIM_TIME_INTERVAL = 15

            # Configuraciones de tamaño de los elementos del juego
            self.TILE_SIZE = 50
            self.FIELD_SIZE = self.FIELD_W, self.FIELD_H = 9, 15
            self.FIELD_RES = self.FIELD_W * self.TILE_SIZE, self.FIELD_H * self.TILE_SIZE

            # Escalas y resolución de la ventana del juego
            self.FIELD_SCALE_W, self.FIELD_SCALE_H = 1.7, 1.0
            self.WIN_RES = self.WIN_W, self.WIN_H = self.FIELD_RES[0] * self.FIELD_SCALE_W, self.FIELD_RES[1] * self.FIELD_SCALE_H

            # Desplazamientos iniciales y configuraciones de movimiento
            self.INIT_POS_OFFSET = self.vec(self.FIELD_W // 2 - 1, 0)
            self.NEXT_POS_OFFSET = self.vec(self.FIELD_W * 1.3, self.FIELD_H * 0.45)
            self.MOVE_DIRECTIONS = {'left': self.vec(-1, 0), 'right': self.vec(1, 0), 'down': self.vec(0, 1)}

            # Definiciones de los Tetrominoes (piezas del Tetris) 
            # ENUMS Cada valor enum puede asociarse con las coordenadas 
            # específicas de ese tetromino o incluso con su matriz de representación.
            self.TETROMINOES = {
                'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
                'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
                'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
                'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
                'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
                'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
                'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
            }
