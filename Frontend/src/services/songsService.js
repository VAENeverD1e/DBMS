import api from './api';

function buildQuery(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return;
    query.append(key, value);
  });
  return query.toString();
}

async function searchSongs({ query, limit = 20, offset = 0 } = {}) {
  const queryString = buildQuery({ query, limit, offset });
  return api.request(`/songs/search?${queryString}`);
}

async function getSongsByGenre({ genre, limit = 20 } = {}) {
  const queryString = buildQuery({ limit });
  return api.request(`/songs/genre/${genre}?${queryString}`);
}

async function getSongById(jamendoId) {
  return api.request(`/songs/${jamendoId}`);
}

export default {
  searchSongs,
  getSongsByGenre,
  getSongById,
};


