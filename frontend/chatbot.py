import sys
import os
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFrame
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class ChatbotWindow(QDialog):
    def __init__(self):
        super().__init__()

        # ✅ Set Window Title & Size
        self.setWindowTitle("🤖 RM Chatbot Assistant")
        self.setGeometry(450, 120, 450, 550)
        self.setStyleSheet("background-color: #F4F6F7;")  # Light Grey Background

        # ✅ Chatbot Header
        self.header = QLabel("💬 RM Chatbot Assistant", self)
        self.header.setFont(QFont("Arial", 16, QFont.Bold))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("color: #0078D7; padding: 10px;")

        # ✅ Chat Display Box
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Arial", 12))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background: white;
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 10px;
            }
        """)

        # ✅ User Input Field
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Type your question here...")
        self.user_input.setFont(QFont("Arial", 12))
        self.user_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 1px solid #0078D7;
                padding: 8px;
                border-radius: 10px;
            }
        """)
        self.user_input.returnPressed.connect(self.process_query)

        # ✅ Send Button
        self.send_button = QPushButton("📨 Send", self)
        self.send_button.setFont(QFont("Arial", 12))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 8px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0053a6;
                border: 2px solid white;
            }
        """)
        self.send_button.clicked.connect(self.process_query)

        # ✅ Layout
        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addWidget(self.chat_display)
        layout.addWidget(self.user_input)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def process_query(self):
        """ Process user query and generate a chatbot response """
        user_text = self.user_input.text().strip()
        if user_text:
            self.chat_display.append(f"🧑‍💼 You: {user_text}")

            # ✅ Smart Responses for Specific Queries
            response = self.get_chatbot_response(user_text)

            self.chat_display.append(f"🤖 Chatbot: {response}")
            self.chat_display.append("")  # Spacing for readability

            self.user_input.clear()

            # ✅ Auto-scroll to the latest message
            self.chat_display.moveCursor(self.chat_display.textCursor().End)

    def get_chatbot_response(self, query):
        """ Generate a relevant response based on the user's query """
        query = query.lower()

        if "loan" in query:
            return "💳 We offer personal, home, and car loans. Check your eligibility with an RM."
        elif "investment" in query:
            return "📈 Investment options include Mutual Funds, Stocks, and Fixed Deposits."
        elif "credit card" in query:
            return "💳 We have various credit cards for cashback, travel, and rewards."
        elif "contact rm" in query:
            return "📞 Your assigned Relationship Manager will contact you soon."
        elif "help" in query or "support" in query:
            return "🛠️ I can assist with loans, investments, credit cards, and RM support."
        else:
            return "🔍 I am still learning. Please contact an RM for complex queries."

# ✅ Run Chatbot
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec())
