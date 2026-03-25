import folium
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import warnings

# Suppress PyQt5 font-related warning
warnings.filterwarnings("ignore", category=UserWarning, module="qt.qpa.fonts")


class MapViewer(QWebEngineView):
    def __init__(self, latitude=17.3850, longitude=78.4867, zoom=12, title="Map Viewer"):
        """
        Display an interactive map using Folium and PyQt5.

        Args:
            latitude: Map center latitude (default: Hyderabad, India)
            longitude: Map center longitude
            zoom: Initial zoom level
            title: Window title
        """
        super().__init__()

        # Create Folium map
        self.map = folium.Map(location=[latitude, longitude], zoom_start=zoom)

        # Add a marker at the center
        folium.Marker(
            location=[latitude, longitude],
            popup=f"Lat: {latitude}, Lon: {longitude}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(self.map)

        # Save map to a temp HTML file next to this script
        map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "map.html")
        self.map.save(map_path)

        # Load the HTML file
        self.setUrl(QUrl.fromLocalFile(map_path))
        self.setWindowTitle(title)
        self.resize(1200, 800)


def main():
    app = QApplication(sys.argv)  # Fixed: pass sys.argv instead of empty list
    viewer = MapViewer(
        latitude=17.3850,   # Hyderabad, India
        longitude=78.4867,
        zoom=12,
        title="Map Viewer - NTTF Project"
    )
    viewer.showMaximized()
    sys.exit(app.exec_())  # Fixed: use sys.exit for proper exit code propagation


if __name__ == "__main__":
    main()
