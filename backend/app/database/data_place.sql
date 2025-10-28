-- ####################### REGION ##############################
-- ##--------------- ROHAN  -------------------------##
-- Image principale de la région
UPDATE places
SET image_url = '/place/rohan.png'
WHERE title = 'Rohan';

-- ############################# PLACE #################################
-- ##--------------- MINAS TIRITH -------------------------##
-- Image principale du lieu
UPDATE places
SET image_url = '/place/minas-tirith.png'
WHERE title = 'Minas Tirith';

-- ==================== SECTIONS DÉTAILLÉES ====================

INSERT INTO entity_descriptions (title, content, image_url, order_index, entity_type, entity_id)
VALUES

-- -------------------- 1. ARCHITECTURE --------------------
(
    'Architecture',
    'Minas Tirith, la Tour de Garde, est une merveille architecturale construite sur sept niveaux successifs, taillés dans le flanc du Mont Mindolluin. Chaque niveau est entouré de remparts de pierre blanche étincelante, d''où son surnom de "Cité Blanche".

Les sept cercles sont disposés en arc de cercle, chacun tourné vers l''est face à Mordor. Les murs font entre 30 et 50 pieds de hauteur selon les niveaux, construits en pierre de Gondor qui brille sous le soleil. Chaque porte est décalée par rapport à la précédente, obligeant les assaillants à traverser toute la largeur de chaque niveau.

Au sommet du septième niveau se dresse la Citadelle et la Tour d''Ecthelion, une flèche d''argent de 300 pieds de hauteur visible à des lieues à la ronde. Le sommet de la tour abrite une chambre vitrée d''où les gardiens scrutent l''horizon jour et nuit.

La Grande Porte du premier niveau est forgée en acier et fer, haute de 40 pieds, ornée de motifs représentant les Sept Étoiles et la Couronne du Gondor. Elle peut résister aux béliers les plus puissants.',
    '/place/ornement-separation.png',
    1,
    'place',
    (SELECT id FROM places WHERE title = 'Minas Tirith')
),

-- -------------------- 2. HISTOIRE --------------------
(
    'Histoire',
    'Minas Tirith fut construite en l''an 3320 du Deuxième Âge sous le nom de Minas Anor (Tour du Soleil), sœur jumelle de Minas Ithil (Tour de la Lune). Elle servait de forteresse occidentale gardant le Gondor contre les menaces venues de Mordor.

Après la chute de Minas Ithil aux mains des Nazgûl en 2002 du Troisième Âge, qui devint Minas Morgul, Minas Anor fut rebaptisée Minas Tirith (Tour de Garde). En 2050, elle devint la capitale du Gondor après l''abandon d''Osgiliath, ravagée par la peste et les guerres.

Durant près de mille ans, la cité fut gouvernée par les Intendants du Gondor, en l''absence du roi. Le dernier roi, Eärnur, disparut en 2050 en répondant au défi du Roi-Sorcier d''Angmar.

En mars 3019 du Troisième Âge, Minas Tirith subit le siège le plus terrible de son histoire lors de la Guerre de l''Anneau. Les forces de Sauron, menées par le Roi-Sorcier, déferlèrent sur la ville. La Grande Porte fut brisée, mais la cité tint bon jusqu''à l''arrivée des Rohirrim et la victoire de la Bataille des Champs du Pelennor.

Le 1er mai 3019, Aragorn II Elessar fut couronné roi dans la Cité Blanche, restaurant la lignée royale après 969 ans d''interruption.',
    '/place/ornement-separation.png',
    2,
    'place',
    (SELECT id FROM places WHERE title = 'Minas Tirith')
),

