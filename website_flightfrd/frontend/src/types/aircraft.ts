export interface Aircraft {
  id: number;
  icao_code: string;
  registration: string | null;
  airline: string | null;
  model: string | null;
  type_code: string | null;
  serial_number: string | null;
  operator: string | null;
  built_date: string | null; // ISO date string
  status: 'active' | 'retired' | 'stored';
  first_flight_date: string | null; // ISO date string
  registration_date: string | null; // ISO date string
  registration_expiry: string | null; // ISO date string
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface Flight {
  id: number;
  flight_number: string | null;
  callsign: string | null;
  aircraft_id: number;
  departure_airport: string | null;
  arrival_airport: string | null;
  departure_time: string | null; // ISO date string
  arrival_time: string | null; // ISO date string
  actual_departure: string | null; // ISO date string
  actual_arrival: string | null; // ISO date string
  status: 'scheduled' | 'active' | 'landed' | 'cancelled' | 'delayed';
  origin_country: string | null;
  destination_country: string | null;
  altitude: number | null;
  ground_speed: number | null;
  vertical_rate: number | null;
  heading: number | null;
  latitude: number | null;
  longitude: number | null;
  on_ground: boolean;
  squawk: string | null;
  baro_altitude: number | null;
  true_track: number | null;
  last_position_update: string | null; // ISO date string
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface AircraftWithFlights extends Aircraft {
  flights: Flight[];
}

export interface AircraftSearchParams {
  page?: number;
  per_page?: number;
  search?: string;
  status?: string;
  airline?: string;
  model?: string;
}

export interface FlightSearchParams {
  page?: number;
  per_page?: number;
  status?: string;
  aircraft_id?: number;
  departure_airport?: string;
  arrival_airport?: string;
}