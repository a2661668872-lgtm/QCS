# 乐享知识库「上岸大礼包」补传进度

space_id: 5975dc79f8e54e9d8113a19bccba5ce9
大礼包根: bd66604cd7df46b7aa2a88d540113061
本地源: D:\小龙的工作台\AI知识库\AI第二大脑_内容创作系统\08_课程资料\第二大脑航海上岸大礼包 (79 文件: 64 md + 6 pdf + 7 zip + 1 pptx + 1 yaml)

## 一级文件夹完整 ID
- 01_高手领航直播: dc0c9b7aa2ea4444b5c5743dfb927e49
- 02_航海相关指南: 9e9050637a714d4c8ad8df5a17eec470
- 03_常用工具: cde9a5aad1144f99909e14d31943eae1
- _原始附件: 73931e0a0a5945c49522439c78b921f5
- 资料总览(page 已存在, skip): 6bc0a1d8e394481d865f44c8b5b83258

## 二级文件夹完整 ID
- 配套Skills(under 01): b647daa5c7e24772a9fe3e01c7623d2a
  - 录音处理: e1f7c7414fa64e8b9be8f36e769020d3 ✅SKILL: b64236b096f446f7958172ffaca5ae0d
  - 朋友圈文案: 06c2cf873cd043a3879697e2cf16263c ✅9/9完成
    - references: 4997eb4f7dee4a2badcb3460a183aadc
    - SKILL: 3338c198dba24a3ebdca9ae5f6965315 [raw 14266B 单次成功！]
    - README: 08624dd1f111494aa6fb66808060fbaa
    - 风格A: c4817d7022ee4329998b64837aa7d531 | 风格B: 00755b7d8e6846a5a280c2be689d3b7e
    - 风格C: adc73549bca44cb2b0aed67fd06cf666 | 风格D: ad5e793b9762486a9a2c03471d00ab7d
    - 风格E: 4293e728c6df4c7e98f8aa17abd41204 | 风格F: bfa6af8c8b4b48ae9f0fc7fe61fe2f5e
    - 风格G: c8c62dc6bc87450f8715a9867c5be133
  - 叁斤爆款笔记: 3114a6f4c1c04e5bae2f77a274ff3401 ✅4/4完成(上轮)
  - 叁斤内容复盘: 99b2267cb6ac48d7894c87072f096c3e ✅3/3完成
    - SKILL: f5cce00ce31a4c9fafda6e1e20038a86 | references: 4c94acf701cc4766a612abe2ec45b566
    - 01-复盘方法论: 9727a74663ea4b4cb6119e915b1f853c | 02-数据总表模板: d27cd9bdbf8745c7bae4d1af9ffec519
  - 叁斤账号定位: 9d641ae5bb9a4be98a6309055e7647cd ✅5/5完成
- 工作台搭建Skill(under 02): 1b2f93178db34bf1ade9c209cfa69f00
- 课程原文(under 02): efade0d8a57f4c1ca26dbf2bad1edbcb
- 课程摘录(under 02): 401e287f0ba34c57854c7ece2ebbc1db

## 已导入页面（md 27/64）
### 配套Skills 完成（录音1+朋友圈9+爆款4+复盘3+定位5=22md）
### 02_航海相关指南 top-level 8md + 工作台搭建Skill 8md+1yaml + 03_常用工具 1md — 待导入

## 工作流要点（关键！）
1. **raw markdown 直传** content_type=markdown：单次 ≤10.3KB 已验证成功。>10KB 文件分两次（首块 entry_import_content 创建，续块 entry_import_content_to_entry force_write=false 追加），在 --- 段落边界切分。
2. base64 分块（markdown_base64）仅 raw 失败时兜底，awk max=3300 字节，Bash: `LC_ALL=C awk -v max=3300 'BEGIN{part=1;n=0} { l=length($0)+1; if (n>0&&n+l>max){part++;n=0} print > (sprintf("/tmp/dw_%02d.md",part)); n+=l }' FILE` 再 base64 -w 0。
3. entry_import_content 必须同时传 parent_id + space_id。
4. entry_import_content_to_entry 必传 entry_id + content_type + content + force_write(false=追加)。
5. Bash 输出上限 20000 字符，中文文本约 2.5 字节/字，单次 cat ≤15KB 安全。

## 待办（按优先级）
- 任务#10 朋友圈文案 8 md（parent=朋友圈文案 folder）：SKILL(14266→2块) + references/README(3565) + 风格A-G(5172~6633, 7个单次)。需先建 references 子文件夹。
- 任务#8 02_航海相关指南 top 8 md + 工作台搭建Skill 8 md+1 yaml + 03_常用工具/工具索引(2578) + 01_高手领航直播 top(第五次摘录4680+资料索引2453)
- 任务#12 课程原文(先导课4: 12851/16996/16385/6983 + 图片附件4: 17297/27617/15171/16797 + 第一课5: 10180/9009/20282/7954/1446) + 课程摘录4(3336/3182/3890/3265) + Codex+Obsidian先导课3(同先导课03-2/4/5)
- 任务#11 二进制 15（6 pdf + 7 zip + 1 pptx + 1 yaml in _原始附件）：file_apply_upload(upload_type=PRE_SIGNED_URL)→curl -X PUT 上传→file_commit_upload(session_id)
- 任务#13 entry_list_children 全量核对
- 收尾: 写 .workbuddy/memory/2026-08-19.md
