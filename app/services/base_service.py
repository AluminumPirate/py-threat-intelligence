class BaseService:
    services = {}

    @classmethod
    def register(cls, service_name):
        def decorator(service_class):
            cls.services[service_name] = service_class()
            return service_class

        return decorator

    def get_info(self, domain_name: str):
        raise NotImplementedError("Subclasses must implement this method")
