import logging 
import os

# create logs folder automatically
if not os.path.exists("logs"):
    os.makedirs("logs")


logging.basicConfig(
    filename="logs/trader.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)
