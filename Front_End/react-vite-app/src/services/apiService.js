/**
 * API Service - handles all backend communication
 */

const API_BASE_URL = 'http://localhost:8001/api';

export const apiService = {
  // Packages
  getPackages: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/packages`);
      if (!response.ok) throw new Error('Failed to fetch packages');
      return await response.json();
    } catch (error) {
      console.error('Error fetching packages:', error);
      return null;
    }
  },

  getPackagesByType: async (type) => {
    try {
      const response = await fetch(`${API_BASE_URL}/packages/type/${type}`);
      if (!response.ok) throw new Error(`Failed to fetch ${type} packages`);
      return await response.json();
    } catch (error) {
      console.error(`Error fetching ${type} packages:`, error);
      return null;
    }
  },

  // Sessions
  createSession: async (phone, packageId, durationHours) => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone,
          package_id: packageId,
          duration_hours: durationHours,
        }),
      });
      if (!response.ok) throw new Error('Failed to create session');
      return await response.json();
    } catch (error) {
      console.error('Error creating session:', error);
      return null;
    }
  },

  checkSessionValidity: async (sessionToken) => {
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/token/${sessionToken}`);
      if (!response.ok) throw new Error('Failed to check session');
      return await response.json();
    } catch (error) {
      console.error('Error checking session:', error);
      return null;
    }
  },

  // Devices
  registerDevice: async (phone, macAddress, deviceName, deviceType = 'phone') => {
    try {
      const response = await fetch(`${API_BASE_URL}/devices`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phone,
          mac_address: macAddress,
          device_name: deviceName,
          device_type: deviceType,
        }),
      });
      if (!response.ok) throw new Error('Failed to register device');
      return await response.json();
    } catch (error) {
      console.error('Error registering device:', error);
      return null;
    }
  },

  getUserDevices: async (phone) => {
    try {
      const response = await fetch(`${API_BASE_URL}/devices/phone/${phone}`);
      if (!response.ok) throw new Error('Failed to fetch devices');
      return await response.json();
    } catch (error) {
      console.error('Error fetching devices:', error);
      return null;
    }
  },

  checkDeviceLimit: async (phone) => {
    try {
      const response = await fetch(`${API_BASE_URL}/devices/phone/${phone}/limit`);
      if (!response.ok) throw new Error('Failed to check device limit');
      return await response.json();
    } catch (error) {
      console.error('Error checking device limit:', error);
      return null;
    }
  },

  // Vouchers
  redeemVoucher: async (code, phone) => {
    try {
      const response = await fetch(`${API_BASE_URL}/vouchers/redeem`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, phone }),
      });
      if (!response.ok) throw new Error('Failed to redeem voucher');
      return await response.json();
    } catch (error) {
      console.error('Error redeeming voucher:', error);
      return null;
    }
  },

  validateVoucher: async (code) => {
    try {
      const response = await fetch(`${API_BASE_URL}/vouchers/${code}`);
      if (!response.ok) throw new Error('Failed to validate voucher');
      return await response.json();
    } catch (error) {
      console.error('Error validating voucher:', error);
      return null;
    }
  },

  // Payments
  createPayment: async (sessionId, phone, amount) => {
    try {
      const response = await fetch(`${API_BASE_URL}/payments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          phone,
          amount,
          method: 'mpesa',
        }),
      });
      if (!response.ok) throw new Error('Failed to create payment');
      return await response.json();
    } catch (error) {
      console.error('Error creating payment:', error);
      return null;
    }
  },

  confirmPayment: async (paymentId, mpesaReceipt) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/payments/${paymentId}/confirm?mpesa_receipt=${mpesaReceipt}`,
        { method: 'POST' }
      );
      if (!response.ok) throw new Error('Failed to confirm payment');
      return await response.json();
    } catch (error) {
      console.error('Error confirming payment:', error);
      return null;
    }
  },

  // Contact
  getContactInfo: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/contact`);
      if (!response.ok) throw new Error('Failed to fetch contact info');
      return await response.json();
    } catch (error) {
      console.error('Error fetching contact info:', error);
      return null;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) throw new Error('Health check failed');
      return await response.json();
    } catch (error) {
      console.error('Error during health check:', error);
      return null;
    }
  },
};
