import uvicorn
from pathlib import Path
import sys

# Add src to Python path
src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
