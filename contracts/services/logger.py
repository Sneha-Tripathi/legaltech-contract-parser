import logging

import logging
import os

LOG_FILE = os.path.join("uploads", "legaltech.log")

os.makedirs("uploads", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)




logger = logging.getLogger("LegalTech")