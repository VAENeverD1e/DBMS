import api from './api';

function buildQuery(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return;
    query.append(key, value);
  });
  return query.toString();
}

async function searchSongs({ query, limit = 20, offset = 0, source } = {}) {
  const queryString = buildQuery({ query, limit, offset, source });
  return api.request(`/songs/search?${queryString}`);
}

async function getSongsByGenre({ genre, limit = 20, source } = {}) {
  const queryString = buildQuery({ limit, source });
  return api.request(`/songs/genre/${genre}?${queryString}`);
}

async function getSongById(jamendoId, source) {
  const queryString = buildQuery({ source });
  return api.request(`/songs/${jamendoId}${queryString ? `?${queryString}` : ''}`);
}

export default {
  searchSongs,
  getSongsByGenre,
  getSongById,
};


