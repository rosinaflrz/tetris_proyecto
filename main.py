# main

from settings import *
from tetris import Tetris, Text
import sys
import pathlib

class App:
    ''' Clase para la aplicación principal '''

    def __init__(self) -> None:
        ''' Inicializa la clase App '''
        # Obtener la configuración del juego
        self.config = Settings.getInstance()
        # Inicializar Pygame y la ventana del juego
        self.initialize_pygame()
        # Cargar imágenes para el juego
        self.images = self.load_images()
        # Crear una instancia del juego Tetris
        self.tetris = Tetris(self)
        # Crear una instancia para manejar el texto en el juego
        self.text = Text(self)

    def initialize_pygame(self) -> None:
        ''' Inicializa pygame y configura la ventana '''
        # Inicializar Pygame
        pg.init()
        # Configurar el título de la ventana
        pg.display.set_caption('Tetris')
        # Establecer la resolución de la ventana
        self.screen = pg.display.set_mode(self.config.WIN_RES)
        # Configurar el reloj para controlar los FPS
        self.clock = pg.time.Clock()
        # Configurar los temporizadores del juego
        self.set_timer()

    def load_images(self) -> list:
        ''' Carga las imágenes del juego '''
        # Buscar archivos de imagen en el directorio especificado
        files = [item for item in pathlib.Path(self.config.SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        # Cargar las imágenes y ajustar su tamaño
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (self.config.TILE_SIZE, self.config.TILE_SIZE)) for image in images]
        return images

    def set_timer(self) -> None:
        ''' Configura el temporizador del juego '''
        # Definir eventos personalizados para los temporizadores
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        # Inicializar variables para detectar los disparos de los temporizadores
        self.anim_trigger = False
        self.fast_anim_trigger = False
        # Establecer los temporizadores
        pg.time.set_timer(self.user_event, self.config.ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, self.config.FAST_ANIM_TIME_INTERVAL)

    def update(self) -> None:
        ''' Actualiza el juego '''
        # Actualizar la lógica del juego Tetris
        self.tetris.update()
        # Controlar los FPS
        self.clock.tick(self.config.FPS)

    def draw(self) -> None:
        ''' Dibuja el juego '''
        # Rellenar el fondo de la pantalla
        self.screen.fill(color=self.config.BG_COLOR)
        # Rellenar el área del campo de juego
        self.screen.fill(color=self.config.FIELD_COLOR, rect=(0, 0, *self.config.FIELD_RES))
        # Dibujar los elementos del juego Tetris
        self.tetris.draw()
        # Dibujar el texto en pantalla
        self.text.draw()
        # Actualizar la pantalla
        pg.display.flip()

    def check_events(self) -> None:
        ''' Revisa los eventos del juego '''
        # Reiniciar los disparadores de los temporizadores
        self.anim_trigger = False
        self.fast_anim_trigger = False
        # Asociar eventos con sus manejadores
        event_handlers = {
            pg.QUIT: self.quit_game,
            pg.KEYDOWN: self.handle_keydown,
            self.user_event: self.handle_user_event,
            self.fast_user_event: self.handle_fast_user_event,
        }

        # Procesar los eventos de Pygame
        for event in pg.event.get():
            handler = event_handlers.get(event.type)
            if handler:
                handler(event)

    def handle_keydown(self, event) -> None:
        ''' Maneja los eventos de tecla presionada '''
        # Si se presiona ESC, salir del juego
        if event.key == pg.K_ESCAPE:
            self.quit_game()
        else:
            # De lo contrario, manejar el control del Tetris
            self.tetris.control(event)

    def handle_user_event(self, event) -> None:
        ''' Maneja el evento de usuario '''
        # Activar el disparador del evento
        self.anim_trigger = True

    def handle_fast_user_event(self, event) -> None:
        ''' Maneja el evento de usuario rápido '''
        # Activar el disparador del evento rápido
        self.fast_anim_trigger = True

    def quit_game(self) -> None:
        ''' Sale del juego '''
        # Finalizar Pygame y salir del programa
        pg.quit()
        sys.exit()

    def run(self) -> None:
        ''' Ejecuta el juego '''
        # Bucle principal del juego
        while True:
            # Revisar eventos
            self.check_events()
            # Actualizar la lógica del juego
            self.update()
            # Dibujar en pantalla
            self.draw()

if __name__ == '__main__':
    # Crear una instancia de la aplicación y ejecutarla
    app = App()
    app.run()
