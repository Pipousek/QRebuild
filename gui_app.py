from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QGroupBox, QLabel, QLineEdit, QSlider, QPushButton, 
                            QFileDialog, QTextEdit, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
import io
from core.qr_generator import generate_qr
from core.qr_extractor import extract_qr
from core.content_analyzer import ContentAnalyzer

class QRCodeRebuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Rebuilder")
        self.setMinimumSize(900, 700)
        
        # Default values
        self.box_size = 10
        self.border = 4
        self.error_correction = 'H'
        self.input_image_path = None
        
        self.init_ui()
        
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left panel - Input
        self.input_group = QGroupBox("Input QR Code")
        input_layout = QVBoxLayout()
        
        self.input_label = QLabel("Drag & drop or click to select image")
        self.input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_label.setMinimumSize(350, 350)
        self.input_label.setStyleSheet("border: 2px dashed #aaa;")
        self.input_label.mousePressEvent = self.select_input_image
        
        input_layout.addWidget(self.input_label)
        
        # Input content area
        self.input_content_single = QLineEdit()
        self.input_content_single.setPlaceholderText("QR Code Content will appear here")
        self.input_content_single.setReadOnly(True)
        
        self.input_content_structured = QTextEdit()
        self.input_content_structured.setPlaceholderText("Structured content will appear here")
        self.input_content_structured.setReadOnly(True)
        self.input_content_structured.setMaximumHeight(100)
        
        input_layout.addWidget(QLabel("Original Content:"))
        input_layout.addWidget(self.input_content_single)
        input_layout.addWidget(QLabel("Structured Content:"))
        input_layout.addWidget(self.input_content_structured)
        
        self.input_group.setLayout(input_layout)
        
        # Right panel - Output
        self.output_group = QGroupBox("Generated QR Code")
        output_layout = QVBoxLayout()
        
        self.output_label = QLabel()
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_label.setMinimumSize(350, 350)
        self.output_label.setStyleSheet("border: 2px dashed #aaa;")
        
        output_layout.addWidget(self.output_label)
        
        # Output content area
        self.output_content_single = QLineEdit()
        self.output_content_single.setPlaceholderText("Generated QR Content will appear here")
        self.output_content_single.setReadOnly(True)
        
        self.output_content_structured = QTextEdit()
        self.output_content_structured.setPlaceholderText("Structured content will appear here")
        self.output_content_structured.setReadOnly(True)
        self.output_content_structured.setMaximumHeight(100)
        
        output_layout.addWidget(QLabel("Original Content:"))
        output_layout.addWidget(self.output_content_single)
        output_layout.addWidget(QLabel("Structured Content:"))
        output_layout.addWidget(self.output_content_structured)
        
        self.output_group.setLayout(output_layout)
        
        # Add panels to main layout
        main_layout.addWidget(self.input_group)
        main_layout.addWidget(self.output_group)
        
        # Controls panel (more compact)
        controls_group = QGroupBox("Settings")
        controls_layout = QVBoxLayout()
        controls_layout.setContentsMargins(5, 5, 5, 5)
        
        # Box Size control
        box_size_layout = QHBoxLayout()
        box_size_layout.addWidget(QLabel("Box Size:"))
        self.box_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.box_size_slider.setRange(5, 30)
        self.box_size_slider.setValue(self.box_size)
        self.box_size_slider.valueChanged.connect(self.update_box_size)
        box_size_layout.addWidget(self.box_size_slider)
        
        self.box_size_input = QLineEdit(str(self.box_size))
        self.box_size_input.setFixedWidth(40)
        self.box_size_input.textEdited.connect(self.update_box_size_from_text)
        box_size_layout.addWidget(self.box_size_input)
        controls_layout.addLayout(box_size_layout)
        
        # Border control
        border_layout = QHBoxLayout()
        border_layout.addWidget(QLabel("Border:"))
        self.border_slider = QSlider(Qt.Orientation.Horizontal)
        self.border_slider.setRange(1, 10)
        self.border_slider.setValue(self.border)
        self.border_slider.valueChanged.connect(self.update_border)
        border_layout.addWidget(self.border_slider)
        
        self.border_input = QLineEdit(str(self.border))
        self.border_input.setFixedWidth(40)
        self.border_input.textEdited.connect(self.update_border_from_text)
        border_layout.addWidget(self.border_input)
        controls_layout.addLayout(border_layout)

        # Error Correction Level (radio buttons)
        error_corr_layout = QHBoxLayout()
        error_corr_layout.addWidget(QLabel("Error Correction:"))
        
        self.error_corr_group = QButtonGroup(self)
        for i, (level, desc) in enumerate([('L', 'Low (7%)'), ('M', 'Medium (15%)'), 
                                          ('Q', 'Quartile (25%)'), ('H', 'High (30%)')]):
            rb = QRadioButton(desc)
            rb.setProperty('level', level)
            if level == 'H':
                rb.setChecked(True)
            self.error_corr_group.addButton(rb, i)
            error_corr_layout.addWidget(rb)
        
        self.error_corr_group.buttonClicked.connect(self.update_error_correction)
        controls_layout.addLayout(error_corr_layout)
        
        # Buttons (compact)
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_qr_code)
        button_layout.addWidget(self.save_button)
        controls_layout.addLayout(button_layout)
        
        controls_group.setLayout(controls_layout)
        controls_group.setMaximumHeight(150)
        
        # Main layout
        container = QVBoxLayout()
        container.addLayout(main_layout)
        container.addWidget(controls_group)
        
        main_widget.setLayout(container)
        self.setCentralWidget(main_widget)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        self.input_label.setAcceptDrops(True)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                self.load_input_image(file_path)
                break
    
    def select_input_image(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.load_input_image(file_path)
    
    def load_input_image(self, file_path):
        self.input_image_path = file_path
        pixmap = QPixmap(file_path)
        self.input_label.setPixmap(
            pixmap.scaled(
                self.input_label.size() - QSize(10, 10),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        
        # Extract QR code content using the core function
        try:
            content = extract_qr(file_path)
            self.input_content_single.setText(content)
            self.output_content_single.setText(content)
            self.structure_content(content)
            self.generate_qr_code(content)
        except Exception as e:
            self.input_content_single.setText(f"Error: {str(e)}")
            self.input_content_structured.clear()
    
    def structure_content(self, content):
        """Format the content in a structured way based on its type."""
        analysis = ContentAnalyzer.analyze(content)
        formatted = ContentAnalyzer.format_structured_content(analysis)
        self._set_structured_content(formatted)

    def _set_structured_content(self, text):
        """Helper to set structured content in both panels."""
        self.input_content_structured.setPlainText(text)
        self.output_content_structured.setPlainText(text)

    def update_error_correction(self, button):
        self.error_correction = button.property('level')
        self.regenerate_qr()
    
    def generate_qr_code(self, content):
        # Use the core function to generate QR code
        img = generate_qr(content, self.box_size, self.border, self.error_correction)
        
        # Convert to QPixmap
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        
        self.output_label.setPixmap(
            pixmap.scaled(
                self.output_label.size() - QSize(10, 10),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
    
    def update_box_size(self, value):
        self.box_size = value
        self.box_size_input.setText(str(value))
        self.regenerate_qr()
    
    def update_box_size_from_text(self):
        try:
            value = int(self.box_size_input.text())
            if 5 <= value <= 30:
                self.box_size = value
                self.box_size_slider.setValue(value)
                self.regenerate_qr()
        except ValueError:
            pass
    
    def update_border(self, value):
        self.border = value
        self.border_input.setText(str(value))
        self.regenerate_qr()
    
    def update_border_from_text(self):
        try:
            value = int(self.border_input.text())
            if 1 <= value <= 10:
                self.border = value
                self.border_slider.setValue(value)
                self.regenerate_qr()
        except ValueError:
            pass
    
    def regenerate_qr(self):
        if self.input_content_single.text() and not self.input_content_single.text().startswith("Error"):
            self.generate_qr_code(self.input_content_single.text())
    
    def clear_all(self):
        self.input_label.clear()
        self.input_label.setText("Drag & drop or click to select image")
        self.input_content_single.clear()
        self.input_content_structured.clear()
        self.output_label.clear()
        self.output_content_single.clear()
        self.output_content_structured.clear()
        self.input_image_path = None
    
    def save_qr_code(self, file_path=None):
        if not self.output_label.pixmap():
            return
            
        if not file_path:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save QR Code", "", "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg)"
            )
        
        if file_path:
            self.output_label.pixmap().save(file_path)