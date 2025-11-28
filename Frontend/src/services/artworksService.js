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

async function getAlbumById(id) {
  try {
    const response = await api.request(`/artworks/${id}`);
    if (response && response.album) {
      return response;
    }
    throw new Error('Invalid album data received');
  } catch (error) {
    console.error('Error fetching album:', error);
    throw error;
  }
}

async function getAlbumTracks(id) {
  try {
    const response = await api.request(`/artworks/${id}/tracks`);
    if (response && Array.isArray(response.tracks)) {
      return response;
    }
    throw new Error('Invalid tracks data received');
  } catch (error) {
    console.error('Error fetching album tracks:', error);
    throw error;
  }
}

export default {
  searchAlbums,
  getAlbumsByGenre,
  getAlbumById,
  getAlbumTracks,
};
