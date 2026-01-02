import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class Logger:
    def __init__(self, module_name="CORE"):
        self.module_name = module_name.upper()

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def log(self, message):
        t = self._get_timestamp()
        print(f"{Colors.CYAN}[{t}] [{self.module_name}] {message}{Colors.ENDC}")

    def success(self, message):
        t = self._get_timestamp()
        print(f"{Colors.GREEN}[{t}] [{self.module_name}] {message}{Colors.ENDC}")

    def warning(self, message):
        t = self._get_timestamp()
        print(f"{Colors.WARNING}[{t}] [{self.module_name}] {message}{Colors.ENDC}")

    def error(self, message):
        t = self._get_timestamp()
        print(f"{Colors.FAIL}[{t}] [{self.module_name}] {message}{Colors.ENDC}")

    def debug(self, message):
        t = self._get_timestamp()
        print(f"{Colors.BLUE}[{t}] [{self.module_name}] {message}{Colors.ENDC}")

if __name__ == "__main__":
    log = Logger("TEST")
    log.log("Starting up...")
    log.success("Connected.")
    log.warning("Slow response.")
    log.error("Something broke.")
    log.debug("Debug info.")