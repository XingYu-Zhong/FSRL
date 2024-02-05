import argparse
import os

from mainlab.mainlab import MainLab
from llmlab.llmlab import LLMLab

parser = argparse.ArgumentParser(description="Example script to parse command line arguments.")
parser.add_argument("-tn", "--task_name", required=True, help="task_name 任务名")
parser.add_argument("-et", "--env_type", required=True, help="env_type 训练类型 train|load|test|llm")
parser.add_argument("-s", "--start_time", required=True, help="交易开始时间")
parser.add_argument("-e", "--end_time", required=True, help="交易结束时间")
parser.add_argument("-lt", "--load_time_steps", required=False, help="继续训练观察数")
parser.add_argument("-p", "--proxy", required=False, help="代理端口")
args = parser.parse_args()
if args.proxy:
    # 设置代理
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:'+args.proxy
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:'+args.proxy
if args.env_type=="load":
    MainLab(args.task_name,args.env_type,args.start_time,args.end_time,int(float(args.load_time_steps)))
elif args.env_type=="train" or args.env_type=="test":
    MainLab(args.task_name, args.env_type, args.start_time, args.end_time)
elif args.env_type=="llm":
    LLMLab(args.task_name, args.env_type, args.start_time, args.end_time)