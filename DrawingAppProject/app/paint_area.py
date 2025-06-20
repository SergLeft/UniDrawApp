from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt, QPoint, QPointF, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QImage, QPolygonF
from core.scene import Scene
from shapes.rectangle import Rectangle
from shapes.circle import Circle
from shapes.star import Star
from math import pi, cos, sin
from operations.subdivision import Subdivision
from operations.deformation import Deformation
from exporters.svg_exporter import SVGExporter as Exporter

class MyPaintArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.scene = Scene()
        self.setMinimumSize(800, 600)

        self.current_tool = None  # "Rectangle", "Circle", "Star"
        self.setMouseTracking(True)

        # Drawing state
        self.start_point = None
        self.temp_end = None
        self.drawing = False  # True when drawing a new shape
        self.temp_shape = None

        # Freehand drawing
        self.is_drawing = False
        self.last_point = None

        # Selection/Manipulation
        self.selected_shape = None
        self.dragging = False
        self.resizing = False
        self.resizing_corner = None  # 0=tl,1=tr,2=bl,3=br
        self.drag_offset = (0, 0)
        self.resize_start = None

        # Undo/redo/history
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.history = []
        self.redo_stack = []

        # Pen settings
        self.pen_color = Qt.black
        self.pen_size = 3


    def mousePressEvent(self, event):
        if self.current_tool is None:
            if event.button() == Qt.LeftButton:
                self.is_drawing = True
                self.last_point = event.pos()
            return

        if self.selected_shape:
            s = self.selected_shape
            size = 8
            handles = [
                (s.x, s.y),  # top-left
                (s.x + s.width, s.y),  # top-right
                (s.x, s.y + s.height),  # bottom-left
                (s.x + s.width, s.y + s.height),  # bottom-right
            ]
            for idx, (hx, hy) in enumerate(handles):
                if abs(event.x() - hx) < size and abs(event.y() - hy) < size:
                    self.resizing = True
                    self.resizing_corner = idx
                    self.resize_start = (s.x, s.y, s.width, s.height, event.x(), event.y())
                    return

        for shape in reversed(self.scene.shapes):
            if shape.contains_point(event.x(), event.y()):
                self.selected_shape = shape
                self.dragging = True
                self.resizing = False
                self.resizing_corner = None
                self.drag_offset = (event.x() - shape.x, event.y() - shape.y)
                self.update()
                return

        self.selected_shape = None
        self.dragging = False
        self.resizing = False
        self.resizing_corner = None

        if event.button() == Qt.LeftButton and self.current_tool:
            self.drawing = True
            self.start_point = event.pos()
            self.temp_end = event.pos()
            self.temp_shape = None

    def resizeEvent(self, event):
        new_image = QImage(self.size(), QImage.Format_RGB32)
        new_image.fill(Qt.white)
        painter = QPainter(new_image)
        painter.drawImage(0, 0, self.image)
        self.image = new_image
        self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing and self.last_point:
            painter = QPainter(self.image)
            pen = QPen(self.pen_color, self.pen_size, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()
            return

        if self.drawing and self.start_point:
            self.temp_end = event.pos()
            self.update()
            return

        if self.dragging and self.selected_shape:
            dx = event.x() - self.drag_offset[0]
            dy = event.y() - self.drag_offset[1]
            self.selected_shape.x = dx
            self.selected_shape.y = dy
            self.update()
            return

        # --- Resizing shape ---
        if self.resizing and self.selected_shape and self.resize_start:
            x0, y0, w0, h0, px0, py0 = self.resize_start
            dx = event.x() - px0
            dy = event.y() - py0
            s = self.selected_shape
            if self.resizing_corner == 0:  # top-left
                s.x = x0 + dx
                s.y = y0 + dy
                s.width = w0 - dx
                s.height = h0 - dy
            elif self.resizing_corner == 1:  # top-right
                s.y = y0 + dy
                s.width = w0 + dx
                s.height = h0 - dy
            elif self.resizing_corner == 2:  # bottom-left
                s.x = x0 + dx
                s.width = w0 - dx
                s.height = h0 + dy
            elif self.resizing_corner == 3:  # bottom-right
                s.width = w0 + dx
                s.height = h0 + dy
            self.update()
            return

    def mouseReleaseEvent(self, event):
        if self.is_drawing:
            self.is_drawing = False
            self.last_point = None
            return

        try:
            if self.drawing and self.start_point and self.temp_end:
                start = self.start_point
                end = self.temp_end
                x = min(start.x(), end.x())
                y = min(start.y(), end.y())
                width = abs(start.x() - end.x())
                height = abs(start.y() - end.y())

                border_color = QColor(0, 0, 0)  # Or your color selection logic
                border_width = 2  # Or your thickness logic
                fill_color = QColor(255, 255, 255)  # Or your fill color logic

                if self.current_tool == "Rectangle":
                    fill_color = QColor(255, 0, 0)
                    shape = Rectangle(x, y, width, height, border_color, border_width, fill_color)
                elif self.current_tool == "Circle":
                    fill_color = QColor(0, 0, 255)
                    shape = Circle(x, y, width, height, border_color, border_width, fill_color)
                elif self.current_tool == "Star":
                    fill_color = QColor(255, 255, 0)
                    shape = Star(x, y, width, height, border_color, border_width, fill_color)
                else:
                    shape = None

                if shape:
                    self.scene.shapes.append(shape)
                self.drawing = False
                self.start_point = None
                self.temp_end = None
                self.temp_shape = None
                self.update()

        except Exception as e:
            print("Error in mouse release:", e)

        self.dragging = False
        self.resizing = False
        self.resizing_corner = None
        self.resize_start = None


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

        # Draw all shapes
        for shape in self.scene.shapes:
            try:
                pen = QPen(shape.border_color, shape.border_width)
                painter.setPen(pen)
                painter.setBrush(shape.fill_color)

                if isinstance(shape, Rectangle):
                    painter.drawRect(shape.x, shape.y, shape.width, shape.height)
                elif isinstance(shape, Circle):
                    painter.drawEllipse(shape.x, shape.y, shape.width, shape.height)
                elif isinstance(shape, Star):
                    points = []
                    cx = shape.x + shape.width / 2
                    cy = shape.y + shape.height / 2
                    outer_r = min(shape.width, shape.height) / 2
                    inner_r = outer_r / 2.5
                    for i in range(10):
                        angle = pi/2 + i * pi/5
                        r = outer_r if i % 2 == 0 else inner_r
                        px = cx + r * cos(angle)
                        py = cy - r * sin(angle)
                        points.append(QPointF(px, py))
                    painter.drawPolygon(QPolygonF(points))
            except Exception as e:
                print(f"Error drawing shape: {e}")

        # Draw preview (while drawing)
        if self.drawing and self.start_point and self.temp_end and self.current_tool:
            pen = QPen(Qt.gray, 1, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            if self.current_tool == "Rectangle":
                x = min(self.start_point.x(), self.temp_end.x())
                y = min(self.start_point.y(), self.temp_end.y())
                width = abs(self.start_point.x() - self.temp_end.x())
                height = abs(self.start_point.y() - self.temp_end.y())
                painter.drawRect(x, y, width, height)
            elif self.current_tool == "Circle":
                x = min(self.start_point.x(), self.temp_end.x())
                y = min(self.start_point.y(), self.temp_end.y())
                width = abs(self.start_point.x() - self.temp_end.x())
                height = abs(self.start_point.y() - self.temp_end.y())
                painter.drawEllipse(x, y, width, height)
            elif self.current_tool == "Star":
                cx = (self.start_point.x() + self.temp_end.x()) / 2
                cy = (self.start_point.y() + self.temp_end.y()) / 2
                outer_r = min(abs(self.temp_end.x() - self.start_point.x()), abs(self.temp_end.y() - self.start_point.y())) / 2
                inner_r = outer_r / 2.5
                points = []
                for i in range(10):
                    angle = pi/2 + i * pi/5
                    r = outer_r if i % 2 == 0 else inner_r
                    px = cx + r * cos(angle)
                    py = cy - r * sin(angle)
                    points.append(QPointF(px, py))
                painter.drawPolygon(QPolygonF(points))

        # Draw selection box and handles
        if self.selected_shape:
            s = self.selected_shape
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(s.x, s.y, s.width, s.height)
            # Draw handles (corners)
            size = 8
            for (hx, hy) in [
                (s.x, s.y),
                (s.x + s.width, s.y),
                (s.x, s.y + s.height),
                (s.x + s.width, s.y + s.height),
            ]:
                painter.fillRect(hx - size // 2, hy - size // 2, size, size, Qt.blue)

        painter.end()

    def apply_subdivision_deformation(self, iterations=2, a=20, b=0.005, c=0):
        #triangle collection
        all_triangles = []
        for shape in self.scene.shapes:
            all_triangles.extend(shape.describeShape())

        #subdivison
        subdivided = Subdivision.apply(all_triangles, iterations)

        #deformation
        deformed = Deformation.apply(subdivided, a, b, c)

        #make new shape
        self.scene.shapes = deformed
        self.update()

    def export_svg(self, filename):
        Exporter.export_to_svg(self.scene.shapes, filename, self.width(), self.height())