import express from 'express';
import dotenv from 'dotenv';
import cookieParser from 'cookie-parser';
import session from 'express-session';
import { pingDB } from './db.js';
import authRoutes from './authRoutes.js';

dotenv.config();

const app = express();
app.use(express.json());
app.use(cookieParser());

// Simple in-memory session for school project (do NOT use in production)
app.use(
  session({
    name: 'sid',
    secret: process.env.SESSION_SECRET || 'dev-secret-change-me',
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      secure: false, // set true if using HTTPS
      maxAge: 1000 * 60 * 60 * 24, // 1 day
    },
  })
);

const PORT = process.env.PORT ? Number(process.env.PORT) : 4000;

// Health check
app.get('/health', async (req, res) => {
  try {
    const ok = await pingDB();
    res.status(200).json({ ok, service: 'api', db: ok ? 'up' : 'down' });
  } catch (err) {
    console.error('[Health] DB ping error:', err?.message);
    res.status(500).json({ ok: false, service: 'api', db: 'down' });
  }
});

// Auth routes
app.use('/auth', authRoutes);

// Example root
app.get('/', (req, res) => {
  res.json({ message: 'Backend is running' });
});

app.listen(PORT, () => {
  console.log(`API listening on http://localhost:${PORT}`);
});