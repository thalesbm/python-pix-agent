# PIX Agent

Um agente inteligente para operações bancárias PIX desenvolvido em Python, utilizando LangGraph para orquestração de fluxos de trabalho e Streamlit para interface de usuário.

### Funcionalidades Principais

- **Consultar Saldo**: Verificação de saldo da conta
- **Consultar Limite**: Verificação de limites de transação
- **Alterar Limite**: Modificação de limites de transação
- **Realizar PIX**: Transferências PIX imediatas
- **Agendar PIX**: Agendamento de transferências PIX
- **Fallback**: Tratamento de intenções não reconhecidas

## Como Usar

**Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua_chave_api_aqui
```

**Instale as dependências**
```bash
python3 -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

**Execução**
```bash
# Execute a aplicação
python3 -m streamlit run python-pix-agent/app.py
```

## Configurações

### OpenAI
- **Modelo**: `gpt-4o-mini`
- **Temperatura**: `0`
- **Tokens máximos**: `1000`
