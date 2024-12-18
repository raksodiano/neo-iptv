import mpv
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget


class VideoPlayerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_DontCreateNativeAncestors)
        self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)

        self.mpv_player = mpv.MPV(
            wid=str(int(self.winId())),
            log_handler=print,
            loglevel='debug'
        )

        # Timer para refrescar el widget y actualizar el paintEvent
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_video)
        self.update_timer.start(100)  # Actualizar cada 100 ms (~10 FPS)

        self.setStyleSheet("background-color: black;")  # Establecer fondo negro

        # Bandera para verificar si el video está reproduciéndose
        self.is_playing = False

    def set_media_player(self, media_player):
        """Establece el reproductor MPV para la renderización del video en este widget"""
        self.mpv_player = media_player
        self.mpv_player.prepare_async = True  # Permite preparación asincrónica

    def play_media(self, media_url):
        """Reproducir video o transmisión IPTV"""
        self.mpv_player.play(media_url)
        self.is_playing = True

    def stop_media(self):
        """Detener la reproducción del video"""
        self.mpv_player.stop()
        self.is_playing = False

    def update_video(self):
        """Actualizar el widget y renderizar el video"""
        if self.is_playing:
            self.update()  # Forzar el paintEvent para redibujar el widget

    def paintEvent(self, event):
        """Evento de pintura personalizado para mostrar contenido mientras el video se está cargando"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.is_playing:
            # Si el video se está reproduciendo, actualizar el widget con el video
            super().paintEvent(event)
        else:
            # Si el video no se está reproduciendo, mostrar mensaje de carga
            painter.fillRect(self.rect(), QColor(0, 0, 0))
            painter.setPen(QColor(255, 255, 255))  # Establecer color del texto en blanco
            painter.setFont(self.font())
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Video is loading...")

    def resizeEvent(self, event):
        """Asegurarse de que el video se redimensione junto con el widget"""
        super().resizeEvent(event)
        if self.is_playing:
            # Sin necesidad de reasociar, MPV manejará la redimensión automáticamente
            self.mpv_player.set_property('geometry', f"{self.width()}x{self.height()}+0+0")
