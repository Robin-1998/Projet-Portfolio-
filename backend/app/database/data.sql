-- -----------------------------
-- Inserts Users
-- -----------------------------
INSERT INTO users (first_name, last_name, email, password, is_admin)
VALUES
('Robin','Admin','10616@holbertonstudents.com','$2y$10$pNic29UShtoK5gwuE0DS8eNQEK.RsZLIt/EO4dkS22aAqrcchuzEm',TRUE),
('Timi','Admin','10614@holbertonstudents.com','$2y$10$1QljT3VlKRLmxEeokVLxKOS/eocY8xb3LP95mSVLJaCURQucH9pKO',TRUE),
('John','Doe','johndoe@gmail.com','$2y$10$O8b3kgMMMZhZ5m0t6bVxZOCHoDXTSgBkJrdwNJixVQXk1Z04TKwBS',FALSE)
ON CONFLICT (email) DO NOTHING;

-- -----------------------------
-- Inserts Relation Types
-- -----------------------------
INSERT INTO relation_types (name)
VALUES
('naissance'), ('résidence'), ('décès'), ('union'), ('voyage'), ('quête'),
('bataille'), ('rencontre'), ('trahison'), ('cérémonie'), ('exploration')
ON CONFLICT (name) DO NOTHING;

-- -----------------------------
-- Inserts Places
-- -----------------------------
-- ==================== RÉGIONS ====================
INSERT INTO places (title, type_place, description, parent_id)
VALUES
('Gondor', 'region', 'Royaume des Hommes du Sud, gardien contre Mordor', NULL),
('Rohan', 'region', 'Royaume des Cavaliers du Rohan', NULL),
('Mordor', 'region', 'Terre sombre de Sauron', NULL),
('Eriador', 'region', 'Région de l''Ouest, incluant la Comté', NULL),
('Rhovanion', 'region', 'Terres Sauvages de l''Est', NULL)
ON CONFLICT (title) DO NOTHING;

-- ==================== LIEUX - GONDOR ====================
INSERT INTO places (title, type_place, description, parent_id)
VALUES
('Minas Tirith', 'capitale', 'Capitale du Gondor, la Cité Blanche', (SELECT id FROM places WHERE title='Gondor')),
('Osgiliath', 'ruine', 'Ancienne capitale en ruines sur l''Anduin', (SELECT id FROM places WHERE title='Gondor')),
('Champ de Pelennor', 'plaine', 'Grande plaine devant Minas Tirith, site de bataille', (SELECT id FROM places WHERE title='Gondor')),
('Minas Morgul', 'forteresse', 'Cité maudite, autrefois Minas Ithil', (SELECT id FROM places WHERE title='Gondor'))
ON CONFLICT (title) DO NOTHING;

-- ==================== LIEUX - ROHAN ====================
INSERT INTO places (title, type_place, description, parent_id)
VALUES
('Edoras', 'capitale', 'Capitale du Rohan, siège du Roi Théoden', (SELECT id FROM places WHERE title='Rohan')),
('Isengard', 'forteresse', 'Forteresse de Saroumane avec la tour d''Orthanc', (SELECT id FROM places WHERE title='Rohan')),
('Fangorn', 'foret', 'Ancienne forêt des Ents', (SELECT id FROM places WHERE title='Rohan')),
('Gouffre de Helm', 'forteresse', 'Forteresse imprenable dans les montagnes', (SELECT id FROM places WHERE title='Rohan')),
('Passage des Morts', 'chemin', 'Chemin hanté menant à travers les montagnes', (SELECT id FROM places WHERE title='Rohan'))
ON CONFLICT (title) DO NOTHING;

-- ==================== LIEUX - MORDOR ====================
INSERT INTO places (title, type_place, description, parent_id)
VALUES
('Montagne du Destin (Orodruin)', 'montagne', 'Volcan où l''Anneau Unique fut forgé', (SELECT id FROM places WHERE title='Mordor')),
('Barad-dûr', 'dark', 'Tour Sombre, forteresse de Sauron', (SELECT id FROM places WHERE title='Mordor')),
('Cirith Ungol', 'forteresse', 'Passage gardé par l''araignée Arachne', (SELECT id FROM places WHERE title='Mordor'))
ON CONFLICT (title) DO NOTHING;

-- ==================== LIEUX - ERIADOR ====================
INSERT INTO places (title, type_place, description, parent_id)
VALUES
('La Comté', 'capitale', 'Terre paisible des Hobbits', (SELECT id FROM places WHERE title='Eriador')),
('Hobbitebourg', 'ville', 'Principal village de la Comté', (SELECT id FROM places WHERE title='Eriador')),
('Cul-de-Sac', 'ville', 'Demeure de Bilbon et Frodon Sacquet', (SELECT id FROM places WHERE title='Eriador')),
('Bree', 'ville', 'Village où Hommes et Hobbits cohabitent', (SELECT id FROM places WHERE title='Eriador')),
('Fondcombe', 'ville', 'Rivendell, refuge elfique d''Elrond', (SELECT id FROM places WHERE title='Eriador')),
('Havre Gris', 'port', 'Port elfique vers les Terres Immortelles', (SELECT id FROM places WHERE title='Eriador')),
('Amon Sûl', 'ruine', 'Ruines de la Tour de Garde (Mont Venteux)', (SELECT id FROM places WHERE title='Eriador')),
('Fourré aux Trolls', 'foret', 'Lieu où Bilbon rencontra les trolls', (SELECT id FROM places WHERE title='Eriador')),
('Moria', 'mine', 'Ancienne cité naine de Khazad-dûm', (SELECT id FROM places WHERE title='Eriador')),
('Col de Caradhras', 'montagne', 'Col périlleux dans les Monts Brumeux', (SELECT id FROM places WHERE title='Eriador'))
ON CONFLICT (title) DO NOTHING;

-- ==================== LIEUX - RHOVANION ====================
INSERT INTO places (title, type_place, description, parent_id)
VALUES
('Erebor (Montagne Solitaire)', 'forteresse', 'Royaume sous la Montagne, reconquis par Thorin', (SELECT id FROM places WHERE title='Rhovanion')),
('Forêt Noire', 'foret', 'Forêt sombre et dangereuse, ancien Vertbois le Grand', (SELECT id FROM places WHERE title='Rhovanion')),
('Lothlórien', 'foret', 'Royaume elfique de Galadriel et Celeborn', (SELECT id FROM places WHERE title='Rhovanion')),
('Caras Galadhon', 'ville', 'Cité des arbres au cœur de la Lothlórien', (SELECT id FROM places WHERE title='Rhovanion')),
('Champs aux Iris', 'plaine', 'Plaine où périt Isildur', (SELECT id FROM places WHERE title='Rhovanion')),
('Emyn Muil', 'montagne', 'Collines rocheuses et labyrinthiques', (SELECT id FROM places WHERE title='Rhovanion')),
('Statues des Rois d''Argonath', 'monument', 'Piliers des Rois, gardiens de l''Anduin', (SELECT id FROM places WHERE title='Rhovanion')),
('Marais des Morts', 'eau', 'Marécages hantés par les morts de batailles anciennes', (SELECT id FROM places WHERE title='Rhovanion'))
ON CONFLICT (title) DO NOTHING;

-- -----------------------------
-- Inserts Races
-- -----------------------------
INSERT INTO races (name, weakness, strength, description, citation)
VALUES
('Humain','Corruptibles par le pouvoir, influençable, faiblesse aux maladies et magie','Stratèges militaires, population nombreuse', 
	$$Les hommes arrivèrent sur Arda avec le lever du soleil. Dans le pays que les elfes appellaient Hildórien,
    "pays des suivants", situé dans la partie extrême-orientale de la Terre du Milieu, les hommes ouvrirent les yeux à 
    cette nouvelle lumière. Contrairement aux elfes, ils étaient mortel et, même selon les critères des nains, leur vie 
    était courte.
    
    Au Premier Âge, certains Hommes migrèrent vers l’ouest et rencontrèrent les Elfes de Beleriand. Parmi eux, trois grandes maisons se distinguèrent : celles de Bëor, Haleth et Hador. Ces lignées devinrent les Edain, alliés des Elfes dans la guerre contre Morgoth.
    À la fin du Premier Âge, les Edain reçurent en récompense l’île de Númenor, un royaume puissant béni par les Valar. Cependant, la soif d’immortalité perdit les Númenóréens : leur orgueil les poussa à défier les Valar, et Númenor fut engloutie.
    Quelques fidèles, menés par Elendil, survécurent et fondèrent en Terre du Milieu les royaumes de Gondor et Arnor.
    Durant le Deuxième Âge, ces royaumes résistèrent à Sauron, mais beaucoup furent détruits pendant la Guerre de la Dernière Alliance.
    Au Troisième Âge, la lignée royale d’Arnor s’éteignit, et celle du Gondor s’affaiblit. L’humanité entra dans une période de déclin. Mais à la fin de cet âge, Aragorn, héritier d’Elendil, rétablit la royauté unifiée sous le nom d’Elessar, marquant le renouveau des Hommes.$$,
	'Leur temps est court, leur impact immense'),
