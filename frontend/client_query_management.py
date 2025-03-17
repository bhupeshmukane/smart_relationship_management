import sys
import os
import django
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget, QMessageBox, QHBoxLayout, QFrame
)
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, QPropertyAnimation

# ✅ Setup Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_relationship_management_system.settings")
django.setup()

from core.models import ClientQuery, User

# ✅ Database Connection Function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bhup@2003",  # Change this to your MySQL password
        database="srms_db"
    )

class QueryManagement(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Set Window Title & Size
        self.setWindowTitle("📌 Client Query Management")
        self.setGeometry(250, 120, 750, 500)
        self.setStyleSheet("background-color: #E3F2FD;")  # Light Blue Background

        # ✅ Background Image
        self.bg_label = QLabel(self)
        bg_path = "static/query_bg.png"
        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path))
        else:
            print("⚠️ Warning: query_bg.png not found!")
            self.bg_label.setStyleSheet("background-color: #B3E5FC;")  # Light Blue Fallback

        self.bg_label.setGeometry(0, 0, 750, 500)

        # ✅ Transparent Glassmorphic Box
        self.dashboard_box = QFrame(self)
        self.dashboard_box.setGeometry(180, 80, 400, 350)
        self.dashboard_box.setStyleSheet("""
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)

        # ✅ Title Label
        self.title = QLabel("📌 Manage Client Queries", self)
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #37474F; margin-bottom: 15px;")

        # ✅ Query List
        self.query_list = QListWidget(self)
        self.query_list.setFixedHeight(250)
        self.query_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
                font-size: 14px;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)

        # ✅ Load Queries
        self.load_queries()

        # ✅ Buttons with Icons & Emojis
        self.resolve_btn = self.create_button("✔ Mark as Resolved", "#28a745", "static/icons/check.png")
        self.refresh_btn = self.create_button("🔄 Refresh List", "#007BFF", "static/icons/refresh.png")
        self.back_btn = self.create_button("🔙 Back to Dashboard", "#FF5733", "static/icons/back.png")

        # ✅ Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.resolve_btn, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.refresh_btn, alignment=Qt.AlignCenter)

        # ✅ Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title, alignment=Qt.AlignCenter)
        layout.addWidget(self.query_list)
        layout.addLayout(button_layout)
        layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # ✅ Connect Buttons
        self.resolve_btn.clicked.connect(self.resolve_query)
        self.refresh_btn.clicked.connect(self.load_queries)
        self.back_btn.clicked.connect(self.go_back_to_dashboard)

        # ✅ Smooth Fade-in Animation
        self.fade_in_animation()

    def create_button(self, text, color, icon_path):
        """ Create a **modern, fully styled button with icons, emojis & hover effect** """
        button = QPushButton(text, self)
        button.setFont(QFont("Arial", 14))
        button.setFixedWidth(250)
        button.setFixedHeight(45)

        # ✅ Add Icon
        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(22, 22))  # ✅ Corrected QSize Import

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

    def load_queries(self):
        """ Load all pending queries into the list """
        self.query_list.clear()
        queries = ClientQuery.objects.filter(status="Pending").order_by("created_at")  # Oldest First

        if queries.exists():
            for query in queries:
                self.query_list.addItem(f"🕒 [{query.created_at.strftime('%Y-%m-%d %H:%M')}] {query.client.username}: {query.subject}")
        else:
            self.query_list.addItem("✅ No pending queries.")

    def resolve_query(self):
        """ Mark selected query as Resolved """
        selected_item = self.query_list.currentItem()
        if not selected_item or "No pending queries" in selected_item.text():
            QMessageBox.warning(self, "⚠ Error", "Please select a query to resolve.")
            return

        # ✅ Extract Query Subject
        query_subject = selected_item.text().split(": ")[1]

        # ✅ Confirm Action
        confirmation = QMessageBox.question(
            self, "Confirm Resolution",
            f"Are you sure you want to mark this query as resolved?\n\n{query_subject}",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            # ✅ Update in Database
            query = ClientQuery.objects.filter(subject=query_subject, status="Pending").first()
            if query:
                query.status = "Resolved"
                query.save()
                QMessageBox.information(self, "✅ Success", "Query marked as resolved.")
                self.load_queries()
            else:
                QMessageBox.warning(self, "⚠ Error", "Could not find the query.")

    def fade_in_animation(self):
        """ Apply fade-in animation for a **smooth UI experience** """
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)  # 800ms duration
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def go_back_to_dashboard(self):
        """ Navigate back to Admin Dashboard """
        from frontend.admin_dashboard import AdminDashboard
        QMessageBox.information(self, "Returning", "Going back to the dashboard...")
        self.new_window = AdminDashboard()
        self.new_window.show()
        self.close()

# ✅ Run Query Management Window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QueryManagement()
    window.show()
    sys.exit(app.exec())
