# 验收对外副作用：读回对象，别信返回信息

> 推送、建仓、改远端设置——这些动作「成功」的判据都是**回读对象本身**。返回信息、退出码、列表接口的字段都可能骗你。

## 一、推送到底上没上：数默认分支树里的 blob

```bash
curl -sS -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/git/trees/main?recursive=1" \
  | python3 -c "import json,sys;print(len([t for t in json.load(sys.stdin).get('tree',[]) if t['type']=='blob']))"
```

- **唯一可靠判据是这个 blob 数**。仓库列表接口的 `size`（KB）**异步滞后**——刚推完、明明有几十个文件的仓库照样显示 0KB；照它判会把有内容的仓当空仓处理。
- 空仓回 `0`（或 404 / 409）。
- 顺带比对 `git/ref/heads/<branch>` 与本地 `git rev-parse HEAD`。

## 二、真·空仓的怪癖：首推只能用 `git push`

GitHub 对「**一次提交都没有**」的仓库，连 `POST /git/blobs` 都回 409「Git Repository is empty」——没有基树可用。所以走 REST 重放提交的工具（`bin/gitpush-api`）**在首推这一步没辙**，它只适合「远端已经有基线」之后的推送。

建仓后的第一推：

```bash
cd <repo> && timeout 60 env GIT_TERMINAL_PROMPT=0 git push -u origin main
```

- github.com 时好时坏：失败就再试一两次（实测同一批三个仓：两个一次过，一个第一次挂到超时、第二次过）。**别裸跑 `git push`**——它抽风时会静默挂满外层超时，白耗一轮。
- 基线上去之后，REST 通道才能接管后续推送。

## 三、动手前先 dry-run

要改远端 / 要重放提交的脚本，先看它打算干什么：

```bash
bin/gitpush-api --dry-run      # 看要重放几个提交、几个 blob
```

## 四、建仓/改设置的四面回读

改完一项回读一项（200 ≠ 内容是你想要的那份）：

| 改了什么 | 回读 |
|:---|:---|
| 建仓 | `GET /repos/<o>/<r>` → `visibility` / `default_branch` / `description` |
| 打标签（PUT 是**全量替换**） | `GET /repos/<o>/<r>/topics` → 比对整份列表（返回按字母序排，别把顺序当没生效） |
| README / 文件内容 | `GET /repos/<o>/<r>/contents/<路径>`（`Accept: application/vnd.github.raw`）→ 在里面 grep 关键字 |
| 可见性 | `GET` 回读 `private` / `visibility` |

## 五、别用管道包着判成败

`cmd | tail -4` 的退出码是 `tail` 的。工具已经 exit 1、`stderr` 里还明写着 HTTP 409，屏幕上你照样读到 `rc=0`，于是把「没推上」当「推上了」——这类假成功一次能把一整轮判断带歪。

- 要看退出码：单独跑，别套管道；或 `set -o pipefail`。
- 更稳的：**不看退出码，看结果**（blob 数、文件存在、内容 grep 命不命中）。
