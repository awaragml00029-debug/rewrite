"""Enhancement Engine - Core text enhancement service using LLM."""

import logging
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from app.services.llm_client import get_llm_client
from app.services.text_analyzer import TextAnalyzer

logger = logging.getLogger(__name__)


class EnhancementEngine:
    """Core engine for enhancing academic writing."""

    def __init__(self):
        self.llm_client = get_llm_client()
        self.text_analyzer = TextAnalyzer()

    async def enhance(
        self,
        text: str,
        level: int,
        discipline: str = 'general',
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Enhance text at specified level.

        Args:
            text: Original text
            level: Enhancement level (1-4)
            discipline: Academic discipline
            progress_callback: Optional callback for progress updates

        Returns:
            Enhancement result with enhanced text, changes, and report
        """
        logger.info(f"Starting enhancement: level={level}, discipline={discipline}")

        original_text = text
        enhanced_text = text
        all_changes = []

        # Track progress
        # Pre-processing + levels + humanization (if level >= 3) + report
        total_stages = min(level + 2, 6) if level < 3 else min(level + 3, 7)
        current_stage = 0

        def update_progress(stage_name: str, percentage: float):
            nonlocal current_stage
            current_stage += 1
            if progress_callback:
                progress_callback({
                    "percentage": (current_stage / total_stages) * 100,
                    "current_stage": stage_name,
                    "total_stages": total_stages,
                    "completed_stages": current_stage,
                    "estimated_time": max(0, (total_stages - current_stage) * 10),
                    "message": f"Processing: {stage_name}"
                })

        try:
            # Stage 0: Pre-analysis
            update_progress("Text Pre-processing", 0)
            await asyncio.sleep(0.5)  # Simulate processing

            # Apply enhancements progressively
            if level >= 1:
                update_progress("Level 1: Basic Corrections", 20)
                enhanced_text, changes = await self._level1_basic_corrections(
                    enhanced_text, discipline
                )
                all_changes.extend(changes)

            if level >= 2:
                update_progress("Level 2: Native Expression", 40)
                enhanced_text, changes = await self._level2_native_expression(
                    enhanced_text, discipline
                )
                all_changes.extend(changes)

            if level >= 3:
                update_progress("Level 3: Academic Style", 60)
                enhanced_text, changes = await self._level3_academic_style(
                    enhanced_text, discipline
                )
                all_changes.extend(changes)

            if level >= 4:
                update_progress("Level 4: Discourse Optimization", 80)
                enhanced_text, changes = await self._level4_discourse_optimization(
                    enhanced_text, discipline
                )
                all_changes.extend(changes)

            # Apply humanization post-processing for Level 3+
            if level >= 3:
                update_progress("Humanization Post-Processing", 85)
                enhanced_text, changes = await self._humanization_postprocess(
                    enhanced_text, discipline
                )
                all_changes.extend(changes)

            # Generate report
            update_progress("Generating Report", 95)
            report = await self._generate_report(original_text, enhanced_text, all_changes)

            update_progress("Complete", 100)

            return {
                "enhanced_text": enhanced_text,
                "changes": all_changes,
                "report": report
            }

        except Exception as e:
            logger.error(f"Enhancement failed: {e}")
            raise

    async def _level1_basic_corrections(
        self,
        text: str,
        discipline: str
    ) -> tuple[str, List[Dict]]:
        """Level 1: Basic grammar and spelling corrections."""
        prompt = f"""Fix ONLY clear grammar and spelling errors in this {discipline} text.

CRITICAL - MINIMAL CHANGES:
- Fix obvious typos and grammar mistakes only
- Do NOT improve style, word choice, or sentence structure
- Keep the author's exact phrasing, even if informal or awkward
- Preserve all original sentence patterns and rhythm
- Maintain any informal language or colloquialisms
- Think: "What would a human do with track changes?" not "How can I improve this?"

Original text:
{text}

Return the text with ONLY grammar/spelling fixes:"""

        try:
            enhanced = await self.llm_client.generate(prompt, temperature=0.65, max_tokens=4000)
            logger.info(f"Level 1 completed: {len(text)} chars -> {len(enhanced)} chars")
            if len(enhanced) == 0:
                logger.error("Level 1 returned empty text, using original")
                return text, []
            changes = self._detect_changes(text, enhanced, "Level 1: Basic Corrections")
            return enhanced, changes
        except Exception as e:
            logger.error(f"Level 1 enhancement failed: {e}")
            return text, []

    async def _level2_native_expression(
        self,
        text: str,
        discipline: str
    ) -> tuple[str, List[Dict]]:
        """Level 2: Native-like expression enhancement."""
        prompt = f"""You are helping improve awkward non-native expressions in this {discipline} text while keeping it authentically human.

CRITICAL - SOUND LIKE A REAL PERSON:
- Fix only the most awkward non-native phrasings
- Make it sound natural but NOT polished or AI-generated
- Keep the author's vocabulary level - don't upgrade simple words to fancy ones
- Preserve the author's sentence patterns and rhythm
- Maintain personality quirks, emphatic statements, and informal touches
- Real people don't speak uniformly - keep variation in tone and style
- Avoid creating smooth, perfect prose - keep some roughness
- Think: "Native English speaker chatting naturally" not "Professional editor's perfect version"

Original text:
{text}

Return naturally improved text that still sounds human-written:"""

        try:
            enhanced = await self.llm_client.generate(prompt, temperature=0.78, max_tokens=4000)
            logger.info(f"Level 2 completed: {len(text)} chars -> {len(enhanced)} chars")
            if len(enhanced) == 0:
                logger.error("Level 2 returned empty text, using original")
                return text, []
            changes = self._detect_changes(text, enhanced, "Level 2: Native Expression")
            return enhanced, changes
        except Exception as e:
            logger.error(f"Level 2 enhancement failed: {e}")
            return text, []

    async def _level3_academic_style(
        self,
        text: str,
        discipline: str
    ) -> tuple[str, List[Dict]]:
        """Level 3: Academic style and conventions."""
        prompt = f"""You are helping a researcher improve their {discipline} paper to meet publication standards while keeping their authentic voice.

CRITICAL - KEEP IT HUMAN (Anti-AI-Detection):
- Add appropriate academic phrasing where needed (hedging, formal connectives)
- Do NOT over-formalize - real academic papers have natural flow, not robotic precision
- Maintain the author's argumentative style and reasoning approach
- Keep varying sentence lengths and structures - real humans don't write perfectly balanced sentences
- Use academic vocabulary selectively - do NOT replace every casual word
- Preserve the author's examples, analogies, and explanations
- Real academic writing has personality - keep it, don't sterilize it
- Keep occasional contractions, personal statements, or direct addresses if present
- Maintain the author's emphasis patterns (bold, italics, exclamation marks if used)
- Real papers have inconsistent formality levels across sections - that's OK
- Don't impose a template structure - keep the author's organization
- Think: "Published paper by a human researcher" not "AI-generated academic template"

AVOID these AI-like patterns:
- Perfect parallel structure in every paragraph
- Overuse of "Moreover", "Furthermore", "Thus", "Hence"
- Every sentence starting with different words (forced variety is detectable)
- Uniform paragraph lengths
- Eliminating all contractions and informal phrases

Original text:
{text}

Return the text with selective academic improvements that preserve human authenticity:"""

        try:
            enhanced = await self.llm_client.generate(prompt, temperature=0.87, max_tokens=4000)
            logger.info(f"Level 3 completed: {len(text)} chars -> {len(enhanced)} chars")
            if len(enhanced) == 0:
                logger.error("Level 3 returned empty text, using original")
                return text, []
            changes = self._detect_changes(text, enhanced, "Level 3: Academic Style")
            return enhanced, changes
        except Exception as e:
            logger.error(f"Level 3 enhancement failed: {e}")
            return text, []

    async def _level4_discourse_optimization(
        self,
        text: str,
        discipline: str
    ) -> tuple[str, List[Dict]]:
        """Level 4: Overall discourse and coherence optimization."""
        prompt = f"""You are helping a researcher improve the flow and coherence of their {discipline} paper while maintaining their natural writing style.

CRITICAL - ANTI-AI-DETECTION PRINCIPLES:
- Improve logical connections and paragraph flow ONLY where genuinely needed
- Do NOT create artificial "perfect" transitions - real writing has natural, sometimes abrupt shifts
- Maintain the author's unique way of organizing thoughts - don't impose a template structure
- Keep the author's sentence variety - mix of long, short, complex, and simple sentences
- Preserve informal transitions if they work ("However" vs "Nevertheless" - both are valid)
- Real human writing has rhythm variations - don't smooth everything out
- Keep occasional rhetorical questions, personal observations, or emphatic statements
- Maintain the author's level of directness vs. indirectness
- Preserve the author's paragraph breaks - don't reorganize structure
- Keep repetition if it serves emphasis (humans do this naturally)
- Think: "How would a human researcher naturally connect these ideas?" not "What's the most sophisticated way?"

AVOID these AI-detector red flags:
- Adding transition words to every paragraph start
- Making every paragraph the same length
- Creating perfectly smooth, flowing prose without any jumps
- Using sophisticated vocabulary for transitions ("Consequently", "Notwithstanding")
- Eliminating all redundancy (some repetition is human)
- Making every topic sentence perfectly clear and structured
- Balancing sentence lengths artificially

REMEMBER: AI detectors look for perfect uniformity, flawless transitions, and robotic consistency. Keep it imperfect and human. Real academic writing has rough edges.

Original text:
{text}

Return the text with minimal, natural flow improvements that a human would make:"""

        try:
            enhanced = await self.llm_client.generate(prompt, temperature=0.92, max_tokens=4000)
            logger.info(f"Level 4 completed: {len(text)} chars -> {len(enhanced)} chars")
            if len(enhanced) == 0:
                logger.error("Level 4 returned empty text, using original")
                return text, []
            changes = self._detect_changes(text, enhanced, "Level 4: Discourse")
            return enhanced, changes
        except Exception as e:
            logger.error(f"Level 4 enhancement failed: {e}")
            return text, []

    async def _humanization_postprocess(
        self,
        text: str,
        discipline: str
    ) -> tuple[str, List[Dict]]:
        """Final humanization pass to remove AI detection markers."""
        prompt = f"""Review this {discipline} text and remove any AI-detection red flags while keeping all improvements.

CRITICAL - REMOVE AI MARKERS:
- If text sounds too polished or uniform, add natural variation
- Replace overused AI transitions ("Moreover", "Furthermore", "Additionally") with simpler ones
- Break up any artificially balanced sentence patterns
- Add back some natural imperfections if everything seems too perfect
- Ensure paragraph lengths vary naturally
- Keep some informal elements or contractions if appropriate for the context
- If transitions appear at every paragraph start, remove some
- Vary the sentence opening patterns more naturally
- Ensure the text doesn't sound like it came from a template

THIS IS CRITICAL: Make MINIMAL changes - only what's needed to pass AI detection. Don't undo the good improvements. Just add natural human roughness where the text is too smooth.

Original text:
{text}

Return text with subtle humanization tweaks (may be identical if already natural):"""

        try:
            enhanced = await self.llm_client.generate(prompt, temperature=0.88, max_tokens=4000)
            logger.info(f"Humanization completed: {len(text)} chars -> {len(enhanced)} chars")
            if len(enhanced) == 0:
                logger.warning("Humanization returned empty text, using original")
                return text, []
            changes = self._detect_changes(text, enhanced, "Humanization")
            return enhanced, changes
        except Exception as e:
            logger.error(f"Humanization failed: {e}")
            return text, []

    def _get_discipline_guidelines(self, discipline: str) -> str:
        """Get discipline-specific writing guidelines."""
        guidelines = {
            "computer_science": """
- Use active voice for methodology: "We propose", "We implement"
- Use passive voice for results: "was observed", "were measured"
- Present tense for general statements
- Past tense for specific experiments
- Moderate hedging""",

            "biology": """
- Prefer passive voice: "Samples were collected", "Data were analyzed"
- Use strong hedging: "suggests", "may indicate"
- Past tense for methods and results
- Present tense for discussion of implications""",

            "social_sciences": """
- Active voice preferred: "This study examines", "We argue"
- Strong hedging required: "suggests", "appears to"
- Present perfect for literature review
- Past tense for methodology""",

            "engineering": """
- Clear, concise language
- Active voice for descriptions: "The system performs"
- Past tense for experiments
- Technical precision over literary style""",

            "general": """
- Balance of active and passive voice
- Moderate hedging
- Appropriate tense for context
- Formal academic vocabulary"""
        }

        return guidelines.get(discipline.lower(), guidelines["general"])

    def _detect_changes(
        self,
        original: str,
        enhanced: str,
        change_type: str
    ) -> List[Dict[str, Any]]:
        """Detect and document changes between original and enhanced text."""
        # Simple change detection using sentence comparison
        # In production, you'd use a proper diff algorithm

        changes = []

        original_sentences = self._split_into_sentences(original)
        enhanced_sentences = self._split_into_sentences(enhanced)

        for i, (orig_sent, enh_sent) in enumerate(zip(original_sentences, enhanced_sentences)):
            if orig_sent != enh_sent:
                changes.append({
                    "id": f"change_{len(changes) + 1}",
                    "type": change_type,
                    "original": orig_sent,
                    "suggested": enh_sent,
                    "reason": self._analyze_change_reason(orig_sent, enh_sent),
                    "severity": 3,
                    "position": {"sentence_index": i}
                })

        return changes

    def _analyze_change_reason(self, original: str, enhanced: str) -> str:
        """Analyze why a change was made."""
        # Simple heuristic-based reason detection
        if len(enhanced.split()) > len(original.split()) * 1.2:
            return "Enhanced clarity and detail"
        elif len(enhanced.split()) < len(original.split()) * 0.8:
            return "Improved conciseness"
        elif original.lower() != enhanced.lower():
            return "Improved vocabulary and expression"
        else:
            return "Grammatical or stylistic improvement"

    async def _generate_report(
        self,
        original: str,
        enhanced: str,
        changes: List[Dict]
    ) -> Dict[str, Any]:
        """Generate enhancement report."""
        # Get text analysis
        original_analysis = await self.text_analyzer.analyze(original)
        enhanced_analysis = await self.text_analyzer.analyze(enhanced)

        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_changes": len(changes),
                "original_score": original_analysis["overall_score"],
                "enhanced_score": enhanced_analysis["overall_score"],
                "improvement": enhanced_analysis["overall_score"] - original_analysis["overall_score"]
            },
            "metrics": {
                "original": {
                    "word_count": original_analysis["statistics"]["word_count"],
                    "lexical_diversity": original_analysis["lexical"]["diversity_score"],
                    "complexity": original_analysis["syntactic"]["complexity"]
                },
                "enhanced": {
                    "word_count": enhanced_analysis["statistics"]["word_count"],
                    "lexical_diversity": enhanced_analysis["lexical"]["diversity_score"],
                    "complexity": enhanced_analysis["syntactic"]["complexity"]
                }
            },
            "change_types": self._summarize_change_types(changes)
        }

    @staticmethod
    def _summarize_change_types(changes: List[Dict]) -> Dict[str, int]:
        """Summarize changes by type."""
        type_counts = {}
        for change in changes:
            change_type = change.get("type", "unknown")
            type_counts[change_type] = type_counts.get(change_type, 0) + 1
        return type_counts

    @staticmethod
    def _split_into_sentences(text: str) -> List[str]:
        """Split text into sentences."""
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
