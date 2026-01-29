# Frontend-Backend Integration Testing Guide

## Current Status
✅ **Backend**: Complete with database models, services, and API endpoints  
✅ **Frontend**: Connected via `apiService.js` with real API calls  

---

## How to Test

### Step 1: Start Both Servers

**Terminal 1 - Backend:**
```bash
cd "C:\Users\gh\OneDrive\Desktop\WiFi ISP\Back_End"
python main.py
```
Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**Terminal 2 - Frontend:**
```bash
cd "C:\Users\gh\OneDrive\Desktop\WiFi ISP\Front End\react-vite-app"
npm run dev
```
Expected output:
```
  ➜  Local:   http://localhost:5173/
```

---

### Step 2: Test Health Check

Open browser console (F12) and run:
```javascript
fetch('http://localhost:8001/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

Expected response:
```json
{
  "status": "healthy",
  "app": "WiFi ISP API",
  "version": "1.0.0",
  "timestamp": "2026-01-29T..."
}
```

---

### Step 3: Test Package Endpoints

**In browser console:**

Get all packages:
```javascript
fetch('http://localhost:8001/api/packages')
  .then(r => r.json())
  .then(d => console.log(d))
```

Get hourly packages only:
```javascript
fetch('http://localhost:8001/api/packages/type/hourly')
  .then(r => r.json())
  .then(d => console.log(d))
```

---

### Step 4: Test Payment Flow (UI)

1. Navigate to: **http://localhost:5173/**
2. Click on a plan card (Hourly/Weekly/Monthly)
3. Fill in phone number (e.g., +254700000000)
4. Select a plan from dropdown
5. Click **"Pay"** button
6. Check console for API response or error message on page

---

### Step 5: Test Session Creation

```javascript
// Create a session
fetch('http://localhost:8001/api/sessions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone: '+254700000000',
    package_id: 1,
    duration_hours: 1
  })
})
  .then(r => r.json())
  .then(d => console.log(d))
```

Response should include `session_token`:
```json
{
  "id": 1,
  "phone": "+254700000000",
  "session_token": "...",
  "start_time": "...",
  "end_time": "...",
  "is_active": true
}
```

---

### Step 6: Test Device Registration

```javascript
fetch('http://localhost:8001/api/devices', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone: '+254700000000',
    mac_address: '00:1A:2B:3C:4D:5E',
    device_name: 'My iPhone',
    device_type: 'phone'
  })
})
  .then(r => r.json())
  .then(d => console.log(d))
```

---

### Step 7: Test Voucher Redeem

```javascript
fetch('http://localhost:8001/api/vouchers/redeem', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: 'WIFI1234567890',
    phone: '+254700000000'
  })
})
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## API Endpoints Summary

### Packages
- `GET /api/packages` - Get all packages
- `GET /api/packages/type/{hourly|weekly|monthly}` - Filter by type
- `GET /api/packages/{id}` - Get specific package

### Sessions
- `POST /api/sessions` - Create session
- `GET /api/sessions/phone/{phone}` - Get active sessions
- `GET /api/sessions/token/{token}` - Check session validity
- `POST /api/sessions/{id}/end` - End session

### Devices
- `POST /api/devices` - Register device
- `GET /api/devices/phone/{phone}` - List user devices
- `GET /api/devices/phone/{phone}/limit` - Check device limit
- `POST /api/devices/{id}/deactivate` - Deactivate device

### Vouchers
- `POST /api/vouchers/redeem` - Redeem voucher
- `GET /api/vouchers/{code}` - Validate voucher
- `GET /api/vouchers/phone/{phone}/redeemed` - List redeemed vouchers

### Payments
- `POST /api/payments` - Create payment
- `POST /api/payments/{id}/confirm` - Confirm with M-Pesa receipt
- `GET /api/payments/phone/{phone}/history` - Payment history

---

## Troubleshooting

### CORS Error
If you see CORS error, check:
1. Backend is running on port 8001
2. Frontend is on localhost:5173
3. Backend has CORS middleware for localhost:5173

### 404 Not Found
- Check package_id exists (GET /api/packages first)
- Check session_id is valid

### Connection Refused
- Verify backend is running (`python main.py` in Back_End folder)
- Check port 8001 is not blocked

### Database Issues
- Delete `wifisp.db` to reset database
- Tables auto-create on backend startup

---

## Next Steps

1. **Add M-Pesa Daraja API integration** in `PaymentService.verify_mpesa_payment()`
2. **Create payment success page** that shows session token
3. **Add device selection** before creating session
4. **Implement voucher entry form** on landing page
5. **Add session history** page showing active WiFi sessions
