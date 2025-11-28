import api from './api';

/**
 * Play History Service
 * Handles recording and fetching user's play history
 */

const playHistoryService = {
  /**
   * Record an artwork play in user's history
   * @param {number} artworkId - The ID of the artwork being played
   * @returns {Promise} - Response from the API
   */
  async recordPlay(artworkId) {
    try {
      const response = await api.request('/users/me/history', {
        method: 'POST',
        body: JSON.stringify({
          artwork_id: artworkId
        })
      });
      return response;
    } catch (error) {
      console.error('Error recording play history:', error);
      throw error;
    }
  },

  /**
   * Get user's play history
   * @param {number} limit - Number of records to return (default: 50)
   * @param {number} offset - Offset for pagination (default: 0)
   * @returns {Promise} - User's play history
   */
  async getPlayHistory(limit = 50, offset = 0) {
    try {
      const response = await api.request(
        `/users/me/history?limit=${limit}&offset=${offset}`,
        {
          method: 'GET'
        }
      );
      return response;
    } catch (error) {
      console.error('Error fetching play history:', error);
      throw error;
    }
  }
};

export default playHistoryService;
