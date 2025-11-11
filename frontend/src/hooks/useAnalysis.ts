/**
 * useAnalysis Hook - Manages text analysis
 */

import { useState, useCallback } from 'react';
import { apiService, AnalysisResult } from '@/services/api';

export const useAnalysis = () => {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = useCallback(async (text: string, discipline: string = 'general') => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiService.analyzeText({
        text,
        discipline,
        analysis_types: ['lexical', 'syntactic', 'discourse'],
      });

      setAnalysisResult(result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'Analysis failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearAnalysis = useCallback(() => {
    setAnalysisResult(null);
    setError(null);
  }, []);

  return {
    analyze,
    clearAnalysis,
    analysisResult,
    loading,
    error,
  };
};
