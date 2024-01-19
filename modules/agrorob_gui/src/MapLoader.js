import React from 'react';
import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents, Polyline} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import NavigationIcon from './navigation_black_24dp.svg';
import L from 'leaflet';
let DefaultIcon = L.icon({
  iconUrl: NavigationIcon,
  shadowUrl: NavigationIcon,
  iconSize: [64,64],
});

L.Marker.prototype.options.icon = DefaultIcon;
const pos = [52.3706361,16.936862599999998]
var i = 0
const poly = [
  pos,
  pos
  // [35.7002, 51.45],
  // [35.7003, 51.45],
  // [35.7002, 51.452]
]

const limeOptions = { color: 'lime' }

function LocationMarker() {
  const [position, setPosition] = useState(null)
  const [polyline,setPolyline] = useState([])
  useEffect(() => {
    const interval = setInterval(() =>     
    fetch("http://localhost:8000/getgpsfix")
    .then(res => res.json())
    .then(
      (result) => {
        // console.log(result.lat)
        // console.log(result.lng)
        setPosition([result.lat, result.lng])
        i = i + 1;
        setPolyline(prevPolyline => [...prevPolyline, [result.lat, result.lng]])
      },
      // Note: it's important to handle errors here
      // instead of a catch() block so that we don't swallow
      // exceptions from actual bugs in components.
      (error) => {
      }
    ), 2000);
  }, [])
  return (position === null) || (i <= 2) ? null : 
    (<>
      <Marker position={position} icon={DefaultIcon}>
        <Popup>Agrorob is here!</Popup>
      </Marker>
      <Polyline pathOptions={limeOptions} positions={polyline} />
    </>)
}

export default class MapLoader extends React.Component {
    render() {
      return <div style={{ height: '500px', width: '100%', float: 'left', zIndex: '1', position: 'relative' }}>
        <MapContainer center={pos} zoom={35} style={{ height: '100vh', width: '100wh' }}>
        <TileLayer
        attribution='© <a href="https://www.mapbox.com/feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/{z}/{x}/{y}?access_token={accessToken}"
        maxZoom="20"
        accessToken='pk.eyJ1IjoiYmFiYWtha2JhcmkiLCJhIjoiY2sxODYxcnVlMWo0bDNvdGdzaWJsZDFzdyJ9.1-2Z4mBSMB4OwqJRSvZUDQ'
      />
      <LocationMarker />
    </MapContainer></div>
    }
  }