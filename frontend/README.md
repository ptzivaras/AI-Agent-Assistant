# Nexus AI - Frontend

Modern React frontend for the Nexus AI Ticket Classification System.

## 🚀 Features

- **Submit Tickets** - Real-time AI classification
- **Live Statistics** - Category & urgency breakdown
- **Ticket History** - View all classified tickets
- **Beautiful UI** - Modern gradient design with smooth animations

## 🛠️ Tech Stack

- **React 18** (via CDN - no npm/build required!)
- **Vanilla CSS** - Responsive gradient design
- **Babel Standalone** - JSX compilation in browser
- **REST API** - FastAPI backend integration

## 📦 Setup

**No installation needed!** Just open `index.html` in your browser.

### Method 1: Direct File Open
```bash
# Windows
start frontend/index.html

# Mac/Linux
open frontend/index.html
```

### Method 2: Local Server (Recommended for API calls)
```bash
# Python
cd frontend
python -m http.server 8080

# Node.js
npx serve frontend

# Then open: http://localhost:8080
```

## ⚙️ Configuration

Make sure the backend is running on `http://localhost:8001`

To change the API URL, edit `app.jsx`:
```javascript
const API_URL = 'http://localhost:8001';
```

## 🎨 UI Components

### Submit Ticket Form
- Text area for ticket message
- Real-time AI classification
- Confidence score display

### Statistics Dashboard
- Total tickets count
- Average confidence
- Category breakdown
- Urgency distribution

### Ticket List
- Recent tickets with classifications
- Color-coded urgency badges
- Sentiment indicators

## 🌈 Design Features

- **Gradient Background** - Purple gradient theme
- **Card-based Layout** - Clean, modern cards
- **Responsive Design** - Works on mobile & desktop
- **Smooth Animations** - Hover effects & transitions
- **Color-coded Badges** - Visual urgency/sentiment indicators

## 📱 Screenshots

### Desktop View
- Two-column layout (form + stats)
- Full ticket list below

### Mobile View
- Single-column stacked layout
- Optimized for touch interaction

## 🔧 Development

### File Structure
```
frontend/
├── index.html    # Main HTML entry point
├── app.jsx       # React component
├── style.css     # Styling
└── README.md     # This file
```

### Making Changes

1. **HTML**: Edit `index.html` for structure
2. **Styling**: Modify `style.css` for appearance
3. **Logic**: Update `app.jsx` for functionality

No build step required - just refresh the browser!

## 🐛 Troubleshooting

### CORS Errors
- Make sure backend has CORS enabled
- Check backend is running on port 8001

### API Connection Failed
- Verify backend server is running
- Check API_URL in app.jsx
- Open browser console for errors

### Tickets Not Loading
- Check network tab for API responses
- Verify backend database has tickets
- Test endpoints: http://localhost:8001/docs

## 🚀 Production Deployment

For production, consider:
1. Using a React build tool (Vite, Create React App)
2. Environment variables for API URL
3. Proper CORS configuration
4. CDN hosting (Netlify, Vercel, GitHub Pages)

## 📝 License

Part of the Nexus AI project.
