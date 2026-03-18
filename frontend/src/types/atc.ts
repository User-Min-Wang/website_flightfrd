export interface ATCMessage {
  id: number;
  frequency: string; // e.g., "118.700"
  callsign: string | null;
  message_type: string; // clearance, contact, taxi, takeoff, landing, etc.
  message_content: string;
  decoded_content?: string | null;
  sender_type?: string | null; // pilot, controller, station
  airport_code?: string | null; // Associated airport ICAO code
  flight_id?: number | null; // Associated flight
  received_at: string; // ISO date string
  processed_at?: string | null; // ISO date string
  signal_strength?: number | null; // Signal strength if available
  modulation?: string | null; // AM, FM, etc.
  channel?: string | null; // Primary, backup, emergency
  is_emergency: boolean; // Emergency communication
  priority_level: number; // Priority level (1-5)
  transcription_confidence?: number | null; // Confidence level of transcription
  verified: boolean; // Whether message has been verified
  verified_by?: number | null; // User who verified
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface ATCMessageFilter {
  frequency?: string;
  callsign?: string;
  message_type?: string;
  airport_code?: string;
  flight_id?: number;
  is_emergency?: boolean;
  priority_min?: number;
  limit?: number;
  offset?: number;
}

export interface ATCStreamEvent {
  type: 'new_message' | 'frequency_change' | 'connection_status';
  data: any;
  timestamp: string; // ISO date string
}

export interface FrequencyInfo {
  frequency: string;
  name: string;
  location: string;
  active: boolean;
}