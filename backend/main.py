from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import training_router, inference_router

app = FastAPI()

# 配置CORS，添加前端的IP地址
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，开发环境使用
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(training_router, prefix="/api/training", tags=["training"])
app.include_router(inference_router, prefix="/api/inference", tags=["inference"]) 