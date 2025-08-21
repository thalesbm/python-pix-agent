from contextlib import ExitStack
from functools import lru_cache
from langgraph.checkpoint.sqlite import SqliteSaver

CHECKPOINT_DB = "database/file:graph_ckpt.db?mode=rwc"

_exit_stack = ExitStack()
SAVER = _exit_stack.enter_context(SqliteSaver.from_conn_string(CHECKPOINT_DB))

@lru_cache(maxsize=1)
def get_saver() -> SqliteSaver:
    return SAVER

import atexit
atexit.register(_exit_stack.close)
