from contextlib import ExitStack
from functools import lru_cache
from langgraph.checkpoint.sqlite import SqliteSaver

from commons.logger import get_logger
logger = get_logger(__name__)

CHECKPOINT_DB = "database/graph_ckpt.db"

_exit_stack = ExitStack()
SAVER = _exit_stack.enter_context(SqliteSaver.from_conn_string(CHECKPOINT_DB))

@lru_cache(maxsize=1)
def get_saver() -> SqliteSaver:
    logger.info("Criando saver")
    return SAVER

import atexit
atexit.register(_exit_stack.close)
