# manager/style_manager.py
from config.settings import (
    COLOR_PRIMARY, COLOR_PRIMARY_LIGHT, COLOR_SECONDARY,
    COLOR_BACKGROUND, COLOR_TEXT_WHITE, COLOR_TEXT_GRAY,
    BUTTON_ROUND_RADIUS, WINDOW_ROUND_RADIUS,
    FONT_MAIN, FONT_SIZE_NORMAL
)

def get_global_style():
    """全局通用样式表（所有界面共用）"""
    return f"""
        QWidget {{
            font-family: {FONT_MAIN}, "Segoe UI", Arial, sans-serif; 
            font-size: {FONT_SIZE_NORMAL}px; 
            color: {COLOR_TEXT_WHITE};
            background-color: {COLOR_BACKGROUND};
        }}

        /* 功能按钮样式 */
        QPushButton {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_PRIMARY}, stop:1 {COLOR_SECONDARY});
            color: white;
            border: 2px solid {COLOR_PRIMARY};
            border-radius: {BUTTON_ROUND_RADIUS}px;
            padding: 10px 25px;
            font-weight: bold;
            transition: all 0.2s ease;
        }}
        QPushButton:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_PRIMARY_LIGHT}, stop:1 {COLOR_SECONDARY});
            border-color: {COLOR_PRIMARY_LIGHT};
            box-shadow: 0 0 20px {COLOR_PRIMARY};
            transform: scale(1.02);
        }}
        QPushButton:pressed {{
            transform: scale(0.98);
        }}

        /* 表格样式 */
        QHeaderView::section {{
            background-color: #0f1b2f;
            color: white;
            border: 1px solid #333;
            padding: 5px;
            font-weight: bold;
        }}
        QHeaderView::section:hover {{
            background-color: #1a2b4f;
        }}

        QTableWidget {{
            background-color: #252525;
            border: 1px solid #333;
            border-radius: 10px;
            gridline-color: #333;
        }}
        QTableWidget::item {{
            color: {COLOR_TEXT_GRAY};
            padding: 10px;
        }}
        QTableWidget::item:selected {{
            background-color: {COLOR_PRIMARY};
            color: #000;
        }}

        /* 输入框样式 */
        QLineEdit {{
            background-color: #252525;
            color: white;
            border: 1px solid #444;
            border-radius: 10px;
            padding: 8px;
        }}
        QLineEdit:focus {{
            border: 1px solid {COLOR_PRIMARY};
            box-shadow: 0 0 10px {COLOR_PRIMARY};
        }}

        /* 弹窗样式 */
        QMessageBox {{
            background-color: #333;
        }}
        QMessageBox QLabel {{
            color: #fff;
        }}

        /* 圆角容器样式 */
        QWidget#round_container {{
            background-color: {COLOR_BACKGROUND};
            border-radius: {WINDOW_ROUND_RADIUS}px;
        }}
    """