-- -------------------- 3. LES SEPT NIVEAUX --------------------
(
    'Les Sept Niveaux',
    'PREMIER NIVEAU : Le niveau le plus bas et le plus vaste, abritant les marchés, les auberges, les entrepôts et les casernes de la garde. C''est ici que bat le cœur commercial de la cité. La population : environ 15 000 habitants.

DEUXIÈME NIVEAU : Quartier résidentiel des artisans et marchands prospères. On y trouve les forges les plus réputées du Gondor, les ateliers de tissage et les échoppes de luxe.

TROISIÈME NIVEAU : Résidences des familles nobles de moindre rang, des capitaines de la garde et des hauts fonctionnaires. Jardins privés ornés de fontaines.

QUATRIÈME NIVEAU : Quartier aristocratique, maisons de pierre blanche avec cours intérieures et jardins suspendus. Demeure de nombreux seigneurs du Gondor.

CINQUIÈME NIVEAU : Les plus hautes familles nobles, proches de la Citadelle. Architecture raffinée, galeries couvertes, bibliothèques privées.

SIXIÈME NIVEAU : Casernes d''élite de la Garde de la Citadelle, armureries, écuries royales, et la Maison de Guérison avec ses jardins d''herbes médicinales.

SEPTIÈME NIVEAU : La Citadelle elle-même. Cour du Roi avec l''Arbre Blanc, Salle du Trône, Salle des Festins, Tour d''Ecthelion, et entrée des Tombeaux des Rois et des Intendants creusés dans la montagne.',
    '/place/ornement-separation.png',
    3,
    'place',
    (SELECT id FROM places WHERE title = 'Minas Tirith')
),

-- -------------------- 4. LIEUX REMARQUABLES --------------------
(
    'Lieux remarquables',
    'L''ARBRE BLANC : Dans la cour de la Citadelle pousse l''Arbre Blanc de Gondor, descendant de Nimloth, lui-même issu de Telperion, l''un des Deux Arbres de Valinor. L''arbre se dessécha sous le règne des Intendants, mais un rejeton fut découvert par Aragorn sur les pentes du Mindolluin et replanté lors de son couronnement.

LA TOUR D''ECTHELION : Nommée d''après l''Intendant qui la fit reconstruire, cette flèche d''argent culmine à 300 pieds. Son sommet abrite une salle vitrée où brûle un feu de veille. De là, les signaux de feu peuvent être allumés pour appeler Rohan.

LES TOMBEAUX : Creusés dans la montagne derrière la Citadelle, les Tombeaux abritent les sépultures des Rois de Gondor et des Intendants. Longs couloirs de pierre noire, statues gisantes sur les sarcophages, silence éternel gardé par les statues des rois.

LA MAISON DE GUÉRISON : Au sixième niveau, vaste complexe médical avec salles de soins, jardins d''herbes médicinales cultivés par les guérisseurs. C''est ici que Faramir, Éowyn et Merry furent soignés après la bataille.

LA GRANDE SALLE : Immense salle du trône pouvant accueillir des centaines de personnes. Colonnes de marbre noir, plafond voûté, trône de pierre noire avec sept marches. Les bannières des grandes maisons du Gondor pendent des murs.

LES FONTAINES : Chaque niveau possède sa fontaine centrale, alimentée par les sources du Mindolluin. La plus belle est celle de la cour de la Citadelle, en marbre blanc sculpté.',
    '/place/ornement-separation.png',
    4,
    'place',
    (SELECT id FROM places WHERE title = 'Minas Tirith')
),

-- -------------------- 5. DÉFENSES MILITAIRES --------------------
(
    'Défenses militaires',
    'FORTIFICATIONS : Sept enceintes muraillées successives en pierre blanche, renforcées par des contreforts. Chaque mur fait entre 30 et 50 pieds de hauteur et 15 à 20 pieds d''épaisseur. Les créneaux permettent aux archers de tirer à couvert.

LA GRANDE PORTE : Porte principale en acier et fer, épaisse de 5 pieds, renforcée par des poutres de chêne. Un pont-levis la précède. Lors du siège de 3019, elle fut brisée par le bélier Grond, manié par le Roi-Sorcier, premier et dernier siège réussi de l''histoire.

GARNISON : En temps de paix, 3000 hommes de la Garde de la Citadelle et de la Garde de la Tour. En temps de guerre, peut mobiliser jusqu''à 6000 soldats stationnés dans la cité, plus les renforts des fiefs.

La Garde de la Citadelle porte l''uniforme noir frappé de l''Arbre Blanc. Soldats d''élite, loyaux jusqu''à la mort. La Garde de la Tour surveille les remparts et les portes, en tuniques blanches et casques ailés.

CATAPULTES ET BALISTES : Chaque niveau est équipé de machines de guerre. Les plus puissantes catapultes sont sur le septième niveau, capables d''envoyer des pierres jusqu''aux portes de Mordor symboliquement.

RÉSERVES : Greniers et citernes pouvant soutenir un siège de six mois pour toute la population. Armureries stockant armes et armures pour équiper 10 000 hommes.

SIGNAUX DE FEU : Système de tours à signaux sur les montagnes, permettant d''appeler Rohan en quelques heures. Sept relais entre Minas Tirith et Edoras.',
    '/place/ornement-separation.png',
    5,
    'place',
    (SELECT id FROM places WHERE title = 'Minas Tirith')
),

