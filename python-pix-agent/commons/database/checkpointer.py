from contextlib import ExitStack
from functools import lru_cache
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver
import atexit

from commons.logger import get_logger
logger = get_logger(__name__)

CHECKPOINT_DB = "temp/database/graph_ckpt.db"

_exit_stack = ExitStack()
atexit.register(_exit_stack.close)

def create_db_dir() -> Path:
    path = Path(CHECKPOINT_DB)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.parent.exists():
        raise RuntimeError(f"Falhou ao criar diretório: {path}")
    logger.info(f"📁 Diretório do DB OK: {path}")
    return path

@lru_cache(maxsize=1)
def get_saver() -> SqliteSaver:
    logger.info("Criando saver")
    db_path = create_db_dir()

    cm = SqliteSaver.from_conn_string(str(db_path))
    saver = _exit_stack.enter_context(cm)

    return saver
