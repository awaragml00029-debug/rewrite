"""JANE API Client - Integration with Journal/Author Name Estimator."""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from zeep import Client
from zeep.exceptions import Fault

from app.core.config import settings

logger = logging.getLogger(__name__)


class JANEClient:
    """Client for JANE (Journal/Author Name Estimator) API."""

    def __init__(self):
        self.wsdl_url = settings.jane_wsdl_url
        self.base_url = settings.jane_base_url
        self.client = None

    async def _get_client(self):
        """Get or create SOAP client."""
        if self.client is None:
            try:
                # Create synchronous client and use it with asyncio.to_thread
                self.client = await asyncio.to_thread(Client, self.wsdl_url)
                logger.info("JANE SOAP client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize JANE client: {e}")
                raise
        return self.client

    async def get_journal_recommendations(
        self,
        text: str,
        filter_string: str = "",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get journal recommendations based on text.

        Args:
            text: Abstract or full text
            filter_string: Optional filter criteria
            limit: Maximum number of results

        Returns:
            List of journal recommendations
        """
        try:
            client = await self._get_client()

            # Call JANE SOAP service
            journals = await asyncio.to_thread(
                client.service.getJournals,
                text,
                filter_string
            )

            # Parse and format results
            recommendations = []
            for journal in journals[:limit]:
                try:
                    recommendations.append({
                        'title': getattr(journal, 'title', 'Unknown'),
                        'similarity_score': float(getattr(journal, 'similarity', 0)),
                        'impact_factor': self._safe_float(getattr(journal, 'impactFactor', None)),
                        'open_access': bool(getattr(journal, 'openAccess', False)),
                        'publisher': getattr(journal, 'publisher', 'Unknown'),
                        'scope': getattr(journal, 'scope', ''),
                        'url': getattr(journal, 'url', ''),
                        'confidence': self._calculate_confidence(
                            float(getattr(journal, 'similarity', 0))
                        )
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse journal: {e}")
                    continue

            # Sort by similarity
            recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)

            logger.info(f"Found {len(recommendations)} journal recommendations")
            return recommendations

        except Fault as e:
            logger.error(f"JANE SOAP fault: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting journal recommendations: {e}")
            return []

    async def find_related_papers(
        self,
        text: str,
        count: int = 20,
        offset: int = 0,
        filter_string: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Find related papers based on text.

        Args:
            text: Input text
            count: Number of results
            offset: Offset for pagination
            filter_string: Optional filter

        Returns:
            List of related papers
        """
        try:
            client = await self._get_client()

            papers = await asyncio.to_thread(
                client.service.getPapers,
                text,
                filter_string,
                count,
                offset
            )

            related_papers = []
            for paper in papers:
                try:
                    related_papers.append({
                        'title': getattr(paper, 'title', 'Unknown'),
                        'authors': self._parse_authors(getattr(paper, 'authors', '')),
                        'year': self._safe_int(getattr(paper, 'year', None)),
                        'journal': getattr(paper, 'journal', ''),
                        'doi': getattr(paper, 'doi', ''),
                        'abstract': getattr(paper, 'abstract', ''),
                        'similarity_score': float(getattr(paper, 'similarity', 0)),
                        'citations': self._safe_int(getattr(paper, 'citations', 0)),
                        'url': getattr(paper, 'url', '')
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse paper: {e}")
                    continue

            logger.info(f"Found {len(related_papers)} related papers")
            return related_papers

        except Fault as e:
            logger.error(f"JANE SOAP fault: {e}")
            return []
        except Exception as e:
            logger.error(f"Error finding related papers: {e}")
            return []

    async def find_potential_collaborators(
        self,
        text: str,
        filter_string: str = "",
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Find potential collaborators (authors) based on text.

        Args:
            text: Input text
            filter_string: Optional filter
            limit: Maximum number of results

        Returns:
            List of potential collaborators
        """
        try:
            client = await self._get_client()

            authors = await asyncio.to_thread(
                client.service.getAuthors,
                text,
                filter_string
            )

            collaborators = []
            for author in authors[:limit]:
                try:
                    collaborators.append({
                        'name': getattr(author, 'name', 'Unknown'),
                        'affiliation': getattr(author, 'affiliation', ''),
                        'email': getattr(author, 'email', ''),
                        'research_areas': self._parse_list(
                            getattr(author, 'researchAreas', [])
                        ),
                        'h_index': self._safe_int(getattr(author, 'hIndex', None)),
                        'total_publications': self._safe_int(
                            getattr(author, 'publicationCount', 0)
                        ),
                        'similarity_score': float(getattr(author, 'similarity', 0)),
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse author: {e}")
                    continue

            logger.info(f"Found {len(collaborators)} potential collaborators")
            return collaborators

        except Fault as e:
            logger.error(f"JANE SOAP fault: {e}")
            return []
        except Exception as e:
            logger.error(f"Error finding collaborators: {e}")
            return []

    def _calculate_confidence(self, similarity_score: float) -> str:
        """Calculate confidence level from similarity score."""
        if similarity_score >= 0.8:
            return 'Very High'
        elif similarity_score >= 0.6:
            return 'High'
        elif similarity_score >= 0.4:
            return 'Medium'
        else:
            return 'Low'

    @staticmethod
    def _parse_authors(authors_string: str) -> List[str]:
        """Parse comma-separated author list."""
        if not authors_string:
            return []
        return [author.strip() for author in authors_string.split(',') if author.strip()]

    @staticmethod
    def _parse_list(value: Any) -> List[str]:
        """Parse list value."""
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            return [item.strip() for item in value.split(',') if item.strip()]
        return []

    @staticmethod
    def _safe_float(value: Any) -> Optional[float]:
        """Safely convert to float."""
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _safe_int(value: Any) -> Optional[int]:
        """Safely convert to int."""
        try:
            return int(value) if value is not None else None
        except (ValueError, TypeError):
            return None
