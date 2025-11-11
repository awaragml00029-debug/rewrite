/**
 * EnhancementProgress Component - Shows enhancement progress
 */

import React, { useEffect, useState } from 'react';
import { Card, Progress, Steps, Space, Tag } from 'antd';
import {
  LoadingOutlined,
  CheckCircleOutlined,
  SyncOutlined,
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

const EnhancementProgress: React.FC<EnhancementProgressProps> = ({
  progress,
}) => {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setElapsed((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const stages = [
    { title: 'Pre-processing', key: 'preprocessing' },
    { title: 'Diagnosis', key: 'diagnosis' },
    { title: 'Level 1', key: 'level1' },
    { title: 'Level 2', key: 'level2' },
    { title: 'Level 3', key: 'level3' },
    { title: 'Level 4', key: 'level4' },
    { title: 'Report', key: 'report' },
  ];

  const getCurrentStageIndex = () => {
    const stageName = progress.current_stage.toLowerCase();
    return stages.findIndex((s) => stageName.includes(s.key));
  };

  const currentIndex = getCurrentStageIndex();

  return (
    <Card className="progress-card" style={{ marginTop: 16, marginBottom: 16 }}>
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        {/* Progress Bar */}
        <div>
          <div style={{ marginBottom: 8 }}>
            <Space>
              <SyncOutlined spin />
              <span>{progress.message || progress.current_stage}</span>
              <Tag color="processing">Elapsed: {formatTime(elapsed)}</Tag>
              <Tag color="blue">
                ETA: {formatTime(progress.estimated_time)}
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
          current={currentIndex}
          size="small"
          items={stages.map((stage, index) => ({
            title: stage.title,
            icon:
              index < currentIndex ? (
                <CheckCircleOutlined />
              ) : index === currentIndex ? (
                <LoadingOutlined />
              ) : undefined,
          }))}
        />
      </Space>
    </Card>
  );
};

export default EnhancementProgress;
