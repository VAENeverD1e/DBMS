import api from './api';

function buildQuery(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return;
    query.append(key, value);
  });
  return query.toString();
}

/**
 * Get current authenticated artist's profile, stats, and recent artworks
 * @returns {Promise<{artist: Object, stats: Object, recent_artworks: Array}>}
 */
async function getCurrentArtist() {
  return api.request('/artists/me');
}

/**
 * Get all artists with optional filters
 * @param {Object} params - Query parameters
 * @param {string} [params.genre] - Filter by genre
 * @param {string} [params.verified] - Filter by verified status
 * @param {string} [params.search] - Search term
 * @param {number} [params.limit=50] - Number of results
 * @param {number} [params.offset=0] - Pagination offset
 * @returns {Promise<{artists: Array, pagination: Object}>}
 */
async function getArtists({ genre, verified, search, limit = 50, offset = 0 } = {}) {
  const queryString = buildQuery({ genre, verified, search, limit, offset });
  return api.request(`/artists/?${queryString}`);
}

/**
 * Get artist by ID
 * @param {number} artistId - Artist ID
 * @returns {Promise<{artist: Object}>}
 */
async function getArtistById(artistId) {
  return api.request(`/artists/${artistId}`);
}

/**
 * Get artist statistics
 * @param {number} artistId - Artist ID
 * @returns {Promise<{stats: Object}>}
 */
async function getArtistStats(artistId) {
  return api.request(`/artists/${artistId}/stats`);
}

/**
 * Get artworks by artist
 * @param {number} artistId - Artist ID
 * @param {Object} params - Query parameters
 * @param {number} [params.limit=50] - Number of results
 * @param {number} [params.offset=0] - Pagination offset
 * @returns {Promise<{artworks: Array, pagination: Object}>}
 */
async function getArtistArtworks(artistId, { limit = 50, offset = 0 } = {}) {
  const queryString = buildQuery({ limit, offset });
  return api.request(`/artists/${artistId}/artworks?${queryString}`);
}

/**
 * Get artist followers
 * @param {number} artistId - Artist ID
 * @param {Object} params - Query parameters
 * @param {number} [params.limit=50] - Number of results
 * @param {number} [params.offset=0] - Pagination offset
 * @returns {Promise<{followers: Array, total: number, pagination: Object}>}
 */
async function getArtistFollowers(artistId, { limit = 50, offset = 0 } = {}) {
  const queryString = buildQuery({ limit, offset });
  return api.request(`/artists/${artistId}/followers?${queryString}`);
}

/**
 * Follow an artist (listener only)
 * @param {number} artistId - Artist ID to follow
 * @returns {Promise<{message: string, data: Object}>}
 */
async function followArtist(artistId) {
  return api.request(`/artists/${artistId}/follow`, {
    method: 'POST',
  });
}

/**
 * Unfollow an artist (listener only)
 * @param {number} artistId - Artist ID to unfollow
 * @returns {Promise<{message: string}>}
 */
async function unfollowArtist(artistId) {
  return api.request(`/artists/${artistId}/follow`, {
    method: 'DELETE',
  });
}

/**
 * Check if current user is following an artist
 * @param {number} artistId - Artist ID
 * @returns {Promise<{is_following: boolean, artist_id: number}>}
 */
async function getFollowRelationship(artistId) {
  return api.request(`/artists/${artistId}/relationship`);
}

/**
 * Update artist profile (artist only)
 * @param {Object} data - Profile data
 * @param {string} [data.genre] - Genre
 * @returns {Promise<{message: string, artist: Object}>}
 */
async function updateArtistProfile(data) {
  return api.request('/artists/me', {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

/**
 * Update artist social links (artist only)
 * @param {string} socialLinks - Social media links
 * @returns {Promise<{message: string, artist: Object}>}
 */
async function updateSocialLinks(socialLinks) {
  return api.request('/artists/me/social-links', {
    method: 'PUT',
    body: JSON.stringify({ social_links: socialLinks }),
  });
}

/**
 * Self-verify artist (artist only)
 * Prerequisites: followers >= 670, artworks >= 3
 * @returns {Promise<Object>}
 */
async function selfVerify() {
  return api.request('/artists/me/verify', {
    method: 'POST',
  });
}

/**
 * Get artwork detail with tracks (artist only, for own artworks)
 * @param {number} artworkId - Artwork ID
 * @returns {Promise<{artwork: Object, tracks: Array}>}
 */
async function getMyArtworkDetail(artworkId) {
  return api.request(`/artists/me/artworks/${artworkId}`);
}

/**
 * Delete an artwork (artist only, for own artworks)
 * @param {number} artworkId - Artwork ID
 * @returns {Promise<{message: string}>}
 */
async function deleteMyArtwork(artworkId) {
  return api.request(`/artists/me/artworks/${artworkId}`, {
    method: 'DELETE',
  });
}

/**
 * Create a new artwork (Single or Album) with file uploads
 * @param {FormData} formData - FormData containing:
 *   - mode: 'single' or 'album'
 *   - title: Artwork title
 *   - genre: Genre name
 *   - cover_image: Cover image file
 *   - track_files[]: Audio files array
 *   - track_titles[]: Track titles array
 *   - track_numbers[]: Track numbers array (optional)
 *   - collaborations[]: Collaborator usernames array (optional)
 * @returns {Promise<{message: string, artwork: Object}>}
 */
async function createArtwork(formData) {
  return api.request('/artists/me/artworks', {
    method: 'POST',
    body: formData,
  });
}

export default {
  getCurrentArtist,
  getArtists,
  getArtistById,
  getArtistStats,
  getArtistArtworks,
  getArtistFollowers,
  followArtist,
  unfollowArtist,
  getFollowRelationship,
  getMyArtworkDetail,
  deleteMyArtwork,
  createArtwork,
  updateArtistProfile,
  updateSocialLinks,
  selfVerify,
};
