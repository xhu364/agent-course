FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_server ./mcp_server
COPY mcp_knowledge_server ./mcp_knowledge_server

EXPOSE 8000

CMD ["python", "-m", "mcp_server.server"]
