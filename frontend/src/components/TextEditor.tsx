/**
 * TextEditor Component - Monaco-based text editor
 */

import React from 'react';
import { Card, Space } from 'antd';
import Editor from '@monaco-editor/react';

interface TextEditorProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const TextEditor: React.FC<TextEditorProps> = ({ value, onChange, disabled = false }) => {
  const handleChange = (newValue: string | undefined) => {
    onChange(newValue || '');
  };

  const wordCount = value.split(/\s+/).filter((w) => w.length > 0).length;
  const charCount = value.length;

  return (
    <Card
      title="Text Editor"
      className="editor-card"
      extra={
        <Space>
          <span>Words: {wordCount}</span>
          <span>|</span>
          <span>Characters: {charCount}</span>
        </Space>
      }
    >
      <Editor
        height="60vh"
        language="plaintext"
        value={value}
        onChange={handleChange}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          wordWrap: 'on',
          automaticLayout: true,
          readOnly: disabled,
          scrollBeyondLastLine: false,
          renderWhitespace: 'selection',
        }}
        theme="vs"
      />
    </Card>
  );
};

export default TextEditor;
