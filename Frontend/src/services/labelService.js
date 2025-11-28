import api from './api';

/**
 * Get all record labels
 * @returns {Promise<{labels: Array}>}
 */
async function getLabels() {
  return api.request('/labels/');
}

/**
 * Get label by ID
 * @param {number} labelId - Label ID
 * @returns {Promise<{label: Object}>}
 */
async function getLabelById(labelId) {
  return api.request(`/labels/${labelId}`);
}

/**
 * Get all artists belonging to a label
 * @param {number} labelId - Label ID
 * @returns {Promise<{artists: Array}>}
 */
async function getLabelArtists(labelId) {
  return api.request(`/labels/${labelId}/artists`);
}

export default {
  getLabels,
  getLabelById,
  getLabelArtists,
};

