// Simple auth middleware for session-based authentication

export function requireAuth(req, res, next) {
  if (!req.session || !req.session.user) {
    return res.status(401).json({ message: 'Not authenticated.' });
  }
  next();
}

export function requireRole(role) {
  return (req, res, next) => {
    if (!req.session || !req.session.user) {
      return res.status(401).json({ message: 'Not authenticated.' });
    }
    if (req.session.user.role !== role) {
      return res.status(403).json({ message: 'Forbidden: insufficient permissions.' });
    }
    next();
  };
}
