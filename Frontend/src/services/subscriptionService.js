// Subscription service for the frontend
// Handles subscription plans, subscription management, and payment processing

import api from './api';

const { request } = api;

/**
 * Get all available subscription plans
 */
async function getPlans() {
  return request('/subscriptions/plans', {
    method: 'GET',
  });
}

/**
 * Subscribe to a plan
 * @param {Object} payload - Subscription details
 * @param {number} payload.plan_id - Plan ID
 * @param {string} payload.payment_method - Payment method (momo, visa, mastercard)
 * @param {number} payload.duration_months - Duration in months (1, 3, or 12)
 * @param {string} payload.card_number - Last 4 digits of card number (optional)
 * @param {string} payload.card_holder_name - Cardholder name (optional)
 */
async function subscribe(payload) {
  return request('/subscriptions/subscribe', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

/**
 * Get current user's active subscription
 */
async function getMySubscription() {
  return request('/subscriptions/me', {
    method: 'GET',
  });
}

/**
 * Get current user's all active subscriptions
 */
async function getMyActiveSubscriptions() {
  return request('/subscriptions/me/active', {
    method: 'GET',
  });
}

/**
 * Get subscription history
 * @param {number} limit - Number of records to return
 * @param {number} offset - Offset for pagination
 */
async function getSubscriptionHistory(limit = 10, offset = 0) {
  return request(`/subscriptions/me/history?limit=${limit}&offset=${offset}`, {
    method: 'GET',
  });
}

/**
 * Cancel active subscription
 */
async function cancelSubscription() {
  return request('/subscriptions/me/cancel', {
    method: 'POST',
  });
}

/**
 * Check subscription status
 */
async function checkSubscriptionStatus() {
  return request('/subscriptions/me/status', {
    method: 'GET',
  });
}

/**
 * Get payment history
 * @param {number} limit - Number of records to return
 * @param {number} offset - Offset for pagination
 */
async function getPaymentHistory(limit = 10, offset = 0) {
  return request(`/payments/me?limit=${limit}&offset=${offset}`, {
    method: 'GET',
  });
}

export default {
  getPlans,
  subscribe,
  getMySubscription,
  getMyActiveSubscriptions,
  getSubscriptionHistory,
  cancelSubscription,
  checkSubscriptionStatus,
  getPaymentHistory,
};
