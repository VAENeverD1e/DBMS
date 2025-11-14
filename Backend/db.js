import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const {
  DB_HOST,
  DB_PORT,
  DB_USER,
  DB_PASSWORD,
  DB_NAME,
  DB_SSL_CA
} = process.env;

let sslConfig = undefined;
if (DB_SSL_CA) {
  const caPath = path.isAbsolute(DB_SSL_CA)
  ? DB_SSL_CA
  : path.resolve(__dirname, DB_SSL_CA);
  if (fs.existsSync(caPath)) {
    sslConfig = { ca: fs.readFileSync(caPath, 'utf8') };
  } else {
    console.warn(`[DB] CA file not found at: ${caPath}. Connection may fail if Aiven requires SSL.`);
  }
}

export const pool = mysql.createPool({
  host: DB_HOST,
  port: DB_PORT ? Number(DB_PORT) : 3306,
  user: DB_USER,
  password: DB_PASSWORD,
  database: DB_NAME,
  ssl: sslConfig,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

export async function pingDB() {
  const [rows] = await pool.query('SELECT 1 AS ok');
  return rows?.[0]?.ok === 1;
}