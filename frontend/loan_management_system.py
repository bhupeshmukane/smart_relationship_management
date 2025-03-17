import sys
import os
import django
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget, QMessageBox, 
    QHBoxLayout, QComboBox, QFrame
)
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QSize

# ✅ Setup Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_relationship_management_system.settings")
django.setup()

from core.models import Loan  # ✅ Import Django model

class LoanManagement(QWidget):
    def __init__(self):
        super().__init__()

        # ✅ Window Settings
        self.setWindowTitle("🏦 Loan Management - Smart Relationship System")
        self.setGeometry(250, 120, 800, 500)
        self.setStyleSheet("background-color: #E3F2FD;")  # Light Blue Background

        # ✅ Background Image (Glassmorphic UI)
        self.bg_label = QLabel(self)
        bg_path = "static/loan_bg.png"
        if os.path.exists(bg_path):
            self.bg_label.setPixmap(QPixmap(bg_path))
        else:
            print("⚠️ Warning: loan_bg.png not found!")
            self.bg_label.setStyleSheet("background-color: #B3E5FC;")  # Light Blue Fallback
        self.bg_label.setGeometry(0, 0, 800, 500)

        ''' # ✅ Transparent Dashboard Box
        self.dashboard_box = QFrame(self)
        self.dashboard_box.setGeometry(150, 80, 500, 350)
        self.dashboard_box.setStyleSheet("""
            background: rgba(255, 255, 255, 0.3);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)'''

        # ✅ Title Label
        self.title = QLabel("🏦 Manage Loan Applications", self)
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #37474F; margin-bottom: 10px;")

        # ✅ Status Filter
        self.filter_label = QLabel("📌 Filter by Status:", self)
        self.filter_label.setFont(QFont("Arial", 12))
        self.status_filter = QComboBox(self)
        self.status_filter.addItems(["All", "Pending", "Approved", "Rejected"])
        self.status_filter.setFixedWidth(200)
        self.status_filter.setStyleSheet("padding: 6px; background: white; border-radius: 6px;")
        self.status_filter.currentIndexChanged.connect(self.load_loans)

        # ✅ Loan List
        self.loan_list = QListWidget(self)
        self.loan_list.setFixedHeight(280)
        self.loan_list.setStyleSheet("""
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

        # ✅ Load Loans
        self.load_loans()

        # ✅ Buttons with Icons
        self.approve_btn = self.create_button("✔ Approve Loan", "#4CAF50", "static/icons/approve.png")
        self.reject_btn = self.create_button("❌ Reject Loan", "#FF5733", "static/icons/reject.png")

        # ✅ Layouts
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.status_filter)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.approve_btn)
        btn_layout.addWidget(self.reject_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addLayout(filter_layout)
        layout.addWidget(self.loan_list)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # ✅ Button Click Actions
        self.approve_btn.clicked.connect(lambda: self.update_loan_status("Approved"))
        self.reject_btn.clicked.connect(lambda: self.update_loan_status("Rejected"))

        # ✅ Smooth Fade-in Animation
        self.fade_in_animation()

    def create_button(self, text, color, icon_path):
        """ Create a **modern button with icon & hover effect** """
        button = QPushButton(text, self)
        button.setFont(QFont("Arial", 12))
        button.setFixedWidth(180)
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

    def load_loans(self):
        """ Load loan applications into the list based on filter """
        self.loan_list.clear()
        status_filter = self.status_filter.currentText()

        if status_filter == "All":
            loans = Loan.objects.all().order_by("applied_at")
        else:
            loans = Loan.objects.filter(status=status_filter).order_by("applied_at")

        if loans.exists():
            for loan in loans:
                self.loan_list.addItem(f"📅 [{loan.applied_at.strftime('%Y-%m-%d')}] {loan.client.username} - {loan.loan_type} - ₹{loan.amount} ({loan.status})")
        else:
            self.loan_list.addItem("✅ No loans found.")

    def update_loan_status(self, new_status):
        """ Update selected loan status """
        selected_item = self.loan_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "⚠️ Error", "Please select a loan to update.")
            return

        # ✅ Extract Loan Data
        loan_info = selected_item.text().split(" - ")
        username = loan_info[1]
        loan_type = loan_info[2].split(" (")[0]

        # ✅ Update in Database
        loan = Loan.objects.filter(client__username=username, loan_type=loan_type, status="Pending").first()
        if loan:
            loan.status = new_status
            loan.save()
            QMessageBox.information(self, "✅ Success", f"Loan marked as {new_status}.")
            self.load_loans()
        else:
            QMessageBox.warning(self, "⚠️ Error", "Could not find loan.")

    def fade_in_animation(self):
        """ Apply fade-in animation for a **smooth UI experience** """
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)  # 800ms duration
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

# ✅ Run Loan Management Window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoanManagement()
    window.show()
    sys.exit(app.exec())
