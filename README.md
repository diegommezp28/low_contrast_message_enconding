# Low-Contrast Overlay Message Encoding

A Streamlit application that allows users to embed and reveal hidden messages in images using low-contrast overlay

## Features

- Embed text messages into images with adjustable overlay strength and position
- Reveal hidden messages from encoded images
- Adjustable font size and text positioning
- Download encoded images

## Docker Deployment

### Prerequisites

- Docker installed on your system
- Git (optional, for cloning the repository)

### Building and Running with Docker

1. Clone the repository (or download the files):
   ```bash
   git clone <repository-url>
   cd pahe_encoder_app
   ```

2. Build the Docker image:
   ```bash
   docker build -t pahe-encoder-app .
   ```

3. Run the container:
   ```bash
   docker run -p 8501:8501 pahe-encoder-app
   ```

4. Access the application:
   Open your web browser and navigate to `http://localhost:8501`

### Docker Compose (Alternative)

If you prefer using Docker Compose, create a `docker-compose.yml` file:

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - .:/app
```

Then run:
```bash
docker-compose up
```

## Development

### Local Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run main.py
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
