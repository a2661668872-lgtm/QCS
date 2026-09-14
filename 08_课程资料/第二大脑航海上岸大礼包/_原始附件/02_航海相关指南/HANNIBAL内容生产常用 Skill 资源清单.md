# 社媒内容生产 Skill 资源清单（合计 56 项）

> 目标：为小红书、小绿书、公众号、抖音、视频号等平台，整理从选题分析、资料研究、知识库、脚本、制作、审核到分发复盘的可复用资源。

## 使用说明

- 其中“技能集合/框架/方法论”需要二次封装，不能都直接当作可安装 Skill。
- 推荐优先顺序：先选 1 个研究工具 + 1 个知识库 + 1 个脚本/制作工具 + 1 个审核工具，跑通小闭环后再扩展。

## 一、按内容生产环节分类

### A. 技能标准、提示词和流程封装

- **1. Agent Skills 规范**｜24,264 stars｜[agentskills/agentskills](https://github.com/agentskills/agentskills)｜用途：定义 SKILL.md、渐进式加载和可复用工作流的统一规范；适合把自己的选题、写作、审核流程封装成可迁移 Skill。｜平台：全部平台
- **2. Anthropic Skills**｜169,334 stars｜[anthropics/skills](https://github.com/anthropics/skills)｜用途：官方公开技能仓库，含文档、PDF、PPT、表格等复杂任务技能参考；可复用其“读取—处理—校验—交付”结构。｜平台：公众号/小红书/全部
- **3. Awesome AI Agent Skills**｜153 stars｜[seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills)｜用途：包含 100+ 可直接参考的 SKILL.md 工作流，适合快速寻找内容研究、写作、自动化和审校模板。｜平台：全部平台
- **4. Pexo Skills**｜765 stars｜[pexoai/pexo-skills](https://github.com/pexoai/pexo-skills)｜用途：面向内容创作的图片、音频、视频技能集合，可作为封面、配图、旁白和短视频制作的起点。｜平台：小红书/抖音/视频号
- **5. Social Media Skills**｜414 stars｜[blacktwist/social-media-skills](https://github.com/blacktwist/social-media-skills)｜用途：覆盖社媒策略、内容创建和分析，适合做平台定位、选题、文案、复盘与迭代。｜平台：小红书/小绿书/公众号/抖音
- **6. Production AI Agent Skills**｜15 stars｜[aiagentwithdhruv/skills](https://github.com/aiagentwithdhruv/skills)｜用途：包含浏览器自动化、内容创作和基础设施技能；适合把资料搜集、发布准备等重复操作串成流程。｜平台：全部平台
- **7. Hugging Face Skills**｜10,926 stars｜[huggingface/skills](https://github.com/huggingface/skills)｜用途：提供数据集创建、模型调用和评测类技能参考；适合为内容知识库增加分类、抽取和评估步骤。｜平台：公众号/全部
- **38. Prompt Engineering Guide**｜77,473 stars｜[dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)｜用途：系统整理提示词、RAG、Agent 和评测方法；适合优化选题分析、脚本生成和审校提示。｜平台：全部平台

### B. 选题研究、网页采集和素材整理

- **8. OpenAI Cookbook**｜75,237 stars｜[openai/openai-cookbook](https://github.com/openai/openai-cookbook)｜用途：大量 API、检索、结构化输出和评测示例；适合搭建选题研究、资料摘要、批量改写等工具链。｜平台：全部平台
- **19. Browser Use**｜109,173 stars｜[browser-use/browser-use](https://github.com/browser-use/browser-use)｜用途：让 Agent 操作网页完成搜索、阅读和表格采集；适合对标账号、竞品和热点研究。｜平台：小红书/抖音/公众号
- **20. Firecrawl**｜167,194 stars｜[firecrawl/firecrawl](https://github.com/firecrawl/firecrawl)｜用途：把网页转成干净 Markdown/结构化内容；适合采集文章、产品页、新闻和案例进入知识库。｜平台：公众号/全部

### C. 知识库、记忆和检索

- **15. LlamaIndex**｜51,637 stars｜[run-llama/llama_index](https://github.com/run-llama/llama_index)｜用途：文档接入、索引、检索和文档 Agent；适合把历史文章、访谈、素材卡变成可检索知识库。｜平台：公众号/全部
- **17. Haystack**｜26,206 stars｜[deepset-ai/haystack](https://github.com/deepset-ai/haystack)｜用途：成熟的检索、问答、管线和评估组件；适合搭建有来源引用的内容研究系统。｜平台：公众号/全部
- **21. Graphiti**｜29,916 stars｜[getzep/graphiti](https://github.com/getzep/graphiti)｜用途：构建时间感知的知识图谱和 Agent 记忆；适合沉淀人物、项目、观点及其关系。｜平台：公众号/全部
- **22. Mem0**｜63,235 stars｜[mem0ai/mem0](https://github.com/mem0ai/mem0)｜用途：为 Agent 提供可管理的长期记忆；适合让内容助手记住账号定位、受众偏好和历史复盘。｜平台：全部平台
- **23. Chroma**｜29,053 stars｜[chroma-core/chroma](https://github.com/chroma-core/chroma)｜用途：轻量向量数据库；适合个人内容库的语义检索和相似素材召回。｜平台：全部平台
- **24. Qdrant**｜33,967 stars｜[qdrant/qdrant](https://github.com/qdrant/qdrant)｜用途：高性能向量检索；适合规模增长后做素材、标题和评论的相似搜索。｜平台：全部平台
- **25. RAGFlow**｜88,259 stars｜[infiniflow/ragflow](https://github.com/infiniflow/ragflow)｜用途：面向复杂文档的 RAG 平台；适合 PDF、网页、表格、图片混合资料的知识库。｜平台：公众号/全部
- **30. AnythingLLM**｜64,706 stars｜[Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm)｜用途：低门槛的文档问答和工作区；适合个人把素材、手册和历史稿集中管理。｜平台：公众号/全部
- **31. Danswer**｜31,589 stars｜[Danswer-AI/danswer](https://github.com/Danswer-AI/danswer)｜用途：连接内部知识源并提供带来源的问答；适合团队内容资料和 SOP 检索。｜平台：公众号/全部

### D. Agent 编排、工具连接和自动化

- **9. OpenAI Swarm**｜21,906 stars｜[openai/swarm](https://github.com/openai/swarm)｜用途：轻量多 Agent 编排示例；适合拆成“研究员—编辑—审核员”协作流程。｜平台：全部平台
- **11. Microsoft AutoGen**｜60,419 stars｜[microsoft/autogen](https://github.com/microsoft/autogen)｜用途：角色型 Agent 协作框架；适合复杂内容生产任务中的研究、写作、审稿分工。｜平台：全部平台
- **12. CrewAI**｜57,069 stars｜[crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)｜用途：以角色和任务组织协作 Agent；适合搭建从选题到脚本、成稿、复盘的流水线。｜平台：全部平台
- **13. LangChain**｜144,237 stars｜[langchain-ai/langchain](https://github.com/langchain-ai/langchain)｜用途：连接模型、工具、检索和结构化输出；适合构建可调用知识库和内容生产工具。｜平台：全部平台
- **14. LangGraph**｜39,668 stars｜[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)｜用途：适合需要人工确认、分支、重试和持久状态的内容工作流。｜平台：全部平台
- **18. Smolagents**｜28,804 stars｜[huggingface/smolagents](https://github.com/huggingface/smolagents)｜用途：轻量代码型 Agent 框架；适合把抓取、清洗、统计和内容初筛组合起来。｜平台：全部平台
- **26. Langflow**｜153,230 stars｜[langflow-ai/langflow](https://github.com/langflow-ai/langflow)｜用途：用可视化节点搭建模型、检索和工具流程；适合不想先写大量代码的内容团队。｜平台：全部平台
- **27. Flowise**｜55,365 stars｜[FlowiseAI/Flowise](https://github.com/FlowiseAI/Flowise)｜用途：可视化构建 LLM 应用、RAG 和 Agent；适合快速做选题助手、文案助手和资料问答。｜平台：全部平台
- **28. n8n**｜200,601 stars｜[n8n-io/n8n](https://github.com/n8n-io/n8n)｜用途：连接表格、飞书、邮件、社媒和模型；适合把内容审批、排期、通知和发布前检查自动化。｜平台：全部平台
- **32. Vercel AI SDK**｜26,182 stars｜[vercel/ai](https://github.com/vercel/ai)｜用途：构建流式聊天、结构化生成和多模型应用；适合做自有选题台、脚本台和审核台。｜平台：全部平台
- **33. MCP Servers**｜89,558 stars｜[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)｜用途：提供模型调用外部数据和工具的标准服务器；适合接入网页、文件、表格和内容平台。｜平台：全部平台
- **34. Composio**｜29,685 stars｜[ComposioHQ/composio](https://github.com/ComposioHQ/composio)｜用途：把大量第三方 SaaS 工具接给 Agent；适合把飞书、Notion、GitHub、邮件等接入内容流。｜平台：全部平台
- **35. LiteLLM**｜56,314 stars｜[BerriAI/litellm](https://github.com/BerriAI/litellm)｜用途：统一调用不同模型并管理路由、成本和降级；适合内容团队按任务选择模型。｜平台：全部平台
- **36. Semantic Kernel**｜28,447 stars｜[microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel)｜用途：提供插件、记忆、规划和流程编排；适合做稳定、可审计的内容生产服务。｜平台：全部平台
- **37. Agno**｜41,705 stars｜[agno-agi/agno](https://github.com/agno-agi/agno)｜用途：快速搭建带工具、记忆和知识库的 Agent；适合做个人内容主编或研究助理。｜平台：全部平台
- **41. Trigger.dev**｜16,014 stars｜[triggerdotdev/trigger.dev](https://github.com/triggerdotdev/trigger.dev)｜用途：适合长任务、定时任务、重试和队列；可用于批量抓取、批量生成和发布排期。｜平台：全部平台
- **42. MCP Python SDK**｜24,001 stars｜[modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)｜用途：开发自有 MCP 工具的基础 SDK；适合把内部素材库、审核器和发布系统封装成可调用工具。｜平台：全部平台

### E. 质量控制和评测

- **10. OpenAI Evals**｜19,166 stars｜[openai/evals](https://github.com/openai/evals)｜用途：用于评估 LLM 和 Agent 系统；适合建立标题、事实、禁用词、风格一致性检查集。｜平台：全部平台

### F. 实战skill（18 项）

- **S1. 从对话工具到自动化工作流——单人如何用 AI 实现 10 人团队的产出**｜[https://scys.com/navigator/](https://scys.com/navigator/)｜用途：把内容研究、写作、审核和分发拆成可委派步骤，适合建立个人内容工厂。｜平台：全部平台｜类型：流程设计/自动化
- **S2. AI 给普通人最好的礼物——Skills 自动化工作流**｜[https://scys.com/navigator/](https://scys.com/navigator/)｜用途：把重复 SOP 封装成可复用 Skill，适合选题、资料整理和审核流程。｜平台：全部平台｜类型：技能封装
- **S3. AI 内容生产工作台**｜[https://scys.com/navigator/hackathon](https://scys.com/navigator/hackathon)｜用途：参考从选题到成稿、成片、发布回流的一体化工作台。｜平台：小红书/抖音/公众号｜类型：内容生产总流程
- **S4. 最强编导，越用越强**｜[https://scys.com/navigator/hackathon](https://scys.com/navigator/hackathon)｜用途：把每次创作沉淀回知识库，让选题、脚本和复盘形成循环。｜平台：抖音/小红书/视频号｜类型：选题/脚本/复盘
- **S5. 视频号爆款内容创作台**｜[https://scys.com/navigator/hackathon](https://scys.com/navigator/hackathon)｜用途：先诊断账号和文案，再搜索爆款、拆解原因并生成二创脚本。｜平台：视频号/抖音｜类型：机会雷达/二创脚本
- **S6. 小红书封面自动化生成网站**｜[https://scys.com/navigator/hackathon](https://scys.com/navigator/hackathon)｜用途：根据文案生成封面、标题、正文和标签，适合批量测试图文表达。｜平台：小红书/小绿书｜类型：封面/标题/正文
- **S7. 小红书 GEO 全品牌运营台**｜[https://scys.com/navigator/hackathon](https://scys.com/navigator/hackathon)｜用途：围绕小红书搜索和品牌内容做自动化运营，适合本地生活、美业和连锁品牌。｜平台：小红书/小绿书｜类型：平台运营/搜索
- **S8. 基于小红书 10 万条数据验证的 AI 情绪营销方法论**｜[https://scys.com/navigator/](https://scys.com/navigator/)｜用途：用大规模内容和评论数据识别情绪需求，辅助选题和标题方向。｜平台：小红书/小绿书｜类型：选题/用户洞察
- **S9. 从 AI 小白到打造知识库**｜[https://scys.com/navigator/](https://scys.com/navigator/)｜用途：适合把个人资料、素材和经验整理为可检索的内容资产。｜平台：公众号/全部｜类型：知识库入门
- **S10. 从设计服务到 AI 漫剧：重构内容生产流程**｜[https://scys.com/navigator/](https://scys.com/navigator/)｜用途：参考从设计服务到 AI 漫剧的生产拆解，适合视觉内容和短视频链路。｜平台：抖音/小红书｜类型：图像/视频工作流
- **S11. 用 AI，没有写不出来的小红书爆款**｜[https://scys.com/navigator/conferences/cmr4al88700n65cr53hqtvo16](https://scys.com/navigator/conferences/cmr4al88700n65cr53hqtvo16)｜用途：关注选赛道、找打法、写人话和 AI 辅助成稿，适合做图文脚本。｜平台：小红书/小绿书｜类型：小红书写作
- **S12. 用 Obsidian 搭建企业知识库，落地 AI 智能体**｜[https://scys.com/navigator/conferences/cmr4al7s200mk5cr557lg1tk7](https://scys.com/navigator/conferences/cmr4al7s200mk5cr557lg1tk7)｜用途：把企业资料、SOP 和经验沉淀到知识库，再让 Agent 调用。｜平台：公众号/全部｜类型：知识库/Agent
- **S13. Skill：把你脑子里的 SOP 变成不睡觉的员工**｜[https://scys.com/navigator/conferences/cmr4al7s200mk5cr557lg1tk7](https://scys.com/navigator/conferences/cmr4al7s200mk5cr557lg1tk7)｜用途：把隐性经验写成可执行的 Skill，适合长期重复的内容任务。｜平台：全部平台｜类型：SOP/技能化
- **S14. 半年 40 亿流量：Seedance 爆款制作全拆解**｜[https://scys.com/navigator/conferences/cmr4al7s200mk5cr557lg1tk7](https://scys.com/navigator/conferences/cmr4al7s200mk5cr557lg1tk7)｜用途：强调剧本、前三秒、画面密度和提示词控制，适合短视频脚本拆解。｜平台：抖音/视频号｜类型：视频脚本/画面
- **S15. 从 0 到 1 搭建 AI 赋能的小红书高效运营体系**｜[https://scys.com/navigator/conferences/cmr4ala3e00pr5cr51i7rm9k6](https://scys.com/navigator/conferences/cmr4ala3e00pr5cr51i7rm9k6)｜用途：覆盖定位、内容、流量、转化和日常运营，适合从零搭小红书账号。｜平台：小红书/小绿书｜类型：运营闭环
- **S16. 小红书搜索流量的黄金入口：搜搜薯强制置顶+信任背书**｜[https://scys.com/navigator/](https://scys.com/navigator/)｜用途：适合把关键词、搜索意图和信任证明写进内容与标题。｜平台：小红书/小绿书｜类型：搜索/分发
- **S17. 单场 880 万：视频号直播的坑与心得**｜[https://scys.com/navigator/conferences/cmr4ala3e00pr5cr51i7rm9k6](https://scys.com/navigator/conferences/cmr4ala3e00pr5cr51i7rm9k6)｜用途：强调选品、服务和直播 SOP，适合把内容生产延伸到直播转化。｜平台：视频号/抖音｜类型：直播脚本/SOP
- **S18. 播客集市：把长播客拆成短视频**｜[https://scys.com/navigator/hackathon](https://scys.com/navigator/hackathon)｜用途：从长音频中选段、字幕、竖屏成片、批量分发并追踪效果。｜平台：抖音/视频号/小红书｜类型：内容拆条/分发

## 二、按平台给出的优先组合

- **小红书/小绿书图文**：Social Media Skills + Firecrawl/Browser Use + LlamaIndex/Chroma + DSPy + 小红书封面自动化 + “用 AI，没有写不出来的小红书爆款”。
- **公众号深度文章**：OpenAI Cookbook + Firecrawl + Haystack/RAGFlow + Graphiti/Mem0 + OpenAI Evals + “从 AI 小白到打造知识库”。
- **抖音/视频号短视频**：Pexo Skills + Browser Use + Seedance 爆款制作拆解 + 播客拆条 + OpenAI Evals；先脚本后画面，再做人工审核。
- **多平台一稿多发**：Blacktwist Social Media Skills + n8n + MCP Servers + LiteLLM + “最强编导，越用越强”。

