"""
Built-in sample corpus of authentic Mising cultural and linguistic texts.

Includes festival descriptions (Ali-Aye-Ligang), traditional proverbs,
folktales (Do:ying), and daily conversational dialogues.
"""

from typing import List
from mising.corpus.reader import CorpusDocument
from mising.corpus.manager import CorpusManager


SAMPLE_DOCUMENTS: List[CorpusDocument] = [
    CorpusDocument(
        id="ali_aye_ligang",
        title="Ali-Aye-Ligang Festival",
        text="""Ali-Aye-Ligang si Mising kídíke botteba lígango.
Si festival si Ginmur polo lékoda léko budhbarlo miduŋ.
'Ali' emnam si aye gí alim mennam, 'Aye' emnam si ali-aye, delo 'Ligang' emnam si binam.
Ami-kídí apong tila Gumrag soki gerduŋ.
Mising agomlo gernam gerdola bulu doolunglo mosumduŋ.
Donyi-Polo agom arumpalo ane-abu kídíke ashírbad langduŋ.""",
        metadata={
            "genre": "cultural_article",
            "region": "Majuli/Dhemaji",
            "year": "2024",
            "topic": "agriculture_festival",
            "english_translation": (
                "Ali-Aye-Ligang is the greatest spring festival of the Mising people. "
                "This festival is held on the first Wednesday of the Ginmur month. "
                "'Ali' means root/seed, 'Aye' means fruit, and 'Ligang' means sowing. "
                "People drink rice beer (apong) and dance the Gumrag dance. "
                "Singing songs in the Mising language, they work in the village. "
                "They receive blessings from mother-father and Donyi-Polo."
            ),
        },
    ),
    CorpusDocument(
        id="proverbs_wisdom",
        title="Traditional Mising Proverbs (Do:ying)",
        text="""Doolung bottepe bírma, ami kampope bírduŋ.
Kénam ami agom kinam ami.
Asi lottokai apong iyémang.
Ane-Abu agom tatlang, kampo lamkulo gelang.
Okum yasangpe kídola mína doolung yasangduŋ.
Simyo-e ekkem doge-mang.""",
        metadata={
            "genre": "proverbs",
            "region": "Lakhimpur/Sonitpur",
            "topic": "traditional_wisdom",
            "english_translation": (
                "A village is not great by size, but by good people. "
                "A wise person is one who understands words. "
                "Spilled water cannot become rice beer. "
                "Listen to the words of mother and father, and walk on a good path. "
                "When houses are kept clean, the whole village becomes clean. "
                "A tiger does not eat its own kind."
            ),
        },
    ),
    CorpusDocument(
        id="folktale_donyi_polo",
        title="The Sun and the Moon (Donyi-Polo)",
        text="""Téne lékolo Donyi delo Polo anyie gídíng-ako doolunglo dungto.
Donyi si amím kénne ane, Polo si abu rupe kídag.
Bulu ami-kídím mídum-pe karsu-dola urom-kídím kumpato.
Mising ami-e Donyi-Polom karsu-dola mosum-to.
Delo bulu asi botte Sianglo kur-la okum múpé yarto.""",
        metadata={
            "genre": "mythology_folktale",
            "region": "Jonai/Dhemaji",
            "topic": "creation_belief",
            "english_translation": (
                "Long ago, the Sun (Donyi) and the Moon (Polo) lived together in one village. "
                "Donyi was the loving mother, and Polo was like the guardian father. "
                "They cared for the humans and protected them from harm. "
                "The Mising people prayed to Donyi-Polo and labored. "
                "Then they crossed the great river Siang and built their homes."
            ),
        },
    ),
    CorpusDocument(
        id="daily_dialogue",
        title="Everyday Conversation in the Village",
        text="""Kuye! No kolo giduŋ?
Ngo dírbílo mosumpe giduŋ. No inlang!
Nok okum-lo asi kaduŋ gí?
Oy! Asi kaduŋ, apong sin kaduŋ.
Melo ngo ane-abu kídím kato. Bulu kampope dungto.
Ténto ngo doolunglo yarto.""",
        metadata={
            "genre": "dialogue",
            "region": "General",
            "topic": "conversational",
            "english_translation": (
                "Hello! Where are you going? "
                "I am going to work in the field. Come along! "
                "Is there water in your house? "
                "Yes! There is water, and there is also apong (rice beverage). "
                "Yesterday I saw mother and father. They were well. "
                "Now I went to the village."
            ),
        },
    ),
]


def load_sample_corpus() -> CorpusManager:
    """
    Load the standard built-in Mising sample corpus.

    Returns:
        A ready-to-use CorpusManager preloaded with sample texts.

    Examples:
        >>> from mising.corpus import load_sample_corpus
        >>> corpus = load_sample_corpus()
        >>> len(corpus)
        4
        >>> corpus.stats()['total_tokens'] > 0
        True
    """
    return CorpusManager(documents=SAMPLE_DOCUMENTS)
