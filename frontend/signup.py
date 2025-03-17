import sys
import os
import re
import mysql.connector
import django   
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QMessageBox, QFrame, QComboBox, QCheckBox, QHBoxLayout
)
from PySide6.QtGui import QFont, QPixmap, QImage, QPainter, QBrush
from PySide6.QtCore import Qt
from django.contrib.auth.hashers import make_password

# ✅ Setup Django Environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_relationship_management_system.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# ✅ Database Connection Function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bhup@2003",  # Change this to your MySQL password
        database="srms_db"
    )

# ✅ Function to Apply Blur Effect to Background Image
def apply_blur(image_path):
    img = QImage(image_path)
    painter = QPainter(img)
    painter.setOpacity(0.3)  # Adjust transparency level
    painter.setBrush(QBrush(Qt.black))
    painter.drawRect(0, 0, img.width(), img.height())
    painter.end()
    return img

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Window Settings
        self.setWindowTitle("Smart Relationship Management - Register")
        self.setGeometry(300, 150, 900, 550)

         # ✅ Set Background Image with Blur
        self.bg_label = QLabel(self)
        bg_path = "static/regi_bg.jpg"  # Ensure this image exists
        if os.path.exists(bg_path):
            blurred_image = apply_blur(bg_path)
            self.bg_label.setPixmap(QPixmap.fromImage(blurred_image))
        else:
            print("⚠️ Warning: Background image not found!")

        self.bg_label.setGeometry(0, 0, 900, 550)

        # ✅ Registration Box
        self.register_box = QFrame(self)
        self.register_box.setGeometry(275, 80, 350, 450)
        self.register_box.setStyleSheet("""
            background: rgba(0, 0, 0, 0.7); 
            border-radius: 15px;
        """)

        # ✅ Title Label
        self.title = QLabel("📝 Register", self)
        self.title.setFont(QFont("Arial", 22, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white;")

        # ✅ Username Input
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("👤 Enter Username")
        self.username.setFont(QFont("Arial", 12))
        self.username.setFixedWidth(250)
        self.username.setStyleSheet("""
            QLineEdit {
                background: white;
                padding: 8px;
                border-radius: 8px;
                font-size: 14px;
            }
        """)

        # ✅ Email Input
        self.email = QLineEdit(self)
        self.email.setPlaceholderText("📧 Enter Email")
        self.email.setFont(QFont("Arial", 12))
        self.email.setFixedWidth(250)
        self.email.setStyleSheet("""
            QLineEdit {
                background: white;
                padding: 8px;
                border-radius: 8px;
                font-size: 14px;
            }
        """)

        # ✅ Password Input
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("🔒 Enter Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFont(QFont("Arial", 12))
        self.password.setFixedWidth(250)
        self.password.setStyleSheet("""
            QLineEdit {
                background: white;
                padding: 8px;
                border-radius: 8px;
                font-size: 14px;
            }
        """)

        # ✅ Show Password Toggle
        self.show_password = QCheckBox("👁 Show Password", self)
        self.show_password.setStyleSheet("color: white; font-size: 12px;")
        self.show_password.stateChanged.connect(self.toggle_password_visibility)

        # ✅ Role Selection Dropdown
        self.role_selector = QComboBox(self)
        self.role_selector.addItems(["Client", "Relationship Manager", "Admin"])  
        self.role_selector.setFont(QFont("Arial", 12))
        self.role_selector.setFixedWidth(250)
        self.role_selector.setStyleSheet("""
            background: white; padding: 6px; border-radius: 5px;
        """)

        # ✅ Register Button
        self.register_button = QPushButton("📌 Register", self)
        self.register_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.register_button.setFixedWidth(250)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0053a6;
                border: 2px solid white;
            }
        """)
        self.register_button.clicked.connect(self.register_user)

        # ✅ Layout Adjustments
        layout = QVBoxLayout()
        layout.addWidget(self.title, alignment=Qt.AlignCenter)
        layout.addWidget(self.username, alignment=Qt.AlignCenter)
        layout.addWidget(self.email, alignment=Qt.AlignCenter)
        layout.addWidget(self.password, alignment=Qt.AlignCenter)
        layout.addWidget(self.show_password, alignment=Qt.AlignCenter)
        layout.addWidget(self.role_selector, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        container = QWidget(self)
        container.setLayout(layout)
        container.setGeometry(300, 100, 300, 400)

    # ✅ Show/Hide Password
    def toggle_password_visibility(self):
        self.password.setEchoMode(QLineEdit.Normal if self.show_password.isChecked() else QLineEdit.Password)

    # ✅ Validate Email Format
    def is_valid_email(self, email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email)

    # ✅ Validate Password Strength
    def is_valid_password(self, password):
        return len(password) >= 6

    # ✅ Register User Function
    def register_user(self):
        username = self.username.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        role = self.role_selector.currentText().lower()

        # ✅ Check if all fields are filled
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        # ✅ Validate Email Format
        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Error", "Invalid email format!")
            return

        # ✅ Validate Password Strength
        if not self.is_valid_password(password):
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters long!")
            return

        hashed_password = make_password(password)  # Hash password

        try:
            # ✅ Check if username or email already exists
            if User.objects.filter(username=username).exists():
                QMessageBox.warning(self, "Error", "Username already exists!")
                return

            if User.objects.filter(email=email).exists():
                QMessageBox.warning(self, "Error", "Email is already registered!")
                return

            # ✅ Create user in database
            User.objects.create(username=username, email=email, password=hashed_password, role=role)

            QMessageBox.information(self, "Success", "Registration Successful!")
            self.close()  # Close registration window

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

# ✅ Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignUpWindow()
    window.show()
    sys.exit(app.exec())
