__author__ = 'Kyle'
from PyQt4.QtWebKit import *
from PyQt4.QtGui import *


class MapWidget(QWebView):
    """
    This is the GMAPS Widget class.
    """

    def __init__(self):

        super().__init__()

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

        var UK = new google.maps.LatLng(51.5072,0.1275);
        var mapOptions = {
            zoom: 6,
            minZoom: 3,
            center: UK,
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

        // Sets the map on all markers in the array.
        function setAllMap(map) {
          for (var i = 0; i < markers.length; i++) {
            markers[i]["Object"].setMap(map);
          }
        }

        function clearMarkers() {
          setAllMap(null);
        }

        // Shows any markers currently in the array.
        function showMarkers() {
          setAllMap(map);
        }

        // Deletes all markers in the array by removing references to them.
        function deleteMarkers() {
          clearMarkers();
          markers = [];
          return "True";
        }









        google.maps.event.addDomListener(window, 'load', initialize);


    </script>
  </head>
  <body>
    <div id="map-canvas"></div>
  </body>
</html> '''
        self.setHtml(self.html)