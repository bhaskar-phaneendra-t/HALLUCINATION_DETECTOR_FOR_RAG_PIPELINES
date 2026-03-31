import logging
import os

from datetime import datetime

log_dir='logs'
os.makedirs(log_dir,exist_ok=True)
def getname_file():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.log'


log_file_path=os.path.join(log_dir,getname_file())


logging.basicConfig(
    filename=log_file_path,
    format='[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
    level=logging.INFO
)

logger=logging.getLogger("hallucination_firewall")