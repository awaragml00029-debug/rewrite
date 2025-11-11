/**
 * AnalysisPanel Component - Displays text analysis results
 */

import React from 'react';
import { Card, Row, Col, Statistic, List, Tag, Space, Progress } from 'antd';
import {
  CheckCircleOutlined,
  WarningOutlined,
  CloseCircleOutlined,
} from '@ant-design/icons';
import { AnalysisResult } from '@/services/api';

interface AnalysisPanelProps {
  result: AnalysisResult;
}

const AnalysisPanel: React.FC<AnalysisPanelProps> = ({ result }) => {
  const getSeverityIcon = (severity: number) => {
    if (severity >= 4)
      return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
    if (severity >= 3)
      return <WarningOutlined style={{ color: '#faad14' }} />;
    return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#52c41a';
    if (score >= 60) return '#faad14';
    return '#ff4d4f';
  };

  const allIssues = [
    ...result.lexical.issues,
    ...result.syntactic.issues,
    ...result.discourse.issues,
  ].sort((a, b) => b.severity - a.severity);

  return (
    <div className="analysis-panel">
      {/* Overall Scores */}
      <Row gutter={16}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Overall Score"
              value={result.overall_score}
              suffix="/ 100"
              valueStyle={{ color: getScoreColor(result.overall_score) }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Lexical Diversity"
              value={(result.lexical.diversity_score * 100).toFixed(1)}
              suffix="/ 100"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Syntactic Complexity"
              value={(result.syntactic.complexity * 100).toFixed(1)}
              suffix="/ 100"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic
              title="Discourse Coherence"
              value={(result.discourse.coherence_score * 100).toFixed(1)}
              suffix="/ 100"
            />
          </Card>
        </Col>
      </Row>

      {/* Statistics */}
      <Card title="Text Statistics" style={{ marginTop: 16 }}>
        <Row gutter={16}>
          <Col xs={12} sm={6}>
            <Statistic title="Total Words" value={result.statistics.word_count} />
          </Col>
          <Col xs={12} sm={6}>
            <Statistic
              title="Sentences"
              value={result.statistics.sentence_count}
            />
          </Col>
          <Col xs={12} sm={6}>
            <Statistic
              title="Avg. Sentence Length"
              value={result.statistics.avg_sentence_length.toFixed(1)}
              suffix="words"
            />
          </Col>
          <Col xs={12} sm={6}>
            <Statistic
              title="Unique Words"
              value={result.statistics.unique_words}
            />
          </Col>
        </Row>
      </Card>

      {/* Issues List */}
      {allIssues.length > 0 && (
        <Card
          title={`Detected Issues (${allIssues.length})`}
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
                      <Tag
                        color={
                          issue.severity >= 4
                            ? 'red'
                            : issue.severity >= 3
                            ? 'orange'
                            : 'blue'
                        }
                      >
                        {issue.type}
                      </Tag>
                      <span>{issue.description}</span>
                    </Space>
                  }
                  description={
                    <div>
                      <strong>Suggestion:</strong> {issue.suggestion}
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}

      {/* Score Breakdown */}
      <Card title="Score Breakdown" style={{ marginTop: 16 }}>
        <Space direction="vertical" style={{ width: '100%' }} size="middle">
          <div>
            <div style={{ marginBottom: 4 }}>
              <strong>Lexical Score:</strong>{' '}
              {(result.lexical.diversity_score * 100).toFixed(0)}%
            </div>
            <Progress
              percent={result.lexical.diversity_score * 100}
              status={
                result.lexical.diversity_score >= 0.6 ? 'success' : 'normal'
              }
            />
          </div>
          <div>
            <div style={{ marginBottom: 4 }}>
              <strong>Syntactic Complexity:</strong>{' '}
              {(result.syntactic.complexity * 100).toFixed(0)}%
            </div>
            <Progress
              percent={result.syntactic.complexity * 100}
              status={result.syntactic.complexity >= 0.5 ? 'success' : 'normal'}
            />
          </div>
          <div>
            <div style={{ marginBottom: 4 }}>
              <strong>Discourse Coherence:</strong>{' '}
              {(result.discourse.coherence_score * 100).toFixed(0)}%
            </div>
            <Progress
              percent={result.discourse.coherence_score * 100}
              status={
                result.discourse.coherence_score >= 0.6 ? 'success' : 'normal'
              }
            />
          </div>
        </Space>
      </Card>
    </div>
  );
};

export default AnalysisPanel;
