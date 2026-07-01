# AI Interviewer 5.0

Production-ready full-stack mock interview platform with React, FastAPI, MongoDB Atlas, Gemini, FAISS, Whisper, gTTS, and PDF report generation.

## Structure

- `backend/` FastAPI service and AI pipeline
- `frontend/` React + Vite app with Tailwind CSS

## Backend Setup

1. Create a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Copy `backend/.env.example` to `backend/.env` and configure MongoDB Atlas + Gemini.
4. Run the API:
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

## Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Copy `frontend/.env.example` to `frontend/.env` and set the API URL.
3. Run the app:
   ```bash
   npm run dev
   ```

## Deployment

### Frontend on Vercel
- Set `VITE_API_URL` to your Render backend URL.
- Use the `frontend/` folder as the project root.

### Backend on Render
- Set build command to `pip install -r backend/requirements.txt`.
- Set start command to `uvicorn app.main:app --host 0.0.0.0 --port 10000 --app-dir backend`.
- Configure environment variables from `backend/.env.example`.

### MongoDB Atlas
- Create a cluster and add your `MONGODB_URI`.
- Allow inbound access for your Render deployment.

## Notes

- Uploads support PDF resumes only.
- RAG indexes are stored locally under `storage/`.
- Gemini fallbacks are built in if the API key is not set, so the app still runs in demo mode.
