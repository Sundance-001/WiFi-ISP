# Quick Testing Checklist

## ✅ Frontend-Backend Integration Complete

---

## Start Servers (Do This First)

```bash
# Terminal 1 - Backend
cd "C:\Users\gh\OneDrive\Desktop\WiFi ISP\Back_End"
python main.py

# Terminal 2 - Frontend  
cd "C:\Users\gh\OneDrive\Desktop\WiFi ISP\Front End\react-vite-app"
npm run dev
```

**Expected:**
- Backend: `Uvicorn running on http://0.0.0.0:8001`
- Frontend: `Local: http://localhost:5173/`

---

## Test 1: Backend Health Check ✅

**Browser Console:**
```javascript
fetch('http://localhost:8001/api/health').then(r=>r.json()).then(console.log)
```

**Expected Response:**
```json
{ "status": "healthy", "app": "WiFi ISP API", "version": "1.0.0" }
```

---

## Test 2: Get All Packages ✅

**Browser Console:**
```javascript
fetch('http://localhost:8001/api/packages').then(r=>r.json()).then(console.log)
```

**Expected:** List of hourly, weekly, monthly packages from DB

---

## Test 3: Full Payment Flow ✅

**Steps:**
1. Open http://localhost:5173/
2. Click any plan card (Hourly/Weekly/Monthly)
3. Enter phone: `+254700000000`
4. Click "Pay" button
5. Check page for ✅ success or ❌ error message
6. Check browser console (F12 → Console) for API response

**Expected Success Message:**
```
✅ Payment initiated! Session: [token]
```

---

## Test 4: Create Device ✅

**Browser Console:**
```javascript
fetch('http://localhost:8001/api/devices', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    phone: '+254700000000',
    mac_address: '00:1A:2B:3C:4D:5E',
    device_name: 'Test Phone',
    device_type: 'phone'
  })
}).then(r=>r.json()).then(console.log)
```

**Expected:** Device created with ID

---

## Test 5: Check Device Limit ✅

**Browser Console:**
```javascript
fetch('http://localhost:8001/api/devices/phone/+254700000000/limit')
  .then(r=>r.json()).then(console.log)
```

**Expected:**
```json
{ "can_add_device": true, "active_devices": 1, "device_limit": 2 }
```

---

## Test 6: Redeem Voucher ✅

**Browser Console:**
```javascript
fetch('http://localhost:8001/api/vouchers/redeem', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    code: 'WIFITEST123456',
    phone: '+254700000000'
  })
}).then(r=>r.json()).then(console.log)
```

**Expected:** Voucher redeemed or error "Voucher not found"

---

## Testing Tools

| Tool | How | Why |
|------|-----|-----|
| **Browser Console** | F12 → Console tab | Quick testing, no setup |
| **Postman** | Import JSON file | Professional, organized |
| **API Docs** | http://localhost:8001/api/docs | Interactive Swagger UI |
| **Network Tab** | F12 → Network tab | See request/response details |

---

## What's Connected

| Component | Status |
|-----------|--------|
| Backend → Database | ✅ SQLAlchemy ORM |
| Backend → API Routes | ✅ FastAPI routers |
| Frontend → API | ✅ apiService.js |
| PaymentForm → API | ✅ Real API calls |
| CORS | ✅ Configured for localhost:5173 |

---

## Common Issues & Fixes

**❌ "Failed to fetch"**
- Check backend running on port 8001
- Check frontend on localhost:5173
- Open browser console

**❌ "CORS error"**
- Backend must be running
- Check CORS middleware in main.py

**❌ "404 Not Found"**
- Package ID might not exist
- Try GET /api/packages first

**❌ "Connection refused"**
- Start backend: `python main.py`

---

## File Locations

```
WiFi ISP/
├── Front End/
│   └── react-vite-app/
│       ├── src/
│       │   ├── services/
│       │   │   └── apiService.js ← API CLIENT
│       │   └── components/
│       │       └── PaymentForm.jsx ← USING API
│       └── package.json
│
└── Back_End/
    ├── main.py ← START HERE
    ├── database.py ← DB CONFIG
    ├── models/ ← DATABASE MODELS
    ├── services/ ← BUSINESS LOGIC
    ├── routers/ ← API ENDPOINTS
    └── requirements.txt
```

---

## Success Criteria

✅ All items should have green checkmarks:

- [ ] Backend starts without errors
- [ ] Frontend loads on http://localhost:5173/
- [ ] Health check returns 200 OK
- [ ] Packages load from database
- [ ] Payment form submits without error
- [ ] Success message displays on page
- [ ] Browser console shows API response
- [ ] No CORS errors in console

---

## Next: Full Integration Tests

1. **Session Flow** - Create session → Get token → Validate token
2. **Device Limit** - Add 2 devices → 3rd should deactivate oldest
3. **Voucher Flow** - Create voucher → Redeem → Validate status
4. **Payment History** - Create payment → Check history list

---

**Status:** 🟢 READY FOR TESTING

Start servers and follow Test 1 above!
