import React from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with React
// Using the recommended fix for Vite/React reliability
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import shadowIcon from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: shadowIcon,
});

function LocationMarker({ onSelectLocation }) {
  useMapEvents({
    click(e) {
      onSelectLocation(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

export default function MapView({ onSelectLocation, selectedArea }) {
  const initialCenter = [22.9734, 78.6569]; // Center of India

  return (
    <div className="w-full h-full bg-slate-950">
      <MapContainer 
        center={initialCenter} 
        zoom={5} 
        scrollWheelZoom={true}
        className="w-full h-full"
      >
        <TileLayer
          attribution='&copy; Google Maps'
          url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
        />
        {selectedArea && (
          <Marker position={[selectedArea.lat, selectedArea.lng]} />
        )}
        <LocationMarker onSelectLocation={onSelectLocation} />
      </MapContainer>
    </div>
  );
}
