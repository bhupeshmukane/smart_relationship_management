import sys
import os
import django
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QMessageBox
)
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QSize

# ✅ Setup Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_relationship_management_system.settings")
django.setup()

from core.models import User, Loan, ClientQuery  # ✅ Import Django Models

class ReportsAnalytics(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Window Settings
        self.setWindowTitle("📊 Reports & Analytics - Smart Relationship System")
        self.setGeometry(300, 150, 800, 500)
        self.setStyleSheet("background-color: #E3F2FD;")  # Light Blue Background

        # ✅ Background Image (Glassmorphic UI)
        self.bg_label = QLabel(self)
        bg_path = "static/reports_bg.png"
        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path))
        else:
            print("⚠️ Warning: reports_bg.png not found!")
            self.bg_label.setStyleSheet("background-color: #B3E5FC;")  # Light Blue Fallback
        self.bg_label.setGeometry(0, 0, 800, 500)

        # ✅ Transparent Dashboard Box
        self.dashboard_box = QFrame(self)
        self.dashboard_box.setGeometry(150, 80, 500, 350)
        self.dashboard_box.setStyleSheet("""
            background: rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)

        # ✅ Title Label
        self.title = QLabel("📊 Reports & Analytics", self)
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #37474F; margin-bottom: 10px;")

        # ✅ Report Labels with Icons
        self.total_clients = QLabel(f"👥 Total Clients: {self.get_total_clients()}", self)
        self.total_clients.setFont(QFont("Arial", 14))
        self.total_clients.setAlignment(Qt.AlignCenter)

        self.active_loans = QLabel(f"💳 Active Loans: {self.get_active_loans()}", self)
        self.active_loans.setFont(QFont("Arial", 14))
        self.active_loans.setAlignment(Qt.AlignCenter)

        self.resolved_queries = QLabel(f"✅ Resolved Queries: {self.get_resolved_queries()}", self)
        self.resolved_queries.setFont(QFont("Arial", 14))
        self.resolved_queries.setAlignment(Qt.AlignCenter)

        # ✅ Graph Button with Icon
        self.show_graph_btn = self.create_button("📈 Show Loan Status Graph", "#0078D7", "static/icons/chart.png")
        self.show_graph_btn.clicked.connect(self.show_graph)

        # ✅ Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.total_clients)
        layout.addWidget(self.active_loans)
        layout.addWidget(self.resolved_queries)
        layout.addWidget(self.show_graph_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # ✅ Smooth Fade-in Animation
        self.fade_in_animation()

    def create_button(self, text, color, icon_path):
        """ Create a **modern button with icon & hover effect** """
        button = QPushButton(text, self)
        button.setFont(QFont("Arial", 12))
        button.setFixedWidth(280)
        button.setFixedHeight(45)

        # ✅ Add Icon
        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(22, 22))  # Adjust icon size

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: white;
                color: {color};
                border: 2px solid {color};
                font-weight: bold;
            }}
        """)
        return button

    def get_total_clients(self):
        """ Get the total number of clients (Handled Exception for DB Query) """
        try:
            return User.objects.filter(role="client").count()
        except Exception as e:
            print(f"⚠️ Error fetching total clients: {e}")
            return 0

    def get_active_loans(self):
        """ Get the number of active loans (Handled Exception for DB Query) """
        try:
            return Loan.objects.filter(status="Approved").count()
        except Exception as e:
            print(f"⚠️ Error fetching active loans: {e}")
            return 0

    def get_resolved_queries(self):
        """ Get the number of resolved queries (Handled Exception for DB Query) """
        try:
            return ClientQuery.objects.filter(status="Resolved").count()
        except Exception as e:
            print(f"⚠️ Error fetching resolved queries: {e}")
            return 0

    def show_graph(self):
        """Generate a pie chart for loan statuses with enhanced styling."""
        try:
            data = {
                "Pending": Loan.objects.filter(status="Pending").count(),
                "Approved": Loan.objects.filter(status="Approved").count(),
                "Rejected": Loan.objects.filter(status="Rejected").count(),
            }
            labels = [key for key, value in data.items() if value > 0]  # Remove empty categories
            values = [value for value in data.values() if value > 0]

            if sum(values) == 0:
                QMessageBox.warning(self, "No Data", "No loan data available to generate graph.")
                return

            colors = ["#FFD700", "#32CD32", "#FF6347"]  # Gold, Green, Red

            plt.figure(figsize=(6, 6))
            plt.pie(values, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140, wedgeprops={"edgecolor": "black"})
            plt.title("📊 Loan Status Distribution", fontsize=14, fontweight="bold")
            plt.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate graph: {e}")

    def fade_in_animation(self):
        """ Apply fade-in animation for a **smooth UI experience** """
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)  # 800ms duration
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

# ✅ Run Reports & Analytics Window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportsAnalytics()
    window.show()
    sys.exit(app.exec())
