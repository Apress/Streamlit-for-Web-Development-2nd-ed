FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Copy app files
COPY . /app

# Add a simple healthcheck (tries to curl the Streamlit app every 30s)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Explicit entrypoint with host binding
ENTRYPOINT ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
