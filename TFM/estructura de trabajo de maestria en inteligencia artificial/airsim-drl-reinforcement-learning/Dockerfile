FROM python:3.9.9

# Create a directory to save the code
ARG APP_ROOT=/app
RUN mkdir -p  $APP_ROOT
WORKDIR $APP_ROOT

# Add system dependencies
RUN apt update && \
    apt install -y vim libgl1-mesa-glx libglib2.0-0 libsm6  libxext6 libxrender1 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY  requirements.txt $APP_ROOT/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy code into container
COPY ./ $APP_ROOT/

# Train
CMD ["python", "main.py", "--mode=train"]