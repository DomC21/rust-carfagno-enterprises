# Rust: A Tool by Carfagno Enterprises

A comprehensive stock analysis tool that leverages news data and AI to provide trading insights.

## Features

- Real-time news analysis for stocks
- Sentiment analysis using ChatGPT
- Interactive dashboard with filtering capabilities
- Export functionality for analysis reports

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your News API and OpenAI API keys

5. Run the backend:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the API URL if needed

4. Run the frontend:
```bash
npm run dev
```

## Deployment

The application is deployed using Render.com:

- Backend: https://rust-carfagno-enterprises.onrender.com
- Frontend: Served via static hosting

### Environment Variables Setup in Render.com

After deploying to Render.com, you need to set up the following environment variables in the Render.com dashboard:

1. Go to the Dashboard > Select your service
2. Navigate to Environment > Environment Variables
3. Add the following variables:
   - `NEWS_API_KEY`: Your News API key
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PORT`: 8000
   - `CORS_ORIGINS`: https://rust-carfagno-enterprises.onrender.com

Note: Never commit API keys or sensitive information directly to the repository.

## Environment Variables

### Backend
- `NEWS_API_KEY`: Your News API key
- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: Server port (default: 8000)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Frontend
- `VITE_API_URL`: Backend API URL

## License

Copyright © 2024 Carfagno Enterprises. All rights reserved.
