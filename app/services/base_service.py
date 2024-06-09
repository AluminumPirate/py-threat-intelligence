from typing import Type, Dict, Callable, Any


class BaseService:
    services: Dict[str, 'BaseService'] = {}

    @classmethod
    def register(cls, service_name: str) -> Callable[[Type['BaseService']], Type['BaseService']]:
        def decorator(service_class: Type['BaseService']) -> Type['BaseService']:
            cls.services[service_name] = service_class()
            return service_class

        return decorator

    def get_info(self, domain_name: str) -> Any:
        raise NotImplementedError("Subclasses must implement this method")
