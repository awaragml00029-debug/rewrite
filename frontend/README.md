# AWIES Frontend

React-based frontend for the Academic Writing Intelligence Enhancement System.

## Features

- 📝 **Monaco Editor** - Professional text editing experience
- 🔍 **Real-time Analysis** - Instant feedback on writing quality
- ✨ **4-Level Enhancement** - Progressive text improvement
- 📊 **Visual Analytics** - Charts and statistics
- 🔄 **Side-by-side Comparison** - See changes in real-time
- 📚 **JANE Integration** - Journal, paper, and author recommendations
- 📱 **Responsive Design** - Works on all devices

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will open at http://localhost:3000

### 3. Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── TextEditor.tsx
│   │   ├── AnalysisPanel.tsx
│   │   ├── DiffViewer.tsx
│   │   ├── EnhancementProgress.tsx
│   │   └── RecommendationPanel.tsx
│   ├── hooks/               # Custom hooks
│   │   ├── useEnhancement.ts
│   │   ├── useAnalysis.ts
│   │   └── useRecommendations.ts
│   ├── services/            # API services
│   │   └── api.ts
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── App.css              # Global styles
├── index.html
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## Usage

### 1. Enter Text

Type or paste your academic text into the editor.

### 2. Select Options

- Choose your **discipline** (Computer Science, Biology, etc.)
- Select **enhancement level** (1-4)

### 3. Analyze

Click **Analyze** to get instant feedback on:
- Lexical quality
- Syntactic complexity
- Discourse coherence
- Detailed suggestions

### 4. Enhance

Click **Enhance** to improve your text:
- Real-time progress tracking
- Level-based improvements
- Side-by-side comparison
- Detailed change explanations

### 5. Get Recommendations

After enhancement, view recommendations for:
- 📖 Suitable journals
- 📄 Related papers
- 👥 Potential collaborators

### 6. Export

Download your enhanced text as a file.

## API Configuration

The frontend connects to the backend API automatically via proxy.

If you need to change the backend URL, edit `vite.config.ts`:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000', // Change this
      changeOrigin: true,
    },
  },
}
```

## Components

### TextEditor

Monaco-based editor with word/character count.

```tsx
<TextEditor
  value={text}
  onChange={setText}
  disabled={false}
/>
```

### AnalysisPanel

Displays comprehensive text analysis results.

```tsx
<AnalysisPanel result={analysisResult} />
```

### DiffViewer

Side-by-side comparison with highlighted changes.

```tsx
<DiffViewer
  original={originalText}
  enhanced={enhancedText}
  changes={changes}
/>
```

### EnhancementProgress

Real-time progress indicator with stages.

```tsx
<EnhancementProgress progress={progressData} />
```

### RecommendationPanel

JANE API recommendations in tabs.

```tsx
<RecommendationPanel
  text={enhancedText}
  discipline={discipline}
/>
```

## Hooks

### useEnhancement

Manages text enhancement process.

```typescript
const { enhance, progress, changes, loading } = useEnhancement();

const result = await enhance(text, level, discipline);
```

### useAnalysis

Handles text analysis.

```typescript
const { analyze, analysisResult, loading } = useAnalysis();

const result = await analyze(text, discipline);
```

### useRecommendations

Fetches JANE API recommendations.

```typescript
const { journals, papers, authors, fetchRecommendations } = useRecommendations();

await fetchRecommendations(text);
```

## Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Ant Design** - UI components
- **Monaco Editor** - Code editor
- **Vite** - Build tool
- **Axios** - HTTP client
- **Chart.js** - Data visualization
- **diff** - Text comparison

## Development

### Code Style

```bash
npm run lint
```

### Type Checking

```bash
npm run type-check
```

### Preview Production Build

```bash
npm run preview
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Troubleshooting

### Port Already in Use

Change the port in `vite.config.ts`:

```typescript
server: {
  port: 3001, // Change port
}
```

### Backend Connection Issues

1. Make sure the backend is running on port 8000
2. Check the proxy configuration in `vite.config.ts`
3. Check browser console for errors

### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## License

MIT License
