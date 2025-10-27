from enum import Enum
from io import BytesIO
from pathlib import Path

from PIL import Image


class TarotCardType(str, Enum):
    major = "major"
    minor = "minor"


class TarotCardVariant:
    parent: "TarotCard"
    is_reversed: bool
    meaning: str
    image: BytesIO

    def __init__(self, parent: "TarotCard", is_reversed: bool, meaning: str, image_dir: str = "static"):
        self.parent = parent
        self.is_reversed = is_reversed
        self.meaning = meaning

        image = Image.open(Path(__file__).parent / image_dir / self.parent.image_path)
        image.load()
        buffer = BytesIO()
        image.rotate(180 * int(self.is_reversed)).save(buffer, format="PNG")
        buffer.seek(0)
        self.image = buffer


class TarotCard:
    name: str
    type_: TarotCardType
    image_path: str
    variants: tuple[TarotCardVariant, TarotCardVariant]

    def __init__(self, name: str, type_: TarotCardType, image_path: str, meanings: tuple[str, str]):
        self.name = name
        self.type_ = type_
        self.image_path = image_path
        self.meanings = meanings

        normal_meaning, reversed_meaning = meanings
        normal_variant = TarotCardVariant(self, False, normal_meaning)
        reversed_variant = TarotCardVariant(self, True, reversed_meaning)
        self.variants = (normal_variant, reversed_variant)


