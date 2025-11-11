/**
 * useEnhancement Hook - Manages text enhancement process
 */

import { useState, useCallback } from 'react';
import { apiService, EnhancementStatus, Change } from '@/services/api';

interface ProgressData {
  percentage: number;
  current_stage: string;
  total_stages: number;
  completed_stages: number;
  estimated_time: number;
  message?: string;
}

interface EnhancementResult {
  enhanced_text: string;
  changes: Change[];
  report: any;
}

export const useEnhancement = () => {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [changes, setChanges] = useState<Change[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const enhance = useCallback(
    async (
      text: string,
      level: number,
      discipline: string = 'general'
    ): Promise<EnhancementResult> => {
      setLoading(true);
      setProgress(null);
      setChanges([]);
      setError(null);

      try {
        // Create enhancement job
        const job = await apiService.createEnhancement({
          text,
          level,
          discipline,
        });

        // Poll for progress and completion
        const finalStatus = await apiService.pollEnhancement(
          job.job_id,
          (status: EnhancementStatus) => {
            if (status.progress) {
              setProgress(status.progress);
            }
          }
        );

        if (!finalStatus.result) {
          throw new Error('Enhancement completed but no result returned');
        }

        setChanges(finalStatus.result.changes || []);

        return finalStatus.result;
      } catch (err: any) {
        const errorMessage = err.message || 'Enhancement failed';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    enhance,
    progress,
    changes,
    loading,
    error,
  };
};
