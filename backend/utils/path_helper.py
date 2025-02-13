import os

def get_project_root():
    """获取项目根目录的绝对路径"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def get_config_path(filename):
    """获取配置文件的完整路径"""
    return os.path.join(get_project_root(), 'config', filename) 