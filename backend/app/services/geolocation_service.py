"""Geolocation service for distance calculation and location management."""

from typing import Tuple, Optional, Dict, Any
from decimal import Decimal
import math
import logging

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

logger = logging.getLogger(__name__)


class GeoLocationService:
    """Service for geolocation operations."""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="quicktym_rental_app")
    
    async def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Convert address string to latitude and longitude.
        
        Args:
            address: Address string to geocode
            
        Returns:
            Tuple of (latitude, longitude) or None if geocoding fails
        """
        try:
            location = self.geolocator.geocode(address, timeout=10)
            if location:
                return (location.latitude, location.longitude)
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Geocoding failed for address '{address}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected geocoding error: {e}")
            return None
    
    async def reverse_geocode(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Convert latitude and longitude to address string.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Address string or None if reverse geocoding fails
        """
        try:
            location = self.geolocator.reverse((latitude, longitude), timeout=10)
            if location:
                return location.address
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Reverse geocoding failed for ({latitude}, {longitude}): {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected reverse geocoding error: {e}")
            return None
    
    def calculate_distance(
        self,
        coord1: Tuple[float, float],
        coord2: Tuple[float, float]
    ) -> float:
        """
        Calculate distance between two coordinates in kilometers.
        
        Args:
            coord1: Tuple of (latitude, longitude) for first location
            coord2: Tuple of (latitude, longitude) for second location
            
        Returns:
            Distance in kilometers
        """
        try:
            distance = geodesic(coord1, coord2).kilometers
            return round(distance, 2)
        except Exception as e:
            logger.error(f"Distance calculation error: {e}")
            # Fallback to Haversine formula
            return self._haversine_distance(coord1, coord2)
    
    def _haversine_distance(
        self,
        coord1: Tuple[float, float],
        coord2: Tuple[float, float]
    ) -> float:
        """
        Calculate distance using Haversine formula (fallback).
        
        Args:
            coord1: Tuple of (latitude, longitude) for first location
            coord2: Tuple of (latitude, longitude) for second location
            
        Returns:
            Distance in kilometers
        """
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Earth's radius in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        # Haversine formula
        a = math.sin(delta_lat / 2)**2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return round(distance, 2)
    
    def calculate_delivery_fee(
        self,
        distance_km: float,
        base_fee: float = 30.0,
        per_km_rate: float = 5.0,
        max_fee: float = 150.0
    ) -> float:
        """
        Calculate delivery fee based on distance.
        
        Args:
            distance_km: Distance in kilometers
            base_fee: Base delivery fee
            per_km_rate: Rate per kilometer
            max_fee: Maximum delivery fee
            
        Returns:
            Calculated delivery fee
        """
        fee = base_fee + (distance_km * per_km_rate)
        return min(round(fee, 2), max_fee)
    
    def estimate_travel_time(
        self,
        distance_km: float,
        avg_speed_kmh: float = 25.0
    ) -> int:
        """
        Estimate travel time in minutes.
        
        Args:
            distance_km: Distance in kilometers
            avg_speed_kmh: Average speed in km/h (default: 25 km/h for city traffic)
            
        Returns:
            Estimated time in minutes
        """
        time_hours = distance_km / avg_speed_kmh
        time_minutes = int(time_hours * 60)
        return max(time_minutes, 10)  # Minimum 10 minutes
    
    def is_within_service_area(
        self,
        coord: Tuple[float, float],
        center: Tuple[float, float],
        radius_km: float = 30.0
    ) -> bool:
        """
        Check if a location is within the service area.
        
        Args:
            coord: Coordinates to check
            center: Center of service area
            radius_km: Service radius in kilometers
            
        Returns:
            True if within service area, False otherwise
        """
        distance = self.calculate_distance(coord, center)
        return distance <= radius_km
    
    def get_bounding_box(
        self,
        center: Tuple[float, float],
        radius_km: float
    ) -> Dict[str, float]:
        """
        Get bounding box around a center point.
        
        Args:
            center: Center coordinates
            radius_km: Radius in kilometers
            
        Returns:
            Dictionary with min/max lat/lon
        """
        lat, lon = center
        
        # Approximate degrees per km (varies by latitude)
        lat_degree_km = 111.0  # 1 degree latitude ≈ 111 km
        lon_degree_km = 111.0 * math.cos(math.radians(lat))
        
        lat_offset = radius_km / lat_degree_km
        lon_offset = radius_km / lon_degree_km
        
        return {
            "min_lat": lat - lat_offset,
            "max_lat": lat + lat_offset,
            "min_lon": lon - lon_offset,
            "max_lon": lon + lon_offset
        }


# Singleton instance
geolocation_service = GeoLocationService()
