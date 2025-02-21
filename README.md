


# TItanInve [![GitHub Stars](https://img.shields.io/github/stars/wbpyer/TItanInve?style=social)](https://github.com/wbpyer/TItanInve) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

 基于大模型的量化投资分析工具，提供数据采集、策略回测与可视化的一站式解决方案


## 🚀 核心功能
- **多源数据集成**：支持股票、基金、加密货币的实时/历史数据抓取
- **策略回测引擎**：内置MA、RSI等经典策略，支持自定义策略回测
- **大模型扩展**：集成LSTM、Prophet等模型进行趋势预测
- **可视化看板**：生成交互式K线图、收益曲线和风险指标热力图
---
## 📦 环境要求
- Python 3.8+
- Redis 6.0+ (缓存服务)
- MySQL 8.0+ 或 PostgreSQL 14+

---

## 🛠️ arch
本项目为前后端分离架构，前端vue3,  后端Python。
titan33-app 为前端。
titan33 为后端。

---

## 📦 快速docker安装
待补充

---

## 📦 命令行安装
```bash
# 克隆项目并进入目录
git clone https://github.com/wbpyer/TItanInve.git && cd TItanInve

# 创建虚拟环境（推荐）
python -m venv venv && source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env  # 修改你的API密钥和数据库配置
```

---



## 快速开始

待补充
---



## 📊 可视化效果
![image](https://github.com/user-attachments/assets/9ec8586a-07c2-4e6d-92d9-2d2b5d7d9605)


---

## 🤝 参与贡献
欢迎通过以下方式参与：
1. 提交Issue报告问题或建议
2. Fork项目并提交Pull Request
3. 完善项目文档

代码规范：
- 使用PEP8代码风格
- 新增功能需包含单元测试
- 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📜 开源协议
本项目采用 [MIT License](LICENSE)，可自由用于商业用途。

---

## 📞 联系我们
- 项目维护者：wbpyer
- 问题反馈：[Issues页面](https://github.com/wbpyer/TItanInve/issues)
- 商务合作：wang63285625@126.com




