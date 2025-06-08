from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt, QPoint, QPointF, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QImage, QPolygonF
from core.scene import Scene
from core.renderer import Renderer
from shapes.rectangle import Rectangle
from shapes.circle import Circle
from shapes.star import Star
from PySide6.QtCore import Qt
from math import pi, cos, sin

class MyPaintArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.scene = Scene()
        self.init_drawing_state()
        self.setMinimumSize(800, 600)

        self.current_tool = None #Rectangle, circle, star
        self.setMouseTracking(True) #track mouse

        self.scene = Scene()

        # Initialisiere Zeichenvariablen
        self.last_point = None
        self.is_drawing = False
        self.history = []
        self.redo_stack = []
        self.pen_color = Qt.black
        self.pen_size = 3
        self.mouse_down = False

        self.selected_shape = None
        self.drag_mode = None

    def init_drawing_state(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

    def find_shape_at(self, point):
        scene_point = self.screen_to_scene(point)

        for shape in reversed(self.scene.shapes):
            if shape.contains_point(scene_point):
                return shape
            return None

    def screen_to_scene(self, point):
        scale = min(self.width() / max(1, self.scene.get_max_x()),
                    self.height() / max(1, self.scene.get_max_y()))
        scene_x = (point.x() / (scale * self.scene.zoom)) + self.scene.view_x
        scene_y = (point.y() / (scale * self.scene.zoom)) + self.scene.view_y
        return QPoint(scene_x, scene_y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.current_tool:   #let's do selection mode!
                self.save_state()
                self.shape_start = event.position().toPoint()
                self.is_drawing_shape = True
                self.temp_end = self.shape_start

            else:
                try:
                    pos = event.position().toPoint()
                    if hasattr(self, 'find_shape_at'):
                        self.selected_shape = self.find_shape_at(pos)

                        if self.selected_shape:     #did you happen to click a shape?
                            self.drag_start = pos
                            self.drage_mode = 'scale' if hasattr(self, 'is_on_handle') and self.is_on_handle(pos) else 'move'
                            return

                    self.save_state()
                    self.last_point = pos
                    self.is_drawing = True

                except Exception as e:
                    print(f"Error in mouse press: {e}")
                    self.save_state()
                    self.last_point = event.position.toPoint()
                    self.is_drawing = True

        elif event.button() == Qt.MiddleButton:
            self.pan_start = event.position().toPoint()
            self.setCursor(Qt.ClosedHandCursor)


    def mouseMoveEvent(self, event):
        if self.is_drawing and self.last_point:
            painter = QPainter(self.image)
            pen = QPen(self.pen_color, self.pen_size, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()

            self.update()

        elif hasattr(self, 'drag_start') and self.selected_shape:   #shape manipulation and shape moving/scaling
            pass

        elif hasattr(self, 'shape_start') and self.is_drawing_shape:    #shape creation
            self.temp_end = event.position().toPoint()
            self.update()

        elif hasattr(self, 'pan_start'):
            delta = event.position().toPoint() - self.pan_start
            self.scene.view_x -= delta.x() / self.scene.zoom
            self.scene.view_y -= delta.y() / self.scene.zoom
            self.pan_start = event.position().toPoint()
            self.update()

        #should concern shape drawing
        elif self.current_tool and hasattr(self, "shape_start"):
            self.temp_end = event.position().toPoint()
            self.update()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and hasattr(self, "is_drawing_shape"):
            shape = None

            try:
                pos = event.position().toPoint()

                if self.current_tool == "Rectangle":
                    shape = Rectangle(
                        min(self.shape_start.x(), pos.x()),
                        min(self.shape_start.y(), pos.y()),
                        abs(pos.x() - self.shape_start.x()),
                        abs(pos.y() - self.shape_start.y()),
                        QColor(255, 0, 0),  # Red fill
                        QColor(0, 0, 0)  # Black border
                    )
                elif self.current_tool == "Circle":
                    radius = int(((pos.x() - self.shape_start.x()) ** 2 + (pos.y() - self.shape_start.y()) ** 2) ** 0.5)
                    shape = Circle(
                        self.shape_start.x(),
                        self.shape_start.y(),
                        radius,
                        self.pen_color,
                        self.pen_size,
                        QColor(0, 255, 0),  # Green fill
                    )
                elif self.current_tool == "Star":
                    size = max(abs(pos.x() - self.shape_start.x()),
                               abs(pos.y() - self.shape_start.y()))
                    shape = Star(
                        self.shape_start.x(),
                        self.shape_start.y(),
                        size,
                        5,
                        self.pen_color,
                        self.pen_size,
                        QColor(255, 255, 0),  # Yellow fill
                    )

                if shape:
                    self.scene.add_shape(shape)
                    self.update()

                self.is_drawing = False
                self.is_drawing_shape = False
                if hasattr(self, "shape_start"):
                    del self.last_point
                self.last_point = None
                self.update()
                return

            except Exception as e:
                print(f"Error in mouse release: {e}")
                import traceback
                traceback.print_exc()

            finally:
                self.is_drawing_shape = False
                if hasattr(self, "shape_start"):
                    del self.shape_start

        elif self.is_drawing:
            self.is_drawing = False


        elif event.button() == Qt.MiddleButton and hasattr(self, 'pan_start'):
            self.setCursor(Qt.ArrowCursor)
            del self.pan_start




    def resizeEvent(self, event):
        new_image = QImage(self.size(), QImage.Format_RGB32)
        new_image.fill(Qt.white)

        # Bestehendes Bild skalieren
        painter = QPainter(new_image)
        painter.drawImage(0, 0, self.image.scaled(self.size(), Qt.KeepAspectRatio))

        self.image = new_image
        self.update()

    def save_state(self):
        self.history.append(self.image.copy())
        self.redo_stack.clear()

    def undo(self):
        if self.history:
            self.redo_stack.append(self.image.copy())
            self.image = self.history.pop()
            self.update()

    def redo(self):
        if self.redo_stack:
            self.history.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.update()

    def clear_tool_selection(self):
        self.current_tool = None


    def clear_canvas(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Leinwand leeren?")
        msg_box.setText("Möchten Sie die Leinwand wirklich leeren?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.button(QMessageBox.Yes).setText("Ja")
        msg_box.button(QMessageBox.No).setText("Nein")

        if msg_box.exec() == QMessageBox.Yes:
            self.image.fill(Qt.white)
            self.history.clear()
            self.redo_stack.clear()
            self.scene.shapes.clear()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.drawImage(0, 0, self.image)

        scale_x = self.width() / max(1, self.scene.get_max_x())
        scale_y = self.height() / max(1, self.scene.get_max_y())

        scale = min(scale_x, scale_y)


        renderer = Renderer(painter, self.width(), self.height(), 0, 0,
                            self.scene.get_max_x(), self.scene.get_max_y(), scale)

        renderer.render_scene(self.scene)

        # Debugging help, current tool status
        painter.setPen(Qt.black)
        painter.drawText(10, 30, f"Tool: {self.current_tool or 'Free Draw'}")
        painter.drawText(10, 50, f"Zoom: {self.scene.zoom:.1f}x")

        for shape in self.scene.shapes:
            pen = QPen(shape.border_color, shape.border_width)
            painter.setPen(pen)
            painter.setBrush(shape.fill_color)

            try:
                painter.setPen(QPen(shape.border_color, shape.border_width))
                painter.setBrush(shape.fill_color)

                if isinstance(shape, Rectangle):
                    painter.drawRect(shape.x, shape.y, shape.width, shape.height)
                elif isinstance(shape, Circle):
                    painter.drawEllipse(
                        QPoint(shape.x, shape.y),
                        shape.radius,
                        shape.radius
                    )
                elif isinstance(shape, Star):
                    points = []
                    for i in range(shape.points *2):
                        radius = shape.size if i % 2 == 0 else shape.size /2
                        angle = (i*2*pi / (shape.points*2)) - pi/2
                        points.append(QPointF(
                            shape.x + radius * cos(angle),
                            shape.y + radius * sin(angle)
                        ))
                    painter.drawPolygon(QPolygonF(points))
            except Exception as e:
                print(f"Error in mouse release: {e}")


        if hasattr(self, "is_drawing_shape") and self.is_drawing_shape:
            pen = QPen(Qt.gray, 1, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            if self.current_tool == "Rectangle" and hasattr(self, "shape_start"):
                painter.drawRect(QRect(self.shape_start, self.temp_end))
            elif self.current_tool == "Circle" and hasattr(self, "shape_start"):
                radius = int(((self.temp_end.x() - self.shape_start.x())**2 + (self.temp_end.y() - self.shape_start.y())**2)**0.5)
                painter.drawEllipse(self.shape_start, radius, radius)


            elif self.current_tool == "Star" and hasattr(self, "shape_start"):
                size = max(abs(self.temp_end.x() - self.shape_start.x()),
                           abs(self.temp_end.y() - self.shape_start.y()))

                points = []

                for i in range(5 * 2):
                    radius = size if i % 2 == 0 else size / 2
                    angle = (i * pi / 5) - pi / 2
                    px = self.shape_start.x() + radius * cos(angle)
                    py = self.shape_start.y() + radius * sin(angle)
                    points.append(QPointF(px, py))
                painter.drawPolygon(QPolygonF(points))

        painter.end()

