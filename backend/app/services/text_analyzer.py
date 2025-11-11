"""Text Analysis Service - Analyzes academic writing quality."""

import logging
import re
from typing import List, Dict, Any
from collections import Counter
import textstat

logger = logging.getLogger(__name__)


class Issue:
    """Represents a writing issue."""

    def __init__(
        self,
        issue_type: str,
        severity: int,
        description: str,
        suggestion: str,
        location: Dict[str, int] = None
    ):
        self.type = issue_type
        self.severity = severity
        self.description = description
        self.suggestion = suggestion
        self.location = location or {}


class TextAnalyzer:
    """Analyzes text for lexical, syntactic, and discourse quality."""

    # Simple academic word list (subset)
    SIMPLE_WORDS = {
        'big': ['substantial', 'considerable', 'significant'],
        'small': ['minimal', 'negligible', 'minor'],
        'good': ['beneficial', 'advantageous', 'favorable', 'positive'],
        'bad': ['detrimental', 'adverse', 'unfavorable', 'negative'],
        'show': ['demonstrate', 'illustrate', 'indicate', 'reveal'],
        'get': ['obtain', 'acquire', 'receive', 'attain'],
        'use': ['utilize', 'employ', 'apply'],
        'very': ['highly', 'extremely', 'considerably'],
        'a lot of': ['numerous', 'substantial', 'considerable'],
        'many': ['numerous', 'multiple', 'various'],
        'thing': ['element', 'aspect', 'component', 'factor'],
        'important': ['significant', 'crucial', 'essential', 'vital'],
    }

    # Common academic collocations
    WRONG_COLLOCATIONS = {
        'make research': 'conduct research',
        'make an experiment': 'conduct an experiment',
        'do a mistake': 'make a mistake',
        'say that': 'indicate that',
        'tell that': 'demonstrate that',
        'very unique': 'unique',
        'more optimal': 'optimal',
    }

    def __init__(self):
        """Initialize the text analyzer."""
        pass

    async def analyze(self, text: str, discipline: str = 'general') -> Dict[str, Any]:
        """
        Perform comprehensive text analysis.

        Args:
            text: The text to analyze
            discipline: Academic discipline (for discipline-specific rules)

        Returns:
            Analysis results with scores and issues
        """
        logger.info(f"Analyzing text of length {len(text)} for discipline: {discipline}")

        # Perform all analyses
        lexical_analysis = self._analyze_lexical(text)
        syntactic_analysis = self._analyze_syntactic(text)
        discourse_analysis = self._analyze_discourse(text)
        statistics = self._calculate_statistics(text)

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            lexical_analysis,
            syntactic_analysis,
            discourse_analysis
        )

        return {
            "overall_score": overall_score,
            "lexical": lexical_analysis,
            "syntactic": syntactic_analysis,
            "discourse": discourse_analysis,
            "statistics": statistics
        }

    def _analyze_lexical(self, text: str) -> Dict[str, Any]:
        """Analyze lexical features (vocabulary)."""
        issues = []

        # 1. Check for simple words
        simple_word_issues = self._detect_simple_words(text)
        issues.extend(simple_word_issues)

        # 2. Check for wrong collocations
        collocation_issues = self._detect_wrong_collocations(text)
        issues.extend(collocation_issues)

        # 3. Calculate lexical diversity
        diversity_score = self._calculate_lexical_diversity(text)

        return {
            "diversity_score": diversity_score,
            "issues": [self._issue_to_dict(issue) for issue in issues]
        }

    def _analyze_syntactic(self, text: str) -> Dict[str, Any]:
        """Analyze syntactic features (sentence structure)."""
        issues = []
        sentences = self._split_sentences(text)

        # 1. Check sentence lengths
        length_issues = self._analyze_sentence_lengths(sentences)
        issues.extend(length_issues)

        # 2. Calculate sentence variety
        variety_score = self._calculate_sentence_variety(sentences)

        # 3. Calculate complexity (using readability metrics)
        complexity = self._calculate_complexity(text)

        return {
            "complexity": complexity,
            "variety_score": variety_score,
            "issues": [self._issue_to_dict(issue) for issue in issues]
        }

    def _analyze_discourse(self, text: str) -> Dict[str, Any]:
        """Analyze discourse features (coherence and organization)."""
        issues = []
        paragraphs = self._split_paragraphs(text)

        # 1. Check for transition words
        transition_issues = self._analyze_transitions(text)
        issues.extend(transition_issues)

        # 2. Calculate coherence score
        coherence_score = self._calculate_coherence(paragraphs)

        return {
            "coherence_score": coherence_score,
            "issues": [self._issue_to_dict(issue) for issue in issues]
        }

    def _detect_simple_words(self, text: str) -> List[Issue]:
        """Detect overly simple vocabulary."""
        issues = []
        text_lower = text.lower()

        for simple_word, alternatives in self.SIMPLE_WORDS.items():
            pattern = r'\b' + re.escape(simple_word) + r'\b'
            matches = list(re.finditer(pattern, text_lower))

            if matches:
                issues.append(Issue(
                    issue_type="simple_vocabulary",
                    severity=3,
                    description=f"Found simple word '{simple_word}' ({len(matches)} occurrences)",
                    suggestion=f"Consider using: {', '.join(alternatives)}"
                ))

        return issues

    def _detect_wrong_collocations(self, text: str) -> List[Issue]:
        """Detect incorrect word collocations."""
        issues = []
        text_lower = text.lower()

        for wrong, correct in self.WRONG_COLLOCATIONS.items():
            if wrong in text_lower:
                issues.append(Issue(
                    issue_type="wrong_collocation",
                    severity=4,
                    description=f"Incorrect collocation: '{wrong}'",
                    suggestion=f"Use '{correct}' instead"
                ))

        return issues

    def _calculate_lexical_diversity(self, text: str) -> float:
        """Calculate lexical diversity (Type-Token Ratio)."""
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return 0.0

        unique_words = set(words)
        # Use corrected TTR (Root TTR) for longer texts
        ttr = len(unique_words) / (len(words) ** 0.5)
        # Normalize to 0-1 scale (assuming typical values 5-15)
        normalized_ttr = min(ttr / 15, 1.0)

        return round(normalized_ttr, 2)

    def _analyze_sentence_lengths(self, sentences: List[str]) -> List[Issue]:
        """Check for sentence length issues."""
        issues = []

        for i, sentence in enumerate(sentences):
            word_count = len(sentence.split())

            if word_count < 10:
                issues.append(Issue(
                    issue_type="sentence_too_short",
                    severity=2,
                    description=f"Sentence {i+1} is very short ({word_count} words)",
                    suggestion="Consider combining with adjacent sentences or adding more detail"
                ))
            elif word_count > 40:
                issues.append(Issue(
                    issue_type="sentence_too_long",
                    severity=3,
                    description=f"Sentence {i+1} is very long ({word_count} words)",
                    suggestion="Consider breaking into multiple sentences for clarity"
                ))

        return issues

    def _calculate_sentence_variety(self, sentences: List[str]) -> float:
        """Calculate sentence structure variety."""
        if not sentences:
            return 0.0

        sentence_lengths = [len(s.split()) for s in sentences]

        # Calculate coefficient of variation
        if not sentence_lengths or len(sentence_lengths) < 2:
            return 0.5

        mean_length = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((x - mean_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)
        std_dev = variance ** 0.5

        if mean_length == 0:
            return 0.0

        cv = std_dev / mean_length
        # Normalize (typical CV is 0.2-0.6)
        variety_score = min(cv / 0.6, 1.0)

        return round(variety_score, 2)

    def _calculate_complexity(self, text: str) -> float:
        """Calculate syntactic complexity using readability metrics."""
        try:
            # Flesch Reading Ease (0-100, higher is easier)
            flesch = textstat.flesch_reading_ease(text)
            # Convert to complexity score (0-1, higher is more complex)
            # Academic writing typically scores 30-50 on Flesch
            complexity = 1 - (flesch / 100)
            complexity = max(0, min(1, complexity))

            return round(complexity, 2)
        except:
            return 0.5

    def _analyze_transitions(self, text: str) -> List[Issue]:
        """Analyze use of transition words."""
        transition_words = [
            'however', 'moreover', 'furthermore', 'nevertheless',
            'therefore', 'consequently', 'thus', 'hence',
            'additionally', 'in addition', 'similarly', 'conversely'
        ]

        text_lower = text.lower()
        found_transitions = [word for word in transition_words if word in text_lower]

        sentences = self._split_sentences(text)
        transitions_per_sentence = len(found_transitions) / max(len(sentences), 1)

        issues = []
        if transitions_per_sentence < 0.1:
            issues.append(Issue(
                issue_type="lack_of_transitions",
                severity=3,
                description="Limited use of transition words",
                suggestion="Add transitions like 'however', 'moreover', 'therefore' to improve flow"
            ))

        return issues

    def _calculate_coherence(self, paragraphs: List[str]) -> float:
        """Calculate discourse coherence score."""
        if not paragraphs:
            return 0.0

        # Simple coherence measure: check for topic consistency
        # In a real implementation, this would use semantic similarity

        # For now, use a basic measure based on word overlap
        total_overlap = 0
        comparisons = 0

        for i in range(len(paragraphs) - 1):
            words1 = set(re.findall(r'\b\w+\b', paragraphs[i].lower()))
            words2 = set(re.findall(r'\b\w+\b', paragraphs[i + 1].lower()))

            if words1 and words2:
                overlap = len(words1 & words2) / len(words1 | words2)
                total_overlap += overlap
                comparisons += 1

        if comparisons == 0:
            return 0.5

        avg_overlap = total_overlap / comparisons
        # Normalize (typical overlap is 0.1-0.3)
        coherence = min(avg_overlap / 0.3, 1.0)

        return round(coherence, 2)

    def _calculate_statistics(self, text: str) -> Dict[str, Any]:
        """Calculate basic text statistics."""
        words = re.findall(r'\b\w+\b', text)
        sentences = self._split_sentences(text)

        word_count = len(words)
        sentence_count = len(sentences)
        avg_sentence_length = word_count / max(sentence_count, 1)
        unique_words = len(set(word.lower() for word in words))

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "unique_words": unique_words
        }

    def _calculate_overall_score(
        self,
        lexical: Dict,
        syntactic: Dict,
        discourse: Dict
    ) -> int:
        """Calculate overall quality score (0-100)."""
        # Weight different aspects
        lexical_weight = 0.35
        syntactic_weight = 0.35
        discourse_weight = 0.30

        # Get scores (0-1)
        lexical_score = lexical["diversity_score"]
        syntactic_score = (syntactic["complexity"] + syntactic["variety_score"]) / 2
        discourse_score = discourse["coherence_score"]

        # Penalize for issues
        total_issues = (
            len(lexical["issues"]) +
            len(syntactic["issues"]) +
            len(discourse["issues"])
        )
        issue_penalty = min(total_issues * 0.05, 0.3)  # Max 30% penalty

        # Calculate weighted score
        weighted_score = (
            lexical_score * lexical_weight +
            syntactic_score * syntactic_weight +
            discourse_score * discourse_weight
        )

        # Apply penalty and convert to 0-100 scale
        final_score = max(0, weighted_score - issue_penalty) * 100

        return round(final_score)

    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitter
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def _split_paragraphs(text: str) -> List[str]:
        """Split text into paragraphs."""
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]

    @staticmethod
    def _issue_to_dict(issue: Issue) -> Dict[str, Any]:
        """Convert Issue object to dictionary."""
        return {
            "type": issue.type,
            "severity": issue.severity,
            "description": issue.description,
            "suggestion": issue.suggestion,
            "location": issue.location
        }
