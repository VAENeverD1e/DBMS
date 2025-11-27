// Playlist API service
import api from './api';

const playlistService = {
  /**
   * Get all user's playlists (own=true)
   * @param {number} limit - Number of results per page (1-100, default 50)
   * @param {number} offset - Pagination offset (default 0)
   * @returns {Promise<Object>} { success: bool, playlists: Array, total_count: number }
   */
  async getUserPlaylists(limit = 50, offset = 0) {
    try {
      const response = await api.request(
        `/playlists/?own=true&limit=${limit}&offset=${offset}`,
        { method: 'GET' }
      );
      return {
        success: true,
        playlists: response.playlists || [],
        // Backend returns pagination object; map count to total_count for context usage
        total_count: (response.pagination && response.pagination.count) || 0,
      };
    } catch (error) {
      console.error('Error fetching user playlists:', error);
      return {
        success: false,
        error: error.message,
        playlists: [],
        total_count: 0,
      };
    }
  },

  /**
   * Get playlist details with all songs
   * @param {number} playlistId - Playlist ID
   * @returns {Promise<Object>} { success: bool, playlist: Object }
   */
  async getPlaylist(playlistId) {
    try {
      const response = await api.request(`/playlists/${playlistId}`, { method: 'GET' });
      return {
        success: true,
        playlist: response,
      };
    } catch (error) {
      console.error(`Error fetching playlist ${playlistId}:`, error);
      return {
        success: false,
        error: error.message,
        playlist: null,
      };
    }
  },

  /**
   * Create a new playlist
   * @param {string} name - Playlist name
   * @returns {Promise<Object>} { success: bool, playlist: Object }
   */
  async createPlaylist(name) {
    try {
      const response = await api.request('/playlists/', {
        method: 'POST',
        body: JSON.stringify({ name }),
      });
      return {
        success: true,
        playlist: response,
      };
    } catch (error) {
      console.error('Error creating playlist:', error);
      return {
        success: false,
        error: error.message || 'Failed to create playlist',
        playlist: null,
      };
    }
  },

  /**
   * Update playlist name
   * @param {number} playlistId - Playlist ID
   * @param {string} name - New playlist name
   * @returns {Promise<Object>} { success: bool, message: string }
   */
  async updatePlaylist(playlistId, name) {
    try {
      const response = await api.request(`/playlists/${playlistId}`, {
        method: 'PUT',
        body: JSON.stringify({ name }),
      });
      return {
        success: true,
        message: response.message || 'Playlist updated successfully',
      };
    } catch (error) {
      console.error(`Error updating playlist ${playlistId}:`, error);
      return {
        success: false,
        error: error.message,
      };
    }
  },

  /**
   * Delete playlist
   * @param {number} playlistId - Playlist ID
   * @returns {Promise<Object>} { success: bool, message: string }
   */
  async deletePlaylist(playlistId) {
    try {
      const response = await api.request(`/playlists/${playlistId}`, {
        method: 'DELETE',
      });
      return {
        success: true,
        message: response.message || 'Playlist deleted successfully',
      };
    } catch (error) {
      console.error(`Error deleting playlist ${playlistId}:`, error);
      return {
        success: false,
        error: error.message,
      };
    }
  },

  /**
   * Add song to playlist
   * @param {number} playlistId - Playlist ID
   * @param {number} songId - Song ID
   * @param {number} orderIndex - Optional position in playlist
   * @returns {Promise<Object>} { success: bool, message: string }
   */
  async addSongToPlaylist(playlistId, songId, orderIndex = null) {
    try {
      const body = { song_id: songId };
      if (orderIndex !== null) {
        body.order_index = orderIndex;
      }
      const response = await api.request(`/playlists/${playlistId}/songs`, {
        method: 'POST',
        body: JSON.stringify(body),
      });
      return {
        success: true,
        message: response.message || 'Song added to playlist successfully',
      };
    } catch (error) {
      console.error(`Error adding song to playlist ${playlistId}:`, error);
      return {
        success: false,
        error: error.message,
        status: error.status,
      };
    }
  },

  /**
   * Remove song from playlist
   * @param {number} playlistId - Playlist ID
   * @param {number} songId - Song ID
   * @returns {Promise<Object>} { success: bool, message: string }
   */
  async removeSongFromPlaylist(playlistId, songId) {
    try {
      const response = await api.request(
        `/playlists/${playlistId}/songs/${songId}`,
        { method: 'DELETE' }
      );
      return {
        success: true,
        message: response.message || 'Song removed from playlist successfully',
      };
    } catch (error) {
      console.error(`Error removing song from playlist ${playlistId}:`, error);
      return {
        success: false,
        error: error.message,
      };
    }
  },
};

export default playlistService;
