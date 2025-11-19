import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Crypto Arcade API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/api/lobbies")
def get_lobbies():
    """Return four lobby options for the 2D crypto-themed game."""
    return {
        "lobbies": [
            {
                "id": "btc-blitz",
                "title": "Bitcoin Blitz",
                "players": 128,
                "difficulty": "Easy",
                "status": "Open",
                "accent": "#F7931A",
                "description": "Fast-paced entry lobby themed around BTC."
            },
            {
                "id": "eth-arenas",
                "title": "Ethereum Arenas",
                "players": 96,
                "difficulty": "Medium",
                "status": "Open",
                "accent": "#627EEA",
                "description": "Skill-based battles with smart challenges."
            },
            {
                "id": "sol-speedrun",
                "title": "Solana Speedrun",
                "players": 64,
                "difficulty": "Hard",
                "status": "Limited",
                "accent": "#14F195",
                "description": "High-speed lobby with leaderboard chases."
            },
            {
                "id": "defi-dungeon",
                "title": "DeFi Dungeon",
                "players": 42,
                "difficulty": "Pro",
                "status": "Tournament",
                "accent": "#FF2E63",
                "description": "End-game strategies and seasonal rewards."
            }
        ]
    }

@app.get("/api/wallet")
def get_wallet():
    """Return a mocked wallet snapshot."""
    return {
        "address": "0xA1b2...D3f4",
        "netWorthUSD": 12543.67,
        "tokens": [
            {"symbol": "BTC", "amount": 0.2371, "priceUSD": 67000.0},
            {"symbol": "ETH", "amount": 3.58, "priceUSD": 3400.0},
            {"symbol": "SOL", "amount": 210.0, "priceUSD": 175.0},
            {"symbol": "USDC", "amount": 1450.12, "priceUSD": 1.0}
        ],
        "nfts": 7
    }

@app.get("/api/user")
def get_user():
    """Return a mocked user profile."""
    return {
        "username": "NeonPilot",
        "level": 27,
        "xp": 18340,
        "xpToNext": 20000,
        "rank": "Diamond",
        "wins": 248,
        "losses": 121,
        "avatar": "https://api.dicebear.com/7.x/identicon/svg?seed=NeonPilot"
    }

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
