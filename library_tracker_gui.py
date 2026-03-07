# ============================================================
# LIBRARY BOOK TRACKER — PyQt6 GUI
# Install dependency: pip install PyQt6
# Run with:          python library_tracker_gui.py
# ============================================================

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor


# ============================================================
# OOP LAYER
# ============================================================

class Book:
    """Represents a single book with a title, author, and borrow status."""

    def __init__(self, title, author):
        self.title = title          # User-defined attribute
        self.author = author        # User-defined attribute
        self.is_borrowed = False    # User-defined attribute

    def borrow(self):
        """Marks book as borrowed. Raises Exception if already borrowed."""
        if self.is_borrowed:
            raise Exception(f'"{self.title}" is already borrowed and not available.')
        self.is_borrowed = True

    def return_book(self):
        """Marks book as returned. Raises Exception if not currently borrowed."""
        if not self.is_borrowed:
            raise Exception(f'"{self.title}" was not borrowed, so it cannot be returned.')
        self.is_borrowed = False

    def get_status(self):
        """Returns the availability status as a string."""
        return "Borrowed" if self.is_borrowed else "Available"


class Library:
    """Holds a collection of Book objects and manages them."""

    def __init__(self, name):
        self.name = name    # User-defined attribute
        self.books = []     # User-defined attribute
        # Pre-load starter books
        self._add_starter_books()

    def _add_starter_books(self):
        self.books.append(Book("The Alchemist", "Paulo Coelho"))
        self.books.append(Book("1984", "George Orwell"))
        self.books.append(Book("To Kill a Mockingbird", "Harper Lee"))

    def add_book(self, title, author):
        """Adds a new book. Raises Exception if duplicate title exists."""
        for b in self.books:
            if b.title.lower() == title.lower():
                raise Exception(f'"{title}" already exists in the library.')
        self.books.append(Book(title, author))

    def find_book(self, title):
        """Finds a book by title (case-insensitive). Raises Exception if not found."""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        raise Exception(f'"{title}" was not found in the library.')


# ============================================================
# GUI LAYER — PyQt6
# ============================================================

