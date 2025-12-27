import os
import csv
from typing import List, Tuple, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ChemLabBuddy:
    """
    Core NLP engine for the chemistry chatbot.
    Loads a CSV FAQ, builds a TF-IDF model on questions,
    and answers user queries based on cosine similarity.
    """

    def __init__(self, faq_path: str, similarity_threshold: float = 0.3):
        self.faq_path = faq_path
        self.similarity_threshold = similarity_threshold

        self.questions: List[str] = []
        self.answers: List[str] = []
        self.topics: List[str] = []

        self.vectorizer: Optional[TfidfVectorizer] = None
        self.question_matrix = None

        print(f"[ChemLabBuddy] Loading FAQ from: {self.faq_path}")

        self._load_faq()
        self._fit_vectorizer()

    def _load_faq(self) -> None:
        """Load questions, answers, and topics from the CSV file."""
        if not os.path.exists(self.faq_path):
            raise FileNotFoundError(f"FAQ file not found: {self.faq_path}")

        with open(self.faq_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            print(f"[ChemLabBuddy] CSV columns: {reader.fieldnames}")

            for row in reader:
                question = row.get("question")
                answer = row.get("answer")
                topic = row.get("topic", "General")

                # Skip bad/incomplete rows
                if not question or not answer:
                    continue

                self.questions.append(question)
                self.answers.append(answer)
                self.topics.append(topic)

        if not self.questions:
            raise ValueError(
                "No questions loaded from FAQ CSV. "
                "Check that the file has 'question' and 'answer' headers and at least one row."
            )

        print(f"[ChemLabBuddy] Loaded {len(self.questions)} Q&A pairs from FAQ.")

    def _fit_vectorizer(self) -> None:
        """Fit TF-IDF vectorizer on questions."""
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.question_matrix = self.vectorizer.fit_transform(self.questions)

    def get_answer(self, user_query: str) -> Tuple[Optional[str], Optional[str], float]:
        """
        Returns (answer, topic, similarity_score).
        If similarity is too low, answer will be None.
        """
        if not user_query.strip():
            return None, None, 0.0

        if self.vectorizer is None or self.question_matrix is None:
            raise RuntimeError("Vectorizer not initialized")

        user_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(user_vec, self.question_matrix).flatten()

        best_idx = int(similarities.argmax())
        best_score = float(similarities[best_idx])

        if best_score < self.similarity_threshold:
            return None, None, best_score

        return self.answers[best_idx], self.topics[best_idx], best_score
