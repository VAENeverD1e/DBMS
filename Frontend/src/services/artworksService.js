import api from './api';

function buildQuery(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return;
    query.append(key, value);
  });
  return query.toString();
}

async function searchAlbums({ query, limit = 20, offset = 0 } = {}) {
  const queryString = buildQuery({ query, limit, offset });
  return api.request(`/artworks/search?${queryString}`);
}

async function getAlbumsByGenre({ genre, limit = 20 } = {}) {
  const queryString = buildQuery({ limit });
  return api.request(`/artworks/genre/${genre}?${queryString}`);
}

async function getAlbumById(jamendoId) {
  return api.request(`/artworks/${jamendoId}`);
}

async function getAlbumTracks(jamendoId) {
  return api.request(`/artworks/${jamendoId}/tracks`);
}

export default {
  searchAlbums,
  getAlbumsByGenre,
  getAlbumById,
  getAlbumTracks,
};