('Nain','Orgueilleux et avare','Résistant et force physique',
$$ Les Nains apparurent dans la Terre du Milieu comme les fils de Durin, l’un des sept Pères des Nains, façonnés par Aulë le Vala. Leur peuple était robuste, tenace et profondément attaché à la terre et aux montagnes. Contrairement aux Hommes, ils étaient immortels par la longévité et leurs vies étaient longues, mais ils n’étaient pas réellement immortels comme les Elfes. Leur apparence trapue, leur barbe fournie et leur constitution solide témoignent de leur nature laborieuse et déterminée.

Au Premier Âge, les Nains s’installèrent principalement dans les montagnes de la Terre du Milieu, creusant des cités souterraines somptueuses telles que Nogrod et Belegost, mais également Khazad-dûm (Moria), qui devint la plus célèbre de toutes. Les Nains vivaient selon des traditions anciennes et un code d’honneur strict, valorisant l’artisanat, la forge, et la richesse de leurs mines. Ils excellaient dans le travail du métal et des pierres précieuses, créant des armes et des bijoux de qualité inégalée.
La culture naine est centrée sur la famille, la loyauté et l’héritage. Les rois et chefs de clans occupaient une place essentielle dans la société. Les Nains sont connus pour leur prudence et leur méfiance envers les étrangers, mais ils nouent de solides amitiés lorsqu’ils trouvent des alliés dignes de confiance. Leur lien avec la terre et les montagnes est presque sacré ; ils considèrent leurs cités et leurs mines comme des trésors à protéger à tout prix.
Malgré leur apparente rigidité et leur amour des richesses, les Nains peuvent se montrer courageux et honorables en temps de guerre. Ils participèrent à de nombreuses batailles contre Morgoth et ses serviteurs, protégeant leurs royaumes et parfois venant en aide aux Elfes et aux Hommes. Cependant, l’avidité et l’orgueil causèrent parfois des conflits internes et des querelles avec d’autres peuples, notamment dans le commerce des pierres et des trésors.
La langue des Nains, le Khuzdul, reste un secret jalousement gardé. Peu de non-Nains la connaissent, et ils l’utilisent surtout pour nommer les lieux et les artefacts. Les Nains parlent aussi les langues communes pour commercer, mais ils conservent leur identité culturelle forte à travers la langue et les traditions transmises de génération en génération.
Ainsi, les Nains incarnent la résilience, la loyauté et l’artisanat. Leur histoire est celle d’un peuple fier, profondément attaché à ses racines et à ses cités souterraines, oscillant entre prudence et bravoure, travail et conflit, mais toujours fidèle à son héritage ancestral.$$,
'Peuple robuste, fier et secret'),
('Elfe', 'prétentieux et isolement hautain', 'Longévité, agilité et conaissance de la magie', 
$$ Les Elfes furent les premiers enfants d’Ilúvatar à éveiller sur Arda, avant même l’arrivée des Hommes. Ils étaient immortels, gracieux et d’une beauté surnaturelle, étroitement liés à la musique et aux chants des Valar. Leur vue perçante et leur ouïe fine, ainsi que leur longévité, leur permettaient d’observer le monde avec une profondeur et une sagesse que les autres peuples n’atteignaient jamais. Ils vivaient en harmonie avec la nature, protégeant les forêts, les rivières et toutes les créatures qui y résidaient.
Au Premier Âge, les Elfes se divisèrent en plusieurs clans et peuples : les Vanyar, les Noldor et les Teleri, chacun avec ses particularités et sa culture. Les Noldor, artisans et guerriers, excellaient dans l’art de la forge et la création de joyaux et armes magiques, tandis que les Teleri, amoureux de la mer, étaient des navigateurs et des chanteurs talentueux. Les Elfes de Beleriand jouèrent un rôle crucial dans la lutte contre Morgoth, forgeant des alliances avec les Hommes et affrontant les armées du mal avec courage et stratégie.
La culture elfique est imprégnée de connaissance, de poésie et d’art. Ils ont une grande sensibilité aux beautés du monde et une compréhension profonde de l’histoire et de la magie. Les villes et cités elfiques, telles que Gondolin et Tirion, reflétaient leur perfection architecturale et leur raffinement. Les Elfes valorisent l’apprentissage, la musique, le chant et la préservation de la mémoire des âges passés, car chaque objet, chaque pierre, chaque arbre porte une histoire.
Bien que puissants et sages, les Elfes ressentent souvent une mélancolie liée à la fuite du temps et à l’éternité de leur vie. Ils peuvent se montrer distants ou méfiants envers les autres peuples, mais lorsqu’ils tissent des liens, ceux-ci sont durables et profonds. Leurs alliances avec les Hommes, comme celles des Edain, sont légendaires et souvent scellées par des mariages ou des pactes de loyauté.
Les Elfes parlent principalement le Quenya et le Sindarin, langues riches et mélodieuses, mais beaucoup connaissent aussi le Westron pour communiquer avec les autres peuples. Leur langage, leur art et leur culture perpétuent la mémoire de la Terre du Milieu et des Valar, faisant d’eux les gardiens de la beauté et du savoir ancien.
Ainsi, les Elfes incarnent la sagesse, la beauté et l’harmonie avec le monde naturel. Leur histoire est celle d’un peuple immortel, créatif et vigilant, oscillant entre mélancolie et grandeur, toujours attentif à la préservation et à la beauté de la Terre du Milieu. $$,
'Sages et distants, Immortels liés à la nature'),
('Aigle géant', 'nombre réduit et intervention rare', 'Rapide, puissant et maître du ciel',
$$ Les Aigles Géants de la Terre du Milieu sont des créatures majestueuses et anciennes, créées par Manwë, le Seigneur des airs, pour veiller sur le monde depuis les hauteurs. Ils sont doués d’une intelligence remarquable et possèdent une vue perçante capable de distinguer le moindre mouvement sur des kilomètres. Leur vol puissant et leur envergure immense leur permet de parcourir de vastes distances et d’intervenir rapidement dans les moments critiques. Bien qu’ils soient indépendants et fiers, leur loyauté envers le Bien et les forces de la lumière est inébranlable.
Au fil des âges, les Aigles Géants ont joué un rôle discret mais crucial dans l’histoire de la Terre du Milieu. Ils viennent souvent en aide aux héros lors des conflits majeurs, sauvant ceux qui se trouvent en danger et transportant des messages ou des êtres précieux à travers des territoires hostiles. Leur présence est souvent associée aux moments de grande importance, tels que la chute de Morgoth et la Guerre de l’Anneau, où leur aide fut déterminante pour les peuples libres.
La culture des Aigles est mystérieuse et peu connue des autres races. Ils vivent dans des lieux élevés et inaccessibles, souvent au sommet des Monts Brumeux ou près des vallées isolées. Leur société semble fondée sur des liens familiaux et une hiérarchie naturelle où les plus âgés, sages et puissants, guident les jeunes générations. Leur longue vie leur permet d’accumuler une grande sagesse et une mémoire de tous les événements qu’ils observent depuis les airs.
Malgré leur puissance, les Aigles Géants préfèrent la prudence et évitent les conflits inutiles. Ils interviennent seulement lorsque le destin du Bien est menacé ou lorsque la justice et l’équilibre du monde l’exigent. Leur majesté et leur aura inspirent crainte et admiration chez tous ceux qui ont la chance de les voir. Ils représentent la vigilance, la liberté et la grandeur de la création d’Ilúvatar.
Le langage des Aigles est inconnu des Hommes et des Elfes, mais il est probable qu’il consiste en cris et appels complexes permettant une communication fine sur de longues distances. Leur intelligence et leur mémoire leur permettent de comprendre les intentions des autres êtres et de coordonner leurs actions lors des événements cruciaux.
Ainsi, les Aigles Géants incarnent la liberté, la sagesse et la protection. Leur histoire est celle d’un peuple puissant et noble, oscillant entre indépendance et intervention providentielle, toujours présent dans l’ombre pour veiller sur la Terre du Milieu et ses habitants. $$,
 'Créatures anciennes, gardiennes des hauteurs'),
