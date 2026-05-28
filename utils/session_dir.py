import os
import uuid
from datetime import datetime

def create_session_dir():
    """创建独立会话目录"""
    base_dir = "outputs"
    session_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = os.path.join(base_dir, f"session_{timestamp}_{session_id}")
    os.makedirs(session_dir, exist_ok=True)
    return session_dir