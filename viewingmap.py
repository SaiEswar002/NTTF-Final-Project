import folium
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import warnings

# Suppress PyQt5 font-related warning
warnings.filterwarnings("ignore", category=UserWarning, module="qt.qpa.fonts")


class MapViewer(QWebEngineView):
    def __init__(self):
        super(MapViewer, self).__init__()

        # Create a Folium Map centered at a specific location (e.g., San Francisco)
        self.map = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

        # Save the map as an HTML file
        self.map.save("map.html")

        # Load the HTML file into the Qt WebEngineView
        self.setUrl(QUrl.fromLocalFile("map.html"))

def main():
    app = QApplication([])
    viewer = MapViewer()
    viewer.showMaximized()
    app.exec_()

if __name__ == "__main__":
    main()
