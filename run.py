__author__ = 'Kyle'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
import json

from MapWidget import *
import urllib.request

class MainWindow(QMainWindow):

    """
    This is main window for the gmaps pyqt4 application.
    """

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Google Maps PyQt4 Application")

        self.mapMarkers = []
        self.API_KEY = "AIzaSyD3hREbHb3M0g8pJL0okru5QKPP_QkBUCg"

        #add a status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        #Create a new stacked layout
        self.stackedLayout = QStackedLayout()

        #Generate Initial Layout
        self.layout()


        #Create the stacked widget
        self.stackedWidget = QWidget()
        self.stackedWidget.setLayout(self.stackedLayout)

        #Set the windows central widget
        self.setCentralWidget(self.stackedWidget)


    def layout(self):

        self.mapGroupBox = QGroupBox("Map Widget")
        self.mapOptionsGroupBox = QGroupBox("Map Options")
        self.mapMarkersGroupBox = QGroupBox("Map Markers")
        self.locationGroupBox = QGroupBox("Location")


        #Layout
        self.mapLayout = QVBoxLayout()
        self.mapOptionsLayout = QHBoxLayout()
        self.mapMarkersLayout = QVBoxLayout()



        #Widgets
        self.map = MapWidget()


        self.clearAllMarkersPushButton = QPushButton("Clear All Markers")
        self.terrainSettingPushButton = QPushButton("Toggle Satellite View")


        self.getMarkersPushButton = QPushButton("Get Markers")

        #Create the progress bar
        self.markersProgressBar = QProgressBar()
        self.markersProgressBar.setTextVisible(True)
        self.markersProgressBar.setFormat("Downloading Markers... %p%")
        self.markersProgressBar.setAlignment(Qt.AlignCenter)

        self.markersListView  = QListWidget()




        self.addMarkerButton = QPushButton("Add Marker")


        self.streetLabel = QLabel("Street")
        self.cityTownLabel = QLabel("City/Town")
        self.countyLabel = QLabel("State/County")
        self.postCodeLabel = QLabel("Zip/Post Code")
        self.countryLabel = QLabel("Country")


        self.street = QLabel()
        self.cityTown = QLabel()
        self.county = QLabel()
        self.postCode = QLabel()
        self.country = QLabel()

        self.addressGrid = QGridLayout()

        self.addressGrid.addWidget(self.streetLabel, 1, 0)
        self.addressGrid.addWidget(self.street, 1, 1)

        self.addressGrid.addWidget(self.cityTownLabel,2,0)
        self.addressGrid.addWidget(self.cityTown,2 ,1)

        self.addressGrid.addWidget(self.countyLabel,3, 0)
        self.addressGrid.addWidget(self.county, 3, 1)

        self.addressGrid.addWidget(self.postCodeLabel, 4, 0)
        self.addressGrid.addWidget(self.postCode,4 ,1)

        self.addressGrid.addWidget(self.countryLabel, 5, 0)
        self.addressGrid.addWidget(self.country, 5, 1)

        #add Address grid to group box
        self.locationGroupBox.setLayout(self.addressGrid)

        #Add Map Marker Widgets to mapMarker Layout
        self.mapMarkersLayout.addWidget(self.clearAllMarkersPushButton)
        self.mapMarkersLayout.addWidget(self.getMarkersPushButton)
        self.mapMarkersLayout.addWidget(self.markersProgressBar)
        self.mapMarkersLayout.addWidget(self.markersListView)

        #Set Layout of Map Markers Group Box
        self.mapMarkersGroupBox.setLayout(self.mapMarkersLayout)

        #Add Options to options layout
        self.mapOptionsLayout.addWidget(self.terrainSettingPushButton)

        #Add Options Layout to options group box
        self.mapOptionsGroupBox.setLayout(self.mapOptionsLayout)



        #Add Widget to layout
        self.mapLayout.addWidget(self.map)

        self.mapGroupBox.setLayout(self.mapLayout)

        self.mainGridLayout = QGridLayout()

        self.mainGridLayout.addWidget(self.mapGroupBox,0 ,0)
        self.mainGridLayout.addWidget(self.mapMarkersGroupBox, 0, 1)
        self.mainGridLayout.addWidget(self.mapOptionsGroupBox, 1, 0)
        self.mainGridLayout.addWidget(self.locationGroupBox, 1, 1)

        #Main Widget for stacked layout.
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainGridLayout)


        #Connections
        self.getMarkersPushButton.clicked.connect(self.getMapMarkers)
        self.clearAllMarkersPushButton.clicked.connect(self.removeMarkers)
        self.markersListView.currentItemChanged.connect(self.getLocationData)

        #Add to Stacked Layout
        self.stackedLayout.addWidget(self.mainWidget)

    def getLocationData(self):

        itemText = self.markersListView.currentItem().text()

        for marker in self.mapMarkers:
            try:
                markerText = marker[2][0]
                if markerText == itemText:
                    addressData = markerText
            except IndexError:
                return False


        splitData = addressData.split(",")

        for each in splitData:
            print(each)



    def getAddress(self, lat, lng):

        response = urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}'.format(lat,lng,self.API_KEY))
        html = response.read().decode("utf-8")

        return html


    def getMapMarkers(self):

        self.markersListView.clear()
        self.mapMarkers = []

        markers = self.map.page().mainFrame().evaluateJavaScript("GetMarkers()")

        for each in markers:
            newMarker = []
            newMarker.append(each["Lat"])
            newMarker.append(each["Lng"])
            self.mapMarkers.append(newMarker)


        self.addMarkersToList()

    def addMarkersToList(self):

        if len(self.mapMarkers) > 0:

            currentValue = self.markersProgressBar.value()

            addValue = 100 / len(self.mapMarkers)

            for marker in self.mapMarkers:
                address = self.getAddress(marker[0], marker[1])
                readAddress = json.loads(address)
                textAddress = []

                for each in readAddress["results"]:
                    for key,value in each.items():
                        if key == "formatted_address":
                            textAddress.append(value)
                if len(marker) == 2:
                    marker.append(textAddress)

                newValue = self.markersProgressBar.value() + addValue

                self.markersProgressBar.setValue(newValue)

            self.markersProgressBar.setValue(100)
            self.markersProgressBar.setValue(0)

            for marker in self.mapMarkers:

                try:
                    markerText = marker[2][0]
                    self.markersListView.addItem(markerText)
                except IndexError:
                    markerText = "Unknown Location"
                    self.markersListView.addItem(markerText)
            self.statusBar.showMessage("Marker Info Collected", 3000)

        else:
            self.statusBar.showMessage("No Markers on the map!", 3000)

    def clearMarkerList(self):

        self.markersListView.clear()

    def removeMarkers(self):

        deleted = self.map.page().mainFrame().evaluateJavaScript("deleteMarkers()")

        if deleted == "True":
            self.statusBar.showMessage("Markers were deleted!",3000)
            self.clearMarkerList()
        else:
            self.statusBar.showMessage("Markers were not deleted!", 3000)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.raise_()
    window.show()
    app.exec_()

