import logging

error_handler = logging.FileHandler("bot_errors.log")
error_handler.setLevel(logging.ERROR)

info_handler = logging.FileHandler("bot_info.log")
info_handler.setLevel(logging.INFO)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[error_handler, info_handler]
)

# Logger for bot-specific messages
logger = logging.getLogger('FarmLifeBot')
