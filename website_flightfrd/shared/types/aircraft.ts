// Shared Aircraft Type Definitions

export interface Aircraft {
  hex: string;
  flight: string;
  altitude: number | null;
  speed: number | null;
  track: number | null;
  vert_rate: number | null;
  lat: number | null;
  lon: number | null;
  seen: number | null;
  seen_pos: number | null;
  rssi: number | null;
  messages: number | null;
  type: string | null;
  sil: number | null;
  nav_altitude: number | null;
  nav_heading: number | null;
  nav_modes: string[] | null;
  category: string | null;
}

export interface Flight {
  id: string;
  flight_number: string;
  departure_airport: string;
  arrival_airport: string;
  departure_time: string;
  arrival_time: string;
  aircraft_type: string;
  status: 'scheduled' | 'boarding' | 'in-air' | 'landed' | 'delayed' | 'cancelled';
  aircraft_hex: string;
}