('Araignée géante', 'Sensibilité à la lumière et vulnérable au feu', 'Population nombreuse et puissant venin', 
$$ Les Araignées Géantes de la Terre du Milieu sont des créatures redoutables et mystérieuses, douées d’une intelligence malveillante et d’une force terrifiante. Elles hantent les forêts sombres et les cavernes profondes, tissant des toiles gigantesques pour capturer leurs proies et régner sur leur domaine avec une patte de fer. Leur agilité et leur venin puissant en font des adversaires mortels pour tout être qui ose s’aventurer dans leurs territoires.
Au cours des âges, certaines de ces araignées devinrent célèbres par leur cruauté et leur ruse. Ungoliant, créature ancestrale du Premier Âge, sema la destruction avec sa faim insatiable et son venin mortel. Plus tard, dans le Second et le Troisième Âge, des araignées comme Shelob hantèrent les cavernes de Cirith Ungol, terrorisant les voyageurs et les héros des peuples libres. Elles sont souvent attirées par la peur et la faiblesse, exploitant les failles des mortels et des Elfes pour assouvir leur faim.
La vie des Araignées Géantes est solennelle et impitoyable. Elles tissent leurs toiles avec patience et précision, utilisant leur ingéniosité pour piéger leurs ennemis et protéger leur territoire. Bien qu’elles soient intelligentes, elles ne connaissent ni loyauté ni pitié ; seules la survie et la domination dictent leurs actions. Leur lien avec l’obscurité et les lieux reculés de la Terre du Milieu renforce leur aura de mystère et de danger.
Malgré leur nature malfaisante, elles jouent un rôle important dans l’équilibre de certains écosystèmes, contrôlant les populations de petites créatures et rappelant aux autres races les périls des lieux inexplorés. Les rares interactions avec les autres peuples se terminent généralement par la fuite ou la mort des intrus, laissant derrière elles des légendes de terreur et de courage.
Le langage des Araignées est inconnu des autres races, mais elles communiquent probablement par signaux et sons spécifiques à leur espèce, coordonnant leurs mouvements et défenses avec efficacité. Leur intelligence leur permet de comprendre les comportements de leurs proies et de planifier des embuscades complexes.
Ainsi, les Araignées Géantes incarnent la ruse, la patience et la menace constante. Leur histoire est celle d’un peuple cruel et méthodique, oscillant entre furtivité et domination, terrorisant les forêts et cavernes de la Terre du Milieu tout en restant une présence fascinante et redoutée par tous. $$,
'Terreur rampante, maîtresse des toiles'),
('Balrog', 'Faible à la lumière d’Eärendil', 'Longévité, puissance physique et magique, arme redoutables',
$$ Les Balrogs sont des démons de feu et d’ombre, créatures terrifiantes nées parmi les Maiar qui furent corrompus par Morgoth avant le Premier Âge. Leur apparence est imposante et effrayante, faite d’ombre tourbillonnante, de flammes et d’une puissance écrasante. Ils inspirent la peur à tous ceux qui croisent leur chemin et sont connus pour leur violence, leur force surnaturelle et leur capacité à manipuler le feu et les ténèbres.
Durant le Premier Âge, les Balrogs servaient comme généraux et lieutenants de Morgoth, semant la destruction dans Beleriand et au-delà. Leur force brute combinée à leur intelligence en fit des adversaires redoutables, capables de mettre à mal les armées d’Elfes et d’Humains. L’un des Balrogs les plus célèbres, Gothmog, commandait les légions de Morgoth et participa à la chute de nombreuses forteresses elfiques. Les Balrogs sont capables de manipuler le feu et l’ombre, frappant avec des fouets de flamme et écrasant leurs ennemis sous leur puissance titanesque.
La culture et la motivation des Balrogs sont entièrement liées à la destruction et à la domination. Ils n’ont ni pitié ni sens moral, obéissant uniquement à la volonté de Morgoth et à leur soif de violence. Leur intelligence leur permet de planifier des embuscades et de mener des attaques stratégiques, mais ils ne connaissent ni loyauté ni fraternité en dehors de leur maître.
Les Balrogs vivent souvent dans les profondeurs des montagnes ou dans des lieux d’ombre et de feu, comme les mines ou les forteresses de Morgoth. Leur longévité est immense et leur nature spirituelle leur confère une puissance que peu de créatures de la Terre du Milieu peuvent égaler. La légende raconte que même le courage et la force des Elfes et des Hommes combinés étaient rarement suffisants pour les vaincre.
Le langage des Balrogs est inconnu, mais leur communication semble se faire par des cris, des rugissements et des manifestations de feu et d’ombre. Leur présence seule impose la terreur et fait fuir les plus courageux. Leur rôle dans l’histoire de la Terre du Milieu est celui de destructeurs impitoyables, rappelant sans cesse la puissance du mal lorsqu’il est libéré.
Ainsi, les Balrogs incarnent la peur, la puissance destructrice et la domination des ténèbres. Leur histoire est celle de créatures redoutables, oscillant entre force brute et intelligence stratégique, terrorisant la Terre du Milieu et marquant à jamais la mémoire des âges.$$,
'Les nains ont creusé trop avidement et trop profondément'),
('Dragon', 'Orgueilleux et avare et cible facile', 'Peau très résistante, rusé, Longévité et puissance destructrice',
$$ Les Dragons de la Terre du Milieu sont des créatures anciennes, puissantes et redoutées, nées ou corrompues par Morgoth dans les premiers âges. Leur taille colossale, leurs écailles impénétrables et leur souffle de feu en font des adversaires presque invincibles, capables de semer la destruction sur leur passage. Leur intelligence, bien que perverse, leur permet de manipuler, tromper et terroriser les autres peuples, accumulant richesses et trésors au fil des siècles.
Au Premier Âge et au Second Âge, les Dragons jouèrent un rôle décisif dans la domination de Morgoth et la crainte qu’il inspirait aux peuples libres. Smaug, le plus célèbre d’entre eux, règne sur la Montagne Solitaire au Troisième Âge, accumulant un trésor immense et détruisant villes et villages par son feu. Les Dragons sont à la fois stratèges et destructeurs : leur ruse est égale à leur force brute, et ils utilisent leur intelligence pour tendre des embuscades et défendre leurs richesses avec acharnement.
La culture des Dragons est centrée sur la possession, la domination et l’avidité. Ils n’ont ni pitié ni sens moral pour les autres créatures, et leur vie s’écoule autour de la protection de leur trésor et de la maîtrise du territoire qu’ils ont choisi. Leur longévité et leur puissance font d’eux des figures légendaires, capables d’inspirer autant l’admiration que la peur.
Les Dragons sont connus pour leur capacité à parler et à manipuler les autres par la ruse et les mots, bien que très peu de mortels osent leur faire face. Leurs lairs, souvent des montagnes ou des cavernes profondes, sont protégés par des pièges naturels et leur vigilance constante. Ils symbolisent l’avidité, la force et le danger, marquant durablement les histoires et légendes des peuples de la Terre du Milieu.
Le langage des Dragons est rare et mystérieux, mais il semble que certains d’entre eux, comme Smaug, puissent converser avec les Humains et même les manipuler par la parole. Leur présence impose le respect et la crainte, et ils apparaissent toujours dans les récits comme des défis majeurs pour les héros.
Ainsi, les Dragons incarnent la puissance, l’avidité et la ruse. Leur histoire est celle de créatures colossales et intelligentes, oscillant entre destruction et domination, terrifiant la Terre du Milieu et laissant derrière eux des légendes de courage et de prudence. $$,
'Ça mon gars c''est un Dragon !'),
('Gobelin', 'Faible endurance, sensibilité à la lumière et lâche', 'Population nombreuse, Adaptabilité',
$$ Les Gobelins, parfois appelés Orques dans certains récits, sont des créatures maléfiques et rusées, corrompues par Morgoth dès les premiers âges. Ils vivent dans des cavernes, des montagnes et des souterrains sombres, loin de la lumière du soleil, et prospèrent dans la peur et le chaos. Leur apparence est hideuse et souvent grotesque, avec des traits féroces et une stature trapue, mais leur nombre et leur ruse compensent largement leur faiblesse physique individuelle.
Au fil des âges, les Gobelins formèrent des sociétés organisées mais brutales, dirigées par des chefs impitoyables et souvent violents. Ils attaquent en meute, utilisant des embuscades et des pièges pour submerger leurs ennemis. Bien qu’ils manquent de courage face aux adversaires puissants ou à la lumière du jour, ils savent exploiter la furtivité et la surprise pour causer de grands ravages. Les Gobelins sont également connus pour leur aptitude à travailler le métal et les armes, forgeant des outils et des armes rudimentaires mais efficaces.
Leur culture est axée sur la survie, la violence et la domination locale. Ils respectent la force et l’autorité de leurs chefs et se livrent souvent à des querelles internes pour le pouvoir. Malgré leur nature malfaisante, les Gobelins ont des structures sociales complexes, avec des divisions en clans et en groupes spécialisés pour la guerre, l’espionnage et la capture des prisonniers.
Les Gobelins ont une langue gutturale et rudimentaire, difficilement compréhensible par les autres peuples, et communiquent principalement par cris et ordres simples. Leur intelligence est suffisante pour organiser des raids et défendre leurs territoires, mais ils restent limités par leur agressivité et leur jalousie. Leur histoire est étroitement liée aux conflits des grands peuples de la Terre du Milieu, agissant souvent comme soldats ou agents du mal lors des guerres de Morgoth et de Sauron.
Ainsi, les Gobelins incarnent la cruauté, la ruse et l’adaptabilité. Leur histoire est celle de créatures petites mais dangereuses, oscillant entre meutes organisées et chaos brutal, terrorisant les montagnes et cavernes de la Terre du Milieu et constituant une menace constante pour les peuples libres. $$,
'Nombreux, cruels, mais faibles et désorganisés'),
('Guetteur dans l''eau', 'Limité à son environnement et sensibilité à la lumière', 'Puissance physique',
$$ Le Guetteur dans l’eau est une créature mystérieuse et terrifiante qui hante les profondeurs sombres et stagnantes des lacs, mares et rivières isolées de la Terre du Milieu. Peu d’informations sont connues sur son origine exacte, mais il est souvent décrit comme une masse monstrueuse, dotée de tentacules puissants et d’yeux perçants, capable de traquer et d’attaquer toute créature qui s’aventure trop près de son domaine. Sa nature aquatique et furtive en fait un prédateur redoutable et presque impossible à prévoir.
Dans les légendes, le Guetteur dans l’eau fut responsable de la perte tragique de plusieurs explorateurs et aventuriers, et il est surtout célèbre pour avoir attaqué les compagnons de la Communauté de l’Anneau à l’entrée de la Moria, fermant ainsi le Pont de Durin à la lumière du jour. Sa force et sa taille lui permettent de saisir et d’emporter des proies dans les profondeurs de l’eau, et ses tentacules peuvent briser portes et barrières pour atteindre sa cible.
La vie du Guetteur est solitaire et territoriale. Il semble protéger son environnement avec un instinct féroce, réagissant à toute intrusion avec violence. Bien qu’il soit intelligent dans ses attaques, il agit principalement par instinct de chasse et par défense de son territoire. Sa présence inspire la peur et la prudence chez tous ceux qui naviguent ou explorent les eaux mystérieuses des montagnes et forêts.
La communication de cette créature reste inconnue, et peu de peuples de la Terre du Milieu ont eu la chance ou le malheur de l’observer de près. Son apparition est généralement précédée par des remous et des éclaboussures, avertissant du danger imminent. Sa longévité et sa force en font une légende durable, et les contes autour du Guetteur servent souvent à prévenir les voyageurs imprudents.
Ainsi, le Guetteur dans l’eau incarne la menace, le mystère et la vigilance des profondeurs. Son histoire est celle d’une créature insaisissable et dangereuse, oscillant entre furtivité et puissance brute, rappelant aux habitants et aventuriers de la Terre du Milieu que certains lieux doivent rester inaccessibles. $$,
'Une masse sombre surgit de l''eau et attaqua la communauté'),
('Mûmak', 'Cible facile et contrôle réduit', 'Puissance physique, endurance et transport de guerre', 
$$ Les Mûmaks, également appelés Oliphants, sont de gigantesques créatures semblables à des éléphants, élevées et utilisées principalement par les peuples du Harad. Leur taille colossale, leur force prodigieuse et leur endurance exceptionnelle en font des instruments de guerre redoutables, capables de renverser des arbres, écraser des fortifications et terrasser des armées entières. Ces bêtes sont intelligentes mais farouchement indépendantes, réagissant aux commandes de leurs maîtres avec précision lorsqu’elles sont dressées, mais pouvant se montrer imprévisibles et destructrices si elles sont enragées.
Au cours des Guerres du Troisième Âge, les Mûmaks furent utilisés par les armées du Harad contre Gondor et ses alliés. Montés par des guerriers armés de lances et de flèches, ils semaient la panique dans les rangs ennemis et servaient à briser les lignes de défense. Leur peau épaisse les rend résistants aux flèches et aux attaques, tandis que leur trompe et leurs défenses puissantes leur permettent de combattre avec une efficacité terrifiante. Leur présence sur le champ de bataille était souvent suffisante pour modifier le cours d’une bataille.
La vie des Mûmaks est généralement liée à l’homme qui les dresse, bien qu’ils possèdent une grande autonomie et un instinct naturel de survie. Ils vivent dans les régions chaudes et sèches du Sud, souvent en troupeaux, et se déplacent avec lenteur mais détermination, transportant charges et guerriers à travers des terrains difficiles. Leur longévité et leur robustesse leur permettent de traverser de longues distances sans fatigue.
Les Mûmaks sont silencieux et communiquent principalement par des cris, barrissements et mouvements corporels. Leur intelligence et leur mémoire leur permettent de reconnaître leurs compagnons humains et de réagir aux ordres avec une coordination étonnante pour des créatures de cette taille. Ils symbolisent la puissance brute, la majesté et le danger contrôlé.
Ainsi, les Mûmaks incarnent la force, l’endurance et la terreur des champs de bataille. Leur histoire est celle de créatures colossales et impressionnantes, oscillant entre puissance sauvage et discipline lorsqu’elles sont dressées, rappelant la grandeur et le danger de la Terre du Milieu. $$,
'Les mûmakils chargèrent, écrasant tout sur leur passage, leurs trompes tonnant comme le tonnerre'),
('Orc', 'Vulnérable à la lumière et traitrise', 'Population nombreuse et adaptabilité', 
$$ Les Orcs sont des créatures maléfiques et corrompues, nées de la perversion des Elfes par Morgoth aux premiers âges, ou selon certaines traditions, issues de créatures tordues et malfaisantes. Ils sont de taille variable, généralement robustes mais hideux, avec une peau sombre ou verdâtre, des traits féroces et une grande agressivité. Leur apparence inspire la peur, et leur nature brutale les rend cruels et imprévisibles.
Tout au long des âges, les Orcs ont servi les seigneurs des ténèbres comme soldats et esclaves, participant à de nombreuses guerres contre les Elfes, les Hommes et les autres peuples libres. Leur discipline militaire est souvent limitée, mais leur nombre immense et leur capacité à attaquer en masse compensent largement leurs faiblesses individuelles. Ils vivent dans des forteresses, des cavernes et des lieux reculés, loin de la lumière et sous la domination de chefs puissants ou de créatures plus redoutables comme les Balrogs.
La culture des Orcs est violente et hiérarchisée par la force. Les plus forts dominent les faibles, et les conflits internes sont fréquents. Bien qu’ils soient organisés pour la guerre, ils manquent souvent de créativité ou de sagesse dans la gouvernance et dépendent entièrement de la direction de leur maître. Ils sont obsédés par la conquête, le pillage et la destruction, et leur loyauté est rarement autre chose que celle dictée par la peur.
Leur langage est guttural, rude et difficilement compréhensible par les autres races. Ils utilisent des cris, des ordres et des sons agressifs pour communiquer sur le champ de bataille. Malgré leur intelligence limitée, certains Orcs font preuve de ruse et d’ingéniosité dans les embuscades et les stratégies de combat.
Ainsi, les Orcs incarnent la cruauté, la violence et l’adaptabilité dans les ténèbres. Leur histoire est celle de créatures nombreuses et brutales, oscillant entre meutes sauvages et armées organisées, terrorisant les peuples libres de la Terre du Milieu et perpétuant l’influence des forces du mal à travers les âges. $$,
'Cruels, malveillants et avides de bataille, mais ils fuient la lumière du soleil'),
('Troll', 'Vulnérable à la lumière et intelligence limité', 'Résistant et puissance physique', 
$$ Les Trolls sont des créatures massives et puissantes, souvent décrites comme des êtres brutaux et peu intelligents, mais d’une force physique colossale. Ils vivent principalement dans les montagnes, les cavernes et les forêts reculées, évitant la lumière du jour qui peut les pétrifier ou les affaiblir selon les variantes de la légende. Leur apparence est hideuse, avec une peau épaisse et rugueuse, des membres robustes et une stature imposante qui inspire la peur aux voyageurs et aventuriers imprudents.
Tout au long des âges, les Trolls furent utilisés comme armes vivantes par les forces du mal, notamment par les Orcs et les serviteurs de Sauron, pour semer destruction et chaos. Leur puissance brute leur permet de démolir des portes, des ponts et toute structure se dressant sur leur passage. Bien que leur intelligence soit limitée, ils font preuve d’une ruse instinctive dans la chasse et l’embuscade, surtout lorsqu’ils travaillent en groupe ou sont guidés par des créatures plus intelligentes.
La vie des Trolls est centrée sur la survie, la chasse et la domination territoriale. Ils sont solitaires ou vivent en petits groupes, et leur culture se résume essentiellement à la force et à la peur qu’ils inspirent. Ils se nourrissent de presque tout ce qu’ils peuvent capturer ou tuer, et leur comportement agressif fait d’eux des prédateurs redoutables pour toutes les créatures qui croisent leur chemin.
Les Trolls communiquent principalement par grognements, cris et mouvements corporels, et leur langage reste incompréhensible aux autres peuples. Leur longévité et leur résistance physique en font des adversaires redoutables, mais leur manque de finesse et de discipline les rend vulnérables face à des ennemis organisés et intelligents.
Ainsi, les Trolls incarnent la force brute, la menace et la sauvagerie. Leur histoire est celle de créatures gigantesques et puissantes, oscillant entre destruction instinctive et obéissance limitée, semant la terreur dans les montagnes et forêts de la Terre du Milieu. $$,
'Ils ont un troll des cavernes !'),
('Uruk', 'Dépendance à un chef', 'Endurance, force physique et organisation militaire', 
$$ Les Uruk-hai sont une race d’Orcs améliorés, créés par Sauron et Saruman pour être plus grands, plus forts et plus résistants que les Orcs ordinaires. Leur apparence est plus imposante, avec une stature massive, une peau sombre et des traits féroces. Ils combinent la brutalité des Orcs avec une endurance et une discipline accrues, ce qui les rend particulièrement redoutables sur les champs de bataille.
Ces créatures sont capables de marcher sur de longues distances sans se fatiguer et de porter des armures lourdes et des armes imposantes. Leur loyauté est envers leurs maîtres, mais ils obéissent sans question à l’autorité d’un chef capable d’imposer le respect par la peur et la force. Les Uruk-hai sont utilisés comme troupes d’élite dans les guerres de Sauron et de Saruman, participant à des sièges, des raids et des combats contre les peuples libres.
La culture des Uruk-hai est centrée sur la guerre, la survie et la domination. Ils vivent en groupes organisés et hiérarchisés, respectant la force et l’efficacité de leurs chefs. Bien qu’ils aient hérité de la cruauté et de la sauvagerie des Orcs, ils possèdent une intelligence suffisante pour mener des embuscades, des stratégies de combat et des raids coordonnés.
Les Uruk-hai sont capables de parler une langue gutturale commune, mais ils se servent surtout de cris, d’ordres et de signaux sur le champ de bataille. Leur histoire est intimement liée aux guerres du Troisième Âge, notamment dans les conflits autour de la Terre du Milieu où ils semèrent la peur et la destruction.
Ainsi, les Uruk-hai incarnent la force, l’endurance et la discipline au service du mal. Leur histoire est celle de créatures créées pour la guerre, oscillant entre brutalité instinctive et efficacité militaire, terrorisant les armées et les villages de la Terre du Milieu. $$,
'Uruk-hai ! Ils ne s''arrêtent jamais, même dans la lumière du jour'),
('Warg', 'Sensibilité à la lumière et vulnérable au feu', 'Rapidité, agilité, attaque en meute', 
$$ Les Wargs sont de gigantesques loups sauvages et féroces, souvent montés par les Orcs et les Uruk-hai dans les guerres de la Terre du Milieu. Leur apparence est terrifiante : des corps musclés, des crocs acérés, des yeux perçants et une agilité surprenante pour leur taille. Ces créatures sont rapides, intelligentes et extrêmement dangereuses, capables de traquer, encercler et déchirer leurs proies en meute.
Durant le Troisième Âge, les Wargs furent largement utilisés par les forces de Sauron et par les tribus d’Orcs pour attaquer les Humains, Elfes et autres peuples libres. Leur vitesse et leur coordination en groupe en font des prédateurs redoutables sur les champs de bataille et dans les forêts. Ils peuvent parcourir de longues distances en poursuivant leurs cibles et attaquent souvent par surprise, semant la panique et la confusion parmi leurs ennemis.
La vie des Wargs est centrée sur la chasse et la survie en meute. Ces créatures sont très sociales et vivent selon une hiérarchie stricte, où les plus forts et les plus rusés dominent. Ils chassent en groupe pour capturer des proies plus grandes qu’eux et pour défendre leur territoire avec acharnement. Leur intelligence leur permet de reconnaître les patterns de mouvement et de réagir stratégiquement pendant les attaques.
Le langage des Wargs est limité aux hurlements, grognements et signes corporels, mais ils communiquent efficacement entre eux et coordonnent leurs attaques avec une étonnante efficacité. Leur instinct de meute, leur férocité et leur endurance font d’eux des alliés redoutables pour les Orcs et les Uruk-hai, et des ennemis mortels pour les peuples libres de la Terre du Milieu.
Ainsi, les Wargs incarnent la vitesse, la coordination et la violence sauvage. Leur histoire est celle de prédateurs intelligents et féroces, oscillant entre chasse instinctive et coopération meurtrière, semant la terreur dans les forêts et sur les champs de bataille de la Terre du Milieu. $$,
'Rapides, agressifs en meute, mais vulnérables seuls'),
('Ent', 'Vulnérable au feu et nombre réduit', 'Puissance physique, endurance, longévité et contrôle de la nature', 
$$ Les Ents sont les gardiens des forêts, créatures antiques et majestueuses de la Terre du Milieu, créées par Yavanna pour protéger les arbres et les forêts contre toute destruction. Ils possèdent une stature colossale, une force prodigieuse et une longévité exceptionnelle, pouvant vivre plusieurs millénaires. Leur apparence évoque les arbres eux-mêmes : leur peau est rugueuse comme l’écorce, leurs cheveux et leurs barbes se confondent avec le feuillage, et leurs mouvements sont à la fois lents et impressionnants.
Les Ents vivent principalement dans les forêts anciennes, comme la forêt de Fangorn, où ils veillent silencieusement sur leur domaine. Ils sont pacifiques par nature et ne se mêlent que rarement aux affaires des autres peuples. Cependant, lorsque leurs forêts sont menacées, ils révèlent une puissance et une férocité terrifiantes. Leurs bras massifs peuvent déraciner des arbres, briser des structures et combattre les forces destructrices, comme cela fut démontré lors de la marche sur Isengard où ils déchaînèrent leur colère sur les fortifications de Saruman.
La culture des Ents est profondément liée à la nature et à la mémoire des arbres. Ils se réunissent en conseil et communiquent avec une lenteur et une réflexion qui reflètent leur longévité. Chaque Ent connaît les forêts et les arbres de son domaine, et leur sagesse est immense, accumulée sur des millénaires. Bien qu’ils soient lents à agir, leur patience et leur vigilance en font des protecteurs efficaces et redoutables.
Les Ents possèdent leur propre langue, l’Entish, complexe et difficile à apprendre pour les autres peuples. Leurs conversations sont longues et détaillées, chaque mot pesé et réfléchi, reflétant leur perception du temps et de la nature. Leur lien avec les arbres leur permet de sentir le moindre changement dans la forêt et de réagir avec discernement face aux menaces.
Ainsi, les Ents incarnent la sagesse, la puissance et la vigilance. Leur histoire est celle de créatures anciennes, oscillant entre la contemplation et l’action, protégeant les forêts de la Terre du Milieu et rappelant aux peuples libres l’importance de respecter et de préserver la nature. $$,
'Nous sommes les Gardiens des Forêts, vieux comme les racines de la terre')
ON CONFLICT (name) DO NOTHING;

