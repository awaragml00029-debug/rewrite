/**
 * RecommendationPanel Component - JANE API recommendations
 */

import React, { useState, useEffect } from 'react';
import { Card, Tabs, List, Tag, Button, Space, Spin, Empty, Progress } from 'antd';
import {
  BookOutlined,
  TeamOutlined,
  ReadOutlined,
  LinkOutlined,
} from '@ant-design/icons';
import { useRecommendations } from '@/hooks/useRecommendations';

interface RecommendationPanelProps {
  text: string;
  discipline: string;
}

const RecommendationPanel: React.FC<RecommendationPanelProps> = ({
  text,
  discipline,
}) => {
  const [activeTab, setActiveTab] = useState('journals');
  const { journals, papers, authors, loading, fetchRecommendations } =
    useRecommendations();

  useEffect(() => {
    if (text) {
      fetchRecommendations(text, 10);
    }
  }, [text, fetchRecommendations]);

  const renderJournalCard = (journal: any) => (
    <List.Item
      actions={[
        <Button
          type="link"
          icon={<LinkOutlined />}
          href={journal.url}
          target="_blank"
          key="visit"
        >
          Visit
        </Button>,
      ]}
    >
      <List.Item.Meta
        avatar={<BookOutlined style={{ fontSize: 24, color: '#1890ff' }} />}
        title={
          <Space>
            <span>{journal.title}</span>
            {journal.open_access && <Tag color="green">Open Access</Tag>}
            <Tag
              color={
                journal.confidence === 'Very High'
                  ? 'red'
                  : journal.confidence === 'High'
                  ? 'orange'
                  : journal.confidence === 'Medium'
                  ? 'blue'
                  : 'default'
              }
            >
              {journal.confidence}
            </Tag>
          </Space>
        }
        description={
          <Space direction="vertical" size="small" style={{ width: '100%' }}>
            <div>
              <strong>Publisher:</strong> {journal.publisher}
            </div>
            {journal.impact_factor && (
              <div>
                <strong>Impact Factor:</strong>{' '}
                <Tag color="blue">{journal.impact_factor.toFixed(2)}</Tag>
              </div>
            )}
            <div>
              <strong>Match Score:</strong>
              <Progress
                percent={Math.round(journal.similarity_score * 100)}
                size="small"
                style={{ width: 200, marginLeft: 8 }}
              />
            </div>
          </Space>
        }
      />
    </List.Item>
  );

  const renderPaperCard = (paper: any) => (
    <List.Item
      actions={[
        <Button
          type="link"
          icon={<LinkOutlined />}
          href={paper.url || `https://doi.org/${paper.doi}`}
          target="_blank"
          key="view"
        >
          View
        </Button>,
      ]}
    >
      <List.Item.Meta
        avatar={<ReadOutlined style={{ fontSize: 24, color: '#52c41a' }} />}
        title={paper.title}
        description={
          <Space direction="vertical" size="small">
            <div>
              <strong>Authors:</strong> {paper.authors.join(', ')}
            </div>
            <div>
              <strong>Journal:</strong> {paper.journal}{' '}
              {paper.year && `(${paper.year})`}
            </div>
            <Space>
              {paper.citations !== undefined && (
                <Tag color="blue">Citations: {paper.citations}</Tag>
              )}
              <Tag color="green">
                Relevance: {(paper.similarity_score * 100).toFixed(0)}%
              </Tag>
            </Space>
            {paper.doi && (
              <div>
                <strong>DOI:</strong> <code>{paper.doi}</code>
              </div>
            )}
          </Space>
        }
      />
    </List.Item>
  );

  const renderAuthorCard = (author: any) => (
    <List.Item>
      <List.Item.Meta
        avatar={<TeamOutlined style={{ fontSize: 24, color: '#722ed1' }} />}
        title={author.name}
        description={
          <Space direction="vertical" size="small">
            <div>
              <strong>Affiliation:</strong> {author.affiliation}
            </div>
            <Space>
              {author.h_index !== undefined && (
                <Tag color="purple">H-index: {author.h_index}</Tag>
              )}
              <Tag color="cyan">
                Publications: {author.total_publications}
              </Tag>
              <Tag color="green">
                Match: {(author.similarity_score * 100).toFixed(0)}%
              </Tag>
            </Space>
          </Space>
        }
      />
    </List.Item>
  );

  return (
    <Card
      title="Literature Recommendations"
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
                  Journals ({journals.length})
                </span>
              ),
              children: (
                <List
                  dataSource={journals}
                  renderItem={renderJournalCard}
                  locale={{ emptyText: <Empty description="No journal recommendations available" /> }}
                />
              ),
            },
            {
              key: 'papers',
              label: (
                <span>
                  <ReadOutlined />
                  Papers ({papers.length})
                </span>
              ),
              children: (
                <List
                  dataSource={papers}
                  renderItem={renderPaperCard}
                  locale={{ emptyText: <Empty description="No paper recommendations available" /> }}
                />
              ),
            },
            {
              key: 'authors',
              label: (
                <span>
                  <TeamOutlined />
                  Authors ({authors.length})
                </span>
              ),
              children: (
                <List
                  dataSource={authors}
                  renderItem={renderAuthorCard}
                  locale={{ emptyText: <Empty description="No author recommendations available" /> }}
                />
              ),
            },
          ]}
        />
      </Spin>
    </Card>
  );
};

export default RecommendationPanel;
