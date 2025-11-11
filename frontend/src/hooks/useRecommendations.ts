/**
 * useRecommendations Hook - Manages JANE API recommendations
 */

import { useState, useCallback } from 'react';
import { apiService, Journal, Paper, Author } from '@/services/api';

export const useRecommendations = () => {
  const [journals, setJournals] = useState<Journal[]>([]);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [authors, setAuthors] = useState<Author[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = useCallback(async (text: string, limit: number = 10) => {
    setLoading(true);
    setError(null);

    try {
      // Fetch all recommendations in parallel
      const [journalsRes, papersRes, authorsRes] = await Promise.allSettled([
        apiService.getJournalRecommendations({ text, limit }),
        apiService.getPaperRecommendations({ text, limit }),
        apiService.getAuthorRecommendations({ text, limit }),
      ]);

      // Handle journals
      if (journalsRes.status === 'fulfilled') {
        setJournals(journalsRes.value);
      } else {
        console.warn('Failed to fetch journals:', journalsRes.reason);
      }

      // Handle papers
      if (papersRes.status === 'fulfilled') {
        setPapers(papersRes.value);
      } else {
        console.warn('Failed to fetch papers:', papersRes.reason);
      }

      // Handle authors
      if (authorsRes.status === 'fulfilled') {
        setAuthors(authorsRes.value);
      } else {
        console.warn('Failed to fetch authors:', authorsRes.reason);
      }

      // Only set error if ALL requests failed
      if (
        journalsRes.status === 'rejected' &&
        papersRes.status === 'rejected' &&
        authorsRes.status === 'rejected'
      ) {
        setError('Failed to fetch recommendations');
      }
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to fetch recommendations';
      setError(errorMessage);
      console.error('Recommendations error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearRecommendations = useCallback(() => {
    setJournals([]);
    setPapers([]);
    setAuthors([]);
    setError(null);
  }, []);

  return {
    journals,
    papers,
    authors,
    loading,
    error,
    fetchRecommendations,
    clearRecommendations,
  };
};
