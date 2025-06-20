from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QToolBar, QPushButton, QLabel,
    QColorDialog, QMenuBar, QSlider, QFileDialog, QApplication
)
from PySide6.QtGui import QPixmap, QKeySequence, QColor, QPolygonF, QImage
from PySide6.QtCore import Qt, QPointF, QRect
from app.paint_area import MyPaintArea
from math import pi, cos, sin

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.paint_area = MyPaintArea(self)
        self.setCentralWidget(self.paint_area)
        self.init_ui()

    def init_ui(self):
        # Toolbar and Menubar
        toolbar = QToolBar("Werkzeuge", self)
        self.addToolBar(toolbar)
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("Datei")
        file_menu.addAction("Öffnen... (Ctrl+O)", self.open_file).setShortcut(QKeySequence(Qt.CTRL | Qt.Key_O))
        file_menu.addAction("Speichern Als... (Ctrl+S)", self.save_file).setShortcut(QKeySequence(Qt.CTRL | Qt.Key_S))
        file_menu.addAction("Beenden... (Ctrl+E)", self.exit_application).setShortcut(QKeySequence(Qt.CTRL | Qt.Key_E))
        file_menu.addAction("Exportieren als SVG... (Ctrl+Shift+E)", self.on_export_clicked).setShortcut(
            QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_E))

        # Edit Menu
        edit_menu = menubar.addMenu("Bearbeiten")
        edit_menu.addAction("Rückgängig (Ctrl+Z)", self.paint_area.undo).setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Z))
        edit_menu.addAction("Wiederholen (Ctrl+Y)", self.paint_area.redo).setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Y))
        edit_menu.addAction("Leeren (Ctrl+X)", self.paint_area.clear_canvas).setShortcut(QKeySequence(Qt.CTRL | Qt.Key_X))

        # Help Menu
        help_menu = menubar.addMenu("Hilfe")
        help_menu.addAction("Informationen (Ctrl+I)", self.show_info).setShortcut(QKeySequence(Qt.CTRL | Qt.Key_I))

        # Toolbar Buttons
        open_button = QPushButton("Öffnen", self)
        open_button.clicked.connect(self.open_file)
        open_button.setIcon(QPixmap("open_32x32.png"))
        toolbar.addWidget(open_button)

        save_button = QPushButton("Speichern", self)
        save_button.clicked.connect(self.save_file)
        save_button.setIcon(QPixmap("saveas_26x26.png"))
        toolbar.addWidget(save_button)

        exit_button = QPushButton("Beenden", self)
        exit_button.clicked.connect(self.exit_application)
        exit_button.setIcon(QPixmap("quit_26x26.png"))
        toolbar.addWidget(exit_button)

        info_button = QPushButton("Info", self)
        info_button.clicked.connect(self.show_info)
        info_button.setIcon(QPixmap("info_32x32.png"))
        toolbar.addWidget(info_button)

        color_button = QPushButton("Farbe wählen", self)
        color_button.clicked.connect(self.choose_color)
        toolbar.addWidget(color_button)

        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(1, 20)
        self.size_slider.setValue(self.paint_area.pen_size)
        self.size_slider.valueChanged.connect(self.change_pen_size)
        toolbar.addWidget(self.size_slider)

        self.slider_value_label = QLabel(f"Pinselgröße: {self.size_slider.value()}", self)
        toolbar.addWidget(self.slider_value_label)
        self.size_slider.valueChanged.connect(lambda value: self.slider_value_label.setText(f"Pinselgröße: {value}"))

        # Scene buttons
        scene1_button = QPushButton("Szene 1", self)
        scene1_button.clicked.connect(lambda: self.load_scene(1))
        toolbar.addWidget(scene1_button)
        scene2_button = QPushButton("Szene 2", self)
        scene2_button.clicked.connect(lambda: self.load_scene(2))
        toolbar.addWidget(scene2_button)
        scene3_button = QPushButton("Szene 3", self)
        scene3_button.clicked.connect(lambda: self.load_scene(3))
        toolbar.addWidget(scene3_button)

        # Zoom Buttons
        zoom_in = QPushButton("+", self)
        zoom_in.clicked.connect(self.zoom_in)
        toolbar.addWidget(zoom_in)

        zoom_out = QPushButton("-", self)
        zoom_out.clicked.connect(self.zoom_out)
        toolbar.addWidget(zoom_out)

        zoom_reset = QPushButton("100%", self)
        zoom_reset.clicked.connect(self.zoom_reset)
        zoom_reset.setMaximumWidth(50)
        toolbar.addWidget(zoom_reset)

        # Shape tool buttons
        self.rect_tool = QPushButton("Rechteck", self)
        self.rect_tool.clicked.connect(lambda: self.set_tool("Rectangle"))
        toolbar.addWidget(self.rect_tool)

        self.circle_tool = QPushButton("Kreis", self)
        self.circle_tool.clicked.connect(lambda: self.set_tool("Circle"))
        toolbar.addWidget(self.circle_tool)

        self.star_tool = QPushButton("Stern", self)
        self.star_tool.clicked.connect(lambda: self.set_tool("Star"))
        toolbar.addWidget(self.star_tool)

        # Subdivision/Deformation/SVG Buttons
        self.btn_deform = QPushButton("Apply Wave Effect")
        self.btn_export = QPushButton("Export as SVG")
        self.btn_reset = QPushButton("Reset Wave Effect")
        toolbar.addWidget(self.btn_deform)
        toolbar.addWidget(self.btn_export)
        toolbar.addWidget(self.btn_reset)
        self.btn_deform.clicked.connect(self.on_deform_clicked)
        self.btn_export.clicked.connect(self.on_export_clicked)
        self.btn_reset.clicked.connect(self.on_reset_clicked)

    # --- File and Color ---
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei öffnen", "",
                                                   "PNG-Bild (*.png);;JPG-Bild (*.jpg);;Alle Dateien (*.*)")
        if file_path:
            loaded_image = QImage(file_path)
            if loaded_image.isNull():
                QMessageBox.warning(self, "Fehler", "Das Bild konnte nicht geladen werden.", QMessageBox.Ok)
            else:
                self.paint_area.image = loaded_image
                self.paint_area.update()
                self.setWindowTitle(f"Meine Leinwand App - {file_path.split('/')[-1]}")

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Datei speichern unter", "",
                                                   "PNG-Bild (*.png);;JPG-Bild (*.jpg);;Alle Dateien (*.*)")
        if file_path:
            if not file_path.endswith(".png") and not file_path.endswith(".jpg"):
                file_path += ".png"
            if self.paint_area.image.save(file_path):
                self.setWindowTitle(f"Meine Leinwand App - {file_path.split('/')[-1]}")
                QMessageBox.information(self, "Erfolg", "Das Bild wurde erfolgreich gespeichert.", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Fehler", "Das Bild konnte nicht gespeichert werden.", QMessageBox.Ok)

    def choose_color(self):
        color = QColorDialog.getColor(self.paint_area.pen_color, self, "Farbe wählen")
        if color.isValid():
            self.paint_area.pen_color = color
            self.paint_area.update()

    # --- SVG Export and Wave Effect ---
    def on_export_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save as SVG", "", "SVG Files (*.svg)")
        if filename:
            self.paint_area.export_svg(filename)

    def on_deform_clicked(self):
        # You can tweak these values or make them user adjustable
        self.paint_area.apply_deformation_and_subdivision(n_subdivisions=3, deform_params={'a': 30, 'b': 1/200, 'c': 0})

    def on_reset_clicked(self):
        self.paint_area.reset_deformation()

    # --- Zoom ---
    def change_pen_size(self, value):
        self.paint_area.pen_size = value

    def zoom_in(self):
        self.paint_area.scene.zoom *= 1.1
        self.paint_area.update()

    def zoom_out(self):
        self.paint_area.scene.zoom *= 0.9
        self.paint_area.update()

    def zoom_reset(self):
        self.paint_area.scene.zoom = 1.0
        self.paint_area.scene.view_x = 0
        self.paint_area.scene.view_y = 0
        self.paint_area.update()

    # --- Tool/Scene Selection ---
    def set_tool(self, tool_name):
        self.is_drawing = False
        self.is_drawing_shape = False
        if self.paint_area.current_tool == tool_name:
            self.paint_area.current_tool = None
        else:
            self.paint_area.current_tool = tool_name
        self.update()
        for btn in [self.rect_tool, self.circle_tool, self.star_tool]:
            btn.setStyleSheet("")
        if tool_name == "Rectangle":
            self.rect_tool.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        elif tool_name == "Circle":
            self.circle_tool.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        elif tool_name == "Star":
            self.star_tool.setStyleSheet("background-color: #000000; color: #FFFFFF;")

    def load_scene(self, scene_id: int):
        try:
            self.paint_area.scene.generate_test_scene(scene_id)
            self.paint_area.update()
        except ValueError:
            QMessageBox.warning(self, "Fehler", "Ungültige Szenen-ID", QMessageBox.Ok)

    # --- Info and Exit ---
    def show_info(self):
        info_box = QMessageBox(self)
        info_box.setIcon(QMessageBox.Information)
        info_box.setWindowTitle("Informationen")
        info_box.setText("Dies ist eine einfache Zeichenanwendung.\n\n"
                         "Verwenden Sie die Menüleiste, um Bilder zu öffnen und zu speichern.\n"
                         "Sie können auch die Pinselgröße und -farbe anpassen.\n\n"
                         "Tastenkombinationen:\n"
                         "Strg + O: Bild öffnen\n"
                         "Strg + S: Bild speichern\n"
                         "Strg + Z: Rückgängig\n"
                         "Strg + Y: Wiederholen\n"
                         "Strg + X: Leinwand leeren\n"
                         "Strg + I: Informationen anzeigen\n"
                         "Strg + E: Anwendung beenden")
        info_box.setStandardButtons(QMessageBox.Ok)
        info_box.exec()

    def exit_application(self):
        self.close()

    def closeEvent(self, event):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Beenden?")
        msg_box.setText("Möchten Sie die Anwendung wirklich beenden?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.button(QMessageBox.Yes).setText("Ja")
        msg_box.button(QMessageBox.No).setText("Nein")
        if msg_box.exec() == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window_size = self.geometry()
        self.move((screen.width() - window_size.width()) // 2, (screen.height() - window_size.height()) // 2)