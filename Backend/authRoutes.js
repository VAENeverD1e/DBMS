import express from 'express';
import bcrypt from 'bcryptjs';
import { pool } from './db.js';

const router = express.Router();

// Helper to shape user object sent to client
function mapUser(row) {
  if (!row) return null;
  return {
    userId: row.UserID,
    email: row.Email,
    username: row.Username,
    firstName: row.FirstName,
    lastName: row.LastName,
    role: row.Role,
  };
}

// POST /auth/register
router.post('/register', async (req, res) => {
  try {
    const { email, username, password, firstName, lastName, role } = req.body;

    if (!email || !username || !password || !role) {
      return res.status(400).json({ message: 'Email, username, password and role are required.' });
    }

    if (!['Listener', 'Artist'].includes(role)) {
      return res.status(400).json({ message: 'Invalid role. Must be Listener or Artist.' });
    }

    const [existingByEmail] = await pool.query('SELECT UserID FROM User WHERE Email = ?', [email]);
    if (existingByEmail.length > 0) {
      return res.status(409).json({ message: 'Email already in use.' });
    }

    const [existingByUsername] = await pool.query('SELECT UserID FROM User WHERE Username = ?', [username]);
    if (existingByUsername.length > 0) {
      return res.status(409).json({ message: 'Username already in use.' });
    }

    const hashed = await bcrypt.hash(password, 10);

    const [result] = await pool.query(
      `INSERT INTO User (Email, Password, Username, FirstName, LastName, Role)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [email, hashed, username, firstName || null, lastName || null, role]
    );

    // log user in immediately by storing data in session
    req.session.user = {
      userId: result.insertId,
      email,
      username,
      firstName: firstName || null,
      lastName: lastName || null,
      role,
    };

    return res.status(201).json({ user: req.session.user });
  } catch (err) {
    console.error('[Auth] Register error:', err);
    return res.status(500).json({ message: 'Internal server error.' });
  }
});

// POST /auth/login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required.' });
    }

    const [rows] = await pool.query('SELECT * FROM User WHERE Email = ?', [email]);
    const userRow = rows[0];
    if (!userRow) {
      return res.status(401).json({ message: 'Invalid email or password.' });
    }

    const passwordMatch = await bcrypt.compare(password, userRow.Password);
    if (!passwordMatch) {
      return res.status(401).json({ message: 'Invalid email or password.' });
    }

    const user = mapUser(userRow);
    req.session.user = user;

    return res.status(200).json({ user });
  } catch (err) {
    console.error('[Auth] Login error:', err);
    return res.status(500).json({ message: 'Internal server error.' });
  }
});

// GET /auth/me
router.get('/me', (req, res) => {
  if (!req.session.user) {
    return res.status(401).json({ user: null });
  }
  return res.status(200).json({ user: req.session.user });
});

// POST /auth/logout
router.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error('[Auth] Logout error:', err);
      return res.status(500).json({ message: 'Failed to log out.' });
    }
    res.clearCookie('sid');
    return res.status(200).json({ message: 'Logged out successfully.' });
  });
});

export default router;
