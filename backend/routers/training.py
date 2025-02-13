from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import json
import os
from utils.path_helper import get_config_path, get_project_root
import logging

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainingConfig(BaseModel):
    task_name: str
    env_type: str
    start_time: str
    end_time: str
    load_time_steps: str = None
    proxy: str = None

@router.post("/start")
async def start_training(config: TrainingConfig):
    try:
        # 使用项目根目录作为工作目录
        project_root = get_project_root()
        cmd = ["python", os.path.join(project_root, "run.py"),
               "-tn", config.task_name,
               "-et", config.env_type,
               "-s", config.start_time,
               "-e", config.end_time]
        
        if config.load_time_steps:
            cmd.extend(["-lt", config.load_time_steps])
        if config.proxy:
            cmd.extend(["-p", config.proxy])
            
        process = subprocess.Popen(cmd, cwd=project_root)
        return {"message": "Training started", "pid": process.pid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/configs")
async def get_configs():
    try:
        mainlab_path = get_config_path('test_mainlab.json')
        llmlab_path = get_config_path('test_llmlab.json')
        
        logger.info(f"Reading config files from: {mainlab_path} and {llmlab_path}")
        
        # 检查文件是否存在
        if not os.path.exists(mainlab_path):
            raise FileNotFoundError(f"Config file not found: {mainlab_path}")
        if not os.path.exists(llmlab_path):
            raise FileNotFoundError(f"Config file not found: {llmlab_path}")
        
        # 读取配置文件
        with open(mainlab_path, "r", encoding='utf-8') as f:
            mainlab_config = json.load(f)
        with open(llmlab_path, "r", encoding='utf-8') as f:
            llmlab_config = json.load(f)
            
        return {
            "mainlab": mainlab_config,
            "llmlab": llmlab_config
        }
    except Exception as e:
        logger.error(f"Error loading configs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/configs/{config_type}/{config_name}")
async def update_config(config_type: str, config_name: str, config: dict):
    try:
        config_file = 'test_mainlab.json' if config_type == 'mainlab' else 'test_llmlab.json'
        config_path = get_config_path(config_file)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        if config_name not in configs:
            raise HTTPException(status_code=404, detail="Config not found")
            
        configs[config_name] = config
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(configs, f, indent=2, ensure_ascii=False)
            
        return {"message": "Config updated successfully"}
    except Exception as e:
        logger.error(f"Error updating config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/configs/{config_type}/{config_name}")
async def delete_config(config_type: str, config_name: str):
    try:
        config_file = 'test_mainlab.json' if config_type == 'mainlab' else 'test_llmlab.json'
        config_path = get_config_path(config_file)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        if config_name not in configs:
            raise HTTPException(status_code=404, detail="Config not found")
            
        del configs[config_name]
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(configs, f, indent=2, ensure_ascii=False)
            
        return {"message": "Config deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/configs/{config_type}")
async def add_config(config_type: str, config: dict):
    try:
        config_file = 'test_mainlab.json' if config_type == 'mainlab' else 'test_llmlab.json'
        config_path = get_config_path(config_file)
        
        with open(config_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        config_name = config.pop('name')
        if config_name in configs:
            raise HTTPException(status_code=400, detail="Config name already exists")
            
        configs[config_name] = config
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(configs, f, indent=2, ensure_ascii=False)
            
        return {"message": "Config added successfully"}
    except Exception as e:
        logger.error(f"Error adding config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 