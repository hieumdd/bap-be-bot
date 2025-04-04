from enum import Enum
from io import BytesIO

from PIL import Image
from pydantic import BaseModel


class TarotCardType(str, Enum):
    major = "major"
    minor = "minor"


class TarotCard(BaseModel):
    type_: TarotCardType
    image_path: str
    name: str
    meaning: str
    meaning_rev: str

    def get_image(self) -> BytesIO:
        with open(f"./app/tarot/tarot_card_static/{self.image_path}", "rb") as f:
            io = BytesIO(f.read())
        io.seek(0)
        return io

    def get_image_rev(self) -> BytesIO:
        image = Image.open(self.get_image())
        io = BytesIO()
        image.rotate(180).save(io, format="JPEG")
        io.seek(0)
        return io


tarot_cards = [
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_magician.jpg",
        name="The Magician",
        meaning="Skill, diplomacy, address, subtlety; sickness, pain, loss, disaster, snares of enemies; self-confidence, will; the Querent, if male.",
        meaning_rev="Physician, Magus, mental disease, disgrace, disquiet.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_high_priestess.jpg",
        name="The High Priestess",
        meaning="Secrets, mystery, the future as yet unrevealed; the woman who interests the Querent, if male; the Querent herself, if female; silence, tenacity; mystery, wisdom, science.",
        meaning_rev="Passion, moral or physical ardour, conceit, surface knowledge.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_empress.jpg",
        name="The Empress",
        meaning="Fruitfulness, action, initiative, length of days; the unknown, clandestine; also difficulty, doubt, ignorance.",
        meaning_rev="Light, truth, the unravelling of involved matters, public rejoicings; according to another reading, vacillation.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_emperor.jpg",
        name="The Emperor",
        meaning="Stability, power, protection, realization; a great person; aid, reason, conviction; also authority and will.",
        meaning_rev="Benevolence, compassion, credit; also confusion to enemies, obstruction, immaturity.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_hierophant.jpg",
        name="The Hierophant",
        meaning="Marriage, alliance, captivity, servitude; by another account, mercy and goodness; inspiration; the man to whom the Querent has recourse.",
        meaning_rev="Society, good understanding, concord, overkindness, weakness.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_lovers.jpg",
        name="The Lovers",
        meaning="Attraction, love, beauty, trials overcome.",
        meaning_rev="Failure, foolish designs. Another account speaks of marriage frustrated and contrarieties of all kinds.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_chariot.jpg",
        name="The Chariot",
        meaning="Succour, providence also war, triumph, presumption, vengeance, trouble.",
        meaning_rev="Riot, quarrel, dispute, litigation, defeat.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="strength.jpg",
        name="Strength",
        meaning="Power, energy, action, courage, magnanimity; also complete success and honours.",
        meaning_rev="Despotism, abuse if power, weakness, discord, sometimes even disgrace.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_hermit.jpg",
        name="The Hermit",
        meaning="Prudence, circumspection; also and especially treason, dissimulation, roguery, corruption.",
        meaning_rev="Concealment, disguise, policy, fear, unreasoned caution.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="wheel_of_fortune.jpg",
        name="Wheel Of Fortune",
        meaning="Destiny, fortune, success, elevation, luck, felicity.",
        meaning_rev="Increase, abundance, superfluity.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="justice.jpg",
        name="Justice",
        meaning="Equity, rightness, probity, executive; triumph of the deserving side in law.",
        meaning_rev="Law in all its departments, legal complications, bigotry, bias, excessive severity.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_hanged_man.jpg",
        name="The Hanged Man",
        meaning="Wisdom, circumspection, discernment, trials, sacrifice, intuition, divination, prophecy.",
        meaning_rev="Selfishness, the crowd, body politic.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="death.jpg",
        name="Death",
        meaning="End, mortality, destruction, corruption also, for a man, the loss of a benefactor for a woman, many contrarieties; for a maid, failure of marriage projects.",
        meaning_rev="Inertia, sleep, lethargy, petrifaction, somnambulism; hope destroyed.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="temperance.jpg",
        name="Temperance",
        meaning="Economy, moderation, frugality, management, accommodation.",
        meaning_rev="Things connected with churches, religions, sects, the priesthood, sometimes even the priest who will marry the Querent; also disunion, unfortunate combinations, competing interests.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_devil.jpg",
        name="The Devil",
        meaning="Ravage, violence, vehemence, extraordinary efforts, force, fatality; that which is predestined but is not for this reason evil.",
        meaning_rev="Evil fatality, weakness, pettiness, blindness.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_tower.jpg",
        name="The Tower",
        meaning="Misery, distress, indigence, adversity, calamity, disgrace, deception, ruin. It is a card in particular of unforeseen catastrophe.",
        meaning_rev="According to one account, the same in a lesser degree also oppression, imprisonment, tyranny.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_star.jpg",
        name="The Star",
        meaning="Loss, theft, privation, abandonment; another reading says-hope and bright prospects,",
        meaning_rev="Arrogance, haughtiness, impotence.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_moon.jpg",
        name="The Moon",
        meaning="Hidden enemies, danger, calumny, darkness, terror, deception, occult forces, error.",
        meaning_rev="Instability, inconstancy, silence, lesser degrees of deception and error.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_sun.jpg",
        name="The Sun",
        meaning="Material happiness, fortunate marriage, contentment.",
        meaning_rev="The same in a lesser sense.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="judgement.jpg",
        name="The Last Judgment",
        meaning="Change of position, renewal, outcome. Another account specifies total loss though lawsuit.",
        meaning_rev="Weakness, pusillanimity, simplicity; also deliberation, decision, sentence.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_fool.jpg",
        name="The Fool",
        meaning="Folly, mania, extravagance, intoxication, delirium, frenzy, bewrayment.",
        meaning_rev="Negligence, absence, distribution, carelessness, apathy, nullity, vanity.",
    ),
    TarotCard(
        type_=TarotCardType.major,
        image_path="the_world.jpg",
        name="The World",
        meaning="Assured success, recompense, voyage, route, emigration, flight, change of place.",
        meaning_rev="Inertia, fixity, stagnation, permanence.",
    ),
    # Minor Arcana - Wands
    TarotCard(
        type_=TarotCardType.minor,
        image_path="page_of_wands.jpg",
        name="Page of Wands",
        meaning="Dark young man, faithful, a lover, an envoy, a postman. Beside a man, he will bear favourable testimony concerning him. A dangerous rival, if followed by the Page of Cups. Has the chief qualities of his suit. He may signify family intelligence.",
        meaning_rev="Anecdotes, announcements, evil news. Also indecision and the instability which accompanies it.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="knight_of_wands.jpg",
        name="Knight of Wands",
        meaning="Departure, absence, flight, emigration. A dark young man, friendly. Change of residence.",
        meaning_rev="Rupture, division, interruption, discord.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="queen_of_wands.jpg",
        name="Queen of Wands",
        meaning="A dark woman, countrywoman, friendly, chaste, loving, honourable. If the card beside her signifies a man, she is well disposed towards him; if a woman, she is interested in the Querent. Also, love of money, or a certain success in business.",
        meaning_rev="Good, economical, obliging, serviceable. Signifies also--but in certain positions and in the neighbourhood of other cards tending in such directions--opposition, jealousy, even deceit and infidelity.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="king_of_wands.jpg",
        name="King of Wands",
        meaning="Dark man, friendly, countryman, generally married, honest and conscientious. The card always signifies honesty, and may mean news concerning an unexpected heritage to fall in before very long.",
        meaning_rev="Good, but severe; austere, yet tolerant.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="ace_of_wands.jpg",
        name="Ace of Wands",
        meaning="Creation, invention, enterprise, the powers which result in these; principle, beginning, source; birth, family, origin, and in a sense the virility which is behind them; the starting point of enterprises; according to another account, money, fortune, inheritance.",
        meaning_rev="Fall, decadence, ruin, perdition, to perish also a certain clouded joy.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="two_of_wands.jpg",
        name="Two of Wands",
        meaning="Between the alternative readings there is no marriage possible; on the one hand, riches, fortune, magnificence; on the other, physical suffering, disease, chagrin, sadness, mortification. The design gives one suggestion; here is a lord overlooking his dominion and alternately contemplating a globe; it looks like the malady, the mortification, the sadness of Alexander amidst the grandeur of this world's wealth.",
        meaning_rev="Surprise, wonder, enchantment, emotion, trouble, fear.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="three_of_wands.jpg",
        name="Three of Wands",
        meaning="He symbolizes established strength, enterprise, effort, trade, commerce, discovery; those are his ships, bearing his merchandise, which are sailing over the sea. The card also signifies able co-operation in business, as if the successful merchant prince were looking from his side towards yours with a view to help you.",
        meaning_rev="The end of troubles, suspension or cessation of adversity, toil and disappointment.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="four_of_wands.jpg",
        name="Four of Wands",
        meaning="They are for once almost on the surface--country life, haven of refuge, a species of domestic harvest-home, repose, concord, harmony, prosperity, peace, and the perfected work of these.",
        meaning_rev="The meaning remains unaltered; it is prosperity, increase, felicity, beauty, embellishment.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="five_of_wands.jpg",
        name="Five of Wands",
        meaning="Imitation, as, for example, sham fight, but also the strenuous competition and struggle of the search after riches and fortune. In this sense it connects with the battle of life. Hence some attributions say that it is a card of gold, gain, opulence.",
        meaning_rev="Litigation, disputes, trickery, contradiction.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="six_of_wands.jpg",
        name="Six of Wands",
        meaning="The card has been so designed that it can cover several significations; on the surface, it is a victor triumphing, but it is also great news, such as might be carried in state by the King's courier; it is expectation crowned with its own desire, the crown of hope, and so forth.",
        meaning_rev="Apprehension, fear, as of a victorious enemy at the gate; treachery, disloyalty, as of gates being opened to the enemy; also indefinite delay.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="seven_of_wands.jpg",
        name="Seven of Wands",
        meaning="It is a card of valour, for, on the surface, six are attacking one, who has, however, the vantage position. On the intellectual plane, it signifies discussion, wordy strife; in business--negotiations, war of trade, barter, competition. It is further a card of success, for the combatant is on the top and his enemies may be unable to reach him.",
        meaning_rev="Perplexity, embarrassments, anxiety. It is also a caution against indecision.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="eight_of_wands.jpg",
        name="Eight of Wands",
        meaning="Activity in undertakings, the path of such activity, swiftness, as that of an express messenger; great haste, great hope, speed towards an end which promises assured felicity; generally, that which is on the move; also the arrows of love.",
        meaning_rev="Arrows of jealousy, internal dispute, stingings of conscience, quarrels; and domestic disputes for persons who are married.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="nine_of_wands.jpg",
        name="Nine of Wands",
        meaning="The card signifies strength in opposition. If attacked, the person will meet an onslaught boldly; and his build shews, that he may prove a formidable antagonist. With this main significance there are all its possible adjuncts--delay, suspension, adjournment.",
        meaning_rev="Obstacles, adversity, calamity.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="ten_of_wands.jpg",
        name="Ten of Wands",
        meaning="A card of many significances, and some of the readings cannot be harmonized. I set aside that which connects it with honour and good faith. The chief meaning is oppression simply, but it is also fortune, gain, any kind of success, and then it is the oppression of these things. It is also a card of false-seeming, disguise, perfidy. The place which the figure is approaching may suffer from the rods that he carries. Success is stultified if the Nine of Swords follows, and if it is a question of a lawsuit, there will be certain loss.",
        meaning_rev="Contrarieties, difficulties, intrigues, and their analogies.",
    ),
    # Minor Arcana - Cups
    TarotCard(
        type_=TarotCardType.minor,
        image_path="page_of_cups.jpg",
        name="Page of Cups",
        meaning="Fair young man, one impelled to render service and with whom the Querent will be connected; a studious youth; news, message; application, reflection, meditation; also these things directed to business.",
        meaning_rev="Taste, inclination, attachment, seduction, deception, artifice.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="knight_of_cups.jpg",
        name="Knight of Cups",
        meaning="Arrival, approach--sometimes that of a messenger; advances, proposition, demeanour, invitation, incitement.",
        meaning_rev="Trickery, artifice, subtlety, swindling, duplicity, fraud.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="queen_of_cups.jpg",
        name="Queen of Cups",
        meaning="Good, fair woman; honest, devoted woman, who will do service to the Querent; loving intelligence, and hence the gift of vision; success, happiness, pleasure; also wisdom, virtue; a perfect spouse and a good mother.",
        meaning_rev="The accounts vary; good woman; otherwise, distinguished woman but one not to be trusted; perverse woman; vice, dishonour, depravity.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="king_of_cups.jpg",
        name="King of Cups",
        meaning="Fair man, man of business, law, or divinity; responsible, disposed to oblige the Querent; also equity, art and science, including those who profess science, law and art; creative intelligence.",
        meaning_rev="Dishonest, double-dealing man; roguery, exaction, injustice, vice, scandal, pillage, considerable loss.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="ace_of_cups.jpg",
        name="Ace of Cups",
        meaning="House of the true heart, joy, content, abode, nourishment, abundance, fertility; Holy Table, felicity hereof.",
        meaning_rev="House of the false heart, mutation, instability, revolution.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="two_of_cups.jpg",
        name="Two of Cups",
        meaning="Love, passion, friendship, affinity, union, concord, sympathy, the interrelation of the sexes, and--as a suggestion apart from all offices of divination--that desire which is not in Nature, but by which Nature is sanctified.",
        meaning_rev='Lust, cupidity, jealousy, wish, desire, but the card may also give, says W., "that desire which is not in nature, but by which nature is sanctified."',
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="three_of_cups.jpg",
        name="Three of Cups",
        meaning="The conclusion of any matter in plenty, perfection and merriment; happy issue, victory, fulfilment, solace, healing,",
        meaning_rev="Expedition, dispatch, achievement, end. It signifies also the side of excess in physical enjoyment, and the pleasures of the senses.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="four_of_cups.jpg",
        name="Four of Cups",
        meaning="Weariness, disgust, aversion, imaginary vexations, as if the wine of this world had caused satiety only; another wine, as if a fairy gift, is now offered the wastrel, but he sees no consolation therein. This is also a card of blended pleasure.",
        meaning_rev="Novelty, presage, new instruction, new relations.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="five_of_cups.jpg",
        name="Five of Cups",
        meaning="A dark, cloaked figure, looking sideways at three prone cups two others stand upright behind him; a bridge is in the background, leading to a small keep or holding. Divanatory Meanings: It is a card of loss, but something remains over; three have been taken, but two are left; it is a card of inheritance, patrimony, transmission, but not corresponding to expectations; with some interpreters it is a card of marriage, but not without bitterness or frustration.",
        meaning_rev="News, alliances, affinity, consanguinity, ancestry, return, false projects.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="six_of_cups.jpg",
        name="Six of Cups",
        meaning="A card of the past and of memories, looking back, as--for example--on childhood; happiness, enjoyment, but coming rather from the past; things that have vanished. Another reading reverses this, giving new relations, new knowledge, new environment, and then the children are disporting in an unfamiliar precinct.",
        meaning_rev="The future, renewal, that which will come to pass presently.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="seven_of_cups.jpg",
        name="Seven of Cups",
        meaning="Fairy favours, images of reflection, sentiment, imagination, things seen in the glass of contemplation; some attainment in these degrees, but nothing permanent or substantial is suggested.",
        meaning_rev="Desire, will, determination, project.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="eight_of_cups.jpg",
        name="Eight of Cups",
        meaning="The card speaks for itself on the surface, but other readings are entirely antithetical--giving joy, mildness, timidity, honour, modesty. In practice, it is usually found that the card shews the decline of a matter, or that a matter which has been thought to be important is really of slight consequence--either for good or evil.",
        meaning_rev="Great joy, happiness, feasting.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="nine_of_cups.jpg",
        name="Nine of Cups",
        meaning="Concord, contentment, physical bien-être; also victory, success, advantage; satisfaction for the Querent or person for whom the consultation is made.",
        meaning_rev="Truth, loyalty, liberty; but the readings vary and include mistakes, imperfections, etc.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="ten_of_cups.jpg",
        name="Ten of Cups",
        meaning="Contentment, repose of the entire heart; the perfection of that state; also perfection of human love and friendship; if with several picture-cards, a person who is taking charge of the Querent's interests; also the town, village or country inhabited by the Querent.",
        meaning_rev="Repose of the false heart, indignation, violence.",
    ),
    # Minor Arcana - Pentacles
    TarotCard(
        type_=TarotCardType.minor,
        image_path="page_of_pentacles.jpg",
        name="Page of Pentacles",
        meaning="Application, study, scholarship, reflection another reading says news, messages and the bringer thereof; also rule, management.",
        meaning_rev="Prodigality, dissipation, liberality, luxury; unfavourable news.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="knight_of_pentacles.jpg",
        name="Knight of Pentacles",
        meaning="Utility, serviceableness, interest, responsibility, rectitude-all on the normal and external plane.",
        meaning_rev="inertia, idleness, repose of that kind, stagnation; also placidity, discouragement, carelessness.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="queen_of_pentacles.jpg",
        name="Queen of Pentacles",
        meaning="Opulence, generosity, magnificence, security, liberty.",
        meaning_rev="Evil, suspicion, suspense, fear, mistrust.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="king_of_pentacles.jpg",
        name="King of Pentacles",
        meaning="Valour, realizing intelligence, business and normal intellectual aptitude, sometimes mathematical gifts and attainments of this kind; success in these paths.",
        meaning_rev="Vice, weakness, ugliness, perversity, corruption, peril.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="ace_of_pentacles.jpg",
        name="Ace of Pentacles",
        meaning="Perfect contentment, felicity, ecstasy; also speedy intelligence; gold.",
        meaning_rev="The evil side of wealth, bad intelligence; also great riches. In any case it shews prosperity, comfortable material conditions, but whether these are of advantage to the possessor will depend on whether the card is reversed or not.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="two_of_pentacles.jpg",
        name="Two of Pentacles",
        meaning="On the one hand it is represented as a card of gaiety, recreation and its connexions, which is the subject of the design; but it is read also as news and messages in writing, as obstacles, agitation, trouble, embroilment.",
        meaning_rev="Enforced gaiety, simulated enjoyment, literal sense, handwriting, composition, letters of exchange.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="three_of_pentacles.jpg",
        name="Three of Pentacles",
        meaning="Métier, trade, skilled labour; usually, however, regarded as a card of nobility, aristocracy, renown, glory.",
        meaning_rev="Mediocrity, in work and otherwise, puerility, pettiness, weakness.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="four_of_pentacles.jpg",
        name="Four of Pentacles",
        meaning="The surety of possessions, cleaving to that which one has, gift, legacy, inheritance.",
        meaning_rev="Suspense, delay, opposition.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="five_of_pentacles.jpg",
        name="Five of Pentacles",
        meaning="The card foretells material trouble above all, whether in the form illustrated--that is, destitution--or otherwise. For some cartomancists, it is a card of love and lovers-wife, husband, friend, mistress; also concordance, affinities. These alternatives cannot be harmonized.",
        meaning_rev="Disorder, chaos, ruin, discord, profligacy.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="six_of_pentacles.jpg",
        name="Six of Pentacles",
        meaning="Presents, gifts, gratification another account says attention, vigilance now is the accepted time, present prosperity, etc.",
        meaning_rev="Desire, cupidity, envy, jealousy, illusion.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="seven_of_pentacles.jpg",
        name="Seven of Pentacles",
        meaning="These are exceedingly contradictory; in the main, it is a card of money, business, barter; but one reading gives altercation, quarrels--and another innocence, ingenuity, purgation.",
        meaning_rev="Cause for anxiety regarding money which it may be proposed to lend.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="eight_of_pentacles.jpg",
        name="Eight of Pentacles",
        meaning="Work, employment, commission, craftsmanship, skill in craft and business, perhaps in the preparatory stage.",
        meaning_rev="Voided ambition, vanity, cupidity, exaction, usury. It may also signify the possession of skill, in the sense of the ingenious mind turned to cunning and intrigue.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="nine_of_pentacles.jpg",
        name="Nine of Pentacles",
        meaning="Prudence, safety, success, accomplishment, certitude, discernment.",
        meaning_rev="Roguery, deception, voided project, bad faith.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="ten_of_pentacles.jpg",
        name="Ten of Pentacles",
        meaning="Gain, riches; family matters, archives, extraction, the abode of a family.",
        meaning_rev="Chance, fatality, loss, robbery, games of hazard; sometimes gift, dowry, pension.",
    ),
    # Minor Arcana - Swords
    TarotCard(
        type_=TarotCardType.minor,
        image_path="page_of_swords.jpg",
        name="Page of Swords",
        meaning="Authority, overseeing, secret service, vigilance, spying, examination, and the qualities thereto belonging.",
        meaning_rev="More evil side of these qualities; what is unforeseen, unprepared state; sickness is also intimated.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="knight_of_swords.jpg",
        name="Knight of Swords",
        meaning="Skill, bravery, capacity, defence, address, enmity, wrath, war, destruction, opposition, resistance, ruin. There is therefore a sense in which the card signifies death, but it carries this meaning only in its proximity to other cards of fatality.",
        meaning_rev="Imprudence, incapacity, extravagance.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="queen_of_swords.jpg",
        name="Queen of Swords",
        meaning="Widowhood, female sadness and embarrassment, absence, sterility, mourning, privation, separation.",
        meaning_rev="Malice, bigotry, artifice, prudery, bale, deceit.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="king_of_swords.jpg",
        name="King of Swords",
        meaning="Whatsoever arises out of the idea of judgment and all its connexions-power, command, authority, militant intelligence, law, offices of the crown, and so forth.",
        meaning_rev="Cruelty, perversity, barbarity, perfidy, evil intention.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="ace_of_swords.jpg",
        name="Ace of Swords",
        meaning="Triumph, the excessive degree in everything, conquest, triumph of force. It is a card of great force, in love as well as in hatred. The crown may carry a much higher significance than comes usually within the sphere of fortune-telling.",
        meaning_rev="The same, but the results are disastrous; another account says--conception, childbirth, augmentation, multiplicity.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="two_of_swords.jpg",
        name="Two of Swords",
        meaning="Conformity and the equipoise which it suggests, courage, friendship, concord in a state of arms; another reading gives tenderness, affection, intimacy. The suggestion of harmony and other favourable readings must be considered in a qualified manner, as Swords generally are not symbolical of beneficent forces in human affairs.",
        meaning_rev="Imposture, falsehood, duplicity, disloyalty.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="three_of_swords.jpg",
        name="Three of Swords",
        meaning="Removal, absence, delay, division, rupture, dispersion, and all that the design signifies naturally, being too simple and obvious to call for specific enumeration.",
        meaning_rev="Mental alienation, error, loss, distraction, disorder, confusion.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="four_of_swords.jpg",
        name="Four of Swords",
        meaning="Vigilance, retreat, solitude, hermit's repose, exile, tomb and coffin. It is these last that have suggested the design.",
        meaning_rev="Wise administration, circumspection, economy, avarice, precaution, testament.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="five_of_swords.jpg",
        name="Five of Swords",
        meaning="Degradation, destruction, revocation, infamy, dishonour, loss, with the variants and analogues of these.",
        meaning_rev="The same; burial and obsequies.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="six_of_swords.jpg",
        name="Six of Swords",
        meaning="Journey by water, route, way, envoy, commissionary, expedient.",
        meaning_rev="Declaration, confession, publicity; one account says that it is a proposal of love.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="seven_of_swords.jpg",
        name="Seven of Swords",
        meaning="Design, attempt, wish, hope, confidence; also quarrelling, a plan that may fail, annoyance. The design is uncertain in its import, because the significations are widely at variance with each other.",
        meaning_rev="Good advice, counsel, instruction, slander, babbling.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="eight_of_swords.jpg",
        name="Eight of Swords",
        meaning="Bad news, violent chagrin, crisis, censure, power in trammels, conflict, calumny; also sickness.",
        meaning_rev="Disquiet, difficulty, opposition, accident, treachery; what is unforeseen; fatality.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="nine_of_swords.jpg",
        name="Nine of Swords",
        meaning="Death, failure, miscarriage, delay, deception, disappointment, despair.",
        meaning_rev="Imprisonment, suspicion, doubt, reasonable fear, shame.",
    ),
    TarotCard(
        type_=TarotCardType.minor,
        image_path="ten_of_swords.jpg",
        name="Ten of Swords",
        meaning="Whatsoever is intimated by the design; also pain, affliction, tears, sadness, desolation. It is not especially a card of violent death.",
        meaning_rev="Advantage, profit, success, favour, but none of these are permanent; also power and authority.",
    ),
]
