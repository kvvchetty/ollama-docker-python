docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

ollama_key
6b288269f8b848bf94f5e9515a8008ea.eImBqBLUr_TZjpLrU1QjE3OP


docker exec -it ollama ollama signin

docker exec -it ollama ollama pull gemma4:31b-cloud


# 1. Clear out your existing Open WebUI container
docker rm -f open-webui

# 2. Create a dedicated bridge network for your AI stack
docker network create ai-network

# 3. Connect your active Ollama container to the new network
docker network connect ai-network ollama

$img = "ghcr.io/open-webui/open-webui:main"

# 4. Deploy Open WebUI inside the same network, pointing directly to the Ollama container name
docker run -d -p 3050:8080 --network ai-network -e OLLAMA_BASE_URL=http://ollama:11434 -v open-webui:/app/backend/data --name open-webui --restart always $img



docker ps

docker start ollama open-webui

before to shutdown PC
docker stop open-webui ollama


 How to Resume After a PC ShutdownTurn on your computer and let Windows load completely.Launch Docker Desktop (if you don't have it set to start with Windows automatically).Open your browser and navigate directly to your dashboard:

 Turn on your computer and let Windows load completely.Launch Docker Desktop (if you don't have it set to start with Windows automatically).Open your browser and navigate directly to your dashboard:http://127.0.0.1:3050

