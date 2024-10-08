from app.general.service import GeneralService


class SERVICE_NAMES:
    GeneralService = "general_service"


class ServiceLocator:
    service = {}

    general_service: GeneralService

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services[name]

    def __getitem__(self, name):
        return self.get(name)

    def __getattr__(self, name):
        return self.get(name)


#  register services


service_locator = ServiceLocator()

email_service = GeneralService()
service_locator.register(SERVICE_NAMES.GeneralService, GeneralService())
