import sys
import os
import logging

# Configurar logging para stderr
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

# Importar o servidor MCP da definição
from server_http import mcp

if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("Iniciando MCP AgentHub Server")
    logger.info(f"Python: {sys.executable}")
    logger.info(f"Diretório: {os.getcwd()}")
    logger.info(f"Argumentos: {sys.argv}")
    logger.info("=" * 80)
    
    try:
        logger.info("Executando MCP via stdio...")
        logger.info("Aguardando conexão de um cliente MCP...")
        mcp.run()
        logger.info("MCP Server encerrou normalmente")
    except KeyboardInterrupt:
        logger.info("MCP Server interrompido pelo usuário")
        sys.exit(0)
    except EOFError:
        logger.info("EOF recebido, encerrando")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)