-- -----------------------------
-- Inserts Characters
-- -----------------------------
INSERT INTO characters (name, birth_date, death_date, era_birth, era_death, gender, profession, description, citation, race_id)
VALUES
('Gimli', 2879, 120, 'Troisième âge', 'Quatrième âge', 'Masculin', 'Guerrier', $$ Gimli, fils de Glóin, est un nain du royaume sous la Montagne d’Erebor, robuste et trapu, avec une barbe rousse épaisse et soigneusement tressée, et un visage à la fois dur et digne, reflet de la fierté de son peuple. Courageux et intrépide, il se montre toujours prêt à défendre ses amis et à affronter le danger, maniant avec habileté sa hache en toutes circonstances. Il rejoint la Communauté de l’Anneau pour représenter les Nains et participe aux grandes batailles de la Guerre de l’Anneau, dont la Moria, le Gouffre de Helm et les Champs du Pelennor, où son courage et sa ténacité sont remarquables. Bien qu’au départ bourru et parfois méfiant envers les Elfes, il développe une profonde amitié avec Legolas, symbolisant la réconciliation entre leurs peuples longtemps rivaux. Gimli admire également la beauté et la sagesse de Galadriel, Dame de Lothlórien, et fait preuve d’un respect sincère pour les merveilles du monde. Après la chute de Sauron, il devient Seigneur des Cavernes Étincelantes, dirigeant un groupe de nains pour embellir les cavernes de Helm’s Deep, et, selon certaines traditions, il est le seul nain à avoir voyagé vers les Terres Immortelles en compagnie de Legolas, scellant ainsi leur amitié indéfectible. $$ ,'Ça compte quand même que pour un !', (SELECT id FROM races WHERE name='Nain')),
('Eowyn', 2995, NULL, 'Troisième âge', 'Quatrième âge', 'Féminin', 'Guerrière, noble', $$ Éowyn est une noble dame du Rohan, sœur du roi Théodred et nièce du roi Théoden, reconnue pour sa beauté, son courage et sa détermination. Blonde et élancée, elle possède un regard pénétrant et une prestance qui inspire respect et admiration. Malgré les conventions de son peuple qui attendent des femmes qu’elles restent à l’abri, Éowyn rêve de gloire et de combat, refusant de se contenter d’une vie passive. Animée par un profond sens de l’honneur et par la volonté de protéger son peuple, elle prend les armes lors de la bataille des Champs du Pelennor, se déguisant en homme sous le nom de Dernhelm. C’est elle qui affronte et terrasse le Roi-Sorcier d’Angmar, accomplissant une prophétie qui semblait impossible. Courageuse, fidèle et parfois tourmentée par ses sentiments, notamment pour Aragorn, Éowyn incarne la force et la résilience face au destin. Après la guerre, elle trouve la paix et l’amour auprès de Faramir à Minas Tirith, et devient une figure respectée et aimée, symbole de bravoure et d’espoir pour le peuple du Rohan et du Gondor. $$, 'Fille du Rohan, nièce du roi Théoden et sœur d’Eomer', (SELECT id FROM races WHERE name='Humain')),
('Sauron', NULL, 3019, $$Avant la création de Arda$$, 'Quatrième âge', 'Masculin', 'Guerrier, magicien et capitaine des armées', $$ Sauron est le puissant et maléfique Seigneur des Ténèbres de la Terre du Milieu, ancien lieutenant de Morgoth, maître de l’Anneau Unique et source de terreur pour toutes les races libres. Créature Maia dotée d’un immense pouvoir, il est capable de manipulation, de magie et d’influence à grande échelle, corrompant les hommes, les elfes et les nains par la peur et la promesse de pouvoir. Après avoir forgé l’Anneau Unique pour contrôler les autres anneaux de pouvoir, Sauron consacre des siècles à étendre son influence et à asseoir sa domination sur la Terre du Milieu, érigeant Barad-dûr et levant d’immenses armées d’Orques, de Nazgûls et de créatures monstrueuses. Bien qu’il n’ait pas de forme physique visible après la chute de Númenor, sa présence malveillante est ressentie partout, un œil ardent et omniprésent symbolisant sa vigilance et sa volonté de contrôle absolu. Sa détermination est inébranlable, et sa ruse, sa cruauté et sa capacité à inspirer la peur font de lui l’adversaire ultime des peuples libres. La destruction de l’Anneau Unique met fin à sa puissance et dissipe son influence, mais son nom reste à jamais gravé dans la mémoire de la Terre du Milieu comme symbole du mal absolu et de la domination par la peur. $$, 'Même la plus petite personne peut changer le cours de l''avenir… sauf Sauron, dont le regard voit tout.', NULL),
('Saroumane', NULL, 3019, $$Avant la création de Arda$$, 'Quatrième âge', 'Masculin', 'Magicien', $$ Saroumane le Blanc est un puissant magicien de l’ordre des Istari, initialement chef du Conseil Blanc et considéré comme le plus sage et le plus influent des magiciens envoyés en Terre du Milieu pour aider à contrer Sauron. Grand, imposant et doté d’une présence charismatique, il inspire respect et admiration, portant une longue robe blanche symbole de son rang et de son autorité. Cependant, son désir de pouvoir et sa fascination pour l’Anneau Unique le conduisent à la corruption, le détournant de sa mission originelle de protéger les peuples libres. À Isengard, il forge une armée d’Orques et d’hommes corrompus, manipulant et trahissant ceux qui lui font confiance, y compris les Rohirrim et les Hommes du Nord. Intelligent, rusé et doté d’une grande maîtrise de la magie et de la connaissance des langues et des stratégies, Saroumane incarne l’orgueil et l’ambition démesurée, devenant un instrument du mal malgré ses intentions initiales. Sa chute, marquée par la destruction de son pouvoir à Isengard et sa déchéance finale, illustre le danger de la soif de domination et la fragilité même des plus grands parmi les sages, laissant derrière lui un exemple de trahison et de corruption par le pouvoir. $$, 'Même le plus sage peut tomber, quand le désir de pouvoir obscurcit son cœur.', NULL),
('Samsagace Gamegie', 2980, 62, 'Troisième âge', 'Quatrième âge', 'Masculin', 'Jardinier', $$ Samsagace Gamgi, plus connu sous le nom de Sam, est un hobbit de la Comté, humble jardinier et fidèle compagnon de Frodon Sacquet dans sa quête pour détruire l’Anneau Unique. Petit, trapu et au cœur généreux, il incarne la loyauté, le courage discret et la détermination des hobbits ordinaires face à des défis extraordinaires. Bien qu’au départ simple serviteur et ami de Frodon, Sam se révèle être un héros à part entière, capable de surmonter la peur, la fatigue et le désespoir pour protéger son maître et accomplir la mission de sauver la Terre du Milieu. Sa persévérance, sa bonté et sa modestie font de lui un soutien inébranlable et souvent le moteur moral de la Communauté, capable de gestes de bravoure impressionnants, comme affronter des ennemis redoutables ou porter l’Anneau quand Frodon est trop affaibli. Après la chute de Sauron, Sam retourne dans la Comté, où il devient un leader respecté, épouse Rosie Cotton et fonde une famille, tout en conservant les valeurs simples mais profondes qui l’ont guidé tout au long de son périple, devenant un symbole de courage, d’amitié et de dévouement sans faille. $$, 'La loyauté et l’amitié sont des armes plus puissantes que n’importe quelle épée.', NULL),
('Nazguls', NULL, NULL, 'Deuxième âge', 'Troisième âge', 'Masculin', 'Guerrier', $$ Les Nazgûls, également appelés les Neuf Cavaliers ou les Spectres de l’Anneau, sont d’anciens rois humains corrompus par les neuf anneaux de pouvoir offerts par Sauron. Transformés en serviteurs immortels et quasi invisibles, ils sont liés à l’Anneau Unique et à la volonté de leur maître, incapables de vivre sans son influence. Revêtus de robes noires et portant des armes terrifiantes, leur présence inspire peur et désespoir, et ils sont capables de traquer sans relâche quiconque porte l’Anneau. Leurs pouvoirs incluent la peur surnaturelle, la capacité à percevoir les intentions des mortels et une endurance surhumaine, faisant d’eux des chasseurs implacables et redoutables. Menés par le Roi-Sorcier d’Angmar, le plus puissant des neuf, les Nazgûl jouent un rôle central dans la tentative de Sauron de reprendre l’Anneau et de dominer la Terre du Milieu, semant terreur et chaos parmi les peuples libres jusqu’à leur destruction avec la chute de Sauron à la fin de la Guerre de l’Anneau. Leur existence symbolise la corruption par le pouvoir et la soumission totale à la volonté du mal. $$, 'Nul ne voit leur visage, nul ne sent leur souffle… et pourtant, la peur précède chacun de leurs pas.', NULL),
('Gothmog', NULL, 3019, 'Troisième âge', 'Troisième âge', 'Masculin', 'Guerrier et chef des armées', $$ Gothmog est un puissant lieutenant des armées de Sauron, connu comme le chef des forces orques lors de la bataille de Minas Tirith au cours de la Guerre de l’Anneau. Cruel, impitoyable et d’une intelligence stratégique redoutable, il prend le commandement des troupes de Mordor après la chute du Roi-Sorcier d’Angmar. Maître dans l’art du siège et de la guerre urbaine, il dirige sans relâche les assauts contre les remparts du Gondor, orchestrant la terreur et la destruction. Bien que ses origines soient incertaines, certains le considèrent comme un orque de haut rang ou un hybride d’orque et de troll, symbole de la brutalité et de la discipline imposée par Sauron à ses légions. Sa férocité et son absence totale de pitié font de lui l’un des plus redoutables capitaines des forces du Mordor. Gothmog incarne la haine aveugle et la soumission absolue au Seigneur des Ténèbres, menant ses troupes jusqu’à la mort dans un déchaînement de rage et de feu. $$, 'L''âge des hommes est achevé, le temps des orques est arrivé !', (SELECT id FROM races WHERE name='Orc')),
('Balin', 2763, 2994, 'Troisième âge', 'Troisième âge', 'Masculin', 'Guerrier et seigneur', $$ Balin, fils de Fundin, est un noble Nain du Peuple de Durin et l’un des compagnons de Thorin Écu-de-Chêne lors de la quête d’Erebor. Sage, courageux et profondément attaché à ses frères d’armes, il se distingue par sa loyauté et son esprit réfléchi, souvent la voix de la raison parmi les Nains. Après la reconquête du Royaume sous la Montagne, Balin entreprend des années plus tard une expédition ambitieuse pour refonder la colonie naine de la Moria, espérant restaurer l’ancienne grandeur de Khazad-dûm. Malgré un début prometteur, son entreprise tourne à la tragédie lorsque les Orques et le Fléau de Durin reprennent la cité. Balin périt aux côtés de ses compagnons, et sa tombe, découverte par la Communauté de l’Anneau, demeure un symbole poignant du courage et de la ténacité des Nains face à des forces bien plus puissantes qu’eux. Balin incarne la sagesse, la mémoire et la fierté du peuple nain, un héros dont la quête illustre à la fois la grandeur et la fatalité de ceux qui cherchent à raviver les gloires perdues. $$, 'Il y en a un que je pourrais appeler roi !', (SELECT id FROM races WHERE name='Nain')),
('Bolg', NULL, 2941, 'Troisième âge', 'Troisième âge', 'Masculin', 'Guerrier et chef des armées', $$ Bolg est un redoutable chef orque du Nord, fils d’Azog le Profanateur. Héritier de la haine de son père envers les Nains, il commande les armées de Gundabad et du Mont Gram lors de la Bataille des Cinq Armées. Cruel, impitoyable et d’une force brutale, Bolg incarne la férocité et la sauvagerie du peuple orque. Son intelligence tactique et sa soif de vengeance font de lui un ennemi redouté, aussi bien des Nains que des Elfes et des Hommes. Durant la bataille, il mène ses troupes avec une rage implacable, semant le chaos et la mort jusqu’à sa confrontation finale avec Beorn, qui met fin à sa vie. La mort de Bolg marque la chute du dernier grand seigneur orque du Nord avant la montée en puissance de Sauron. Bolg symbolise la brutalité vengeresse et la corruption du mal, une force née de la haine et consumée par elle. $$, 'Alors vint Bolg, fils d’Azog, dont tu as tué le père en Moria. C’était un orque puissant, d’une lignée ancienne.', (SELECT id FROM races WHERE name='Orc')),
('Gandalf', NULL, NULL, $$Avant la création de Arda$$, NULL, 'Masculin', 'Magicien', $$ Gandalf est un Maiar envoyé en Terre du Milieu sous l’apparence d’un vieil homme sage et puissant, membre de l’ordre des Istari. Connu sous le nom de Gandalf le Gris, puis Gandalf le Blanc après sa résurrection, il joue un rôle central dans la lutte contre Sauron et la protection des peuples libres. Sage, bienveillant et doté d’une profonde connaissance des langues, des cultures et de la magie de la Terre du Milieu, il guide et conseille les héros, tels que Bilbo, Frodon et la Communauté de l’Anneau. Gandalf est à la fois un stratège et un mentor, capable d’inspirer courage et espoir dans les moments les plus sombres. Sa maîtrise du feu, de la lumière et de la magie subtile, ainsi que son habileté à manipuler les forces de la nature, en font un adversaire redoutable pour les serviteurs de Sauron. Il incarne la sagesse, la persévérance et le sacrifice, un pilier moral et spirituel dans la lutte contre le mal, guidant la Terre du Milieu vers la victoire et la restauration de l’équilibre. $$, 'Je suis un serviteur du Feu Secret, détenteur de la flamme d’Anor. Le feu sombre ne vous servira à rien, flamme d’Udûn.', NULL),
('Arwen', 241, 121, 'Troisième âge', 'Quatrième âge', 'Féminin', 'Noble', $$ Arwen est une noble elfe de la Maison de l’Evenstar, fille d’Elrond, seigneur de Fondcombe. D’une beauté et d’une grâce légendaires, elle incarne l’élégance et la sagesse des Elfes. Profondément attachée à la Terre du Milieu et à ses habitants, elle choisit l’amour de l’humain Aragorn, renonçant à l’immortalité pour partager sa vie avec lui. Courageuse et déterminée, Arwen joue un rôle discret mais crucial dans la lutte contre Sauron, offrant soutien et espoir à ceux qui défendent la liberté. Sa patience, sa sagesse et sa capacité à inspirer le courage font d’elle un symbole de lumière et de persévérance au cœur des temps sombres. Elle représente l’amour, le sacrifice et l’harmonie entre les peuples de la Terre du Milieu, illustrant la force tranquille et la profondeur des Elfes face aux épreuves du monde mortel. $$, 'Je renonce à l’immortalité pour partager la vie avec toi.', (SELECT id FROM races WHERE name='Elfe'))
ON CONFLICT (name) DO NOTHING;

