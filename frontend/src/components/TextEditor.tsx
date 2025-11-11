/**
 * TextEditor Component - Monaco-based text editor
 */

import React, { useRef } from 'react';
import { Card, Space, Tag, message } from 'antd';
import Editor from '@monaco-editor/react';
import type { editor } from 'monaco-editor';

interface TextEditorProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const MAX_CHARS = 4000;

const TextEditor: React.FC<TextEditorProps> = ({ value, onChange, disabled = false }) => {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);

  const handleChange = (newValue: string | undefined) => {
    onChange(newValue || '');
  };

  const handleEditorDidMount = (editor: editor.IStandaloneCodeEditor) => {
    editorRef.current = editor;

    // Add custom context menu actions
    editor.addAction({
      id: 'paste-from-clipboard',
      label: 'Paste',
      keybindings: [2089], // Ctrl+V
      contextMenuGroupId: 'clipboard',
      contextMenuOrder: 1,
      run: async (ed) => {
        try {
          const text = await navigator.clipboard.readText();
          const selection = ed.getSelection();
          if (selection) {
            ed.executeEdits('paste', [{
              range: selection,
              text: text,
            }]);
          }
        } catch (err) {
          message.warning('Unable to access clipboard. Please use Ctrl+V or right-click → Paste from browser menu.');
        }
      },
    });

    editor.addAction({
      id: 'google-search-selection',
      label: 'Search on Google',
      contextMenuGroupId: 'navigation',
      contextMenuOrder: 1,
      precondition: 'editorHasSelection',
      run: (ed) => {
        const selection = ed.getSelection();
        if (selection) {
          const selectedText = ed.getModel()?.getValueInRange(selection);
          if (selectedText) {
            const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(selectedText)}`;
            window.open(searchUrl, '_blank', 'noopener,noreferrer');
          }
        }
      },
    });

    editor.addAction({
      id: 'google-scholar-search',
      label: 'Search on Google Scholar',
      contextMenuGroupId: 'navigation',
      contextMenuOrder: 2,
      precondition: 'editorHasSelection',
      run: (ed) => {
        const selection = ed.getSelection();
        if (selection) {
          const selectedText = ed.getModel()?.getValueInRange(selection);
          if (selectedText) {
            const searchUrl = `https://scholar.google.com/scholar?q=${encodeURIComponent(selectedText)}`;
            window.open(searchUrl, '_blank', 'noopener,noreferrer');
          }
        }
      },
    });
  };

  const wordCount = value.split(/\s+/).filter((w) => w.length > 0).length;
  const charCount = value.length;
  const isOverLimit = charCount > MAX_CHARS;
  const percentUsed = (charCount / MAX_CHARS) * 100;

  return (
    <Card
      title="Text Editor"
      className="editor-card"
      extra={
        <Space>
          <span>Words: {wordCount}</span>
          <span>|</span>
          <span style={{ color: isOverLimit ? '#ff4d4f' : charCount > MAX_CHARS * 0.9 ? '#faad14' : 'inherit' }}>
            Characters: {charCount} / {MAX_CHARS}
          </span>
          {isOverLimit && (
            <Tag color="error">Over limit by {charCount - MAX_CHARS} chars</Tag>
          )}
          {!isOverLimit && percentUsed > 90 && (
            <Tag color="warning">{(100 - percentUsed).toFixed(0)}% remaining</Tag>
          )}
        </Space>
      }
    >
      <Editor
        height="60vh"
        language="plaintext"
        value={value}
        onChange={handleChange}
        onMount={handleEditorDidMount}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          wordWrap: 'on',
          automaticLayout: true,
          readOnly: disabled,
          scrollBeyondLastLine: false,
          renderWhitespace: 'selection',
          contextmenu: true,
        }}
        theme="vs"
      />
    </Card>
  );
};

export default TextEditor;
