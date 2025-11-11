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
