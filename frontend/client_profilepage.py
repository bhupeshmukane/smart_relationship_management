import sys
import os
import django
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QComboBox, QFileDialog, QFrame, QHBoxLayout
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

# ✅ Setup Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_relationship_management_system.settings")
django.setup()

from core.models import User

class ClientProfilePage(QWidget):
    def __init__(self, client_username):
        super().__init__()

        # ✅ Fetch Client Info
        self.client_user = User.objects.filter(username=client_username, role="client").first()
        if not self.client_user:
            raise ValueError("Invalid Client Account!")

        # ✅ Window Setup
        self.setWindowTitle("Client Profile")
        self.setGeometry(200, 100, 850, 550)
        self.setStyleSheet("background-color: #F5F7FA;")  # Light Grey Background

        # ✅ Main Layout (Holds Everything)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)

        # ✅ Profile Picture Section (Centered)
        pic_layout = QVBoxLayout()
        self.profile_pic = QLabel(self)
        self.profile_pic.setFixedSize(120, 120)
        self.profile_pic.setAlignment(Qt.AlignCenter)
        self.profile_pic.setPixmap(QPixmap("static/icons/user_icon.png").scaled(120, 120, Qt.KeepAspectRatio))
        self.profile_pic.setStyleSheet("""
            border: 4px solid #007BFF;
            border-radius: 60px; /* Fully Circular */
            background-color: white;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
        """)

        self.upload_btn = QPushButton("📷 Change Photo", self)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #007BFF; color: white;
                border-radius: 5px; padding: 7px;
                font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0056b3; }
        """)
        self.upload_btn.clicked.connect(self.upload_picture)

        pic_layout.addWidget(self.profile_pic, alignment=Qt.AlignCenter)
        pic_layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)

        # ✅ User Info Section (Properly Aligned)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        self.name_input = self.create_labeled_input("Full Name", self.client_user.username)
        self.email_input = self.create_labeled_input("Email", self.client_user.email)
        self.dob_input = self.create_labeled_input("Date of Birth", "01-01-1990")
        self.phone_input = self.create_labeled_input("Contact", "+123 456 7890")

        # ✅ Gender Dropdown (Aligned)
        gender_layout = QHBoxLayout()
        gender_layout.setSpacing(10)

        gender_label = QLabel("Gender")
        gender_label.setFont(QFont("Arial", 11, QFont.Bold))
        gender_label.setStyleSheet("color: #555; padding-right: 10px;")

        self.gender_dropdown = QComboBox()
        self.gender_dropdown.addItems(["Male", "Female", "Other"])
        self.gender_dropdown.setFixedHeight(35)
        self.gender_dropdown.setStyleSheet("""
            padding: 8px; border: 1px solid #ccc; border-radius: 6px;
            background-color: white; font-size: 14px;
        """)

        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_dropdown)

        # ✅ Save Button (Full Width)
        self.save_btn = QPushButton("💾 Save Changes", self)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745; color: white;
                padding: 12px; border-radius: 6px; font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #218838; }
        """)

        # ✅ Adding Elements to Main Layout
        main_layout.addLayout(pic_layout)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(gender_layout)
        main_layout.addWidget(self.save_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def create_labeled_input(self, label_text, default_value=""):
        """ Creates a horizontally aligned labeled input field """
        container = QHBoxLayout()
        container.setSpacing(10)

        label = QLabel(label_text)
        label.setFont(QFont("Arial", 11, QFont.Bold))
        label.setStyleSheet("color: #555; width: 120px;")

        input_field = QLineEdit()
        input_field.setText(default_value)
        input_field.setFixedHeight(35)
        input_field.setStyleSheet("""
            padding: 10px; border: 1px solid #ccc; border-radius: 6px;
            background-color: white; font-size: 14px;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        """)
        input_field.setPlaceholderText(f"Enter {label_text}...")

        container.addWidget(label)
        container.addWidget(input_field)

        self.layout().addLayout(container)
        return input_field

    def upload_picture(self):
        """ Upload new profile picture """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.profile_pic.setPixmap(QPixmap(file_path).scaled(120, 110, Qt.KeepAspectRatio))

# ✅ Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientProfilePage("test_client")
    window.show()
    sys.exit(app.exec())
