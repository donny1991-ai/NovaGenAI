import re
from typing import Dict, List, Set, Any

class MalaysianCodeSwitcher:
    """
    MalaysianCodeSwitcher is a natural language processing preprocessor designed
    to detect, analyze, and tag code-switching between standard Malay, English,
    Mandarin, and local dialects/Manglish phrases. This is critical for optimizing
    low-latency trilingual conversational voice agents like "James".
    """
    
    def __init__(self):
        # Local colloquial and Manglish discourse markers
        self.colloquial_markers: Set[str] = {
            "lah", "leh", "meh", "lor", "sikit", "bos", "boss", "jom", "la", 
            "kan", "wey", "wei", "giler", "best", "chop", "tapao", "makan", 
            "belanja", "terbaik", "steady", "habis", "geng", "kantoi"
        }
        
        # Malay-English code-switching transition markers
        # E.g., "actually", "basically", "so", "then", "macam", "atau", "sebab"
        self.transition_markers: Set[str] = {
            "actually", "basically", "so", "then", "like", "macam", "sebab", 
            "sekarang", "tapi", "and", "or", "atau", "meaning", "faham"
        }

    def tokenize(self, text: str) -> List[str]:
        """
        Cleans and tokenizes text, converting it to lowercase.
        """
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        return clean_text.split()

    def analyze_code_switching(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the text and returns statistics on colloquialism density
        and code-switching transitions.
        """
        tokens = self.tokenize(text)
        if not tokens:
            return {
                "word_count": 0,
                "colloquial_count": 0,
                "transition_count": 0,
                "colloquialism_density": 0.0,
                "identified_colloquialisms": []
            }
            
        found_colloquial = [w for w in tokens if w in self.colloquial_markers]
        found_transitions = [w for w in tokens if w in self.transition_markers]
        
        density = len(found_colloquial) / len(tokens)
        
        return {
            "word_count": len(tokens),
            "colloquial_count": len(found_colloquial),
            "transition_count": len(found_transitions),
            "colloquialism_density": round(density, 3),
            "identified_colloquialisms": list(set(found_colloquial))
        }

    def suggest_voice_synthesizer_tuning(self, text: str) -> Dict[str, Any]:
        """
        Analyzes text phonetics and colloquial markers, providing tuning suggestions
        for voice synthesis engines (e.g., ElevenLabs multilingual model) to ensure
        natural Malaysian conversational cadence.
        """
        analysis = self.analyze_code_switching(text)
        density = analysis["colloquialism_density"]
        
        # Determine appropriate voice parameters based on density
        if density > 0.15:
            tuning = {
                "stability": 0.65,          # Lower stability allows for more natural colloquial inflection
                "similarity_boost": 0.85,    # High clarity boost for accent accuracy
                "style_exaggeration": 0.15,  # Moderate style exaggeration to render local dialects
                "recommended_voice_model": "ElevenLabs Multilingual v2",
                "cadence_mode": "Conversational Colloquial (Manglish / Mixed Code)"
            }
        elif analysis["transition_count"] > 2:
            tuning = {
                "stability": 0.75,
                "similarity_boost": 0.80,
                "style_exaggeration": 0.05,
                "recommended_voice_model": "ElevenLabs Multilingual v2",
                "cadence_mode": "Corporate Formal (Malay-English Bilingual Transition)"
            }
        else:
            tuning = {
                "stability": 0.80,
                "similarity_boost": 0.75,
                "style_exaggeration": 0.00,
                "recommended_voice_model": "ElevenLabs English-Only or Multilingual v2",
                "cadence_mode": "Standard Formal Broadcast"
            }
            
        return {
            "colloquialism_density": density,
            "tuning_parameters": tuning
        }
