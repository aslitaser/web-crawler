import logging
from logstash_async.handler import AsynchronousLogstashHandler

# Set up the logstash handler
logstash_host = 'localhost'
logstash_port = 5000
logstash_handler = AsynchronousLogstashHandler(logstash_host, logstash_port, database_path=None)

# Configure logging to use the logstash handler
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('web_crawler')
logger.addHandler(logstash_handler)
