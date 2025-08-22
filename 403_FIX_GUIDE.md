# 🔧 RAG Chatbot - 403 Error Fix & Port Configuration

## 🚨 **Issue: 403 Forbidden Responses**

The 403 Forbidden error was caused by **Apple's AirPlay service** which runs on port 5000 by default on macOS.

### ✅ **Solution: Fixed Port Configuration**

I've updated the application to use different ports to avoid conflicts:

- **Demo Mode**: Port 5001 ✅
- **Full Flask App**: Port 5002 ✅  
- **Streamlit**: Port 8501 ✅

## 🚀 **Corrected Step-by-Step Instructions**

### **Step 1: Activate Environment**
```bash
source rag-env/bin/activate
```

### **Step 2: Choose Your Application**

#### **Option A: Demo Mode (Lightweight, No Model Downloads)**
```bash
python demo_flask.py
```
- **URL**: http://localhost:5001
- **Status Check**: `curl http://localhost:5001/status`

#### **Option B: Full RAG System**
```bash
python src/app.py
```
- **URL**: http://localhost:5002  
- **Status Check**: `curl http://localhost:5002/status`

#### **Option C: Streamlit Interface**
```bash
streamlit run streamlit_app.py
```
- **URL**: http://localhost:8501

## 🧪 **Test the Fix**

### **Test Demo App (Port 5001):**
```bash
# Check status
curl http://localhost:5001/status

# Test query
curl -X POST http://localhost:5001/demo_ask \
  -d "query=What are the main findings?" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### **Test Full App (Port 5002):**
```bash
# Check status
curl http://localhost:5002/status

# Ask question
curl -X POST http://localhost:5002/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main findings?"}'

# Upload file
curl -X POST http://localhost:5002/upload \
  -F "files=@your_paper.pdf"
```

## 🔍 **Verify No Port Conflicts**

```bash
# Check what's running on ports
lsof -i :5000  # Should show AirPlay
lsof -i :5001  # Should show demo app (if running)
lsof -i :5002  # Should show main app (if running)
lsof -i :8501  # Should show Streamlit (if running)
```

## 📋 **Current Working Setup**

✅ **Demo App**: http://localhost:5001 (Working)  
✅ **Full App**: http://localhost:5002 (Ready to start)  
✅ **Streamlit**: http://localhost:8501 (Ready to start)  
❌ **Port 5000**: Blocked by AirPlay (Avoided)  

## 🎯 **Quick Start Command**

For immediate testing without 403 errors:
```bash
source rag-env/bin/activate && python demo_flask.py
```

Then visit: http://localhost:5001

## 💡 **Prevention Tips**

1. **Always check ports first**: `lsof -i :5000`
2. **Use non-standard ports**: 5001, 5002, etc.
3. **On macOS**: Be aware of AirPlay using port 5000
4. **For production**: Use environment variables for port configuration

Your RAG chatbot is now configured to avoid the 403 error! 🎉
