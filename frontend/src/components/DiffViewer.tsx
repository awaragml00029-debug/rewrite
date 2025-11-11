/**
 * DiffViewer Component - Side-by-side text comparison
 */

import React, { useMemo } from 'react';
import { Card, Row, Col, List, Tag, Space, Button, message } from 'antd';
import { InfoCircleOutlined, CopyOutlined } from '@ant-design/icons';
import { diffWords } from 'diff';
import { Change } from '@/services/api';
import './DiffViewer.css';

interface DiffViewerProps {
  original: string;
  enhanced: string;
  changes?: Change[];
}

const DiffViewer: React.FC<DiffViewerProps> = ({
  original,
  enhanced,
  changes = [],
}) => {
  const wordDiff = useMemo(() => {
    return diffWords(original, enhanced);
  }, [original, enhanced]);

  const handleCopyEnhanced = async () => {
    try {
      // Try modern clipboard API first
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(enhanced);
        message.success('Enhanced text copied to clipboard!');
      } else {
        // Fallback to older method
        const textArea = document.createElement('textarea');
        textArea.value = enhanced;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
          const successful = document.execCommand('copy');
          if (successful) {
            message.success('Enhanced text copied to clipboard!');
          } else {
            throw new Error('execCommand failed');
          }
        } catch (execErr) {
          message.error('Failed to copy text. Please select and copy manually.');
        } finally {
          document.body.removeChild(textArea);
        }
      }
    } catch (err) {
      console.error('Copy failed:', err);
      message.error('Failed to copy text. Please select and copy manually.');
    }
  };

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

  const getSeverityColor = (severity: number) => {
    if (severity >= 4) return 'red';
    if (severity >= 3) return 'orange';
    if (severity >= 2) return 'blue';
    return 'green';
  };

  return (
    <div className="diff-viewer">
      {/* Side-by-side comparison */}
      <Row gutter={16}>
        <Col xs={24} lg={12}>
          <Card title="Original Text" className="original-card" size="small">
            <div className="text-display original-text">{original}</div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card
            title="Enhanced Text"
            className="enhanced-card"
            size="small"
            extra={
              <Button
                type="primary"
                size="small"
                icon={<CopyOutlined />}
                onClick={handleCopyEnhanced}
              >
                Copy
              </Button>
            }
          >
            <div className="text-display enhanced-text">{enhanced}</div>
          </Card>
        </Col>
      </Row>

      {/* Unified diff view */}
      <Card
        title="Detailed Comparison"
        className="unified-diff-card"
        style={{ marginTop: 16 }}
      >
        {renderWordDiff()}
      </Card>

      {/* Changes list */}
      {changes.length > 0 && (
        <Card
          title={`Modifications (${changes.length})`}
          className="changes-card"
          style={{ marginTop: 16 }}
        >
          <List
            dataSource={changes}
            renderItem={(change) => (
              <List.Item>
                <List.Item.Meta
                  avatar={<InfoCircleOutlined style={{ fontSize: 20 }} />}
                  title={
                    <Space>
                      <Tag color={getSeverityColor(change.severity)}>
                        {change.type}
                      </Tag>
                    </Space>
                  }
                  description={
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <div>
                        <span className="change-label">Original:</span>{' '}
                        <span className="change-original">
                          {change.original}
                        </span>
                      </div>
                      <div>
                        <span className="change-label">Modified to:</span>{' '}
                        <span className="change-suggested">
                          {change.suggested}
                        </span>
                      </div>
                      {change.reason && (
                        <div>
                          <span className="change-label">Reason:</span>{' '}
                          <span className="change-reason">{change.reason}</span>
                        </div>
                      )}
                    </Space>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}
    </div>
  );
};

export default DiffViewer;
