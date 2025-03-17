import sys
import os
import django
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QFrame
)
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QSize

# ✅ Ensure frontend path is recognized
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Import chatbot module (Handle missing module)
try:
    from frontend.chatbot import ChatbotWindow
except ModuleNotFoundError:
    print("⚠️ Warning: 'frontend.chatbot' module not found!")

# ✅ Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_relationship_management_system.settings")
django.setup()

from core.models import ClientQuery, User  # ✅ Import models


class RM_Dashboard(QWidget):
    def __init__(self, rm_username):
        super().__init__()

        # ✅ Fetch RM User Details
        self.rm_user = User.objects.filter(username=rm_username, role="rm").first()
        if not self.rm_user:
            QMessageBox.critical(self, "Error", "Invalid RM Account!")
            sys.exit(1)  # Exit if RM is not found

        # ✅ Window Settings
        self.setWindowTitle("RM Dashboard - Smart Relationship Management")
        self.setGeometry(300, 100, 900, 580)
        self.setStyleSheet("background-color: #EAEDED;")  # Light Gray Background

        # ✅ Background Image
        self.bg_label = QLabel(self)
        bg_path = "static/background_rm.png"
        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path).scaled(900, 580, Qt.KeepAspectRatioByExpanding))
        else:
            print("⚠️ Warning: background_rm.png not found!")
        self.bg_label.setGeometry(0, 0, 900, 580)

        # ✅ Dashboard Box (Compact & Modern)
        self.dashboard_box = QFrame(self)
        self.dashboard_box.setGeometry(250, 80, 400, 420)
        self.dashboard_box.setStyleSheet("""
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        """)

        # ✅ Profile Section
        self.profile_label = QLabel(f"👤 {self.rm_user.username}", self)
        self.profile_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.profile_label.setStyleSheet("color: white;")
        self.profile_label.setAlignment(Qt.AlignCenter)

        self.branch_label = QLabel("🏦 Branch: Mumbai Central", self)
        self.branch_label.setFont(QFont("Arial", 13))
        self.branch_label.setStyleSheet("color: white;")
        self.branch_label.setAlignment(Qt.AlignCenter)

        self.clients_handled_label = QLabel(f"👥 Clients: {self.get_clients_count()}", self)
        self.clients_handled_label.setFont(QFont("Arial", 13))
        self.clients_handled_label.setStyleSheet("color: white;")
        self.clients_handled_label.setAlignment(Qt.AlignCenter)

        self.resolved_queries_label = QLabel(f"✅ Resolved Queries: {self.get_resolved_queries_count()}", self)
        self.resolved_queries_label.setFont(QFont("Arial", 13))
        self.resolved_queries_label.setStyleSheet("color: white;")
        self.resolved_queries_label.setAlignment(Qt.AlignCenter)

        # ✅ Buttons (Full-Width & Well Spaced)
        self.chatbot_btn = self.create_button("🤖 Chat with AI", "#673AB7", "static/icons/chatbot.png")
        self.view_queries_btn = self.create_button("📩 View Queries", "#4CAF50", "static/icons/queries.png")
        self.manage_products_btn = self.create_button("💰 Manage Products", "#2196F3", "static/icons/products.png")
        self.handle_loans_btn = self.create_button("📋 Handle Loans", "#FF9800", "static/icons/loans.png")
        self.logout_btn = self.create_button("🚪 Logout", "#FF5733", "static/icons/logout.png")

        # ✅ Button Click Actions
        self.chatbot_btn.clicked.connect(self.open_chatbot)
        self.logout_btn.clicked.connect(self.logout)

        # ✅ Layout (Column Format, Clean & Professional)
        layout = QVBoxLayout()
        layout.addWidget(self.profile_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.branch_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.clients_handled_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.resolved_queries_label, alignment=Qt.AlignCenter)

        layout.addWidget(self.view_queries_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.manage_products_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.handle_loans_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.chatbot_btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.logout_btn, alignment=Qt.AlignCenter)

        container = QWidget(self)
        container.setLayout(layout)
        container.setGeometry(270, 95, 360, 390)

        # ✅ Smooth Fade-in Animation
        self.fade_in_animation()

    def create_button(self, text, color, icon_path):
        """ Create a button with an icon and hover effect """
        button = QPushButton(text, self)
        button.setFont(QFont("Arial", 13))
        button.setFixedWidth(320)
        button.setFixedHeight(45)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: white;
                color: {color};
                border: 2px solid {color};
            }}
        """)

        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))

        return button

    def get_clients_count(self):
        """ Fetch number of clients """
        return User.objects.filter(role="client").count()

    def get_resolved_queries_count(self):
        """ Fetch number of resolved queries """
        return ClientQuery.objects.filter(status="Resolved").count()

    def fade_in_animation(self):
        """ Apply fade-in animation for smooth effect """
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def open_chatbot(self):
        """ Open Chatbot Window with Error Handling """
        try:
            self.chatbot_window = ChatbotWindow()
            self.chatbot_window.show()
        except NameError:
            QMessageBox.critical(self, "Error", "Chatbot module not found!")

    def logout(self):
        """ Logout RM and return to Login """
        QMessageBox.information(self, "Logout", "You have been logged out.")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RM_Dashboard("admin1")
    window.show()
    sys.exit(app.exec())
