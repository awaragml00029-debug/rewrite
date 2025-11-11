/**
 * API Service - Handles all backend API calls
 */

import axios, { AxiosInstance } from 'axios';

// Types
export interface AnalysisRequest {
  text: string;
  discipline?: string;
  analysis_types?: string[];
}

export interface EnhanceRequest {
  text: string;
  level: number;
  discipline?: string;
  options?: Record<string, any>;
}

export interface RecommendationRequest {
  text: string;
  filters?: string;
  limit?: number;
}

export interface AnalysisResult {
  overall_score: number;
  lexical: {
    diversity_score: number;
    issues: Issue[];
  };
  syntactic: {
    complexity: number;
    variety_score: number;
    issues: Issue[];
  };
  discourse: {
    coherence_score: number;
    issues: Issue[];
  };
  statistics: {
    word_count: number;
    sentence_count: number;
    avg_sentence_length: number;
    unique_words: number;
  };
}

export interface Issue {
  type: string;
  severity: number;
  description: string;
  suggestion: string;
  location?: Record<string, any>;
}

export interface EnhancementJob {
  job_id: string;
  status: string;
  message: string;
}

export interface EnhancementStatus {
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress?: {
    percentage: number;
    current_stage: string;
    total_stages: number;
    completed_stages: number;
    estimated_time: number;
    message?: string;
  };
  result?: {
    enhanced_text: string;
    changes: Change[];
    report: any;
  };
  error?: string;
}

export interface Change {
  id: string;
  type: string;
  original: string;
  suggested: string;
  reason: string;
  severity: number;
  position?: any;
}

export interface Journal {
  title: string;
  similarity_score: number;
  impact_factor?: number;
  open_access: boolean;
  publisher: string;
  url: string;
  confidence: string;
}

export interface Paper {
  title: string;
  authors: string[];
  year?: number;
  journal: string;
  doi: string;
  similarity_score: number;
  citations?: number;
  url: string;
}

export interface Author {
  name: string;
  affiliation: string;
  h_index?: number;
  total_publications: number;
  similarity_score: number;
}

class APIService {
  private client: AxiosInstance;

  constructor(baseURL: string = '/api') {
    this.client = axios.create({
      baseURL,
      timeout: 120000, // 2 minutes
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          // Server responded with error
          console.error('API Error:', error.response.data);
          throw new Error(error.response.data.error?.message || error.response.data.detail || 'API request failed');
        } else if (error.request) {
          // Request made but no response
          console.error('Network Error:', error.request);
          throw new Error('Network error - please check your connection');
        } else {
          // Something else happened
          console.error('Error:', error.message);
          throw error;
        }
      }
    );
  }

  /**
   * Health check
   */
  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }

  /**
   * Analyze text
   */
  async analyzeText(request: AnalysisRequest): Promise<AnalysisResult> {
    const response = await this.client.post('/analyze', request);
    return response.data;
  }

  /**
   * Create enhancement job
   */
  async createEnhancement(request: EnhanceRequest): Promise<EnhancementJob> {
    const response = await this.client.post('/enhance', request);
    return response.data;
  }

  /**
   * Get enhancement status
   */
  async getEnhancementStatus(jobId: string): Promise<EnhancementStatus> {
    const response = await this.client.get(`/enhance/status/${jobId}`);
    return response.data;
  }

  /**
   * Poll enhancement status until complete
   */
  async pollEnhancement(
    jobId: string,
    onProgress?: (status: EnhancementStatus) => void
  ): Promise<EnhancementStatus> {
    return new Promise((resolve, reject) => {
      const interval = setInterval(async () => {
        try {
          const status = await this.getEnhancementStatus(jobId);

          if (onProgress) {
            onProgress(status);
          }

          if (status.status === 'completed') {
            clearInterval(interval);
            resolve(status);
          } else if (status.status === 'failed') {
            clearInterval(interval);
            reject(new Error(status.error || 'Enhancement failed'));
          }
        } catch (error) {
          clearInterval(interval);
          reject(error);
        }
      }, 1000); // Poll every second
    });
  }

  /**
   * Get journal recommendations
   */
  async getJournalRecommendations(request: RecommendationRequest): Promise<Journal[]> {
    const response = await this.client.post('/recommendations/journals', request);
    return response.data.journals;
  }

  /**
   * Get paper recommendations
   */
  async getPaperRecommendations(request: RecommendationRequest): Promise<Paper[]> {
    const response = await this.client.post('/recommendations/papers', request);
    return response.data.papers;
  }

  /**
   * Get author recommendations
   */
  async getAuthorRecommendations(request: RecommendationRequest): Promise<Author[]> {
    const response = await this.client.post('/recommendations/authors', request);
    return response.data.authors;
  }
}

// Export singleton instance
export const apiService = new APIService();
export default apiService;