---------------------description -----------------
INSERT INTO descriptions (entity_type, entity_id, title, content, order_index)
VALUES
('character', 1, 'Apparence', 'Grand, cheveux argentés', 1),
('character', 1, 'Histoire', 'Né dans les montagnes du Nord', 2),
('character', 2, 'Histoire', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 1),
('race', 2, 'Origine', 'Peuple ancien du désert', 1);


-- -----------------------------
-- Inserts History
-- -----------------------------
INSERT INTO history (name, description, citation, start_year, end_year, era, place_id, relation_type_id)
VALUES
('Bataille des Champs du Pelennor', $$ La bataille du Champ de Pelennor se déroula devant les remparts de Minas Tirith, capitale du Gondor, pendant la Guerre de l’Anneau. Les forces de Sauron, composées d’Orques, de Haradrim et de Mumakil, assiégèrent la ville avec une violence dévastatrice. Les armées du Gondor, menées par le roi Théoden et les chevaliers du Rohan, résistèrent héroïquement. Les renforts d’Aragorn, venant des terres d’Anduin avec les armées des morts, permirent de briser l’assaut. Ce fut un moment décisif dans la lutte contre Sauron, où le courage et le sacrifice se mêlèrent dans une lutte titanesque entre le bien et le mal. $$,'Les armées du Gondor et les alliés du rohan affrontèrent le Mordor dans un dernier souffle de courage..',3019,3019,'Troisième âge',(SELECT id FROM places WHERE title='Minas Tirith'),(SELECT id FROM relation_types WHERE name='bataille')),
('Bataille des cinq armés', $$ La bataille des Cinq Armées eut lieu aux portes d’Erebor, après que le dragon Smaug fut mort. Les peuples de Nains, Elfes et Hommes revendiquaient la richesse de la Montagne Solitaire, tandis que des Orques et des Wargs arrivaient pour profiter du chaos. Thorin Écu-de-Chêne et sa compagnie durent faire face à ces forces opposées, et la bataille fut féroce et sanglante. Malgré les pertes, l’union temporaire des différentes armées permit de repousser les envahisseurs et de sécuriser Erebor. Cet affrontement marqua la fin d’une ère pour les Nains et changea durablement l’équilibre des forces dans la région. $$, 'Des peuples différents s’unirent et s’affrontèrent pour le trésor d’Erebor.',2941, 2941,'Troisième âge', (SELECT id FROM places WHERE title='Erebor (Montagne Solitaire)'), (SELECT id FROM relation_types WHERE name='bataille')),
('Anniversaire de Bilbon Sacquet', $$ Le centenaire anniversaire de Bilbon Sacquet fut célébré dans la Comté avec faste et festivités. Tous les Hobbits du village se rassemblèrent pour partager nourriture, musique et danses, honorant la longévité exceptionnelle de Bilbon. Mais derrière cette fête joyeuse se cachait un moment crucial : Bilbon disparut mystérieusement après avoir utilisé l’Anneau Unique, laissant Frodo hériter de cette lourde responsabilité. L’événement symbolise à la fois la joie de la vie simple des Hobbits et l’amorce d’une aventure qui allait changer la Terre du Milieu. $$ ,'Bilbon organisa une grande fête pour ses 111 ans.',3001,3001,'Troisième âge',(SELECT id FROM places WHERE title='Hobbitebourg'),(SELECT id FROM relation_types WHERE name='cérémonie'))
ON CONFLICT (name, start_year, place_id) DO NOTHING;

