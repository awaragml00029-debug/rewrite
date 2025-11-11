/**
 * Main Application Component
 */

import React, { useState } from 'react';
import { Layout, Card, Select, Button, Space, message } from 'antd';
import { ThunderboltOutlined, FileTextOutlined } from '@ant-design/icons';
import TextEditor from './components/TextEditor';
import AnalysisPanel from './components/AnalysisPanel';
import DiffViewer from './components/DiffViewer';
import EnhancementProgress from './components/EnhancementProgress';
import RecommendationPanel from './components/RecommendationPanel';
import { useEnhancement } from './hooks/useEnhancement';
import { useAnalysis } from './hooks/useAnalysis';
import './App.css';

const { Header, Content } = Layout;
const { Option } = Select;

type ViewMode = 'edit' | 'analysis' | 'compare';

const App: React.FC = () => {
  const [text, setText] = useState('');
  const [enhancedText, setEnhancedText] = useState('');
  const [selectedLevel, setSelectedLevel] = useState(2);
  const [discipline, setDiscipline] = useState('general');
  const [viewMode, setViewMode] = useState<ViewMode>('edit');

  const { enhance, progress, changes, loading: enhancing } = useEnhancement();
  const { analyze, analysisResult, loading: analyzing } = useAnalysis();

  const isProcessing = enhancing || analyzing;

  // Handle text analysis
  const handleAnalyze = async () => {
    if (!text.trim()) {
      message.warning('Please enter some text first');
      return;
    }

    try {
      await analyze(text, discipline);
      setViewMode('analysis');
      message.success('Analysis completed!');
    } catch (error: any) {
      message.error(error.message || 'Analysis failed');
    }
  };

  // Handle text enhancement
  const handleEnhance = async () => {
    if (!text.trim()) {
      message.warning('Please enter some text first');
      return;
    }

    try {
      const result = await enhance(text, selectedLevel, discipline);
      setEnhancedText(result.enhanced_text);
      setViewMode('compare');
      message.success('Enhancement completed!');
    } catch (error: any) {
      message.error(error.message || 'Enhancement failed');
    }
  };

  // Handle export
  const handleExport = () => {
    const exportText = enhancedText || text;
    const blob = new Blob([exportText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `awies_export_${Date.now()}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    message.success('Exported successfully!');
  };

  return (
    <Layout className="app-layout">
      <Header className="app-header">
        <div className="header-content">
          <div className="logo">
            <ThunderboltOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
            <span className="logo-text">AWIES</span>
          </div>
          <div className="subtitle">Academic Writing Intelligence Enhancement System</div>
        </div>
      </Header>

      <Content className="app-content">
        <div className="container">
          {/* Control Panel */}
          <Card className="control-panel">
            <Space wrap size="middle">
              {/* Discipline Selector */}
              <div>
                <label>Discipline: </label>
                <Select
                  value={discipline}
                  onChange={setDiscipline}
                  style={{ width: 180 }}
                  disabled={isProcessing}
                >
                  <Option value="general">General</Option>
                  <Option value="computer_science">Computer Science</Option>
                  <Option value="biology">Biology</Option>
                  <Option value="social_sciences">Social Sciences</Option>
                  <Option value="engineering">Engineering</Option>
                </Select>
              </div>

              {/* Enhancement Level */}
              <div>
                <label>Enhancement Level: </label>
                <Select
                  value={selectedLevel}
                  onChange={setSelectedLevel}
                  style={{ width: 220 }}
                  disabled={isProcessing}
                >
                  <Option value={1}>Level 1 - Basic Corrections</Option>
                  <Option value={2}>Level 2 - Native Expression</Option>
                  <Option value={3}>Level 3 - Academic Style</Option>
                  <Option value={4}>Level 4 - Discourse Optimization</Option>
                </Select>
              </div>

              {/* Action Buttons */}
              <Button
                icon={<FileTextOutlined />}
                onClick={handleAnalyze}
                loading={analyzing}
                disabled={enhancing}
              >
                Analyze
              </Button>

              <Button
                type="primary"
                icon={<ThunderboltOutlined />}
                onClick={handleEnhance}
                loading={enhancing}
                disabled={analyzing}
              >
                Enhance
              </Button>

              {enhancedText && (
                <Button onClick={handleExport}>Export</Button>
              )}

              {/* View Mode Toggle */}
              <div className="view-toggle">
                <Button.Group>
                  <Button
                    type={viewMode === 'edit' ? 'primary' : 'default'}
                    onClick={() => setViewMode('edit')}
                  >
                    Edit
                  </Button>
                  <Button
                    type={viewMode === 'analysis' ? 'primary' : 'default'}
                    onClick={() => setViewMode('analysis')}
                    disabled={!analysisResult}
                  >
                    Analysis
                  </Button>
                  <Button
                    type={viewMode === 'compare' ? 'primary' : 'default'}
                    onClick={() => setViewMode('compare')}
                    disabled={!enhancedText}
                  >
                    Compare
                  </Button>
                </Button.Group>
              </div>
            </Space>
          </Card>

          {/* Progress Indicator */}
          {isProcessing && progress && (
            <EnhancementProgress progress={progress} />
          )}

          {/* Main Content Area */}
          <div className="main-content">
            {viewMode === 'edit' && (
              <TextEditor
                value={text}
                onChange={setText}
                disabled={isProcessing}
              />
            )}

            {viewMode === 'analysis' && analysisResult && (
              <AnalysisPanel result={analysisResult} />
            )}

            {viewMode === 'compare' && enhancedText && (
              <DiffViewer
                original={text}
                enhanced={enhancedText}
                changes={changes}
              />
            )}
          </div>

          {/* Recommendations Panel */}
          {enhancedText && (
            <RecommendationPanel text={enhancedText} discipline={discipline} />
          )}
        </div>
      </Content>
    </Layout>
  );
};

export default App;