# Stylesheet — forest green theme
STYLE = """
    QMainWindow, QWidget#main_widget {
        background-color: #f5f5f0;
    }

    /* Sidebar */
    QWidget#sidebar {
        background-color: #1a2e1a;
        border-radius: 0px;
    }
    QLabel#app_title {
        color: #ffffff;
        font-size: 16px;
        font-weight: bold;
        padding: 6px 0px;
    }
    QLabel#app_subtitle {
        color: rgba(255,255,255,0.45);
        font-size: 11px;
    }

    /* Nav buttons */
    QPushButton#nav_btn {
        background-color: transparent;
        color: rgba(255,255,255,0.65);
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        text-align: left;
        font-size: 13px;
    }
    QPushButton#nav_btn:hover {
        background-color: rgba(255,255,255,0.08);
        color: #ffffff;
    }
    QPushButton#nav_btn_active {
        background-color: rgba(255,255,255,0.15);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        text-align: left;
        font-size: 13px;
        font-weight: bold;
    }

    /* Cards / panels */
    QWidget#panel {
        background-color: #ffffff;
        border-radius: 12px;
    }

    /* Table */
    QTableWidget {
        background-color: #ffffff;
        border: 1px solid #e0e5e0;
        border-radius: 10px;
        gridline-color: #f0f0ec;
        font-size: 13px;
    }
    QTableWidget::item {
        padding: 8px 12px;
        color: #1a2e1a;
    }
    QTableWidget::item:selected {
        background-color: #e8f5e9;
        color: #1a2e1a;
    }
    QHeaderView::section {
        background-color: #f5f5f0;
        color: #4a5e4a;
        font-size: 11px;
        font-weight: bold;
        padding: 8px 12px;
        border: none;
        border-bottom: 1px solid #dde5dd;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Input fields */
    QLineEdit {
        background-color: #f5f5f0;
        border: 1.5px solid #d5ddd5;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        color: #1a2e1a;
    }
    QLineEdit:focus {
        border-color: #2d6a2d;
        background-color: #ffffff;
    }

    /* Primary button */
    QPushButton#primary_btn {
        background-color: #2d6a2d;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 11px 24px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton#primary_btn:hover {
        background-color: #245224;
    }
    QPushButton#primary_btn:pressed {
        background-color: #1a3d1a;
    }

    /* Section labels */
    QLabel#section_title {
        color: #1a2e1a;
        font-size: 18px;
        font-weight: bold;
    }
    QLabel#section_desc {
        color: #7a8e7a;
        font-size: 12px;
    }
    QLabel#field_label {
        color: #4a5e4a;
        font-size: 11px;
        font-weight: bold;
    }

    /* Toast notification */
    QLabel#toast_success {
        background-color: #1a2e1a;
        color: #ffffff;
        border-radius: 20px;
        padding: 10px 22px;
        font-size: 12px;
        font-weight: bold;
    }
    QLabel#toast_error {
        background-color: #7f1d1d;
        color: #ffffff;
        border-radius: 20px;
        padding: 10px 22px;
        font-size: 12px;
        font-weight: bold;
    }

    /* Divider */
    QFrame#divider {
        color: #e0e5e0;
    }

    /* Stats bar */
    QLabel#stat_label {
        color: rgba(255,255,255,0.5);
        font-size: 11px;
    }
    QLabel#stat_value {
        color: #ffffff;
        font-size: 13px;
        font-weight: bold;
    }
"""


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.library = Library("My Library")
        self.setWindowTitle("Library Book Tracker")
        self.setMinimumSize(780, 520)
        self.resize(860, 560)

        # Central widget
        root = QWidget()
        root.setObjectName("main_widget")
        self.setCentralWidget(root)
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Build sidebar + content
        layout.addWidget(self._build_sidebar())
        layout.addWidget(self._build_content(), stretch=1)

        self.setStyleSheet(STYLE)
        self._switch_page(0)

    # ----------------------------------------------------------
    # SIDEBAR
    # ----------------------------------------------------------
    def _build_sidebar(self):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 28, 16, 28)
        layout.setSpacing(4)

        # App title
        icon = QLabel("📚")
        icon.setFont(QFont("Segoe UI Emoji", 28))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        title = QLabel("Library\nTracker")
        title.setObjectName("app_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        # Nav buttons
        self.nav_buttons = []
        nav_items = [
            ("📋  All Books", 0),
            ("📖  Borrow",    1),
            ("🔄  Return",    2),
            ("➕  Add Book",  3),
        ]
        for label, idx in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("nav_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self._switch_page(i))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        layout.addStretch()

        # Stats
        self.stat_total   = self._stat_row(layout, "Total Books")
        self.stat_avail   = self._stat_row(layout, "Available")
        self.stat_borrowed = self._stat_row(layout, "Borrowed")

        return sidebar

    def _stat_row(self, parent_layout, label_text):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setObjectName("stat_label")
        val = QLabel("0")
        val.setObjectName("stat_value")
        val.setAlignment(Qt.AlignmentFlag.AlignRight)
        row.addWidget(lbl)
        row.addWidget(val)
        parent_layout.addLayout(row)
        return val

    def _update_stats(self):
        total    = len(self.library.books)
        borrowed = sum(1 for b in self.library.books if b.is_borrowed)
        avail    = total - borrowed
        self.stat_total.setText(str(total))
        self.stat_avail.setText(str(avail))
        self.stat_borrowed.setText(str(borrowed))

    # ----------------------------------------------------------
    # CONTENT AREA
    # ----------------------------------------------------------
    def _build_content(self):
        self.stack = QStackedWidget()
        self.stack.setContentsMargins(20, 20, 20, 20)

        self.stack.addWidget(self._page_all_books())   # 0
        self.stack.addWidget(self._page_borrow())      # 1
        self.stack.addWidget(self._page_return())      # 2
        self.stack.addWidget(self._page_add_book())    # 3

        # Toast overlay (sits on top)
        self.toast_label = QLabel("")
        self.toast_label.setObjectName("toast_success")
        self.toast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toast_label.setParent(self.stack)
        self.toast_label.hide()

        self.toast_timer = QTimer()
        self.toast_timer.setSingleShot(True)
        self.toast_timer.timeout.connect(self.toast_label.hide)

        return self.stack

    def _switch_page(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setObjectName("nav_btn_active" if i == index else "nav_btn")
            btn.setStyleSheet(STYLE)  # Re-apply to refresh object name
        if index == 0:
            self._refresh_table()
        self._update_stats()

    # ----------------------------------------------------------
    # PAGE 0 — All Books
    # ----------------------------------------------------------
    def _page_all_books(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("All Books")
        title.setObjectName("section_title")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Title", "Author", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 110)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        layout.addWidget(self.table)

        return page

    def _refresh_table(self):
        self.table.setRowCount(0)
        for book in self.library.books:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(book.title))
            self.table.setItem(row, 1, QTableWidgetItem(book.author))

            # Colored status badge via item background
            status_item = QTableWidgetItem(book.get_status())
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if book.is_borrowed:
                status_item.setForeground(QColor("#92400e"))
                status_item.setBackground(QColor("#fef3c7"))
            else:
                status_item.setForeground(QColor("#166534"))
                status_item.setBackground(QColor("#dcfce7"))
            self.table.setItem(row, 2, status_item)
            self.table.setRowHeight(row, 42)

    # ----------------------------------------------------------
    # PAGE 1 — Borrow
    # ----------------------------------------------------------
    def _page_borrow(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        QLabel("📖", parent=page)  # just for spacing feel
        title = QLabel("Borrow a Book")
        title.setObjectName("section_title")
        desc = QLabel("Enter the exact title of the book you'd like to borrow.")
        desc.setObjectName("section_desc")
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(10)

        lbl = QLabel("BOOK TITLE")
        lbl.setObjectName("field_label")
        layout.addWidget(lbl)

        self.borrow_input = QLineEdit()
        self.borrow_input.setPlaceholderText("e.g. 1984")
        self.borrow_input.returnPressed.connect(self._handle_borrow)
        layout.addWidget(self.borrow_input)
        layout.addSpacing(6)

        btn = QPushButton("Borrow Book")
        btn.setObjectName("primary_btn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._handle_borrow)
        layout.addWidget(btn)
        layout.addStretch()
        return page

    def _handle_borrow(self):
        title = self.borrow_input.text().strip()
        try:
            if not title:
                raise ValueError("Please enter a book title.")
            book = self.library.find_book(title)
            book.borrow()
            self.borrow_input.clear()
            self._update_stats()
            self._show_toast(f'✓  "{book.title}" borrowed successfully!', success=True)
        except Exception as e:
            self._show_toast(f'✕  {e}', success=False)

    # ----------------------------------------------------------
    # PAGE 2 — Return
    # ----------------------------------------------------------
    def _page_return(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel("Return a Book")
        title.setObjectName("section_title")
        desc = QLabel("Enter the title of the book you are returning.")
        desc.setObjectName("section_desc")
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(10)

        lbl = QLabel("BOOK TITLE")
        lbl.setObjectName("field_label")
        layout.addWidget(lbl)

        self.return_input = QLineEdit()
        self.return_input.setPlaceholderText("e.g. 1984")
        self.return_input.returnPressed.connect(self._handle_return)
        layout.addWidget(self.return_input)
        layout.addSpacing(6)

        btn = QPushButton("Return Book")
        btn.setObjectName("primary_btn")
        btn.setStyleSheet("QPushButton#primary_btn { background-color: #0d6e6e; } QPushButton#primary_btn:hover { background-color: #0a5555; }")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._handle_return)
        layout.addWidget(btn)
        layout.addStretch()
        return page

    def _handle_return(self):
        title = self.return_input.text().strip()
        try:
            if not title:
                raise ValueError("Please enter a book title.")
            book = self.library.find_book(title)
            book.return_book()
            self.return_input.clear()
            self._update_stats()
            self._show_toast(f'✓  "{book.title}" returned. Thank you!', success=True)
        except Exception as e:
            self._show_toast(f'✕  {e}', success=False)

    # ----------------------------------------------------------
    # PAGE 3 — Add Book
    # ----------------------------------------------------------
    def _page_add_book(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel("Add a New Book")
        title.setObjectName("section_title")
        desc = QLabel("Fill in the details to add a book to the library.")
        desc.setObjectName("section_desc")
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(10)

        lbl1 = QLabel("BOOK TITLE")
        lbl1.setObjectName("field_label")
        layout.addWidget(lbl1)
        self.add_title_input = QLineEdit()
        self.add_title_input.setPlaceholderText("e.g. The Great Gatsby")
        layout.addWidget(self.add_title_input)
        layout.addSpacing(8)

        lbl2 = QLabel("AUTHOR")
        lbl2.setObjectName("field_label")
        layout.addWidget(lbl2)
        self.add_author_input = QLineEdit()
        self.add_author_input.setPlaceholderText("e.g. F. Scott Fitzgerald")
        self.add_author_input.returnPressed.connect(self._handle_add)
        layout.addWidget(self.add_author_input)
        layout.addSpacing(6)

        btn = QPushButton("Add Book")
        btn.setObjectName("primary_btn")
        btn.setStyleSheet("QPushButton#primary_btn { background-color: #5b21b6; } QPushButton#primary_btn:hover { background-color: #4c1d95; }")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._handle_add)
        layout.addWidget(btn)
        layout.addStretch()
        return page

    def _handle_add(self):
        title  = self.add_title_input.text().strip()
        author = self.add_author_input.text().strip()
        try:
            if not title or not author:
                raise ValueError("Title and author cannot be empty.")
            self.library.add_book(title, author)
            self.add_title_input.clear()
            self.add_author_input.clear()
            self._update_stats()
            self._show_toast(f'✓  "{title}" added to the library!', success=True)
        except Exception as e:
            self._show_toast(f'✕  {e}', success=False)

    # ----------------------------------------------------------
    # TOAST NOTIFICATION
    # ----------------------------------------------------------
    def _show_toast(self, message, success=True):
        self.toast_label.setObjectName("toast_success" if success else "toast_error")
        self.toast_label.setStyleSheet(STYLE)
        self.toast_label.setText(message)
        self.toast_label.adjustSize()

        # Center it at the bottom of the stack
        sw = self.stack.width()
        sh = self.stack.height()
        tw = self.toast_label.width() + 40
        th = self.toast_label.height()
        self.toast_label.setFixedSize(tw, th + 10)
        self.toast_label.move((sw - tw) // 2, sh - th - 40)
        self.toast_label.raise_()
        self.toast_label.show()

        self.toast_timer.start(3000)

    def resizeEvent(self, event):
        """Reposition toast on window resize."""
        super().resizeEvent(event)
        if self.toast_label.isVisible():
            sw = self.stack.width()
            sh = self.stack.height()
            tw = self.toast_label.width()
            th = self.toast_label.height()
            self.toast_label.move((sw - tw) // 2, sh - th - 40)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())