-- -----------------------------
-- Inserts Map Geometry
-- -----------------------------
-- ==================== RÉGIONS ====================

-- MORDOR
INSERT INTO map_region (name, shape_data, place_id)
VALUES
('Mordor', ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[5148,2377],[4476,2405],[3924,2273],[3996,3270],[4976,3286],[5148,2377]]]}'), (SELECT id FROM places WHERE title='Mordor'))
ON CONFLICT (name) DO NOTHING;

-- GONDOR
INSERT INTO map_region (name, shape_data, place_id)
VALUES
('Gondor', ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[1452,2866],[1928,2518],[2528,2425],[3000,2586],[3776,2570],[3860,3334],[2936,3294],[2348,2854],[1452,2866]]]}'), (SELECT id FROM places WHERE title='Gondor'))
ON CONFLICT (name) DO NOTHING;

-- ERIADOR
INSERT INTO map_region (name, shape_data, place_id)
VALUES
('Eriador', ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[1794,2325],[2340,2215],[2856,1449],[2860,1059],[2672,587],[2132,391],[1236,441],[1010,755],[978,1099],[1462,1753],[1794,2325]]]}'), (SELECT id FROM places WHERE title='Eriador'))
ON CONFLICT (name) DO NOTHING;

-- RHOVANION
INSERT INTO map_region (name, shape_data, place_id)
VALUES
('Rhovanion', ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[2636,1897],[2952,1281],[2772,593],[4420,609],[4216,2218],[3784,2254],[3528,2470],[3232,2138],[3228,1970],[2636,1897]]]}'), (SELECT id FROM places WHERE title='Rhovanion'))
ON CONFLICT (name) DO NOTHING;

