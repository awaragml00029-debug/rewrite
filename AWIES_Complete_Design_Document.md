# 学术写作智能提升系统（AWIES）完整设计文档

## 目录
1. [项目概述](#1-项目概述)
2. [系统架构设计](#2-系统架构设计)
3. [核心功能模块](#3-核心功能模块)
4. [技术实现方案](#4-技术实现方案)
5. [数据库设计](#5-数据库设计)
6. [API设计规范](#6-api设计规范)
7. [前端界面设计](#7-前端界面设计)
8. [部署与运维](#8-部署与运维)
9. [测试策略](#9-测试策略)
10. [项目实施计划](#10-项目实施计划)

---

## 1. 项目概述

### 1.1 项目背景
非英语母语的学术研究者在撰写英文论文时，常面临表达不够地道、不符合学术写作规范等问题。同时，查找相关文献和选择合适的投稿期刊也是耗时的工作。本系统旨在通过AI技术解决这些痛点。

### 1.2 核心目标
- **提升Native程度**：将学术英语写作提升至接近母语者水平
- **保持学术诚信**：明确标注AI辅助，不用于规避检测
- **智能文献推荐**：集成JANE API，提供期刊、文献和作者推荐
- **个性化学习**：根据用户写作习惯提供定制化改进

### 1.3 目标用户
- 非英语母语的研究生和博士生
- 需要发表英文论文的学者
- 科研机构的研究人员
- 高校教师

### 1.4 系统特色
- **渐进式改写**：四级改写系统，用户可控
- **实时对比**：改写前后对比，标注修改原因
- **学科定制**：针对不同学科的写作规范
- **文献集成**：一站式写作和文献查找

---

## 2. 系统架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                         前端层                               │
│  Web App (React) | Mobile App | Desktop App (Electron)      │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   API Gateway      │
                    │   (Kong/Nginx)     │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                         服务层                               │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ 文本分析服务 │ 改写引擎服务 │ JANE集成服务 │ 用户管理服务   │
│ (Python)     │ (Python)     │ (Python)     │ (Node.js)      │
└──────────────┴──────────────┴──────────────┴────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                         数据层                               │
├────────────┬────────────┬────────────┬──────────────────────┤
│ PostgreSQL │   Redis    │ Elasticsearch │  MongoDB         │
│ (主数据库) │  (缓存)    │   (搜索引擎)  │ (文档存储)       │
└────────────┴────────────┴────────────┴──────────────────────┘
```

### 2.2 微服务架构

```yaml
services:
  text-analysis-service:
    description: "文本分析和问题诊断"
    port: 8001
    dependencies:
      - spaCy
      - NLTK
      - transformers
    
  enhancement-service:
    description: "核心改写引擎"
    port: 8002
    dependencies:
      - LangChain
      - Claude API
      - GPT-4 API
    
  jane-integration-service:
    description: "JANE API集成"
    port: 8003
    dependencies:
      - zeep (SOAP client)
      - requests
    
  user-service:
    description: "用户管理和认证"
    port: 8004
    dependencies:
      - JWT
      - OAuth2
    
  document-service:
    description: "文档管理"
    port: 8005
    dependencies:
      - python-docx
      - PyPDF2
      - pandoc
```

### 2.3 数据流设计

```mermaid
graph LR
    A[用户上传文本] --> B[文本预处理]
    B --> C[文本分析服务]
    C --> D{问题诊断}
    D --> E[改写引擎]
    E --> F[人工确认]
    F --> G[JANE API]
    G --> H[推荐结果]
    H --> I[最终输出]
    
    J[模式库] --> E
    K[用户偏好] --> E
    L[学科规范] --> E
```

---

## 3. 核心功能模块

### 3.1 文本分析模块

#### 3.1.1 词汇分析器

```python
class LexicalAnalyzer:
    """词汇层面分析"""
    
    def __init__(self):
        self.academic_word_list = self.load_awl()
        self.collocation_db = self.load_collocations()
        
    def analyze(self, text):
        issues = []
        
        # 1. 检测过于简单的词汇
        simple_words = self.detect_simple_vocabulary(text)
        if simple_words:
            issues.append({
                'type': 'simple_vocabulary',
                'items': simple_words,
                'severity': 3,
                'suggestions': self.get_academic_alternatives(simple_words)
            })
        
        # 2. 检测错误的词汇搭配
        wrong_collocations = self.detect_wrong_collocations(text)
        if wrong_collocations:
            issues.append({
                'type': 'wrong_collocation',
                'items': wrong_collocations,
                'severity': 4,
                'suggestions': self.get_correct_collocations(wrong_collocations)
            })
        
        # 3. 检测词汇多样性
        diversity_score = self.calculate_lexical_diversity(text)
        if diversity_score < 0.5:
            issues.append({
                'type': 'low_diversity',
                'score': diversity_score,
                'severity': 2
            })
        
        return issues
    
    def detect_simple_vocabulary(self, text):
        """检测过于简单的词汇"""
        simple_words_map = {
            'big': ['substantial', 'considerable', 'significant'],
            'small': ['minimal', 'negligible', 'minor'],
            'good': ['beneficial', 'advantageous', 'favorable'],
            'bad': ['detrimental', 'adverse', 'unfavorable'],
            'show': ['demonstrate', 'illustrate', 'indicate'],
            'get': ['obtain', 'acquire', 'receive']
        }
        # 实现检测逻辑
        return detected_words
```

#### 3.1.2 句法分析器

```python
class SyntacticAnalyzer:
    """句法结构分析"""
    
    def analyze(self, text):
        issues = []
        sentences = self.split_sentences(text)
        
        # 1. 句子长度分析
        length_issues = self.analyze_sentence_lengths(sentences)
        
        # 2. 句式多样性
        variety_score = self.calculate_sentence_variety(sentences)
        
        # 3. 语法复杂度
        complexity = self.analyze_grammatical_complexity(sentences)
        
        # 4. 并列句与复合句比例
        clause_ratio = self.analyze_clause_structures(sentences)
        
        return {
            'length_issues': length_issues,
            'variety_score': variety_score,
            'complexity': complexity,
            'clause_ratio': clause_ratio
        }
```

#### 3.1.3 语篇分析器

```python
class DiscourseAnalyzer:
    """语篇连贯性分析"""
    
    def analyze(self, text):
        paragraphs = self.split_paragraphs(text)
        
        # 1. 段落结构分析
        paragraph_structure = self.analyze_paragraph_structure(paragraphs)
        
        # 2. 衔接词使用
        transitions = self.analyze_transitions(text)
        
        # 3. 主题连贯性
        coherence_score = self.calculate_coherence(paragraphs)
        
        # 4. 指代关系
        reference_chains = self.analyze_reference_chains(text)
        
        return {
            'structure': paragraph_structure,
            'transitions': transitions,
            'coherence': coherence_score,
            'references': reference_chains
        }
```

### 3.2 改写引擎模块

#### 3.2.1 四级改写系统

```python
class EnhancementEngine:
    """核心改写引擎"""
    
    def __init__(self):
        self.llm = LLMInterface()
        self.pattern_db = PatternDatabase()
        self.discipline_rules = DisciplineRules()
    
    async def enhance(self, text, level, discipline='general'):
        """
        分级改写
        Level 1: 基础纠错
        Level 2: Native表达
        Level 3: 学术规范
        Level 4: 整体润色
        """
        
        # 保存原始文本用于对比
        original = text
        
        # 逐级应用改写
        if level >= 1:
            text = await self.level1_basic_corrections(text)
            
        if level >= 2:
            text = await self.level2_native_expression(text, discipline)
            
        if level >= 3:
            text = await self.level3_academic_style(text, discipline)
            
        if level >= 4:
            text = await self.level4_discourse_optimization(text)
        
        # 生成改写报告
        report = self.generate_enhancement_report(original, text)
        
        return text, report
    
    async def level1_basic_corrections(self, text):
        """Level 1: 基础纠错"""
        
        # 语法检查
        text = await self.correct_grammar(text)
        
        # 拼写检查
        text = self.correct_spelling(text)
        
        # 标点符号
        text = self.correct_punctuation(text)
        
        # 基本词汇替换
        replacements = {
            r'\bbig\b': 'large',
            r'\bsmall\b': 'minor',
            r'\bgood\b': 'positive',
            r'\bbad\b': 'negative'
        }
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    async def level2_native_expression(self, text, discipline):
        """Level 2: Native表达优化"""
        
        prompt = f"""
        Task: Enhance the following academic text to sound more native while preserving the exact meaning.
        
        Discipline: {discipline}
        
        Focus on:
        1. Natural collocations (e.g., "conduct research" not "make research")
        2. Academic phrases that native speakers commonly use
        3. Proper preposition usage
        4. Idiomatic expressions suitable for academic writing
        
        Text: {text}
        
        Rules:
        - Maintain the original meaning precisely
        - Keep the academic tone
        - Do not add new information
        - Preserve all citations and references
        
        Output the enhanced text only.
        """
        
        enhanced = await self.llm.generate(prompt)
        
        # 应用词汇搭配数据库
        enhanced = self.apply_collocation_fixes(enhanced)
        
        return enhanced
    
    async def level3_academic_style(self, text, discipline):
        """Level 3: 学术规范优化"""
        
        # 应用学科特定规则
        rules = self.discipline_rules.get_rules(discipline)
        
        # Hedging策略
        text = self.apply_hedging(text, rules['hedging_level'])
        
        # 语态调整
        if rules['preferred_voice'] == 'passive':
            text = self.increase_passive_voice(text)
        elif rules['preferred_voice'] == 'active':
            text = self.increase_active_voice(text)
        
        # 时态规范
        text = self.standardize_tenses(text, rules['tense_rules'])
        
        # 学术词汇提升
        text = await self.enhance_academic_vocabulary(text)
        
        return text
    
    async def level4_discourse_optimization(self, text):
        """Level 4: 语篇优化"""
        
        # 段落重组
        paragraphs = self.split_paragraphs(text)
        
        # 优化每个段落
        enhanced_paragraphs = []
        for para in paragraphs:
            # 确保有主题句
            para = self.ensure_topic_sentence(para)
            
            # 改进句子间的衔接
            para = self.improve_sentence_flow(para)
            
            # 多样化过渡词
            para = self.diversify_transitions(para)
            
            enhanced_paragraphs.append(para)
        
        # 段落间衔接
        text = self.improve_paragraph_transitions(enhanced_paragraphs)
        
        return text
```

#### 3.2.2 学科特定规则

```python
class DisciplineRules:
    """学科特定写作规范"""
    
    RULES = {
        'computer_science': {
            'preferred_voice': 'mixed',
            'hedging_level': 'moderate',
            'common_phrases': [
                'We propose', 'Our approach', 'The algorithm',
                'Experimental results show', 'Performance evaluation'
            ],
            'tense_rules': {
                'methodology': 'present',
                'results': 'past',
                'discussion': 'present'
            }
        },
        
        'biology': {
            'preferred_voice': 'passive',
            'hedging_level': 'high',
            'common_phrases': [
                'It was observed that', 'Data were collected',
                'Samples were analyzed', 'Results suggest'
            ],
            'tense_rules': {
                'methodology': 'past',
                'results': 'past',
                'discussion': 'present'
            }
        },
        
        'social_sciences': {
            'preferred_voice': 'active',
            'hedging_level': 'high',
            'common_phrases': [
                'This study examines', 'Findings indicate',
                'The analysis reveals', 'Evidence suggests'
            ],
            'tense_rules': {
                'literature_review': 'present_perfect',
                'methodology': 'past',
                'discussion': 'present'
            }
        }
    }
```

### 3.3 JANE API集成模块

#### 3.3.1 API连接器

```python
import asyncio
from zeep import Client
from typing import List, Dict, Optional
import logging

class JANEConnector:
    """JANE API连接器"""
    
    def __init__(self):
        self.wsdl_url = 'http://jane.biosemantics.org:8080/JaneServer/services/JaneSOAPServer?wsdl'
        self.base_url = 'http://jane.biosemantics.org/'
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化SOAP客户端"""
        try:
            self.client = Client(self.wsdl_url)
            logging.info("JANE SOAP client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize JANE client: {e}")
            raise
    
    async def get_journal_recommendations(
        self, 
        text: str, 
        filter_string: str = ""
    ) -> List[Dict]:
        """
        获取期刊推荐
        
        Args:
            text: 输入文本（摘要或全文）
            filter_string: 过滤条件
            
        Returns:
            期刊推荐列表
        """
        try:
            # 异步调用SOAP服务
            journals = await asyncio.to_thread(
                self.client.service.getJournals,
                text,
                filter_string
            )
            
            # 解析并格式化结果
            recommendations = []
            for journal in journals:
                recommendations.append({
                    'title': journal.title,
                    'similarity_score': journal.similarity,
                    'impact_factor': getattr(journal, 'impactFactor', None),
                    'open_access': getattr(journal, 'openAccess', False),
                    'publisher': getattr(journal, 'publisher', 'Unknown'),
                    'scope': getattr(journal, 'scope', ''),
                    'url': getattr(journal, 'url', ''),
                    'confidence': self._calculate_confidence(journal.similarity)
                })
            
            # 按相似度排序
            recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return recommendations[:10]  # 返回前10个推荐
            
        except Exception as e:
            logging.error(f"Error getting journal recommendations: {e}")
            return []
    
    async def find_related_papers(
        self, 
        text: str, 
        count: int = 20, 
        offset: int = 0
    ) -> List[Dict]:
        """
        查找相关论文
        
        Args:
            text: 输入文本
            count: 返回数量
            offset: 偏移量（用于分页）
            
        Returns:
            相关论文列表
        """
        try:
            papers = await asyncio.to_thread(
                self.client.service.getPapers,
                text,
                "",  # filter_string
                count,
                offset
            )
            
            related_papers = []
            for paper in papers:
                related_papers.append({
                    'title': paper.title,
                    'authors': self._parse_authors(paper.authors),
                    'year': getattr(paper, 'year', None),
                    'journal': getattr(paper, 'journal', ''),
                    'doi': getattr(paper, 'doi', ''),
                    'abstract': getattr(paper, 'abstract', ''),
                    'similarity_score': paper.similarity,
                    'citations': getattr(paper, 'citations', 0),
                    'url': getattr(paper, 'url', '')
                })
            
            return related_papers
            
        except Exception as e:
            logging.error(f"Error finding related papers: {e}")
            return []
    
    async def find_potential_collaborators(
        self, 
        text: str, 
        filter_string: str = ""
    ) -> List[Dict]:
        """
        查找潜在合作者
        
        Args:
            text: 输入文本
            filter_string: 过滤条件
            
        Returns:
            潜在合作者列表
        """
        try:
            authors = await asyncio.to_thread(
                self.client.service.getAuthors,
                text,
                filter_string
            )
            
            collaborators = []
            for author in authors:
                collaborators.append({
                    'name': author.name,
                    'affiliation': getattr(author, 'affiliation', ''),
                    'email': getattr(author, 'email', ''),
                    'research_areas': getattr(author, 'researchAreas', []),
                    'h_index': getattr(author, 'hIndex', None),
                    'total_publications': getattr(author, 'publicationCount', 0),
                    'similarity_score': author.similarity,
                    'recent_papers': self._get_recent_papers(author)
                })
            
            return collaborators[:20]  # 返回前20个推荐
            
        except Exception as e:
            logging.error(f"Error finding collaborators: {e}")
            return []
    
    def _calculate_confidence(self, similarity_score: float) -> str:
        """计算推荐置信度"""
        if similarity_score >= 0.8:
            return 'Very High'
        elif similarity_score >= 0.6:
            return 'High'
        elif similarity_score >= 0.4:
            return 'Medium'
        else:
            return 'Low'
    
    def _parse_authors(self, authors_string: str) -> List[str]:
        """解析作者列表"""
        if not authors_string:
            return []
        return [author.strip() for author in authors_string.split(',')]
    
    def _get_recent_papers(self, author) -> List[Dict]:
        """获取作者近期论文"""
        # 这里可以实现获取作者近期论文的逻辑
        return []
```

#### 3.3.2 推荐引擎

```python
class RecommendationEngine:
    """推荐引擎"""
    
    def __init__(self):
        self.jane_connector = JANEConnector()
        self.text_processor = TextProcessor()
    
    async def generate_recommendations(
        self, 
        text: str, 
        recommendation_types: List[str]
    ) -> Dict:
        """
        生成综合推荐报告
        
        Args:
            text: 改写后的文本
            recommendation_types: 需要的推荐类型
            
        Returns:
            推荐报告
        """
        
        # 提取关键内容用于查询
        query_text = self.text_processor.extract_key_content(text)
        
        recommendations = {}
        
        # 并发获取所有推荐
        tasks = []
        
        if 'journals' in recommendation_types:
            tasks.append(self._get_journal_recommendations(query_text))
            
        if 'papers' in recommendation_types:
            tasks.append(self._get_paper_recommendations(query_text))
            
        if 'authors' in recommendation_types:
            tasks.append(self._get_author_recommendations(query_text))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        for result in results:
            if not isinstance(result, Exception):
                recommendations.update(result)
        
        # 生成推荐报告
        report = self.format_recommendation_report(recommendations)
        
        return report
    
    async def _get_journal_recommendations(self, text: str) -> Dict:
        """获取期刊推荐"""
        journals = await self.jane_connector.get_journal_recommendations(text)
        
        # 增强推荐结果
        for journal in journals:
            # 添加投稿建议
            journal['submission_tips'] = self._get_submission_tips(journal)
            # 添加匹配原因
            journal['match_reasons'] = self._analyze_match_reasons(journal, text)
        
        return {'journals': journals}
    
    async def _get_paper_recommendations(self, text: str) -> Dict:
        """获取相关论文推荐"""
        papers = await self.jane_connector.find_related_papers(text)
        
        # 分类论文
        categorized = {
            'highly_relevant': [],
            'methodology_similar': [],
            'topic_related': []
        }
        
        for paper in papers:
            category = self._categorize_paper(paper, text)
            categorized[category].append(paper)
        
        return {'papers': categorized}
    
    def format_recommendation_report(self, recommendations: Dict) -> Dict:
        """格式化推荐报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': self._generate_summary(recommendations),
            'recommendations': recommendations,
            'action_items': self._generate_action_items(recommendations)
        }
        
        return report
```

---

## 4. 技术实现方案

### 4.1 技术栈详细说明

#### 4.1.1 后端技术栈

```yaml
core_framework:
  language: Python 3.10+
  framework: FastAPI
  advantages:
    - 异步支持
    - 自动API文档
    - 类型检查
    - 高性能

nlp_processing:
  - spaCy: "工业级NLP库"
  - NLTK: "学术文本处理"
  - TextBlob: "情感分析"
  - Transformers: "BERT模型集成"

llm_integration:
  - LangChain: "LLM编排框架"
  - Anthropic Claude API: "主要改写引擎"
  - OpenAI GPT-4: "备用改写引擎"
  - Local Models: "快速诊断和分类"

database:
  primary: PostgreSQL 14+
  cache: Redis 7.0
  search: Elasticsearch 8.0
  document: MongoDB 5.0

message_queue:
  - RabbitMQ: "任务队列"
  - Celery: "异步任务处理"

monitoring:
  - Prometheus: "指标收集"
  - Grafana: "可视化监控"
  - Sentry: "错误追踪"
```

#### 4.1.2 前端技术栈

```yaml
framework:
  - React 18
  - TypeScript 5.0
  - Next.js 14 (SSR支持)

state_management:
  - Redux Toolkit
  - React Query (API状态)

ui_components:
  - Ant Design: "主要UI库"
  - TailwindCSS: "样式系统"
  - Monaco Editor: "代码编辑器"

realtime:
  - Socket.io: "实时通信"
  - WebRTC: "协作编辑"

visualization:
  - D3.js: "数据可视化"
  - Recharts: "图表组件"
  - diff2html: "文本对比"
```

### 4.2 开发环境配置

```bash
# 后端环境配置
# requirements.txt

# Core Framework
fastapi==0.104.0
uvicorn==0.23.2
pydantic==2.4.0

# NLP Libraries
spacy==3.7.0
nltk==3.8.1
transformers==4.35.0
textblob==0.17.1

# LLM Integration
langchain==0.0.330
anthropic==0.7.0
openai==1.3.0

# Database
asyncpg==0.29.0
redis==5.0.0
motor==3.3.0
elasticsearch==8.10.0

# JANE API
zeep==4.2.1

# Utils
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-docx==1.0.0
PyPDF2==3.0.0
pandas==2.1.0
numpy==1.26.0

# Testing
pytest==7.4.0
pytest-asyncio==0.21.0
httpx==0.25.0

# Monitoring
prometheus-client==0.18.0
sentry-sdk==1.35.0
```

### 4.3 Docker配置

```dockerfile
# Dockerfile for Enhancement Service

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_lg

# Copy application code
COPY . .

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml

version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: awies_db
      POSTGRES_USER: awies_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  elasticsearch:
    image: elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    volumes:
      - elastic_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  text-analysis:
    build:
      context: ./services/text-analysis
      dockerfile: Dockerfile
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://awies_user:${DB_PASSWORD}@postgres/awies_db
      REDIS_URL: redis://redis:6379
    ports:
      - "8001:8000"

  enhancement-service:
    build:
      context: ./services/enhancement
      dockerfile: Dockerfile
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://awies_user:${DB_PASSWORD}@postgres/awies_db
      REDIS_URL: redis://redis:6379
      CLAUDE_API_KEY: ${CLAUDE_API_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8002:8000"

  jane-integration:
    build:
      context: ./services/jane-integration
      dockerfile: Dockerfile
    depends_on:
      - redis
    environment:
      REDIS_URL: redis://redis:6379
    ports:
      - "8003:8000"

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - text-analysis
      - enhancement-service
      - jane-integration

volumes:
  postgres_data:
  redis_data:
  elastic_data:
```

---

## 5. 数据库设计

### 5.1 核心数据表

```sql
-- 用户表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    institution VARCHAR(200),
    discipline VARCHAR(100),
    subscription_tier VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}'::jsonb
);

-- 文档表
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500),
    original_text TEXT NOT NULL,
    enhanced_text TEXT,
    document_type VARCHAR(50), -- 'paper', 'abstract', 'thesis', etc.
    discipline VARCHAR(100),
    enhancement_level INTEGER,
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 改写记录表
CREATE TABLE enhancement_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    segment_index INTEGER,
    original_segment TEXT,
    enhanced_segment TEXT,
    enhancement_type VARCHAR(50),
    change_reason TEXT,
    confidence_score FLOAT,
    accepted BOOLEAN DEFAULT false,
    user_feedback VARCHAR(20), -- 'accepted', 'rejected', 'modified'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 问题诊断表
CREATE TABLE diagnosis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    issue_type VARCHAR(100),
    severity INTEGER CHECK (severity >= 1 AND severity <= 5),
    location_start INTEGER,
    location_end INTEGER,
    description TEXT,
    suggestion TEXT,
    resolved BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- JANE推荐结果表
CREATE TABLE jane_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    recommendation_type VARCHAR(50), -- 'journal', 'paper', 'author'
    title TEXT,
    authors TEXT[],
    similarity_score FLOAT,
    metadata JSONB,
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    user_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 写作模式库表
CREATE TABLE writing_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pattern_type VARCHAR(100),
    discipline VARCHAR(100),
    non_native_pattern TEXT,
    native_alternatives TEXT[],
    example_sentences TEXT[],
    usage_frequency INTEGER DEFAULT 0,
    effectiveness_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户学习记录表
CREATE TABLE user_learning_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    pattern_id UUID REFERENCES writing_patterns(id),
    times_encountered INTEGER DEFAULT 1,
    times_corrected INTEGER DEFAULT 0,
    last_encountered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mastery_level FLOAT DEFAULT 0.0
);

-- 会话历史表
CREATE TABLE enhancement_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id),
    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_end TIMESTAMP,
    total_changes INTEGER DEFAULT 0,
    accepted_changes INTEGER DEFAULT 0,
    time_spent_seconds INTEGER,
    session_metadata JSONB DEFAULT '{}'::jsonb
);

-- 创建索引
CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(processing_status);
CREATE INDEX idx_enhancement_records_document ON enhancement_records(document_id);
CREATE INDEX idx_diagnosis_document ON diagnosis_results(document_id);
CREATE INDEX idx_jane_document ON jane_recommendations(document_id);
CREATE INDEX idx_patterns_discipline ON writing_patterns(discipline);
CREATE INDEX idx_learning_user ON user_learning_records(user_id);
CREATE INDEX idx_sessions_user ON enhancement_sessions(user_id);

-- 创建视图：用户统计
CREATE VIEW user_statistics AS
SELECT 
    u.id,
    u.username,
    COUNT(DISTINCT d.id) as total_documents,
    COUNT(DISTINCT er.id) as total_enhancements,
    AVG(er.confidence_score) as avg_confidence,
    COUNT(DISTINCT jr.id) as total_recommendations
FROM users u
LEFT JOIN documents d ON u.id = d.user_id
LEFT JOIN enhancement_records er ON d.id = er.document_id
LEFT JOIN jane_recommendations jr ON d.id = jr.document_id
GROUP BY u.id, u.username;
```

### 5.2 Redis缓存设计

```python
# Redis缓存键设计

class RedisKeys:
    """Redis键命名规范"""
    
    # 用户相关
    USER_SESSION = "session:{user_id}"  # 用户会话
    USER_PREFERENCES = "user:pref:{user_id}"  # 用户偏好
    USER_QUOTA = "user:quota:{user_id}:{date}"  # 用户配额
    
    # 文档处理
    DOC_PROCESSING = "doc:processing:{doc_id}"  # 处理中的文档
    DOC_CACHE = "doc:cache:{doc_id}"  # 文档缓存
    
    # 模式缓存
    PATTERN_CACHE = "pattern:{discipline}:{type}"  # 模式缓存
    COLLOCATION_CACHE = "collocation:{word}"  # 搭配缓存
    
    # JANE API缓存
    JANE_JOURNAL = "jane:journal:{text_hash}"  # 期刊推荐缓存
    JANE_PAPER = "jane:paper:{text_hash}"  # 论文推荐缓存
    JANE_AUTHOR = "jane:author:{text_hash}"  # 作者推荐缓存
    
    # 速率限制
    RATE_LIMIT_API = "rate:api:{user_id}:{endpoint}"  # API速率限制
    RATE_LIMIT_LLM = "rate:llm:{user_id}"  # LLM调用限制
    
    # 统计数据
    STATS_DAILY = "stats:daily:{date}"  # 每日统计
    STATS_USER = "stats:user:{user_id}:{date}"  # 用户统计
```

---

## 6. API设计规范

### 6.1 RESTful API设计

```yaml
# API端点设计

authentication:
  POST /api/auth/register:
    description: "用户注册"
    body: { email, password, username, institution }
    response: { user_id, access_token }
    
  POST /api/auth/login:
    description: "用户登录"
    body: { email, password }
    response: { access_token, refresh_token }
    
  POST /api/auth/refresh:
    description: "刷新令牌"
    body: { refresh_token }
    response: { access_token }

documents:
  POST /api/documents:
    description: "创建文档"
    body: { title, text, document_type, discipline }
    response: { document_id, status }
    
  GET /api/documents/{document_id}:
    description: "获取文档"
    response: { document_data }
    
  PUT /api/documents/{document_id}:
    description: "更新文档"
    body: { title, text }
    response: { success }
    
  DELETE /api/documents/{document_id}:
    description: "删除文档"
    response: { success }

enhancement:
  POST /api/enhance:
    description: "文本改写"
    body: { text, level, discipline, options }
    response: { enhanced_text, changes, report }
    
  POST /api/enhance/{document_id}:
    description: "改写文档"
    body: { level, options }
    response: { job_id, status }
    
  GET /api/enhance/status/{job_id}:
    description: "获取改写状态"
    response: { status, progress, result }

analysis:
  POST /api/analyze:
    description: "文本分析"
    body: { text, analysis_types }
    response: { issues, suggestions, score }

recommendations:
  POST /api/recommendations/journals:
    description: "期刊推荐"
    body: { text, filters }
    response: { journals[] }
    
  POST /api/recommendations/papers:
    description: "论文推荐"
    body: { text, count, offset }
    response: { papers[] }
    
  POST /api/recommendations/authors:
    description: "作者推荐"
    body: { text, filters }
    response: { authors[] }

user:
  GET /api/user/profile:
    description: "用户资料"
    response: { user_data }
    
  PUT /api/user/profile:
    description: "更新资料"
    body: { profile_data }
    response: { success }
    
  GET /api/user/statistics:
    description: "使用统计"
    response: { statistics }
```

### 6.2 WebSocket事件

```javascript
// WebSocket事件定义

// 客户端 -> 服务器
{
  "start_enhancement": {
    "document_id": "uuid",
    "level": 1-4,
    "options": {}
  },
  
  "accept_change": {
    "change_id": "uuid",
    "modified_text": "string"
  },
  
  "reject_change": {
    "change_id": "uuid",
    "reason": "string"
  }
}

// 服务器 -> 客户端
{
  "enhancement_progress": {
    "progress": 0-100,
    "current_section": "string",
    "estimated_time": "seconds"
  },
  
  "change_suggestion": {
    "change_id": "uuid",
    "original": "string",
    "suggested": "string",
    "reason": "string",
    "type": "string"
  },
  
  "enhancement_complete": {
    "document_id": "uuid",
    "total_changes": "number",
    "report_url": "string"
  }
}
```

### 6.3 错误处理规范

```python
# 错误响应格式

class ErrorResponse:
    """统一错误响应格式"""
    
    def __init__(self, code: str, message: str, details: dict = None):
        self.error = {
            "code": code,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }

# 错误代码定义
ERROR_CODES = {
    # 认证错误 (1xxx)
    "1001": "Invalid credentials",
    "1002": "Token expired",
    "1003": "Insufficient permissions",
    
    # 验证错误 (2xxx)
    "2001": "Invalid input format",
    "2002": "Missing required field",
    "2003": "Text too long",
    
    # 业务错误 (3xxx)
    "3001": "Document not found",
    "3002": "Enhancement failed",
    "3003": "Quota exceeded",
    
    # 外部服务错误 (4xxx)
    "4001": "JANE API unavailable",
    "4002": "LLM service error",
    "4003": "Database connection error",
    
    # 系统错误 (5xxx)
    "5001": "Internal server error",
    "5002": "Service temporarily unavailable",
    "5003": "Rate limit exceeded"
}
```

---

## 7. 前端界面设计

### 7.1 主要页面结构

```typescript
// 页面路由结构

const routes = {
  '/': HomePage,
  '/login': LoginPage,
  '/register': RegisterPage,
  '/dashboard': DashboardPage,
  '/editor': EditorPage,
  '/editor/:documentId': DocumentEditorPage,
  '/analysis/:documentId': AnalysisPage,
  '/recommendations/:documentId': RecommendationsPage,
  '/history': HistoryPage,
  '/settings': SettingsPage,
  '/help': HelpPage
};
```

### 7.2 核心组件设计

```typescript
// 文本编辑器组件
interface EditorProps {
  initialText: string;
  onTextChange: (text: string) => void;
  enhancements?: Enhancement[];
  showDiff?: boolean;
}

// 对比显示组件
interface DiffViewerProps {
  original: string;
  enhanced: string;
  changes: Change[];
  onAccept: (changeId: string) => void;
  onReject: (changeId: string) => void;
}

// 推荐卡片组件
interface RecommendationCardProps {
  type: 'journal' | 'paper' | 'author';
  data: RecommendationData;
  onSave: (id: string) => void;
  onRate: (id: string, rating: number) => void;
}

// 进度指示器
interface ProgressIndicatorProps {
  current: number;
  total: number;
  stage: string;
  estimatedTime?: number;
}
```

### 7.3 用户界面流程

```mermaid
graph TD
    A[登录/注册] --> B[仪表板]
    B --> C[新建文档]
    B --> D[打开历史文档]
    C --> E[输入/粘贴文本]
    D --> E
    E --> F[选择改写级别]
    F --> G[文本分析]
    G --> H[问题诊断显示]
    H --> I[开始改写]
    I --> J[实时显示改写进度]
    J --> K[对比显示结果]
    K --> L{用户确认}
    L -->|接受| M[JANE推荐]
    L -->|修改| N[手动编辑]
    N --> M
    M --> O[导出结果]
```

### 7.4 核心组件详细实现

#### 7.4.1 主编辑器组件

```tsx
// src/components/Editor/MainEditor.tsx

import React, { useState, useCallback, useEffect } from 'react';
import { Card, Button, Select, Space, Divider, Spin, message } from 'antd';
import {
  FileTextOutlined,
  ThunderboltOutlined,
  CheckCircleOutlined,
  DownloadOutlined
} from '@ant-design/icons';
import MonacoEditor from '@monaco-editor/react';
import DiffViewer from './DiffViewer';
import AnalysisPanel from './AnalysisPanel';
import RecommendationPanel from './RecommendationPanel';
import EnhancementProgress from './EnhancementProgress';
import { useEnhancement } from '@/hooks/useEnhancement';
import { useAnalysis } from '@/hooks/useAnalysis';

interface MainEditorProps {
  initialText?: string;
  discipline?: string;
}

const MainEditor: React.FC<MainEditorProps> = ({
  initialText = '',
  discipline = 'general'
}) => {
  // State management
  const [text, setText] = useState(initialText);
  const [enhancedText, setEnhancedText] = useState('');
  const [selectedLevel, setSelectedLevel] = useState(2);
  const [viewMode, setViewMode] = useState<'edit' | 'compare' | 'analysis'>('edit');
  const [isProcessing, setIsProcessing] = useState(false);

  // Custom hooks
  const { enhance, progress, changes } = useEnhancement();
  const { analyze, analysisResult } = useAnalysis();

  // Handle text analysis
  const handleAnalyze = useCallback(async () => {
    if (!text.trim()) {
      message.warning('请输入文本');
      return;
    }

    setIsProcessing(true);
    setViewMode('analysis');

    try {
      await analyze(text, discipline);
      message.success('分析完成');
    } catch (error) {
      message.error('分析失败：' + error.message);
    } finally {
      setIsProcessing(false);
    }
  }, [text, discipline, analyze]);

  // Handle text enhancement
  const handleEnhance = useCallback(async () => {
    if (!text.trim()) {
      message.warning('请输入文本');
      return;
    }

    setIsProcessing(true);

    try {
      const result = await enhance(text, selectedLevel, discipline);
      setEnhancedText(result.enhanced_text);
      setViewMode('compare');
      message.success('改写完成');
    } catch (error) {
      message.error('改写失败：' + error.message);
    } finally {
      setIsProcessing(false);
    }
  }, [text, selectedLevel, discipline, enhance]);

  // Handle export
  const handleExport = useCallback(() => {
    const exportText = enhancedText || text;
    const blob = new Blob([exportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `enhanced_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }, [text, enhancedText]);

  return (
    <div className="main-editor-container">
      {/* Toolbar */}
      <Card className="toolbar-card">
        <Space split={<Divider type="vertical" />}>
          {/* Enhancement Level Selector */}
          <Space>
            <span>改写级别：</span>
            <Select
              value={selectedLevel}
              onChange={setSelectedLevel}
              style={{ width: 200 }}
              disabled={isProcessing}
            >
              <Select.Option value={1}>Level 1 - 基础纠错</Select.Option>
              <Select.Option value={2}>Level 2 - Native表达</Select.Option>
              <Select.Option value={3}>Level 3 - 学术规范</Select.Option>
              <Select.Option value={4}>Level 4 - 整体润色</Select.Option>
            </Select>
          </Space>

          {/* Action Buttons */}
          <Space>
            <Button
              type="default"
              icon={<FileTextOutlined />}
              onClick={handleAnalyze}
              loading={isProcessing && viewMode === 'analysis'}
            >
              文本分析
            </Button>
            <Button
              type="primary"
              icon={<ThunderboltOutlined />}
              onClick={handleEnhance}
              loading={isProcessing && viewMode !== 'analysis'}
            >
              开始改写
            </Button>
            {enhancedText && (
              <Button
                icon={<DownloadOutlined />}
                onClick={handleExport}
              >
                导出结果
              </Button>
            )}
          </Space>

          {/* View Mode Toggle */}
          <Space>
            <Button
              type={viewMode === 'edit' ? 'primary' : 'default'}
              onClick={() => setViewMode('edit')}
            >
              编辑
            </Button>
            <Button
              type={viewMode === 'compare' ? 'primary' : 'default'}
              onClick={() => setViewMode('compare')}
              disabled={!enhancedText}
            >
              对比
            </Button>
            <Button
              type={viewMode === 'analysis' ? 'primary' : 'default'}
              onClick={() => setViewMode('analysis')}
              disabled={!analysisResult}
            >
              分析
            </Button>
          </Space>
        </Space>
      </Card>

      {/* Progress Indicator */}
      {isProcessing && progress && (
        <EnhancementProgress progress={progress} />
      )}

      {/* Main Content Area */}
      <div className="content-area">
        {viewMode === 'edit' && (
          <Card title="文本编辑器" className="editor-card">
            <MonacoEditor
              height="60vh"
              language="plaintext"
              value={text}
              onChange={(value) => setText(value || '')}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                wordWrap: 'on',
                automaticLayout: true
              }}
            />
            <div className="editor-stats">
              <Space>
                <span>字数：{text.split(/\s+/).filter(w => w).length}</span>
                <span>字符数：{text.length}</span>
              </Space>
            </div>
          </Card>
        )}

        {viewMode === 'compare' && enhancedText && (
          <DiffViewer
            original={text}
            enhanced={enhancedText}
            changes={changes}
            onAcceptChange={(changeId) => {
              // Handle change acceptance
              console.log('Accepted change:', changeId);
            }}
            onRejectChange={(changeId) => {
              // Handle change rejection
              console.log('Rejected change:', changeId);
            }}
          />
        )}

        {viewMode === 'analysis' && analysisResult && (
          <AnalysisPanel result={analysisResult} />
        )}
      </div>

      {/* Recommendations Panel (shown after enhancement) */}
      {enhancedText && (
        <RecommendationPanel text={enhancedText} discipline={discipline} />
      )}
    </div>
  );
};

export default MainEditor;
```

#### 7.4.2 对比显示组件

```tsx
// src/components/Editor/DiffViewer.tsx

import React, { useMemo } from 'react';
import { Card, Row, Col, Tag, Tooltip, Space, Button } from 'antd';
import {
  CheckOutlined,
  CloseOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';
import { diffWords, diffSentences } from 'diff';
import './DiffViewer.css';

interface Change {
  id: string;
  type: string;
  original: string;
  suggested: string;
  reason: string;
  severity: number;
  position: { start: number; end: number };
}

interface DiffViewerProps {
  original: string;
  enhanced: string;
  changes?: Change[];
  onAcceptChange?: (changeId: string) => void;
  onRejectChange?: (changeId: string) => void;
}

const DiffViewer: React.FC<DiffViewerProps> = ({
  original,
  enhanced,
  changes = [],
  onAcceptChange,
  onRejectChange
}) => {
  // Calculate word-level diff
  const wordDiff = useMemo(() => {
    return diffWords(original, enhanced);
  }, [original, enhanced]);

  // Calculate sentence-level diff
  const sentenceDiff = useMemo(() => {
    return diffSentences(original, enhanced);
  }, [original, enhanced]);

  // Render word diff with highlighting
  const renderWordDiff = () => {
    return (
      <div className="diff-content">
        {wordDiff.map((part, index) => {
          const className = part.added
            ? 'diff-added'
            : part.removed
            ? 'diff-removed'
            : 'diff-unchanged';

          return (
            <span key={index} className={className}>
              {part.value}
            </span>
          );
        })}
      </div>
    );
  };

  // Get severity color
  const getSeverityColor = (severity: number) => {
    if (severity >= 4) return 'red';
    if (severity >= 3) return 'orange';
    if (severity >= 2) return 'blue';
    return 'green';
  };

  // Get change type label
  const getChangeTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'grammar': '语法',
      'vocabulary': '词汇',
      'collocation': '搭配',
      'style': '风格',
      'structure': '结构',
      'academic': '学术规范'
    };
    return labels[type] || type;
  };

  return (
    <div className="diff-viewer-container">
      {/* Side-by-side comparison */}
      <Row gutter={16}>
        <Col span={12}>
          <Card
            title="原始文本"
            className="original-card"
            size="small"
          >
            <div className="text-display original-text">
              {original}
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card
            title="改写后文本"
            className="enhanced-card"
            size="small"
          >
            <div className="text-display enhanced-text">
              {enhanced}
            </div>
          </Card>
        </Col>
      </Row>

      {/* Unified diff view */}
      <Card
        title="详细对比"
        className="unified-diff-card"
        style={{ marginTop: 16 }}
      >
        {renderWordDiff()}
      </Card>

      {/* Changes list */}
      {changes.length > 0 && (
        <Card
          title={`修改详情（${changes.length}处）`}
          className="changes-card"
          style={{ marginTop: 16 }}
        >
          <Space direction="vertical" style={{ width: '100%' }} size="middle">
            {changes.map((change) => (
              <Card
                key={change.id}
                size="small"
                className="change-item"
                extra={
                  <Space>
                    <Tag color={getSeverityColor(change.severity)}>
                      {getChangeTypeLabel(change.type)}
                    </Tag>
                    {onAcceptChange && (
                      <Button
                        type="text"
                        size="small"
                        icon={<CheckOutlined />}
                        onClick={() => onAcceptChange(change.id)}
                      >
                        接受
                      </Button>
                    )}
                    {onRejectChange && (
                      <Button
                        type="text"
                        size="small"
                        danger
                        icon={<CloseOutlined />}
                        onClick={() => onRejectChange(change.id)}
                      >
                        拒绝
                      </Button>
                    )}
                  </Space>
                }
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  <div>
                    <span className="change-label">原文：</span>
                    <span className="change-original">{change.original}</span>
                  </div>
                  <div>
                    <span className="change-label">修改为：</span>
                    <span className="change-suggested">{change.suggested}</span>
                  </div>
                  <div>
                    <Tooltip title="修改原因">
                      <InfoCircleOutlined style={{ marginRight: 8 }} />
                    </Tooltip>
                    <span className="change-reason">{change.reason}</span>
                  </div>
                </Space>
              </Card>
            ))}
          </Space>
        </Card>
      )}
    </div>
  );
};

export default DiffViewer;
```

#### 7.4.3 文本分析面板

```tsx
// src/components/Editor/AnalysisPanel.tsx

import React from 'react';
import { Card, Row, Col, Progress, List, Tag, Statistic, Space } from 'antd';
import {
  CheckCircleOutlined,
  WarningOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface Issue {
  type: string;
  severity: number;
  description: string;
  suggestion: string;
  location?: { start: number; end: number };
}

interface AnalysisResult {
  overall_score: number;
  lexical: {
    diversity_score: number;
    issues: Issue[];
  };
  syntactic: {
    complexity: number;
    variety_score: number;
    issues: Issue[];
  };
  discourse: {
    coherence_score: number;
    issues: Issue[];
  };
  statistics: {
    word_count: number;
    sentence_count: number;
    avg_sentence_length: number;
    unique_words: number;
  };
}

interface AnalysisPanelProps {
  result: AnalysisResult;
}

const AnalysisPanel: React.FC<AnalysisPanelProps> = ({ result }) => {
  // Get severity icon
  const getSeverityIcon = (severity: number) => {
    if (severity >= 4) return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
    if (severity >= 3) return <WarningOutlined style={{ color: '#faad14' }} />;
    return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
  };

  // Get score color
  const getScoreColor = (score: number) => {
    if (score >= 80) return '#52c41a';
    if (score >= 60) return '#faad14';
    return '#ff4d4f';
  };

  // Prepare chart data
  const scoreData = {
    labels: ['词汇', '句法', '语篇'],
    datasets: [{
      label: '得分',
      data: [
        result.lexical.diversity_score * 100,
        result.syntactic.variety_score * 100,
        result.discourse.coherence_score * 100
      ],
      backgroundColor: [
        'rgba(255, 99, 132, 0.5)',
        'rgba(54, 162, 235, 0.5)',
        'rgba(255, 206, 86, 0.5)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
      ],
      borderWidth: 1,
    }]
  };

  // Collect all issues
  const allIssues = [
    ...result.lexical.issues,
    ...result.syntactic.issues,
    ...result.discourse.issues
  ].sort((a, b) => b.severity - a.severity);

  return (
    <div className="analysis-panel-container">
      {/* Overall Score */}
      <Row gutter={16}>
        <Col span={6}>
          <Card>
            <Statistic
              title="综合得分"
              value={result.overall_score}
              suffix="/ 100"
              valueStyle={{ color: getScoreColor(result.overall_score) }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="词汇多样性"
              value={(result.lexical.diversity_score * 100).toFixed(1)}
              suffix="/ 100"
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="句法复杂度"
              value={(result.syntactic.complexity * 100).toFixed(1)}
              suffix="/ 100"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="语篇连贯性"
              value={(result.discourse.coherence_score * 100).toFixed(1)}
              suffix="/ 100"
            />
          </Card>
        </Col>
      </Row>

      {/* Statistics */}
      <Card title="文本统计" style={{ marginTop: 16 }}>
        <Row gutter={16}>
          <Col span={6}>
            <Statistic title="总字数" value={result.statistics.word_count} />
          </Col>
          <Col span={6}>
            <Statistic title="句子数" value={result.statistics.sentence_count} />
          </Col>
          <Col span={6}>
            <Statistic
              title="平均句长"
              value={result.statistics.avg_sentence_length.toFixed(1)}
              suffix="词"
            />
          </Col>
          <Col span={6}>
            <Statistic title="独特词汇" value={result.statistics.unique_words} />
          </Col>
        </Row>
      </Card>

      {/* Score Visualization */}
      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={12}>
          <Card title="分项得分">
            <Bar
              data={scoreData}
              options={{
                responsive: true,
                plugins: {
                  legend: { display: false },
                  title: { display: false }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    max: 100
                  }
                }
              }}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="问题分布">
            <Doughnut
              data={{
                labels: ['严重', '中等', '轻微'],
                datasets: [{
                  data: [
                    allIssues.filter(i => i.severity >= 4).length,
                    allIssues.filter(i => i.severity === 3).length,
                    allIssues.filter(i => i.severity < 3).length,
                  ],
                  backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                  ],
                }]
              }}
            />
          </Card>
        </Col>
      </Row>

      {/* Issues List */}
      <Card
        title={`发现的问题（${allIssues.length}个）`}
        style={{ marginTop: 16 }}
      >
        <List
          dataSource={allIssues}
          renderItem={(issue) => (
            <List.Item>
              <List.Item.Meta
                avatar={getSeverityIcon(issue.severity)}
                title={
                  <Space>
                    <Tag color={issue.severity >= 4 ? 'red' : issue.severity >= 3 ? 'orange' : 'blue'}>
                      {issue.type}
                    </Tag>
                    <span>{issue.description}</span>
                  </Space>
                }
                description={
                  <div>
                    <strong>建议：</strong>{issue.suggestion}
                  </div>
                }
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
};

export default AnalysisPanel;
```

#### 7.4.4 进度指示器组件

```tsx
// src/components/Editor/EnhancementProgress.tsx

import React, { useEffect, useState } from 'react';
import { Card, Progress, Steps, Space, Tag } from 'antd';
import {
  LoadingOutlined,
  CheckCircleOutlined,
  SyncOutlined
} from '@ant-design/icons';

interface ProgressData {
  percentage: number;
  current_stage: string;
  total_stages: number;
  completed_stages: number;
  estimated_time: number;
  message?: string;
}

interface EnhancementProgressProps {
  progress: ProgressData;
}

const EnhancementProgress: React.FC<EnhancementProgressProps> = ({ progress }) => {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setElapsed(prev => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const stages = [
    { title: '文本预处理', key: 'preprocessing' },
    { title: '问题诊断', key: 'diagnosis' },
    { title: 'Level 1 纠错', key: 'level1' },
    { title: 'Level 2 优化', key: 'level2' },
    { title: 'Level 3 规范', key: 'level3' },
    { title: 'Level 4 润色', key: 'level4' },
    { title: '生成报告', key: 'report' },
  ];

  const getCurrentStageIndex = () => {
    return stages.findIndex(s =>
      progress.current_stage.toLowerCase().includes(s.key)
    );
  };

  return (
    <Card className="progress-card" style={{ marginTop: 16, marginBottom: 16 }}>
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        {/* Progress Bar */}
        <div>
          <div style={{ marginBottom: 8 }}>
            <Space>
              <SyncOutlined spin />
              <span>{progress.message || progress.current_stage}</span>
              <Tag color="processing">
                已用时：{formatTime(elapsed)}
              </Tag>
              <Tag color="blue">
                预计剩余：{formatTime(progress.estimated_time)}
              </Tag>
            </Space>
          </div>
          <Progress
            percent={Math.round(progress.percentage)}
            status="active"
            strokeColor={{
              '0%': '#108ee9',
              '100%': '#87d068',
            }}
          />
        </div>

        {/* Stages */}
        <Steps
          current={getCurrentStageIndex()}
          size="small"
          items={stages.map((stage, index) => ({
            title: stage.title,
            icon: index < getCurrentStageIndex()
              ? <CheckCircleOutlined />
              : index === getCurrentStageIndex()
              ? <LoadingOutlined />
              : undefined
          }))}
        />
      </Space>
    </Card>
  );
};

export default EnhancementProgress;
```

#### 7.4.5 推荐面板组件

```tsx
// src/components/Editor/RecommendationPanel.tsx

import React, { useState, useEffect } from 'react';
import { Card, Tabs, List, Tag, Rate, Button, Space, Tooltip, Spin } from 'antd';
import {
  BookOutlined,
  TeamOutlined,
  ReadOutlined,
  LinkOutlined,
  StarOutlined
} from '@ant-design/icons';
import { useRecommendations } from '@/hooks/useRecommendations';

interface Journal {
  title: string;
  similarity_score: number;
  impact_factor?: number;
  open_access: boolean;
  publisher: string;
  url: string;
  confidence: string;
}

interface Paper {
  title: string;
  authors: string[];
  year: number;
  journal: string;
  doi: string;
  similarity_score: number;
  citations: number;
  url: string;
}

interface Author {
  name: string;
  affiliation: string;
  h_index?: number;
  total_publications: number;
  similarity_score: number;
}

interface RecommendationPanelProps {
  text: string;
  discipline: string;
}

const RecommendationPanel: React.FC<RecommendationPanelProps> = ({
  text,
  discipline
}) => {
  const [activeTab, setActiveTab] = useState('journals');
  const {
    journals,
    papers,
    authors,
    loading,
    fetchRecommendations
  } = useRecommendations();

  useEffect(() => {
    fetchRecommendations(text);
  }, [text]);

  // Render journal card
  const renderJournalCard = (journal: Journal) => (
    <List.Item
      actions={[
        <Button
          type="link"
          icon={<LinkOutlined />}
          href={journal.url}
          target="_blank"
        >
          访问
        </Button>,
        <Button
          type="text"
          icon={<StarOutlined />}
        >
          收藏
        </Button>
      ]}
    >
      <List.Item.Meta
        avatar={<BookOutlined style={{ fontSize: 24, color: '#1890ff' }} />}
        title={
          <Space>
            <span>{journal.title}</span>
            {journal.open_access && (
              <Tag color="green">开放获取</Tag>
            )}
            <Tag color={
              journal.confidence === 'Very High' ? 'red' :
              journal.confidence === 'High' ? 'orange' :
              journal.confidence === 'Medium' ? 'blue' : 'default'
            }>
              {journal.confidence}
            </Tag>
          </Space>
        }
        description={
          <Space direction="vertical" size="small">
            <div>
              <strong>出版商：</strong>{journal.publisher}
            </div>
            {journal.impact_factor && (
              <div>
                <strong>影响因子：</strong>
                <Tag color="blue">{journal.impact_factor.toFixed(2)}</Tag>
              </div>
            )}
            <div>
              <strong>匹配度：</strong>
              <Progress
                percent={Math.round(journal.similarity_score * 100)}
                size="small"
                style={{ width: 200 }}
              />
            </div>
          </Space>
        }
      />
    </List.Item>
  );

  // Render paper card
  const renderPaperCard = (paper: Paper) => (
    <List.Item
      actions={[
        <Button
          type="link"
          icon={<LinkOutlined />}
          href={paper.url || `https://doi.org/${paper.doi}`}
          target="_blank"
        >
          查看
        </Button>
      ]}
    >
      <List.Item.Meta
        avatar={<ReadOutlined style={{ fontSize: 24, color: '#52c41a' }} />}
        title={paper.title}
        description={
          <Space direction="vertical" size="small">
            <div>
              <strong>作者：</strong>{paper.authors.join(', ')}
            </div>
            <div>
              <strong>期刊：</strong>{paper.journal} ({paper.year})
            </div>
            <Space>
              <Tag color="blue">被引：{paper.citations}</Tag>
              <Tag color="green">
                相关性：{(paper.similarity_score * 100).toFixed(0)}%
              </Tag>
            </Space>
            {paper.doi && (
              <div>
                <strong>DOI：</strong>
                <code>{paper.doi}</code>
              </div>
            )}
          </Space>
        }
      />
    </List.Item>
  );

  // Render author card
  const renderAuthorCard = (author: Author) => (
    <List.Item>
      <List.Item.Meta
        avatar={<TeamOutlined style={{ fontSize: 24, color: '#722ed1' }} />}
        title={author.name}
        description={
          <Space direction="vertical" size="small">
            <div>
              <strong>机构：</strong>{author.affiliation}
            </div>
            <Space>
              {author.h_index && (
                <Tag color="purple">H-index: {author.h_index}</Tag>
              )}
              <Tag color="cyan">发表数：{author.total_publications}</Tag>
              <Tag color="green">
                匹配度：{(author.similarity_score * 100).toFixed(0)}%
              </Tag>
            </Space>
          </Space>
        }
      />
    </List.Item>
  );

  return (
    <Card
      title="文献推荐"
      className="recommendation-panel"
      style={{ marginTop: 16 }}
    >
      <Spin spinning={loading}>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={[
            {
              key: 'journals',
              label: (
                <span>
                  <BookOutlined />
                  推荐期刊 ({journals.length})
                </span>
              ),
              children: (
                <List
                  dataSource={journals}
                  renderItem={renderJournalCard}
                  locale={{ emptyText: '暂无推荐期刊' }}
                />
              )
            },
            {
              key: 'papers',
              label: (
                <span>
                  <ReadOutlined />
                  相关文献 ({papers.length})
                </span>
              ),
              children: (
                <List
                  dataSource={papers}
                  renderItem={renderPaperCard}
                  locale={{ emptyText: '暂无相关文献' }}
                />
              )
            },
            {
              key: 'authors',
              label: (
                <span>
                  <TeamOutlined />
                  相关作者 ({authors.length})
                </span>
              ),
              children: (
                <List
                  dataSource={authors}
                  renderItem={renderAuthorCard}
                  locale={{ emptyText: '暂无相关作者' }}
                />
              )
            }
          ]}
        />
      </Spin>
    </Card>
  );
};

export default RecommendationPanel;
```

### 7.5 自定义Hooks实现

```typescript
// src/hooks/useEnhancement.ts

import { useState, useCallback } from 'react';
import axios from 'axios';

interface ProgressData {
  percentage: number;
  current_stage: string;
  total_stages: number;
  completed_stages: number;
  estimated_time: number;
  message?: string;
}

interface Change {
  id: string;
  type: string;
  original: string;
  suggested: string;
  reason: string;
  severity: number;
}

interface EnhancementResult {
  enhanced_text: string;
  changes: Change[];
  report: any;
}

export const useEnhancement = () => {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [changes, setChanges] = useState<Change[]>([]);
  const [loading, setLoading] = useState(false);

  const enhance = useCallback(async (
    text: string,
    level: number,
    discipline: string
  ): Promise<EnhancementResult> => {
    setLoading(true);
    setProgress(null);
    setChanges([]);

    try {
      // Create enhancement job
      const response = await axios.post('/api/enhance', {
        text,
        level,
        discipline
      });

      const jobId = response.data.job_id;

      // Poll for progress
      return await pollEnhancementStatus(jobId);
    } catch (error) {
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const pollEnhancementStatus = async (jobId: string): Promise<EnhancementResult> => {
    return new Promise((resolve, reject) => {
      const interval = setInterval(async () => {
        try {
          const response = await axios.get(`/api/enhance/status/${jobId}`);
          const { status, progress: progressData, result } = response.data;

          if (progressData) {
            setProgress(progressData);
          }

          if (status === 'completed') {
            clearInterval(interval);
            setChanges(result.changes || []);
            resolve(result);
          } else if (status === 'failed') {
            clearInterval(interval);
            reject(new Error('Enhancement failed'));
          }
        } catch (error) {
          clearInterval(interval);
          reject(error);
        }
      }, 1000);
    });
  };

  return {
    enhance,
    progress,
    changes,
    loading
  };
};
```

```typescript
// src/hooks/useAnalysis.ts

import { useState, useCallback } from 'react';
import axios from 'axios';

export const useAnalysis = () => {
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyze = useCallback(async (text: string, discipline: string) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/analyze', {
        text,
        discipline,
        analysis_types: ['lexical', 'syntactic', 'discourse']
      });
      setAnalysisResult(response.data);
      return response.data;
    } catch (error) {
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    analyze,
    analysisResult,
    loading
  };
};
```

```typescript
// src/hooks/useRecommendations.ts

import { useState, useCallback } from 'react';
import axios from 'axios';

export const useRecommendations = () => {
  const [journals, setJournals] = useState<any[]>([]);
  const [papers, setPapers] = useState<any[]>([]);
  const [authors, setAuthors] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = useCallback(async (text: string) => {
    setLoading(true);
    try {
      // Fetch all recommendations in parallel
      const [journalsRes, papersRes, authorsRes] = await Promise.all([
        axios.post('/api/recommendations/journals', { text }),
        axios.post('/api/recommendations/papers', { text }),
        axios.post('/api/recommendations/authors', { text })
      ]);

      setJournals(journalsRes.data.journals || []);
      setPapers(papersRes.data.papers || []);
      setAuthors(authorsRes.data.authors || []);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    journals,
    papers,
    authors,
    loading,
    fetchRecommendations
  };
};
```

### 7.6 样式文件

```css
/* src/components/Editor/DiffViewer.css */

.diff-viewer-container {
  padding: 16px;
}

.text-display {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-wrap;
  word-wrap: break-word;
  padding: 16px;
  border-radius: 4px;
  max-height: 500px;
  overflow-y: auto;
}

.original-text {
  background-color: #fff7e6;
}

.enhanced-text {
  background-color: #f0f9ff;
}

.diff-content {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 2;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.diff-added {
  background-color: #d4f4dd;
  color: #0c5f20;
  padding: 2px 4px;
  border-radius: 2px;
}

.diff-removed {
  background-color: #ffe7e7;
  color: #d01f1f;
  padding: 2px 4px;
  text-decoration: line-through;
  border-radius: 2px;
}

.diff-unchanged {
  color: #333;
}

.change-item {
  transition: all 0.3s;
}

.change-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.change-label {
  font-weight: 600;
  color: #666;
  margin-right: 8px;
}

.change-original {
  color: #d01f1f;
  background-color: #ffe7e7;
  padding: 2px 6px;
  border-radius: 3px;
}

.change-suggested {
  color: #0c5f20;
  background-color: #d4f4dd;
  padding: 2px 6px;
  border-radius: 3px;
}

.change-reason {
  color: #555;
  font-style: italic;
}
```

---

## 8. 部署与运维

### 8.1 生产环境部署

```yaml
# kubernetes deployment

apiVersion: apps/v1
kind: Deployment
metadata:
  name: awies-enhancement-service
  labels:
    app: enhancement-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: enhancement-service
  template:
    metadata:
      labels:
        app: enhancement-service
    spec:
      containers:
      - name: enhancement-service
        image: awies/enhancement-service:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: awies-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: awies-secrets
              key: redis-url
        - name: CLAUDE_API_KEY
          valueFrom:
            secretKeyRef:
              name: awies-secrets
              key: claude-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### 8.2 监控配置

```yaml
# Prometheus配置

global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'awies-services'
    static_configs:
      - targets:
        - 'text-analysis:8001'
        - 'enhancement-service:8002'
        - 'jane-integration:8003'
        
  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']
      
  - job_name: 'redis-exporter'
    static_configs:
      - targets: ['redis-exporter:9121']

# 告警规则
rule_files:
  - "alerts.yml"

alerting:
  alertmanagers:
    - static_configs:
      - targets: ['alertmanager:9093']
```

### 8.3 备份策略

```bash
#!/bin/bash
# backup.sh - 自动备份脚本

# 数据库备份
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME | \
  gzip > /backups/db_$(date +%Y%m%d_%H%M%S).sql.gz

# Redis备份
redis-cli --rdb /backups/redis_$(date +%Y%m%d_%H%M%S).rdb

# 上传到S3
aws s3 sync /backups s3://awies-backups/$(date +%Y%m%d)/

# 清理旧备份（保留30天）
find /backups -type f -mtime +30 -delete
```

### 8.4 性能优化

```python
# 性能优化配置

class PerformanceConfig:
    """性能优化配置"""
    
    # 缓存策略
    CACHE_TTL = {
        'pattern_cache': 3600 * 24,  # 24小时
        'jane_recommendations': 3600 * 6,  # 6小时
        'user_preferences': 3600,  # 1小时
        'document_cache': 1800  # 30分钟
    }
    
    # 并发限制
    CONCURRENCY_LIMITS = {
        'llm_calls': 10,  # LLM并发调用
        'jane_api': 5,  # JANE API并发
        'document_processing': 20  # 文档处理并发
    }
    
    # 批处理配置
    BATCH_SIZES = {
        'text_segments': 10,  # 文本分段批处理
        'pattern_matching': 100,  # 模式匹配批处理
        'database_inserts': 500  # 数据库插入批处理
    }
    
    # 速率限制
    RATE_LIMITS = {
        'free_tier': {
            'daily_words': 5000,
            'api_calls': 100
        },
        'pro_tier': {
            'daily_words': 50000,
            'api_calls': 1000
        },
        'enterprise': {
            'daily_words': -1,  # 无限制
            'api_calls': -1
        }
    }
```

---

## 9. 测试策略

### 9.1 单元测试

```python
# test_enhancement.py

import pytest
from enhancement_engine import EnhancementEngine

class TestEnhancement:
    
    @pytest.fixture
    def engine(self):
        return EnhancementEngine()
    
    def test_basic_corrections(self, engine):
        """测试基础纠错"""
        text = "This is a big problem in the research."
        enhanced = engine.level1_basic_corrections(text)
        assert "big" not in enhanced
        assert "large" in enhanced or "significant" in enhanced
    
    def test_collocation_fixes(self, engine):
        """测试搭配修正"""
        text = "We need to make a research on this topic."
        enhanced = engine.fix_collocations(text)
        assert "conduct research" in enhanced
        
    def test_hedging_application(self, engine):
        """测试模糊限制语"""
        text = "This proves that the hypothesis is correct."
        enhanced = engine.apply_hedging(text, level='high')
        assert any(word in enhanced for word in ['suggests', 'indicates', 'may'])
    
    @pytest.mark.parametrize("discipline,expected_voice", [
        ("computer_science", "mixed"),
        ("biology", "passive"),
        ("humanities", "active")
    ])
    def test_discipline_specific(self, engine, discipline, expected_voice):
        """测试学科特定规则"""
        text = "We conducted the experiment."
        enhanced = engine.apply_discipline_rules(text, discipline)
        # 验证语态转换
        if expected_voice == "passive":
            assert "was conducted" in enhanced
```

### 9.2 集成测试

```python
# test_integration.py

import asyncio
import pytest
from httpx import AsyncClient
from main import app

class TestAPIIntegration:
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        """测试完整工作流"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 1. 用户注册
            register_response = await client.post("/api/auth/register", json={
                "email": "test@example.com",
                "password": "testpass123",
                "username": "testuser"
            })
            assert register_response.status_code == 201
            
            # 2. 登录
            login_response = await client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "testpass123"
            })
            token = login_response.json()["access_token"]
            
            # 3. 创建文档
            headers = {"Authorization": f"Bearer {token}"}
            doc_response = await client.post("/api/documents", 
                headers=headers,
                json={
                    "title": "Test Paper",
                    "text": "This is a test text with some problems.",
                    "discipline": "computer_science"
                })
            doc_id = doc_response.json()["document_id"]
            
            # 4. 改写文档
            enhance_response = await client.post(f"/api/enhance/{doc_id}",
                headers=headers,
                json={
                    "level": 2,
                    "options": {"preserve_citations": True}
                })
            job_id = enhance_response.json()["job_id"]
            
            # 5. 等待完成
            await asyncio.sleep(2)
            
            # 6. 获取结果
            status_response = await client.get(f"/api/enhance/status/{job_id}",
                headers=headers)
            assert status_response.json()["status"] == "completed"
```

### 9.3 性能测试

```python
# performance_test.py

from locust import HttpUser, task, between

class AWIESUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """登录获取token"""
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "testpass123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def enhance_text(self):
        """测试文本改写"""
        self.client.post("/api/enhance", 
            headers=self.headers,
            json={
                "text": "This is a test text for performance testing.",
                "level": 2,
                "discipline": "general"
            })
    
    @task(2)
    def get_recommendations(self):
        """测试推荐功能"""
        self.client.post("/api/recommendations/journals",
            headers=self.headers,
            json={
                "text": "Machine learning in healthcare applications"
            })
    
    @task(1)
    def analyze_text(self):
        """测试文本分析"""
        self.client.post("/api/analyze",
            headers=self.headers,
            json={
                "text": "Sample text for analysis",
                "analysis_types": ["lexical", "syntactic"]
            })
```

---

## 10. 项目实施计划

### 10.1 开发阶段划分

```mermaid
gantt
    title AWIES项目开发计划
    dateFormat  YYYY-MM-DD
    
    section 第一阶段
    需求分析与设计    :a1, 2024-01-01, 14d
    技术选型与POC     :a2, after a1, 7d
    基础架构搭建      :a3, after a2, 14d
    
    section 第二阶段
    文本分析模块      :b1, after a3, 21d
    基础改写引擎      :b2, after b1, 28d
    数据库设计实现    :b3, after a3, 14d
    
    section 第三阶段
    Native表达优化    :c1, after b2, 21d
    学术规范模块      :c2, after c1, 14d
    JANE API集成      :c3, after c1, 14d
    
    section 第四阶段
    前端开发         :d1, after b1, 35d
    API开发          :d2, after b2, 21d
    集成测试         :d3, after d2, 14d
    
    section 第五阶段
    性能优化         :e1, after d3, 14d
    安全审计         :e2, after e1, 7d
    部署上线         :e3, after e2, 7d
```

### 10.2 里程碑计划

| 阶段 | 里程碑 | 预计完成时间 | 交付物 |
|------|--------|------------|--------|
| Phase 1 | MVP版本 | 2024-03-31 | 基础文本改写功能 |
| Phase 2 | Beta版本 | 2024-05-31 | 完整改写+基础推荐 |
| Phase 3 | RC版本 | 2024-07-31 | 全功能+性能优化 |
| Phase 4 | 正式版 | 2024-09-01 | 生产环境部署 |

### 10.3 团队组成

```yaml
team_structure:
  project_manager: 1
  backend_developers: 3
  frontend_developers: 2
  nlp_engineers: 2
  devops_engineer: 1
  ui_ux_designer: 1
  qa_engineers: 2
  total: 12

responsibilities:
  backend_team:
    - API开发
    - 数据库设计
    - 业务逻辑实现
    
  nlp_team:
    - 文本分析算法
    - 改写引擎优化
    - 模式库维护
    
  frontend_team:
    - 用户界面开发
    - 交互设计实现
    - 性能优化
    
  devops:
    - CI/CD搭建
    - 生产环境部署
    - 监控告警配置
```

### 10.4 风险管理

| 风险类型 | 描述 | 影响 | 缓解措施 |
|---------|------|------|---------|
| 技术风险 | LLM API不稳定 | 高 | 多供应商备份方案 |
| 性能风险 | 大文本处理慢 | 中 | 异步处理+缓存优化 |
| 安全风险 | 用户数据泄露 | 高 | 加密存储+访问控制 |
| 法律风险 | 学术诚信争议 | 中 | 明确使用条款+免责声明 |
| 市场风险 | 竞争产品多 | 中 | 差异化功能+优质服务 |

### 10.5 成功指标

```yaml
kpis:
  technical:
    - 平均响应时间 < 2秒
    - 系统可用性 > 99.9%
    - 改写准确率 > 95%
    
  business:
    - 月活跃用户 > 10,000
    - 付费转化率 > 5%
    - 用户满意度 > 4.5/5
    
  quality:
    - 代码覆盖率 > 80%
    - Bug修复时间 < 24小时
    - 安全漏洞数 = 0
```

---

## 附录

### A. 技术参考资源

- [spaCy Documentation](https://spacy.io/docs)
- [LangChain Documentation](https://docs.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JANE API Documentation](http://jane.biosemantics.org/)
- [Academic Writing Guidelines](https://www.academic-writing.org/)

### B. 学术写作规范参考

- APA Style Guide (7th Edition)
- Chicago Manual of Style
- IEEE Editorial Style Manual
- Nature Style Guide
- Science Magazine Style Guide

### C. 开源协议

本项目建议采用 MIT License，允许商业使用但需保留版权声明。

### D. 联系方式

- 项目官网：www.awies.ai
- 技术支持：support@awies.ai
- 商务合作：business@awies.ai
- GitHub：github.com/awies/awies-system

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2024-01-15 | 初始设计文档 |
| v1.1 | 2024-01-20 | 添加JANE API集成 |
| v1.2 | 2024-01-25 | 完善技术实现细节 |
| v1.3 | 2024-01-30 | 添加测试和部署方案 |

---

**文档编写者**：AWIES技术团队  
**最后更新**：2024-01-30  
**文档状态**：正式版

---

*本文档为AWIES（Academic Writing Intelligence Enhancement System）的完整设计方案，包含系统架构、技术实现、部署运维等所有关键信息。*
