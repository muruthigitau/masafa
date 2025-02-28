from django.core.cache import cache

class MultiTenantRouter:
    def db_for_read(self, model, **hints):
        """Direct read queries to the correct tenant database."""
        tenant_db = cache.get("tenant_db")
        
        # Try fetching tenant info from cache if not found in hints
        if not tenant_db:
            tenant_name = hints.get('tenant_name', None)
            if tenant_name:
                tenant_db = cache.get(f"tenant_db")
        
        # Debugging output for checking tenant_db in hints and cache
        
        # If tenant_db is available, return the correct tenant database
        if tenant_db:
            return tenant_db
        
        # Fallback to default database if not found
        return 'default'

    def db_for_write(self, model, **hints):
        """Direct write queries to the correct tenant database."""
        tenant_db = cache.get("tenant_db")
        
        # Try fetching tenant info from cache if not found in hints
        if not tenant_db:
            tenant_name = hints.get('tenant_name', None)
            if tenant_name:
                tenant_db = cache.get(f"tenant_db")
        
        # Debugging output for checking tenant_db in hints and cache
        
        # If tenant_db is available, return the correct tenant database
        if tenant_db:
            return tenant_db
        
        # Fallback to default database if not found
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if both objects are in the same database."""
        db_obj1 = cache.get("tenant_db")
        db_obj2 = cache.get("tenant_db")
        
        # Allow if both objects have the same tenant_db or are in the default database
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return True  # Allow if both objects are in the default database