-- ROHAN
INSERT INTO map_region (name, shape_data, place_id)
VALUES
('Rohan', ST_GeomFromGeoJSON('{"type":"Polygon","coordinates":[[[2456,1985],[2472,2385],[3320,2634],[3212,2029],[2644,1937],[2456,1985]]]}'), (SELECT id FROM places WHERE title='Rohan'))
ON CONFLICT (name) DO NOTHING;

-- ==================== LIEUX (MARKERS) ====================

-- MORDOR
INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Montagne du Destin (Orodruin)', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[4204,2558]}'), 'montagne'::marker_type, (SELECT id FROM places WHERE title='Montagne du Destin (Orodruin)'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Barad-dûr', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[4391,2496]}'), 'dark'::marker_type, (SELECT id FROM places WHERE title='Barad-dûr'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Cirith Ungol', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3912,2609]}'), 'forteresse'::marker_type, (SELECT id FROM places WHERE title='Cirith Ungol'))
ON CONFLICT (name) DO NOTHING;

-- GONDOR
INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Minas Tirith', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3498,2657]}'), 'capitale'::marker_type, (SELECT id FROM places WHERE title='Minas Tirith'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Osgiliath', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3630,2687]}'), 'ruine'::marker_type, (SELECT id FROM places WHERE title='Osgiliath'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Champ de Pelennor', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3550,2705]}'), 'plaine'::marker_type, (SELECT id FROM places WHERE title='Champ de Pelennor'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Minas Morgul', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3811,2687]}'), 'forteresse'::marker_type, (SELECT id FROM places WHERE title='Minas Morgul'))
ON CONFLICT (name) DO NOTHING;

