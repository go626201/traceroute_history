# 使用一个基础镜像，例如 Ubuntu
FROM ubuntu:latest

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    traceroute \
    python3 \
    python3-venv \
    python3-pip

# 设置工作目录
WORKDIR /traceroute_history

# 将本地文件复制到镜像中
COPY . .

# 创建并激活虚拟环境
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# 安装 Python 依赖
RUN pip3 install -r traceroute_history/requirements.txt

# 设置入口点或默认命令
ENTRYPOINT ["python3", "traceroute_history/traceroute_history.py"]
