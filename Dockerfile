# 使用一个基础镜像，例如 Ubuntu
FROM ubuntu:latest

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    traceroute \
    python3 \
    python3-pip

# 设置工作目录
WORKDIR /traceroute_history

# 将本地文件复制到镜像中
COPY . .

# 安装 Python 依赖（如果有的话）
RUN pip3 install -r requirements.txt

# 设置入口点或默认命令
ENTRYPOINT ["python3", "traceroute_history.py"]