tarot_cards = [
    TarotCard(
        name="The Magician",
        type_=TarotCardType.major,
        image_path="the_magician.jpg",
        meanings=(
            "Skill, diplomacy, address, subtlety; sickness, pain, loss, disaster, snares of enemies; self-confidence, will; the Querent, if male.",
            "Physician, Magus, mental disease, disgrace, disquiet.",
        ),
    ),
    TarotCard(
        name="The High Priestess",
        type_=TarotCardType.major,
        image_path="the_high_priestess.jpg",
        meanings=(
            "Secrets, mystery, the future as yet unrevealed; the woman who interests the Querent, if male; the Querent herself, if female; silence, tenacity; mystery, wisdom, science.",
            "Passion, moral or physical ardour, conceit, surface knowledge.",
        ),
    ),
    TarotCard(
        name="The Empress",
        type_=TarotCardType.major,
        image_path="the_empress.jpg",
        meanings=(
            "Fruitfulness, action, initiative, length of days; the unknown, clandestine; also difficulty, doubt, ignorance.",
            "Light, truth, the unravelling of involved matters, public rejoicings; according to another reading, vacillation.",
        ),
    ),
    TarotCard(
        name="The Emperor",
        type_=TarotCardType.major,
        image_path="the_emperor.jpg",
        meanings=(
            "Stability, power, protection, realization; a great person; aid, reason, conviction; also authority and will.",
            "Benevolence, compassion, credit; also confusion to enemies, obstruction, immaturity.",
        ),
    ),
    TarotCard(
        name="The Hierophant",
        type_=TarotCardType.major,
        image_path="the_hierophant.jpg",
        meanings=(
            "Marriage, alliance, captivity, servitude; by another account, mercy and goodness; inspiration; the man to whom the Querent has recourse.",
            "Society, good understanding, concord, overkindness, weakness.",
        ),
    ),
    TarotCard(
        name="The Lovers",
        type_=TarotCardType.major,
        image_path="the_lovers.jpg",
        meanings=(
            "Attraction, love, beauty, trials overcome.",
            "Failure, foolish designs. Another account speaks of marriage frustrated and contrarieties of all kinds.",
        ),
    ),
    TarotCard(
        name="The Chariot",
        type_=TarotCardType.major,
        image_path="the_chariot.jpg",
        meanings=(
            "Succour, providence also war, triumph, presumption, vengeance, trouble.",
            "Riot, quarrel, dispute, litigation, defeat.",
        ),
    ),
    TarotCard(
        name="Strength",
        type_=TarotCardType.major,
        image_path="strength.jpg",
        meanings=(
            "Power, energy, action, courage, magnanimity; also complete success and honours.",
            "Despotism, abuse if power, weakness, discord, sometimes even disgrace.",
        ),
    ),
    TarotCard(
        name="The Hermit",
        type_=TarotCardType.major,
        image_path="the_hermit.jpg",
        meanings=(
            "Prudence, circumspection; also and especially treason, dissimulation, roguery, corruption.",
            "Concealment, disguise, policy, fear, unreasoned caution.",
        ),
    ),
    TarotCard(
        name="Wheel Of Fortune",
        type_=TarotCardType.major,
        image_path="wheel_of_fortune.jpg",
        meanings=(
            "Destiny, fortune, success, elevation, luck, felicity.",
            "Increase, abundance, superfluity.",
        ),
    ),
    TarotCard(
        name="Justice",
        type_=TarotCardType.major,
        image_path="justice.jpg",
        meanings=(
            "Equity, rightness, probity, executive; triumph of the deserving side in law.",
            "Law in all its departments, legal complications, bigotry, bias, excessive severity.",
        ),
    ),
    TarotCard(
        name="The Hanged Man",
        type_=TarotCardType.major,
        image_path="the_hanged_man.jpg",
        meanings=(
            "Wisdom, circumspection, discernment, trials, sacrifice, intuition, divination, prophecy.",
            "Selfishness, the crowd, body politic.",
        ),
    ),
    TarotCard(
        name="Death",
        type_=TarotCardType.major,
        image_path="death.jpg",
        meanings=(
            "End, mortality, destruction, corruption also, for a man, the loss of a benefactor for a woman, many contrarieties; for a maid, failure of marriage projects.",
            "Inertia, sleep, lethargy, petrifaction, somnambulism; hope destroyed.",
        ),
    ),
    TarotCard(
        name="Temperance",
        type_=TarotCardType.major,
        image_path="temperance.jpg",
        meanings=(
            "Economy, moderation, frugality, management, accommodation.",
            "Things connected with churches, religions, sects, the priesthood, sometimes even the priest who will marry the Querent; also disunion, unfortunate combinations, competing interests.",
        ),
    ),
    TarotCard(
        name="The Devil",
        type_=TarotCardType.major,
        image_path="the_devil.jpg",
        meanings=(
            "Ravage, violence, vehemence, extraordinary efforts, force, fatality; that which is predestined but is not for this reason evil.",
            "Evil fatality, weakness, pettiness, blindness.",
        ),
    ),
    TarotCard(
        name="The Tower",
        type_=TarotCardType.major,
        image_path="the_tower.jpg",
        meanings=(
            "Misery, distress, indigence, adversity, calamity, disgrace, deception, ruin. It is a card in particular of unforeseen catastrophe.",
            "According to one account, the same in a lesser degree also oppression, imprisonment, tyranny.",
        ),
    ),
    TarotCard(
        name="The Star",
        type_=TarotCardType.major,
        image_path="the_star.jpg",
        meanings=(
            "Loss, theft, privation, abandonment; another reading says-hope and bright prospects,",
            "Arrogance, haughtiness, impotence.",
        ),
    ),
    TarotCard(
        name="The Moon",
        type_=TarotCardType.major,
        image_path="the_moon.jpg",
        meanings=(
            "Hidden enemies, danger, calumny, darkness, terror, deception, occult forces, error.",
            "Instability, inconstancy, silence, lesser degrees of deception and error.",
        ),
    ),
    TarotCard(
        name="The Sun",
        type_=TarotCardType.major,
        image_path="the_sun.jpg",
        meanings=(
            "Material happiness, fortunate marriage, contentment.",
            "The same in a lesser sense.",
        ),
    ),
    TarotCard(
        name="The Last Judgment",
        type_=TarotCardType.major,
        image_path="judgement.jpg",
        meanings=(
            "Change of position, renewal, outcome. Another account specifies total loss though lawsuit.",
            "Weakness, pusillanimity, simplicity; also deliberation, decision, sentence.",
        ),
    ),
    TarotCard(
        name="The Fool",
        type_=TarotCardType.major,
        image_path="the_fool.jpg",
        meanings=(
            "Folly, mania, extravagance, intoxication, delirium, frenzy, bewrayment.",
            "Negligence, absence, distribution, carelessness, apathy, nullity, vanity.",
        ),
    ),
    TarotCard(
        name="The World",
        type_=TarotCardType.major,
        image_path="the_world.jpg",
        meanings=(
            "Assured success, recompense, voyage, route, emigration, flight, change of place.",
            "Inertia, fixity, stagnation, permanence.",
        ),
    ),
    # Minor Arcana - Wands
    TarotCard(
        name="Page of Wands",
        type_=TarotCardType.minor,
        image_path="page_of_wands.jpg",
        meanings=(
            "Dark young man, faithful, a lover, an envoy, a postman. Beside a man, he will bear favourable testimony concerning him. A dangerous rival, if followed by the Page of Cups. Has the chief qualities of his suit. He may signify family intelligence.",
            "Anecdotes, announcements, evil news. Also indecision and the instability which accompanies it.",
        ),
    ),
    TarotCard(
        name="Knight of Wands",
        type_=TarotCardType.minor,
        image_path="knight_of_wands.jpg",
        meanings=(
            "Departure, absence, flight, emigration. A dark young man, friendly. Change of residence.",
            "Rupture, division, interruption, discord.",
        ),
    ),
    TarotCard(
        name="Queen of Wands",
        type_=TarotCardType.minor,
        image_path="queen_of_wands.jpg",
        meanings=(
            "A dark woman, countrywoman, friendly, chaste, loving, honourable. If the card beside her signifies a man, she is well disposed towards him; if a woman, she is interested in the Querent. Also, love of money, or a certain success in business.",
            "Good, economical, obliging, serviceable. Signifies also--but in certain positions and in the neighbourhood of other cards tending in such directions--opposition, jealousy, even deceit and infidelity.",
        ),
    ),
    TarotCard(
        name="King of Wands",
        type_=TarotCardType.minor,
        image_path="king_of_wands.jpg",
        meanings=(
            "Dark man, friendly, countryman, generally married, honest and conscientious. The card always signifies honesty, and may mean news concerning an unexpected heritage to fall in before very long.",
            "Good, but severe; austere, yet tolerant.",
        ),
    ),
    TarotCard(
        name="Ace of Wands",
        type_=TarotCardType.minor,
        image_path="ace_of_wands.jpg",
        meanings=(
            "Creation, invention, enterprise, the powers which result in these; principle, beginning, source; birth, family, origin, and in a sense the virility which is behind them; the starting point of enterprises; according to another account, money, fortune, inheritance.",
            "Fall, decadence, ruin, perdition, to perish also a certain clouded joy.",
        ),
    ),
    TarotCard(
        name="Two of Wands",
        type_=TarotCardType.minor,
        image_path="two_of_wands.jpg",
        meanings=(
            "Between the alternative readings there is no marriage possible; on the one hand, riches, fortune, magnificence; on the other, physical suffering, disease, chagrin, sadness, mortification. The design gives one suggestion; here is a lord overlooking his dominion and alternately contemplating a globe; it looks like the malady, the mortification, the sadness of Alexander amidst the grandeur of this world's wealth.",
            "Surprise, wonder, enchantment, emotion, trouble, fear.",
        ),
    ),
    TarotCard(
        name="Three of Wands",
        type_=TarotCardType.minor,
        image_path="three_of_wands.jpg",
        meanings=(
            "He symbolizes established strength, enterprise, effort, trade, commerce, discovery; those are his ships, bearing his merchandise, which are sailing over the sea. The card also signifies able co-operation in business, as if the successful merchant prince were looking from his side towards yours with a view to help you.",
            "The end of troubles, suspension or cessation of adversity, toil and disappointment.",
        ),
    ),
    TarotCard(
        name="Four of Wands",
        type_=TarotCardType.minor,
        image_path="four_of_wands.jpg",
        meanings=(
            "They are for once almost on the surface--country life, haven of refuge, a species of domestic harvest-home, repose, concord, harmony, prosperity, peace, and the perfected work of these.",
            "The meaning remains unaltered; it is prosperity, increase, felicity, beauty, embellishment.",
        ),
    ),
    TarotCard(
        name="Five of Wands",
        type_=TarotCardType.minor,
        image_path="five_of_wands.jpg",
        meanings=(
            "Imitation, as, for example, sham fight, but also the strenuous competition and struggle of the search after riches and fortune. In this sense it connects with the battle of life. Hence some attributions say that it is a card of gold, gain, opulence.",
            "Litigation, disputes, trickery, contradiction.",
        ),
    ),
    TarotCard(
        name="Six of Wands",
        type_=TarotCardType.minor,
        image_path="six_of_wands.jpg",
        meanings=(
            "The card has been so designed that it can cover several significations; on the surface, it is a victor triumphing, but it is also great news, such as might be carried in state by the King's courier; it is expectation crowned with its own desire, the crown of hope, and so forth.",
            "Apprehension, fear, as of a victorious enemy at the gate; treachery, disloyalty, as of gates being opened to the enemy; also indefinite delay.",
        ),
    ),
    TarotCard(
        name="Seven of Wands",
        type_=TarotCardType.minor,
        image_path="seven_of_wands.jpg",
        meanings=(
            "It is a card of valour, for, on the surface, six are attacking one, who has, however, the vantage position. On the intellectual plane, it signifies discussion, wordy strife; in business--negotiations, war of trade, barter, competition. It is further a card of success, for the combatant is on the top and his enemies may be unable to reach him.",
            "Perplexity, embarrassments, anxiety. It is also a caution against indecision.",
        ),
    ),
    TarotCard(
        name="Eight of Wands",
        type_=TarotCardType.minor,
        image_path="eight_of_wands.jpg",
        meanings=(
            "Activity in undertakings, the path of such activity, swiftness, as that of an express messenger; great haste, great hope, speed towards an end which promises assured felicity; generally, that which is on the move; also the arrows of love.",
            "Arrows of jealousy, internal dispute, stingings of conscience, quarrels; and domestic disputes for persons who are married.",
        ),
    ),
    TarotCard(
        name="Nine of Wands",
        type_=TarotCardType.minor,
        image_path="nine_of_wands.jpg",
        meanings=(
            "The card signifies strength in opposition. If attacked, the person will meet an onslaught boldly; and his build shews, that he may prove a formidable antagonist. With this main significance there are all its possible adjuncts--delay, suspension, adjournment.",
            "Obstacles, adversity, calamity.",
        ),
    ),
    TarotCard(
        name="Ten of Wands",
        type_=TarotCardType.minor,
        image_path="ten_of_wands.jpg",
        meanings=(
            "A card of many significances, and some of the readings cannot be harmonized. I set aside that which connects it with honour and good faith. The chief meaning is oppression simply, but it is also fortune, gain, any kind of success, and then it is the oppression of these things. It is also a card of false-seeming, disguise, perfidy. The place which the figure is approaching may suffer from the rods that he carries. Success is stultified if the Nine of Swords follows, and if it is a question of a lawsuit, there will be certain loss.",
            "Contrarieties, difficulties, intrigues, and their analogies.",
        ),
    ),
    # Minor Arcana - Cups
    TarotCard(
        name="Page of Cups",
        type_=TarotCardType.minor,
        image_path="page_of_cups.jpg",
        meanings=(
            "Fair young man, one impelled to render service and with whom the Querent will be connected; a studious youth; news, message; application, reflection, meditation; also these things directed to business.",
            "Taste, inclination, attachment, seduction, deception, artifice.",
        ),
    ),
    TarotCard(
        name="Knight of Cups",
        type_=TarotCardType.minor,
        image_path="knight_of_cups.jpg",
        meanings=(
            "Arrival, approach--sometimes that of a messenger; advances, proposition, demeanour, invitation, incitement.",
            "Trickery, artifice, subtlety, swindling, duplicity, fraud.",
        ),
    ),
    TarotCard(
        name="Queen of Cups",
        type_=TarotCardType.minor,
        image_path="queen_of_cups.jpg",
        meanings=(
            "Good, fair woman; honest, devoted woman, who will do service to the Querent; loving intelligence, and hence the gift of vision; success, happiness, pleasure; also wisdom, virtue; a perfect spouse and a good mother.",
            "The accounts vary; good woman; otherwise, distinguished woman but one not to be trusted; perverse woman; vice, dishonour, depravity.",
        ),
    ),
    TarotCard(
        name="King of Cups",
        type_=TarotCardType.minor,
        image_path="king_of_cups.jpg",
        meanings=(
            "Fair man, man of business, law, or divinity; responsible, disposed to oblige the Querent; also equity, art and science, including those who profess science, law and art; creative intelligence.",
            "Dishonest, double-dealing man; roguery, exaction, injustice, vice, scandal, pillage, considerable loss.",
        ),
    ),
    TarotCard(
        name="Ace of Cups",
        type_=TarotCardType.minor,
        image_path="ace_of_cups.jpg",
        meanings=(
            "House of the true heart, joy, content, abode, nourishment, abundance, fertility; Holy Table, felicity hereof.",
            "House of the false heart, mutation, instability, revolution.",
        ),
    ),
    TarotCard(
        name="Two of Cups",
        type_=TarotCardType.minor,
        image_path="two_of_cups.jpg",
        meanings=(
            "Love, passion, friendship, affinity, union, concord, sympathy, the interrelation of the sexes, and--as a suggestion apart from all offices of divination--that desire which is not in Nature, but by which Nature is sanctified.",
            'Lust, cupidity, jealousy, wish, desire, but the card may also give, says W., "that desire which is not in nature, but by which nature is sanctified."',
        ),
    ),
    TarotCard(
        name="Three of Cups",
        type_=TarotCardType.minor,
        image_path="three_of_cups.jpg",
        meanings=(
            "The conclusion of any matter in plenty, perfection and merriment; happy issue, victory, fulfilment, solace, healing,",
            "Expedition, dispatch, achievement, end. It signifies also the side of excess in physical enjoyment, and the pleasures of the senses.",
        ),
    ),
    TarotCard(
        name="Four of Cups",
        type_=TarotCardType.minor,
        image_path="four_of_cups.jpg",
        meanings=(
            "Weariness, disgust, aversion, imaginary vexations, as if the wine of this world had caused satiety only; another wine, as if a fairy gift, is now offered the wastrel, but he sees no consolation therein. This is also a card of blended pleasure.",
            "Novelty, presage, new instruction, new relations.",
        ),
    ),
    TarotCard(
        name="Five of Cups",
        type_=TarotCardType.minor,
        image_path="five_of_cups.jpg",
        meanings=(
            "A dark, cloaked figure, looking sideways at three prone cups two others stand upright behind him; a bridge is in the background, leading to a small keep or holding. Divanatory Meanings: It is a card of loss, but something remains over; three have been taken, but two are left; it is a card of inheritance, patrimony, transmission, but not corresponding to expectations; with some interpreters it is a card of marriage, but not without bitterness or frustration.",
            "News, alliances, affinity, consanguinity, ancestry, return, false projects.",
        ),
    ),
    TarotCard(
        name="Six of Cups",
        type_=TarotCardType.minor,
        image_path="six_of_cups.jpg",
        meanings=(
            "A card of the past and of memories, looking back, as--for example--on childhood; happiness, enjoyment, but coming rather from the past; things that have vanished. Another reading reverses this, giving new relations, new knowledge, new environment, and then the children are disporting in an unfamiliar precinct.",
            "The future, renewal, that which will come to pass presently.",
        ),
    ),
    TarotCard(
        name="Seven of Cups",
        type_=TarotCardType.minor,
        image_path="seven_of_cups.jpg",
        meanings=(
            "Fairy favours, images of reflection, sentiment, imagination, things seen in the glass of contemplation; some attainment in these degrees, but nothing permanent or substantial is suggested.",
            "Desire, will, determination, project.",
        ),
    ),
    TarotCard(
        name="Eight of Cups",
        type_=TarotCardType.minor,
        image_path="eight_of_cups.jpg",
        meanings=(
            "The card speaks for itself on the surface, but other readings are entirely antithetical--giving joy, mildness, timidity, honour, modesty. In practice, it is usually found that the card shews the decline of a matter, or that a matter which has been thought to be important is really of slight consequence--either for good or evil.",
            "Great joy, happiness, feasting.",
        ),
    ),
    TarotCard(
        name="Nine of Cups",
        type_=TarotCardType.minor,
        image_path="nine_of_cups.jpg",
        meanings=(
            "Concord, contentment, physical bien-être; also victory, success, advantage; satisfaction for the Querent or person for whom the consultation is made.",
            "Truth, loyalty, liberty; but the readings vary and include mistakes, imperfections, etc.",
        ),
    ),
    TarotCard(
        name="Ten of Cups",
        type_=TarotCardType.minor,
        image_path="ten_of_cups.jpg",
        meanings=(
            "Contentment, repose of the entire heart; the perfection of that state; also perfection of human love and friendship; if with several picture-cards, a person who is taking charge of the Querent's interests; also the town, village or country inhabited by the Querent.",
            "Repose of the false heart, indignation, violence.",
        ),
    ),
    # Minor Arcana - Pentacles
    TarotCard(
        name="Page of Pentacles",
        type_=TarotCardType.minor,
        image_path="page_of_pentacles.jpg",
        meanings=(
            "Application, study, scholarship, reflection another reading says news, messages and the bringer thereof; also rule, management.",
            "Prodigality, dissipation, liberality, luxury; unfavourable news.",
        ),
    ),
    TarotCard(
        name="Knight of Pentacles",
        type_=TarotCardType.minor,
        image_path="knight_of_pentacles.jpg",
        meanings=(
            "Utility, serviceableness, interest, responsibility, rectitude-all on the normal and external plane.",
            "inertia, idleness, repose of that kind, stagnation; also placidity, discouragement, carelessness.",
        ),
    ),
    TarotCard(
        name="Queen of Pentacles",
        type_=TarotCardType.minor,
        image_path="queen_of_pentacles.jpg",
        meanings=(
            "Opulence, generosity, magnificence, security, liberty.",
            "Evil, suspicion, suspense, fear, mistrust.",
        ),
    ),
    TarotCard(
        name="King of Pentacles",
        type_=TarotCardType.minor,
        image_path="king_of_pentacles.jpg",
        meanings=(
            "Valour, realizing intelligence, business and normal intellectual aptitude, sometimes mathematical gifts and attainments of this kind; success in these paths.",
            "Vice, weakness, ugliness, perversity, corruption, peril.",
        ),
    ),
    TarotCard(
        name="Ace of Pentacles",
        type_=TarotCardType.minor,
        image_path="ace_of_pentacles.jpg",
        meanings=(
            "Perfect contentment, felicity, ecstasy; also speedy intelligence; gold.",
            "The evil side of wealth, bad intelligence; also great riches. In any case it shews prosperity, comfortable material conditions, but whether these are of advantage to the possessor will depend on whether the card is reversed or not.",
        ),
    ),
    TarotCard(
        name="Two of Pentacles",
        type_=TarotCardType.minor,
        image_path="two_of_pentacles.jpg",
        meanings=(
            "On the one hand it is represented as a card of gaiety, recreation and its connexions, which is the subject of the design; but it is read also as news and messages in writing, as obstacles, agitation, trouble, embroilment.",
            "Enforced gaiety, simulated enjoyment, literal sense, handwriting, composition, letters of exchange.",
        ),
    ),
    TarotCard(
        name="Three of Pentacles",
        type_=TarotCardType.minor,
        image_path="three_of_pentacles.jpg",
        meanings=(
            "Métier, trade, skilled labour; usually, however, regarded as a card of nobility, aristocracy, renown, glory.",
            "Mediocrity, in work and otherwise, puerility, pettiness, weakness.",
        ),
    ),
    TarotCard(
        name="Four of Pentacles",
        type_=TarotCardType.minor,
        image_path="four_of_pentacles.jpg",
        meanings=(
            "The surety of possessions, cleaving to that which one has, gift, legacy, inheritance.",
            "Suspense, delay, opposition.",
        ),
    ),
    TarotCard(
        name="Five of Pentacles",
        type_=TarotCardType.minor,
        image_path="five_of_pentacles.jpg",
        meanings=(
            "The card foretells material trouble above all, whether in the form illustrated--that is, destitution--or otherwise. For some cartomancists, it is a card of love and lovers-wife, husband, friend, mistress; also concordance, affinities. These alternatives cannot be harmonized.",
            "Disorder, chaos, ruin, discord, profligacy.",
        ),
    ),
    TarotCard(
        name="Six of Pentacles",
        type_=TarotCardType.minor,
        image_path="six_of_pentacles.jpg",
        meanings=(
            "Presents, gifts, gratification another account says attention, vigilance now is the accepted time, present prosperity, etc.",
            "Desire, cupidity, envy, jealousy, illusion.",
        ),
    ),
    TarotCard(
        name="Seven of Pentacles",
        type_=TarotCardType.minor,
        image_path="seven_of_pentacles.jpg",
        meanings=(
            "These are exceedingly contradictory; in the main, it is a card of money, business, barter; but one reading gives altercation, quarrels--and another innocence, ingenuity, purgation.",
            "Cause for anxiety regarding money which it may be proposed to lend.",
        ),
    ),
    TarotCard(
        name="Eight of Pentacles",
        type_=TarotCardType.minor,
        image_path="eight_of_pentacles.jpg",
        meanings=(
            "Work, employment, commission, craftsmanship, skill in craft and business, perhaps in the preparatory stage.",
            "Voided ambition, vanity, cupidity, exaction, usury. It may also signify the possession of skill, in the sense of the ingenious mind turned to cunning and intrigue.",
        ),
    ),
    TarotCard(
        name="Nine of Pentacles",
        type_=TarotCardType.minor,
        image_path="nine_of_pentacles.jpg",
        meanings=(
            "Prudence, safety, success, accomplishment, certitude, discernment.",
            "Roguery, deception, voided project, bad faith.",
        ),
    ),
    TarotCard(
        name="Ten of Pentacles",
        type_=TarotCardType.minor,
        image_path="ten_of_pentacles.jpg",
        meanings=(
            "Gain, riches; family matters, archives, extraction, the abode of a family.",
            "Chance, fatality, loss, robbery, games of hazard; sometimes gift, dowry, pension.",
        ),
    ),
    # Minor Arcana - Swords
    TarotCard(
        name="Page of Swords",
        type_=TarotCardType.minor,
        image_path="page_of_swords.jpg",
        meanings=(
            "Authority, overseeing, secret service, vigilance, spying, examination, and the qualities thereto belonging.",
            "More evil side of these qualities; what is unforeseen, unprepared state; sickness is also intimated.",
        ),
    ),
    TarotCard(
        name="Knight of Swords",
        type_=TarotCardType.minor,
        image_path="knight_of_swords.jpg",
        meanings=(
            "Skill, bravery, capacity, defence, address, enmity, wrath, war, destruction, opposition, resistance, ruin. There is therefore a sense in which the card signifies death, but it carries this meaning only in its proximity to other cards of fatality.",
            "Imprudence, incapacity, extravagance.",
        ),
    ),
    TarotCard(
        name="Queen of Swords",
        type_=TarotCardType.minor,
        image_path="queen_of_swords.jpg",
        meanings=(
            "Widowhood, female sadness and embarrassment, absence, sterility, mourning, privation, separation.",
            "Malice, bigotry, artifice, prudery, bale, deceit.",
        ),
    ),
    TarotCard(
        name="King of Swords",
        type_=TarotCardType.minor,
        image_path="king_of_swords.jpg",
        meanings=(
            "Whatsoever arises out of the idea of judgment and all its connexions-power, command, authority, militant intelligence, law, offices of the crown, and so forth.",
            "Cruelty, perversity, barbarity, perfidy, evil intention.",
        ),
    ),
    TarotCard(
        name="Ace of Swords",
        type_=TarotCardType.minor,
        image_path="ace_of_swords.jpg",
        meanings=(
            "Triumph, the excessive degree in everything, conquest, triumph of force. It is a card of great force, in love as well as in hatred. The crown may carry a much higher significance than comes usually within the sphere of fortune-telling.",
            "The same, but the results are disastrous; another account says--conception, childbirth, augmentation, multiplicity.",
        ),
    ),
    TarotCard(
        name="Two of Swords",
        type_=TarotCardType.minor,
        image_path="two_of_swords.jpg",
        meanings=(
            "Conformity and the equipoise which it suggests, courage, friendship, concord in a state of arms; another reading gives tenderness, affection, intimacy. The suggestion of harmony and other favourable readings must be considered in a qualified manner, as Swords generally are not symbolical of beneficent forces in human affairs.",
            "Imposture, falsehood, duplicity, disloyalty.",
        ),
    ),
    TarotCard(
        name="Three of Swords",
        type_=TarotCardType.minor,
        image_path="three_of_swords.jpg",
        meanings=(
            "Removal, absence, delay, division, rupture, dispersion, and all that the design signifies naturally, being too simple and obvious to call for specific enumeration.",
            "Mental alienation, error, loss, distraction, disorder, confusion.",
        ),
    ),
    TarotCard(
        name="Four of Swords",
        type_=TarotCardType.minor,
        image_path="four_of_swords.jpg",
        meanings=(
            "Vigilance, retreat, solitude, hermit's repose, exile, tomb and coffin. It is these last that have suggested the design.",
            "Wise administration, circumspection, economy, avarice, precaution, testament.",
        ),
    ),
    TarotCard(
        name="Five of Swords",
        type_=TarotCardType.minor,
        image_path="five_of_swords.jpg",
        meanings=(
            "Degradation, destruction, revocation, infamy, dishonour, loss, with the variants and analogues of these.",
            "The same; burial and obsequies.",
        ),
    ),
    TarotCard(
        name="Six of Swords",
        type_=TarotCardType.minor,
        image_path="six_of_swords.jpg",
        meanings=(
            "Journey by water, route, way, envoy, commissionary, expedient.",
            "Declaration, confession, publicity; one account says that it is a proposal of love.",
        ),
    ),
    TarotCard(
        name="Seven of Swords",
        type_=TarotCardType.minor,
        image_path="seven_of_swords.jpg",
        meanings=(
            "Design, attempt, wish, hope, confidence; also quarrelling, a plan that may fail, annoyance. The design is uncertain in its import, because the significations are widely at variance with each other.",
            "Good advice, counsel, instruction, slander, babbling.",
        ),
    ),
    TarotCard(
        name="Eight of Swords",
        type_=TarotCardType.minor,
        image_path="eight_of_swords.jpg",
        meanings=(
            "Bad news, violent chagrin, crisis, censure, power in trammels, conflict, calumny; also sickness.",
            "Disquiet, difficulty, opposition, accident, treachery; what is unforeseen; fatality.",
        ),
    ),
    TarotCard(
        name="Nine of Swords",
        type_=TarotCardType.minor,
        image_path="nine_of_swords.jpg",
        meanings=(
            "Death, failure, miscarriage, delay, deception, disappointment, despair.",
            "Imprisonment, suspicion, doubt, reasonable fear, shame.",
        ),
    ),
    TarotCard(
        name="Ten of Swords",
        type_=TarotCardType.minor,
        image_path="ten_of_swords.jpg",
        meanings=(
            "Whatsoever is intimated by the design; also pain, affliction, tears, sadness, desolation. It is not especially a card of violent death.",
            "Advantage, profit, success, favour, but none of these are permanent; also power and authority.",
        ),
    ),
]
