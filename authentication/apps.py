from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        # Garante que o import só acontece quando o app está totalmente carregado
        def load_signals():
            import authentication.signals
        self.run_once(load_signals)

    def run_once(self, func):
        if not hasattr(self, '_has_run'):
            func()
            self._has_run = True