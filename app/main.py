import sys
from PySide6.QtWidgets import QApplication
from app.ui.add_movie_ui import AddMovieForm

app = QApplication(sys.argv)
window = AddMovieForm()
window.resize(800, 600)
window.show()
sys.exit(app.exec())