-- -------------------- 6. POPULATION ET SOCIÉTÉ --------------------
(
    'Population et société',
    'DÉMOGRAPHIE : Population totale d''environ 40 000 habitants en temps de paix, répartis sur les sept niveaux. Durant le siège de 3019, la population avait été évacuée vers les refuges des montagnes, ne laissant que les soldats et volontaires.

STRUCTURE SOCIALE :
- Noblesse (environ 5%) : grandes familles descendant de Númenor, propriétaires terriens des fiefs
- Bourgeoisie (15%) : marchands riches, capitaines, hauts fonctionnaires
- Artisans et commerçants (30%) : forgerons, tisserands, orfèvres réputés
- Peuple (40%) : ouvriers, serviteurs, gardiens
- Garde militaire (10%) : soldats professionnels

GOUVERNEMENT : La cité est dirigée par l''Intendant du Gondor, qui gouverne au nom du roi absent. Après le retour d''Aragorn, restauration de la monarchie. Conseil des Seigneurs pour les décisions importantes.

ÉCONOMIE : La cité vit du commerce avec les fiefs du Gondor, des taxes et tributs, et de l''artisanat de luxe. Les forgerons de Minas Tirith sont réputés pour leurs armes et armures. Le marché du premier niveau attire marchands de tout le sud de la Terre du Milieu.

CULTURE : Centre culturel et intellectuel du Gondor. Grandes bibliothèques contenant archives et manuscrits de Númenor. Écoles de formation pour les chevaliers et les scribes. Traditions númenóréennes préservées : langue sindarin parlée par la noblesse, respect des anciennes coutumes.',
    '/place/ornement-separation.png',
    6,
    'place',
    (SELECT id FROM places WHERE title = 'Minas Tirith')
),

-- -------------------- 7. APRÈS LA GUERRE --------------------
(
    'Le Quatrième Âge',
    'Après la défaite de Sauron et la destruction de l''Anneau, Minas Tirith retrouva sa splendeur d''antan sous le règne du Roi Elessar (Aragorn II).

RESTAURATION : Les dégâts du siège furent réparés. La Grande Porte fut reforgée en mithril et acier par les nains de la Montagne Solitaire, cadeau de Gimli. L''Arbre Blanc refleurit dans la cour de la Citadelle.

COURONNEMENT : Le 1er mai 3019, Aragorn fut couronné par Gandalf dans la cité. Présence de représentants de tous les Peuples Libres : elfes, nains, hobbits, hommes du Rohan et du Gondor. Mariage d''Aragorn et Arwen Undómiel.

RÉFORMES : Aragorn restaura la justice et la loi dans tout le royaume. Les fiefs du Gondor jurèrent de nouveau allégeance. Alliance renforcée avec le Rohan (serment d''Eorl renouvelé). Paix avec les Orientaux et les Haradrim.

PROSPÉRITÉ : Le commerce reprit avec vigueur. Les routes furent sécurisées. La population de la cité doubla en vingt ans, atteignant 80 000 habitants. Construction de nouveaux quartiers hors des murs.

ÈRE DE PAIX : Sous Aragorn et ses descendants, le Gondor connut plus d''un siècle de paix et de prospérité. Minas Tirith redevint le phare de la civilisation en Terre du Milieu, centre du savoir et des arts.

Le règne d''Aragorn dura 120 ans (il mourut en l''an 120 du Quatrième Âge). Son fils Eldarion lui succéda et poursuivit son œuvre.',
    '/place/ornement-separation.png',
    8,
    'place',
    (SELECT id FROM places WHERE title = 'Minas Tirith')
)

ON CONFLICT (title) DO NOTHING;
