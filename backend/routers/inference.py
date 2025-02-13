from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess

router = APIRouter()

class InferenceConfig(BaseModel):
    task_name: str
    start_time: str
    end_time: str
    proxy: str = None

@router.post("/start")
async def start_inference(config: InferenceConfig):
    try:
        cmd = ["python", "run.py", 
               "-tn", config.task_name,
               "-et", "test",  # 推理时使用test模式
               "-s", config.start_time,
               "-e", config.end_time]
        
        if config.proxy:
            cmd.extend(["-p", config.proxy])
            
        process = subprocess.Popen(cmd)
        return {"message": "Inference started", "pid": process.pid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 