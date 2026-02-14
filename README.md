# OpenClaw Telegram ASR (Local, Base Model)

一个可本地部署的 Telegram 语音转文字方案，面向 OpenClaw 工作流，默认使用 `faster-whisper` `base` 模型（CPU）。

## 特性

- 本地转写（不走云端 API）
- 中文优先（可切换 auto / en）
- 兼容 Telegram 语音文件（`.ogg` / Opus）
- 输出纯文本和分段时间戳（可选）
- 低成本部署（2C / 8G 也可用）

## 目录结构

- `scripts/asr_demo.py`：核心转写脚本
- `scripts/install.sh`：一键安装依赖与 Python venv
- `scripts/run_demo.sh`：快速运行 demo

## 快速开始

```bash
cd openclaw-telegram-asr
bash scripts/install.sh
bash scripts/run_demo.sh /path/to/voice.ogg zh
```

> 第二个参数语言可选：`zh` / `en` / `auto`

## 手动运行

```bash
.venv/bin/python scripts/asr_demo.py \
  --input /path/to/voice.ogg \
  --model base \
  --language zh \
  --compute-type int8 \
  --output /tmp/asr.txt \
  --segments-json /tmp/asr_segments.json
```

## 资源建议（CPU）

- 模型：`base`
- 转写时：短时高 CPU（2 核会吃满）
- 内存：约 0.8~1.5GB 增量
- 空闲时：几乎无额外开销

## OpenClaw 集成建议

推荐做成“收到语音才触发”的按需脚本：

1. 捕获 Telegram 语音文件路径
2. 调用 `scripts/asr_demo.py` 转写
3. 将转写文本回注入当前会话

这样可保持空闲资源占用最低。

## License

MIT
