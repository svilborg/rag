FROM huggingface/transformers-pytorch-gpu:latest

ENV HF_HOME=/cache

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    apt-utils \
    ca-certificates \
    wget \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# pip libs
RUN pip install pandas \
    && pip install transformers ctransformers torch \
    && pip install langchain sentence-transformers \
    && pip install qdrant-client fastembed

# Clean up
RUN rm -rf /root/.cache/pip

CMD ["bash"]