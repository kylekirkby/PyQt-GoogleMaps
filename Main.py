import sys
import time

from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import urllib.request

class GoogleMap(QWebView):

    def __init__(self):
        
        super().__init__()

        self.page().mainFrame().addToJavaScriptWindowObject("GoogleMap", self)

        self.loadFinished.connect(self.on_loadFinished)


        self.html='''<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Simple markers</title>
    <style>
      html, body, #map-canvas {
        height: 100%;
        width: 100%
        margin: 0px;
        padding: 0px
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
    <script>
     
        var map;
        var markers = [];
        var geocoder;
        var results = [];
        var coords = [];
        var highestLevel;
       
       
        function initialize() {
       
        geocoder = new google.maps.Geocoder();
       
        var NY = new google.maps.LatLng(40.739112,-73.785848);
        var mapOptions = {
        zoom: 4,
        minZoom: 3,
        center: NY,
        mapTypeId: google.maps.MapTypeId.TERRAIN
        }
        map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
       
        google.maps.event.addListener(map, 'click', function(event) {
        addMarker(event.latLng);
        });
       
       
       
       
       
        // // bounds of the desired area
        // var allowedBounds = new google.maps.LatLngBounds(
        // new google.maps.LatLng(70.33956792419954, 178.01171875),
        // new google.maps.LatLng(83.86483689701898, -88.033203125)
        // );
        // var lastValidCenter = map.getCenter();
       
        // google.maps.event.addListener(map, 'center_changed', function() {
        // if (allowedBounds.contains(map.getCenter())) {
        // // still within valid bounds, so save the last valid position
        // lastValidCenter = map.getCenter();
        // return;
        // }
       
        // // not valid anymore => return to last valid position
        // map.panTo(lastValidCenter);
        // });
       
       
        }
       
       
       
       
        function codeLatLng(lat,lng) {
       
           var results;
           var lat = parseFloat(lat);
           var lng = parseFloat(lng);

           coords.push(lat);
           coords.push(lng);
       
           var latlng = new google.maps.LatLng(lat, lng);
       
            var address;

           geocoder.geocode({'latLng': latlng}, function(results, status) {

               if (status == google.maps.GeocoderStatus.OK) {

                    for( var i = 0; i < results.length; i++){

                         address = results[5].formatted_address;

                    }
    
                    console.log(results[5].formatted_address);
                     highestLevel = results.slice(-1)[0];
       
                    }
       
            else {
              console.log("fail");
            }
       
       
        });

       return address;
       
       
        }
       
       
        function addMarker(location) {
       
       
        var marker = new google.maps.Marker({
        position: location,
        map: map
        });

        //markers.push(marker);

        var lat = marker.getPosition().lat();
        var lng = marker.getPosition().lng();

        var actualAddress = codeLatLng(lat,lng);
        markers.push({"Address":actualAddress,"Object":marker,"Lat":lat,"Lng":lng});

       
        google.maps.event.addListener(marker, 'rightclick', function(event) {
        marker.setMap(null);
        });
       
       
        google.maps.event.addListener(marker, 'click', function(event) {
       
        
        var lat = marker.getPosition().lat();
        
        var lng = marker.getPosition().lng();

        coords2.push(lng);
        coords2.push(lat);

        //console.log(markers.indexOf(marker));
        
        //console.log(lat + " " + lng);
       

        
        //console.log(highestLevel);
       
       
       
        });

       
       
       
       
        }

         function GetMarkers(){

           return markers;

        }
    
 

        
       
       
       
       
        google.maps.event.addDomListener(window, 'load', initialize);


    </script>
  </head>
  <body>
    <div id="map-canvas"></div>
  </body>
</html> '''
        self.setHtml(self.html)


    pyqtSlot(str)  
    def showMessage(self, message):
        print("Message from website:", message)


        

    pyqtSlot()
    
    def on_loadFinished(self):
        getJsValue = """ 
GoogleMap.showMessage("Hello");
"""  
        value = self.page().mainFrame().evaluateJavaScript("GetMarkers()") 
        print(value)

    

    


class GoogleMapsWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle("Maps")
      
        self.create_map()
        self.layout()

    def layout(self):

        self.getMarkersPushButton = QPushButton("Get Markers")

        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.google_maps)
        self.vLayout.addWidget(self.getMarkersPushButton)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.vLayout)

        self.setCentralWidget(self.mainWidget)


        self.getMarkersPushButton.clicked.connect(self.getMarkers)

    def getAddress(self, lat, lng):
        key = "AIzaSyD3hREbHb3M0g8pJL0okru5QKPP_QkBUCg"

        response = urllib.request.urlopen('https://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&key={2}'.format(lat,lng,key))
        html = response.read()
        print(html)


    def getMarkers(self):

        markers = self.google_maps.page().mainFrame().evaluateJavaScript("GetMarkers()")
        print("Writing to file...")
        with open("markers.txt", mode="w", encoding="utf-8") as myFile:
            myFile.write(str(markers))
            print("Completed file write.")
        for each in markers:
            print(each["Lat"])
            print(each["Lng"])

            self.getAddress(each["Lat"],each["Lng"])


    def showMarker(self, markerStr):
        print(markerStr)


    def create_map(self):
        self.google_maps = GoogleMap()
        
##        self.google_maps.page().mainFrame().addToJavaScriptWindowObject("GoogleMapsWindow", self.google_maps)
##        self.google_maps.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
##        self.google_maps.settings().setAttribute(QWebSettings.JavascriptCanOpenWindows, True)
##        self.google_maps.settings().setAttribute(QWebSettings.JavascriptCanAccessClipboard, True)


        

        
if __name__=="__main__":
    application=QApplication(sys.argv)
    window=GoogleMapsWindow()
    window.show()
    window.raise_()
    application.exec_()
    print()
    
        
    
