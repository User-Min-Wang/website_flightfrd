import json
import pickle
from datetime import datetime, timedelta
from extensions import redis_client


class CacheService:
    """
    Service class for managing Redis cache operations
    """
    
    def __init__(self, default_ttl=3600):  # Default TTL: 1 hour
        self.default_ttl = default_ttl
        self.redis_client = redis_client

    def set(self, key, value, ttl=None):
        """
        Set a value in cache
        
        Args:
            key: Cache key
            value: Value to cache (will be serialized)
            ttl: Time-to-live in seconds (uses default if not provided)
            
        Returns:
            bool: Success status
        """
        try:
            # Serialize the value
            serialized_value = self._serialize(value)
            
            # Use provided TTL or default
            ttl_to_use = ttl or self.default_ttl
            
            # Set in Redis
            result = self.redis_client.setex(key, ttl_to_use, serialized_value)
            
            return result
            
        except Exception as e:
            print(f"Error setting cache: {str(e)}")
            return False

    def get(self, key):
        """
        Get a value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        try:
            # Get from Redis
            value = self.redis_client.get(key)
            
            if value is None:
                return None
                
            # Deserialize the value
            deserialized_value = self._deserialize(value)
            
            return deserialized_value
            
        except Exception as e:
            print(f"Error getting cache: {str(e)}")
            return None

    def delete(self, key):
        """
        Delete a value from cache
        
        Args:
            key: Cache key
            
        Returns:
            bool: Success status
        """
        try:
            result = self.redis_client.delete(key)
            return result > 0  # Returns number of deleted keys, convert to boolean
            
        except Exception as e:
            print(f"Error deleting cache: {str(e)}")
            return False

    def exists(self, key):
        """
        Check if a key exists in cache
        
        Args:
            key: Cache key
            
        Returns:
            bool: Whether key exists
        """
        try:
            result = self.redis_client.exists(key)
            return result > 0
            
        except Exception as e:
            print(f"Error checking cache existence: {str(e)}")
            return False

    def set_json(self, key, value, ttl=None):
        """
        Set a JSON-serializable value in cache
        
        Args:
            key: Cache key
            value: JSON-serializable value to cache
            ttl: Time-to-live in seconds (uses default if not provided)
            
        Returns:
            bool: Success status
        """
        try:
            # Serialize to JSON
            json_value = json.dumps(value)
            
            # Use provided TTL or default
            ttl_to_use = ttl or self.default_ttl
            
            # Set in Redis
            result = self.redis_client.setex(key, ttl_to_use, json_value)
            
            return result
            
        except Exception as e:
            print(f"Error setting JSON cache: {str(e)}")
            return False

    def get_json(self, key):
        """
        Get a JSON value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached JSON value or None if not found
        """
        try:
            # Get from Redis
            value = self.redis_client.get(key)
            
            if value is None:
                return None
                
            # Deserialize from JSON
            deserialized_value = json.loads(value.decode('utf-8'))
            
            return deserialized_value
            
        except Exception as e:
            print(f"Error getting JSON cache: {str(e)}")
            return None

    def _serialize(self, obj):
        """
        Serialize an object for storage in Redis
        
        Args:
            obj: Object to serialize
            
        Returns:
            Serialized object as bytes
        """
        return pickle.dumps(obj)

    def _deserialize(self, data):
        """
        Deserialize an object retrieved from Redis
        
        Args:
            data: Serialized data as bytes
            
        Returns:
            Deserialized object
        """
        return pickle.loads(data)

    def increment(self, key, amount=1):
        """
        Increment a numeric value in cache
        
        Args:
            key: Cache key
            amount: Amount to increment by (default: 1)
            
        Returns:
            New value after increment
        """
        try:
            result = self.redis_client.incrby(key, amount)
            return result
            
        except Exception as e:
            print(f"Error incrementing cache: {str(e)}")
            return None

    def expire(self, key, ttl):
        """
        Set expiration time for a key
        
        Args:
            key: Cache key
            ttl: Time-to-live in seconds
            
        Returns:
            bool: Success status
        """
        try:
            result = self.redis_client.expire(key, ttl)
            return result
            
        except Exception as e:
            print(f"Error setting expiration: {str(e)}")
            return False

    def clear_pattern(self, pattern):
        """
        Delete all keys matching a pattern
        
        Args:
            pattern: Pattern to match (e.g., "flight:*")
            
        Returns:
            int: Number of deleted keys
        """
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                result = self.redis_client.delete(*keys)
                return result
            return 0
            
        except Exception as e:
            print(f"Error clearing pattern: {str(e)}")
            return 0

    def get_keys(self, pattern="*"):
        """
        Get all keys matching a pattern
        
        Args:
            pattern: Pattern to match (default: "*")
            
        Returns:
            list: List of matching keys
        """
        try:
            keys = self.redis_client.keys(pattern)
            return [key.decode('utf-8') for key in keys]
            
        except Exception as e:
            print(f"Error getting keys: {str(e)}")
            return []