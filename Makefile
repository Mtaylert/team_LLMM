build:
    docker build -t llmm-app .

run:
    docker run -p 8080:8080 llmm-app