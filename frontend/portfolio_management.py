import sys
import os
import django
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QListWidget, QFrame
)
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QSize

# ✅ Setup Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_relationship_management_system.settings")
django.setup()

from core.models import Portfolio  # ✅ Import Django Model

class PortfolioManagement(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Window Settings
        self.setWindowTitle("📊 Portfolio Management - Smart Relationship System")
        self.setGeometry(250, 120, 800, 500)
        self.setStyleSheet("background-color: #E3F2FD;")  # Light Blue Background

        # ✅ Background Image (Glassmorphic UI)
        self.bg_label = QLabel(self)
        bg_path = "static/portfolio_bg.png"
        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path))
        else:
            print("⚠️ Warning: portfolio_bg.png not found!")
            self.bg_label.setStyleSheet("background-color: #B3E5FC;")  # Light Blue Fallback
        self.bg_label.setGeometry(0, 0, 800, 500)

        '''# ✅ Transparent Dashboard Box
        self.dashboard_box = QFrame(self)
        self.dashboard_box.setGeometry(150, 80, 500, 350)
        self.dashboard_box.setStyleSheet("""
            background: rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)'''

        # ✅ Title Label
        self.title = QLabel("📊 Manage Client Portfolios", self)
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #37474F; margin-bottom: 10px;")

        # ✅ Portfolio List
        self.portfolio_list = QListWidget(self)
        self.portfolio_list.setFixedHeight(280)
        self.portfolio_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background: #4CAF50;
                color: white;
            }
        """)

        # ✅ Load Portfolios
        self.load_portfolio()

        # ✅ Buttons with Icons
        self.add_btn = self.create_button("➕ Add Investment", "#4CAF50", "static/icons/add.png")
        self.edit_btn = self.create_button("✏ Edit Investment", "#2196F3", "static/icons/edit.png")
        self.delete_btn = self.create_button("🗑 Delete Investment", "#FF5733", "static/icons/delete.png")

        # ✅ Layouts
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.portfolio_list)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # ✅ Button Click Actions
        self.add_btn.clicked.connect(self.add_investment)
        self.edit_btn.clicked.connect(self.edit_investment)
        self.delete_btn.clicked.connect(self.delete_investment)

        # ✅ Smooth Fade-in Animation
        self.fade_in_animation()

    def create_button(self, text, color, icon_path):
        """ Create a **modern button with icon & hover effect** """
        button = QPushButton(text, self)
        button.setFont(QFont("Arial", 12))
        button.setFixedWidth(200)
        button.setFixedHeight(40)

        # ✅ Add Icon
        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(20, 20))  # Adjust icon size

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
                font-weight: bold;
            }}
        """)
        return button

    def load_portfolio(self):
        """ Load all portfolio investments into the list """
        self.portfolio_list.clear()
        portfolios = Portfolio.objects.all()

        if portfolios.exists():
            for investment in portfolios:
                self.portfolio_list.addItem(f"📈 {investment.client.username} - {investment.investment_type}: ₹{investment.amount} (P/L: ₹{investment.profit_loss})")
        else:
            self.portfolio_list.addItem("✅ No investments found.")

    def add_investment(self):
        """ Open Add Investment Window """
        QMessageBox.information(self, "⚙️ Feature Coming", "Add Investment functionality coming soon!")

    def edit_investment(self):
        """ Edit selected investment """
        QMessageBox.information(self, "⚙️ Feature Coming", "Edit Investment functionality coming soon!")

    def delete_investment(self):
        """ Delete selected investment """
        selected_item = self.portfolio_list.currentItem()
        if not selected_item or "No investments found" in selected_item.text():
            QMessageBox.warning(self, "⚠️ Error", "Please select an investment to delete.")
            return
        
        QMessageBox.information(self, "✅ Success", "Investment deleted successfully.")
        self.load_portfolio()

    def fade_in_animation(self):
        """ Apply fade-in animation for a **smooth UI experience** """
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)  # 800ms duration
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

# ✅ Run Portfolio Management Window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortfolioManagement()
    window.show()
    sys.exit(app.exec())