-- ERIADOR
INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Fourré aux Trolls', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2542,1147]}'), 'foret'::marker_type, (SELECT id FROM places WHERE title='Fourré aux Trolls'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Amon Sûl', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2278,1121]}'), 'ruine'::marker_type, (SELECT id FROM places WHERE title='Amon Sûl'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Moria', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2770,1533]}'), 'mine'::marker_type, (SELECT id FROM places WHERE title='Moria'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Col de Caradhras', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2758,1433]}'), 'montagne'::marker_type, (SELECT id FROM places WHERE title='Col de Caradhras'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Bree', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2036,1149]}'), 'ville'::marker_type, (SELECT id FROM places WHERE title='Bree'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('La Comté', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[1522,1205]}'), 'capitale'::marker_type, (SELECT id FROM places WHERE title='La Comté'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Hobbitebourg', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[1482,1121]}'), 'ville'::marker_type, (SELECT id FROM places WHERE title='Hobbitebourg'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Cul-de-Sac', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[1536,1145]}'), 'special'::marker_type, (SELECT id FROM places WHERE title='Cul-de-Sac'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Fondcombe', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2704,1121]}'), 'ville'::marker_type, (SELECT id FROM places WHERE title='Fondcombe'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Havre Gris', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[1096,1191]}'), 'port'::marker_type, (SELECT id FROM places WHERE title='Havre Gris'))
ON CONFLICT (name) DO NOTHING;

-- RHOVANION
INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Emyn Muil', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3456,2081]}'), 'montagne'::marker_type, (SELECT id FROM places WHERE title='Emyn Muil'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Erebor (Montagne Solitaire)', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3940,955]}'), 'forteresse'::marker_type, (SELECT id FROM places WHERE title='Erebor (Montagne Solitaire)'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Foret Noire', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3632,1375]}'), 'foret'::marker_type, (SELECT id FROM places WHERE title='foret Noire'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Champs aux Iris', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3170,1321]}'), 'plaine'::marker_type, (SELECT id FROM places WHERE title='Champs aux Iris'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Lothlórien', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2976,1639]}'), 'foret'::marker_type, (SELECT id FROM places WHERE title='Lothlórien'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Caras Galadhon', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3034,1659]}'), 'ville'::marker_type, (SELECT id FROM places WHERE title='Caras Galadhon'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Statues des Rois d''Argonath', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3294,2104]}'), 'monument'::marker_type, (SELECT id FROM places WHERE title='Statues des Rois d''Argonath'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Marais des Morts', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[3664,2171]}'), 'eau'::marker_type, (SELECT id FROM places WHERE title='Marais des Morts'))
ON CONFLICT (name) DO NOTHING;

-- ROHAN
INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Isengard', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2527,2031]}'), 'forteresse'::marker_type, (SELECT id FROM places WHERE title='Isengard'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Edoras', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2750,2345]}'), 'capitale'::marker_type, (SELECT id FROM places WHERE title='Edoras'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Fangorn', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2768,1959]}'), 'foret'::marker_type, (SELECT id FROM places WHERE title='Fangorn'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Gouffre de Helm', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2530,2259]}'), 'forteresse'::marker_type, (SELECT id FROM places WHERE title='Gouffre de Helm'))
ON CONFLICT (name) DO NOTHING;

INSERT INTO map_marker (name, location, type, place_id)
VALUES
('Passage des Morts', ST_GeomFromGeoJSON('{"type":"Point","coordinates":[2688,2447]}'), 'chemin'::marker_type, (SELECT id FROM places WHERE title='Passage des Morts'))
ON CONFLICT (name) DO NOTHING;
