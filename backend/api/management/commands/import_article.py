"""
Management command : python manage.py import_article

Ce command importe automatiquement toutes les données d'un article
dans la base de données Django après la migration.

Usage :
    python manage.py import_article              # import le 1er article trouvé
    python manage.py import_article --id <uuid>  # import un article précis
    python manage.py import_article --create     # crée un nouvel article s'il n'en existe pas
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from api.models import Article, Author, ArticleAuthor


# ══════════════════════════════════════════════════════════════
#  DONNÉES DE L'ARTICLE
# ══════════════════════════════════════════════════════════════

ARTICLE_DATA = {
    "title_fr":    "Évaluation et Cartographie des Infrastructures Routières Urbaines de N'Djamena",
    "title_en":    "Evaluation and Mapping of Urban Road Infrastructure in N'Djamena",
    "title_ar":    "تقييم ورسم خرائط البنية التحتية للطرق الحضرية في انجمينا",
    "subtitle_fr": "Approche Multi-Source par SIG, Télédétection et Intelligence Artificielle Appliquée à la Ville de N'Djamena, Tchad",
    "subtitle_en": "Multi-Source Approach using GIS, Remote Sensing and Artificial Intelligence Applied to N'Djamena, Chad",
    "subtitle_ar": "نهج متعدد المصادر باستخدام نظم المعلومات الجغرافية والاستشعار عن بعد والذكاء الاصطناعي",
    "abstract_fr": "L'état des infrastructures routières constitue un indicateur clé du développement urbain et de la qualité de vie des populations. N'Djamena, capitale du Tchad, illustre cette problématique avec un réseau routier de plus de 1 000 km dont la majorité est en état médiocre à critique. Cette étude propose une approche méthodologique intégrée combinant SIG, photogrammétrie drone GNSS RTK et deep learning (YOLOv8) pour cartographier, évaluer et analyser l'ensemble du réseau routier. Les résultats révèlent que 63 % du réseau présente un PCI inférieur à 50 (médiocre à très mauvais), avec une concentration spatiale dans les arrondissements périphériques. Le modèle IA atteint une précision mAP@0.5 de 91,3 %.",
    "abstract_en": "The condition of road infrastructure is a key indicator of urban development and quality of life. N'Djamena illustrates this issue with a road network of over 1,000 km, mostly in poor to critical condition. This study proposes an integrated methodological approach combining GIS, drone GNSS RTK photogrammetry and deep learning (YOLOv8). Results reveal 63% of the network has PCI below 50. The AI model achieves 91.3% mAP@0.5 accuracy.",
    "abstract_ar": "يُعد حالة البنية التحتية للطرق مؤشراً رئيسياً للتنمية الحضرية. تجسد نجامينا هذه المشكلة بشبكة طرق تزيد عن 1000 كم معظمها في حالة سيئة. تقترح هذه الدراسة نهجًا متكاملًا يجمع GIS والتصوير بالطائرات بدون طيار والتعلم العميق (YOLOv8). النتائج: 63% بمؤشر PCI أقل من 50، ودقة نموذج الذكاء الاصطناعي 91.3%.",
    "keywords_fr": "GIS, PCI, IRI, Télédétection, Intelligence Artificielle, N'Djamena, Géomatique urbaine",
    "keywords_en": "GIS, PCI, IRI, Remote Sensing, Artificial Intelligence, N'Djamena, Urban Geomatics",
    "keywords_ar": "GIS, PCI, IRI, استشعار عن بعد, ذكاء اصطناعي, انجمينا, جيوماتيكا حضرية",
    "journal_name": "Revue de Géomatique & d'Ingénierie Urbaine",
    "volume":        "Vol. 1",
    "year":          2026,
    "doi":           "10.kiceko/hpb.2026.routier-ndjamena",
    "status":        "published",
    "meta_description_fr": "L'état des infrastructures routières constitue un indicateur clé du développement urbain. N'Djamena illustre cette problématique avec un réseau routier de plus de 1 000 km en état critique.",
    "meta_description_en": "Road infrastructure condition is a key indicator of urban development. N'Djamena illustrates this with a 1,000+ km road network mostly in poor condition.",
    "key_metrics": [
        {"label": "Réseau cartographié",    "value": "1 015", "unit": "km", "icon": "🛣️"},
        {"label": "PCI moyen global",        "value": "46,0",  "unit": "",   "icon": "📊"},
        {"label": "Précision modèle IA",     "value": "91,3",  "unit": "%",  "icon": "🤖"},
        {"label": "Réseau en état critique", "value": "63",    "unit": "%",  "icon": "⚠️"},
    ],
    "references": [
        "ASTM International. (2020). ASTM D6433-20: Standard Practice for Roads and Parking Lots Pavement Condition Index Surveys.",
        "Banque mondiale. (2023). Chad Infrastructure Assessment Report. Washington D.C.",
        "Fan, R. et al. (2022). Pothole detection based on disparity transformation and road surface modeling. IEEE Transactions on Image Processing, 29, 897–908.",
        "Maeda, H. et al. (2018). Road damage detection and classification using deep neural networks. Computer-Aided Civil and Infrastructure Engineering, 33(12), 1127–1141.",
        "Mahamat, A. (2018). Mobilité urbaine et transport à N'Djamena. Revue Tchadienne de Sciences Sociales, 4(2), 12–29.",
        "Mohan, A. et al. (2021). Crack detection using image processing: A critical review. Alexandria Engineering Journal, 57(2), 787–798.",
        "Papagiannakis, A.T. & Masad, E.A. (2008). Pavement Design and Materials. Hoboken, NJ: John Wiley & Sons.",
        "PDNA. (2020). Post-Disaster Needs Assessment Rapport Inondations Tchad 2020. N'Djamena.",
        "Sayers, M.W. et al. (1986). Guidelines for Conducting and Calibrating Road Roughness Measurements. World Bank Technical Paper No. 46.",
        "Shahin, M.Y. & Kohn, S.D. (1979). Pavement Maintenance Management for Roads and Parking Lots. US Army Engineer Waterways Experiment Station.",
        "Ultralytics. (2023). YOLOv8: A New Era of Object Detection. https://github.com/ultralytics/ultralytics",
        "Yohannes, T. & Soromessa, T. (2019). Assessment of road conditions using GIS in Addis Ababa. Ethiopian Journal of Environmental Studies, 12(2), 143–157.",
        "Bambé H.P. (2026). Évaluation et Cartographie des Infrastructures Routières de N'Djamena. Revue de Géomatique & d'Ingénierie Urbaine, vol.1.",
    ],
    "content_sections": [
        {"order":1,"slug":"introduction","title_fr":"1. Introduction","title_en":"1. Introduction","title_ar":"1. مقدمة",
         "content_fr":"<p>Les infrastructures routières représentent l'épine dorsale du développement économique et social de toute agglomération urbaine. Elles conditionnent l'accessibilité aux services essentiels, la mobilité des personnes et des biens, l'attractivité économique et la résilience face aux aléas naturels.</p><p>N'Djamena, capitale et principal pôle économique de la République du Tchad, illustre de manière paradigmatique cette problématique. Malgré leur importance stratégique, les infrastructures routières de N'Djamena ne font l'objet d'aucune cartographie systématique, exhaustive et quantitative.</p><p>Le présent article vise à combler ce vide en proposant une approche méthodologique intégrée, innovante et reproductible, combinant géomatique avancée, photogrammétrie par drone et intelligence artificielle.</p>",
         "content_en":"<p>Road infrastructure represents the backbone of economic and social development of any urban agglomeration. N'Djamena illustrates this issue paradigmatically — despite their strategic importance, N'Djamena's road infrastructure has never been systematically and quantitatively mapped.</p><p>This article aims to fill this gap by proposing an integrated, innovative and reproducible methodological approach, combining advanced geomatics, drone photogrammetry and artificial intelligence.</p>",
         "content_ar":"<p>تمثل البنية التحتية للطرق العمود الفقري للتنمية الاقتصادية والاجتماعية لأي تجمع حضري. انجمينا توضح هذه المشكلة بشكل مثالي. تهدف هذه المقالة إلى سد هذه الفجوة من خلال اقتراح منهجية متكاملة ومبتكرة.</p>"},
        {"order":2,"slug":"objectifs-recherche","title_fr":"1.1 Objectifs de la recherche","title_en":"1.1 Research Objectives","title_ar":"1.1 أهداف البحث",
         "content_fr":"<ul><li>Cartographier de manière exhaustive l'ensemble du réseau routier de N'Djamena (voies primaires, secondaires, tertiaires et pistes non revêtues)</li><li>Établir une nomenclature fonctionnelle en cinq catégories adaptée au contexte tchadien</li><li>Évaluer l'état de chaque segment routier via les indices PCI et IRI</li><li>Mettre en œuvre une chaîne de traitement deep learning pour la détection automatisée des dégradations</li><li>Produire un tableau de bord cartographique interactif pour les décideurs</li><li>Formuler des recommandations stratégiques pour la réhabilitation du réseau</li></ul>",
         "content_en":"<ul><li>Comprehensively map the entire road network of N'Djamena</li><li>Establish a functional nomenclature in five road categories</li><li>Evaluate each road segment using PCI and IRI indices</li><li>Implement a deep learning processing chain for automated damage detection</li><li>Produce an interactive cartographic dashboard for decision-makers</li><li>Formulate strategic recommendations for network rehabilitation</li></ul>",
         "content_ar":"<ul><li>رسم خرائط شاملة لشبكة الطرق بأكملها في انجمينا</li><li>إنشاء تسمية وظيفية في خمس فئات</li><li>تقييم كل قطاع من الطرق عبر مؤشرات PCI و IRI</li><li>تنفيذ سلسلة معالجة تعلم عميق للكشف الآلي عن الأضرار</li><li>إنتاج لوحة قيادة خرائطية تفاعلية</li><li>صياغة توصيات استراتيجية لإعادة تأهيل الشبكة</li></ul>"},
        {"order":3,"slug":"zone-etude","title_fr":"2. Zone d'étude : N'Djamena","title_en":"2. Study Area: N'Djamena","title_ar":"2. منطقة الدراسة: انجمينا",
         "content_fr":"<p>N'Djamena (12°06'N, 15°02'E) est la capitale de la République du Tchad, située à la confluence du fleuve Chari et du Logone, à la frontière camerounaise. La ville est divisée en <strong>dix arrondissements administratifs</strong> couvrant <strong>294 km²</strong>.</p><p>Le réseau routier estimé totalise environ <strong>1 015 km</strong> de voies toutes catégories. Seuls 15 à 18 % bénéficient d'un revêtement bitumineux ou bétonné, concentrés dans les arrondissements centraux (1er, 2ème, 6ème).</p><p><strong>⚠ Facteurs aggravants :</strong> Inondations saisonnières (500-600 mm/an), trafic de poids lourds non régulé, absence de drainage sur plus de 70 % du linéaire, maintenance exclusivement curative et croissance démographique non maîtrisée.</p>",
         "content_en":"<p>N'Djamena (12°06'N, 15°02'E) is the capital of Chad, at the confluence of the Chari and Logone rivers on the Cameroonian border. The city has <strong>ten administrative districts</strong> covering <strong>294 km²</strong>.</p><p>The road network totals approximately <strong>1,015 km</strong>. Only 15-18% has bituminous or concrete pavement, concentrated in central districts.</p><p><strong>⚠ Aggravating factors:</strong> Seasonal flooding (500-600 mm/year), unregulated heavy traffic, no drainage on 70%+ of the network.</p>",
         "content_ar":"<p>انجمينا (12°06'N, 15°02'E) هي عاصمة تشاد، تقع عند ملتقى نهر شاري ولوغون. تنقسم إلى <strong>عشر مقاطعات إدارية</strong> تغطي <strong>294 كم²</strong>.</p><p>شبكة الطرق تبلغ حوالي <strong>1015 كم</strong>. فقط 15-18% لديها رصف إسفلتي أو خرساني.</p>"},
        {"order":4,"slug":"revue-litterature","title_fr":"3. Revue de littérature","title_en":"3. Literature Review","title_ar":"3. مراجعة الأدبيات",
         "content_fr":"<p>Le <strong>Pavement Condition Index (PCI)</strong>, développé par l'US Army Corps of Engineers et normalisé ASTM D6433-20, constitue la méthode de référence mondiale d'évaluation visuelle des chaussées sur une échelle de 0 à 100. L'<strong>International Roughness Index (IRI)</strong> mesure la rugosité longitudinale du profil de chaussée.</p><p>L'émergence du deep learning a ouvert de nouvelles perspectives pour l'automatisation du diagnostic des chaussées. Les architectures CNN de type <strong>YOLO, Faster R-CNN et EfficientDet</strong> permettent la détection et la classification automatique des dégradations avec des niveaux de précision proches de l'expert humain.</p>",
         "content_en":"<p>The <strong>Pavement Condition Index (PCI)</strong>, standardized ASTM D6433-20, is the world reference method for visual pavement evaluation on a 0-100 scale. The <strong>International Roughness Index (IRI)</strong> measures longitudinal roughness.</p><p>Deep learning architectures such as <strong>YOLO, Faster R-CNN and EfficientDet</strong> enable automatic damage detection with human-expert-level accuracy.</p>",
         "content_ar":"<p><strong>مؤشر حالة الرصف (PCI)</strong> المعياري ASTM D6433-20 هو المرجع العالمي للتقييم البصري على مقياس 0-100. <strong>مؤشر الخشونة الدولي (IRI)</strong> يقيس الخشونة الطولية.</p><p>معماريات التعلم العميق مثل <strong>YOLO و Faster R-CNN</strong> تتيح الكشف الآلي عن الأضرار بدقة قريبة من الخبير البشري.</p>"},
        {"order":5,"slug":"methodologie","title_fr":"4. Méthodologie","title_en":"4. Methodology","title_ar":"4. المنهجية",
         "content_fr":"<p>La méthodologie se décompose en <strong>cinq phases successives</strong> :</p><ol><li><strong>Phase 1</strong> — Collecte et préparation des données géospatiales</li><li><strong>Phase 2</strong> — Cartographie et catégorisation du réseau</li><li><strong>Phase 3</strong> — Évaluation PCI et IRI</li><li><strong>Phase 4</strong> — Détection IA avec YOLOv8</li><li><strong>Phase 5</strong> — Tableau de bord cartographique interactif</li></ol>",
         "content_en":"<p>The methodology has <strong>five successive phases</strong>:</p><ol><li><strong>Phase 1</strong> — Geospatial data collection and preparation</li><li><strong>Phase 2</strong> — Network mapping and categorization</li><li><strong>Phase 3</strong> — PCI and IRI evaluation</li><li><strong>Phase 4</strong> — AI detection with YOLOv8</li><li><strong>Phase 5</strong> — Interactive cartographic dashboard</li></ol>",
         "content_ar":"<p>تنقسم المنهجية إلى <strong>خمس مراحل متتالية</strong>:</p><ol><li><strong>المرحلة 1</strong> — جمع البيانات الجغرافية وإعدادها</li><li><strong>المرحلة 2</strong> — الرسم الخرائطي والتصنيف</li><li><strong>المرحلة 3</strong> — تقييم PCI و IRI</li><li><strong>المرحلة 4</strong> — كشف الذكاء الاصطناعي بـ YOLOv8</li><li><strong>المرحلة 5</strong> — لوحة القيادة الخرائطية التفاعلية</li></ol>"},
        {"order":6,"slug":"collecte-donnees","title_fr":"4.1 Collecte des données","title_en":"4.1 Data Collection","title_ar":"4.1 جمع البيانات",
         "content_fr":"<p><strong>Données géospatiales de base :</strong> Extraction depuis OpenStreetMap (OSM) via l'API Overpass, complétée par ASTER GDEM v3 et Sentinel-2 (10 m).</p><p><strong>Levés GPS terrain :</strong> GNSS RTK (précision ≤ 2 cm) pour les axes primaires/secondaires, GPS randonnée (±5 m) pour les pistes tertiaires.</p><p><strong>Drone photogrammétrie :</strong> DJI Mavic 3, résolution 5 cm/px, recouvrement 80%/70%.</p>",
         "content_en":"<p><strong>Base geospatial data:</strong> OpenStreetMap via Overpass API, complemented by ASTER GDEM v3 and Sentinel-2 (10 m).</p><p><strong>Field GPS surveys:</strong> GNSS RTK (≤ 2 cm) for primary/secondary axes, hiking GPS (±5 m) for tertiary tracks.</p><p><strong>Drone photogrammetry:</strong> DJI Mavic 3, 5 cm/px resolution, 80%/70% overlap.</p>",
         "content_ar":"<p><strong>البيانات الجغرافية الأساسية:</strong> OpenStreetMap عبر API Overpass، بالإضافة إلى ASTER GDEM v3 و Sentinel-2.</p><p><strong>مسوحات GPS الميدانية:</strong> GNSS RTK (≤ 2 سم) للمحاور الرئيسية.</p><p><strong>تصوير بالطائرات بدون طيار:</strong> DJI Mavic 3، دقة 5 سم/بكسل.</p>"},
        {"order":7,"slug":"evaluation-pci-iri","title_fr":"4.2 Évaluation PCI et IRI","title_en":"4.2 PCI and IRI Evaluation","title_ar":"4.2 تقييم PCI و IRI",
         "content_fr":"<p>Le PCI est calculé conformément à ASTM D6433-20 sur des sections de <strong>50 m</strong> (voies bitumées) et <strong>30 m</strong> (pistes).</p><p>L'IRI est mesuré par profilométrie inertielle via accéléromètre triaxial (norme ISO 8608) et par estimation depuis le profil LiDAR extrait des orthophotos drone.</p>",
         "content_en":"<p>PCI is calculated according to ASTM D6433-20 on <strong>50 m sections</strong> (paved roads) and <strong>30 m</strong> (tracks).</p><p>IRI is measured by inertial profilometry via triaxial accelerometer (ISO 8608) and from LiDAR profile extracted from drone orthophotos.</p>",
         "content_ar":"<p>يتم حساب PCI وفقاً لـ ASTM D6433-20 على أقسام <strong>50 م</strong> (طرق معبدة) و <strong>30 م</strong> (مسارات).</p>"},
        {"order":8,"slug":"detection-ia-yolov8","title_fr":"4.3 Détection IA — YOLOv8","title_en":"4.3 AI Detection — YOLOv8","title_ar":"4.3 كشف الذكاء الاصطناعي — YOLOv8",
         "content_fr":"<p>Un pipeline de traitement automatisé est développé autour du modèle <strong>YOLOv8</strong>. Le jeu de données d'entraînement comprend <strong>8 500 images annotées</strong> manuellement, complétées par CrackForest et Road Damage Dataset.</p><p><strong>Quatre classes cibles :</strong> fissures, nids-de-poule, orniérage et déchaussement de bordure.</p><p>🤖 <strong>Performance :</strong> mAP@0.5 = <strong>91,3 %</strong> — mAP@0.5:0.95 = <strong>72,8 %</strong></p>",
         "content_en":"<p>An automated pipeline around <strong>YOLOv8</strong> with <strong>8,500 manually annotated images</strong>, supplemented by CrackForest and Road Damage Dataset.</p><p><strong>Four target classes:</strong> cracks, potholes, rutting and edge stripping.</p><p>🤖 <strong>Performance:</strong> mAP@0.5 = <strong>91.3%</strong> — mAP@0.5:0.95 = <strong>72.8%</strong></p>",
         "content_ar":"<p>خط معالجة آلي حول <strong>YOLOv8</strong> مع <strong>8500 صورة موضحة يدوياً</strong>.</p><p><strong>أربع فئات:</strong> الشقوق، الحفر، الأخاديد، تقشير الحواف.</p><p>🤖 <strong>الأداء:</strong> mAP@0.5 = <strong>91.3%</strong></p>"},
        {"order":9,"slug":"resultats","title_fr":"5. Résultats","title_en":"5. Results","title_ar":"5. النتائج",
         "content_fr":"<p>L'inventaire exhaustif a permis de recenser et cartographier <strong>1 015,3 km</strong> de voies sur les dix arrondissements :</p><ul><li>Voies primaires V1 : <strong>84,7 km</strong> (8,3 %)</li><li>Voies secondaires V2 : <strong>141,2 km</strong> (13,9 %)</li><li>Voies tertiaires V3 : <strong>219,8 km</strong> (21,7 %)</li><li>Pistes non revêtues V4 : <strong>391,4 km</strong> (38,6 %)</li><li>Voies périurbaines V5 : <strong>178,2 km</strong> (17,6 %)</li></ul><p>Taux de revêtement : <strong>18,7 %</strong></p>",
         "content_en":"<p>The exhaustive inventory mapped <strong>1,015.3 km</strong> across ten districts:</p><ul><li>Primary roads V1: <strong>84.7 km</strong> (8.3%)</li><li>Secondary roads V2: <strong>141.2 km</strong> (13.9%)</li><li>Tertiary roads V3: <strong>219.8 km</strong> (21.7%)</li><li>Unpaved tracks V4: <strong>391.4 km</strong> (38.6%)</li><li>Peri-urban V5: <strong>178.2 km</strong> (17.6%)</li></ul><p>Pavement rate: <strong>18.7%</strong></p>",
         "content_ar":"<p>تم رسم خرائط <strong>1015.3 كم</strong> عبر المقاطعات العشر:</p><ul><li>V1: <strong>84.7 كم</strong> (8.3%)</li><li>V2: <strong>141.2 كم</strong> (13.9%)</li><li>V3: <strong>219.8 كم</strong> (21.7%)</li><li>V4: <strong>391.4 كم</strong> (38.6%)</li><li>V5: <strong>178.2 كم</strong> (17.6%)</li></ul>"},
        {"order":10,"slug":"etat-reseau","title_fr":"5.2 État du réseau par arrondissement","title_en":"5.2 Network Condition by District","title_ar":"5.2 حالة الشبكة حسب المقاطعة",
         "content_fr":"<p>Le PCI moyen global de <strong>46,0</strong> classe le réseau dans la catégorie « Médiocre ». Les arrondissements périphériques (7ème, 4ème, 8ème) présentent les scores les plus faibles.</p><p>📊 <strong>Situation critique :</strong> Plus de <strong>63 %</strong> du réseau routier présente un PCI &lt; 50 (médiocre à très mauvais).</p><p>L'indice de Moran global (I = 0,68 ; p &lt; 0,001) confirme une auto-corrélation spatiale positive significative : les dégradations se concentrent géographiquement dans trois clusters — frange nord-est, extensions sud-ouest et marchés centraux.</p>",
         "content_en":"<p>The overall average PCI of <strong>46.0</strong> classifies the network as 'Poor'. Peripheral districts (7th, 4th, 8th) show the lowest scores.</p><p>📊 <strong>Critical situation:</strong> More than <strong>63%</strong> has PCI &lt; 50.</p><p>Global Moran's index (I = 0.68; p &lt; 0.001) confirms significant positive spatial autocorrelation across three clusters.</p>",
         "content_ar":"<p>متوسط PCI الإجمالي <strong>46.0</strong> يصنف الشبكة في فئة 'سيئة'. المقاطعات الطرفية (7، 4، 8) تظهر أدنى الدرجات.</p><p>📊 <strong>وضع حرج:</strong> أكثر من <strong>63%</strong> بمؤشر PCI &lt; 50.</p>"},
        {"order":11,"slug":"performance-ia","title_fr":"5.3 Performance du modèle IA","title_en":"5.3 AI Model Performance","title_ar":"5.3 أداء نموذج الذكاء الاصطناعي",
         "content_fr":"<p><strong>127 400</strong> images drone traitées automatiquement<br><strong>342 800</strong> dégradations géoréférencées détectées</p><p>Répartition : faïençage <strong>41,2 %</strong> — nids-de-poule <strong>28,7 %</strong> — fissures longitudinales <strong>19,4 %</strong> — orniérage <strong>10,7 %</strong></p><p>Accord de <strong>87,3 %</strong> entre le diagnostic automatisé et l'évaluation visuelle expert.</p>",
         "content_en":"<p><strong>127,400</strong> drone images automatically processed<br><strong>342,800</strong> georeferenced damages detected</p><p>Distribution: cracking <strong>41.2%</strong> — potholes <strong>28.7%</strong> — longitudinal cracks <strong>19.4%</strong> — rutting <strong>10.7%</strong></p><p><strong>87.3%</strong> agreement between automated and expert evaluation.</p>",
         "content_ar":"<p><strong>127,400</strong> صورة معالجة تلقائياً<br><strong>342,800</strong> ضرر جغرافي مكتشف</p><p>التوزيع: تشقق <strong>41.2%</strong> — حفر <strong>28.7%</strong> — شقوق طولية <strong>19.4%</strong> — أخاديد <strong>10.7%</strong></p>"},
        {"order":12,"slug":"discussion","title_fr":"6. Discussion et Implications","title_en":"6. Discussion and Implications","title_ar":"6. المناقشة والآثار",
         "content_fr":"<p>Les résultats démontrent la faisabilité d'une approche géomatique intégrée à coût maîtrisé en contexte africain à ressources limitées.</p><p>Sur la base des coûts unitaires de réhabilitation en Afrique centrale, les besoins d'investissement sont estimés entre <strong>280 et 420 milliards FCFA</strong> sur 10 ans — une base de plaidoyer structurée pour la Banque mondiale, la BAD et l'Union européenne.</p><p>La méthodologie est conçue pour être reproductible dans d'autres villes tchadiennes (Moundou, Sarh, Abéché) et en Afrique centrale et de l'Ouest.</p>",
         "content_en":"<p>Results demonstrate the feasibility of an integrated geomatic approach at controlled cost in resource-limited African context.</p><p>Investment needs are estimated at <strong>280-420 billion FCFA</strong> over 10 years — a structured advocacy base for the World Bank, AfDB and EU.</p><p>The methodology is designed to be reproducible in other Chadian cities and comparable African urban contexts.</p>",
         "content_ar":"<p>تُظهر النتائج جدوى نهج جيوماتيكي متكامل في السياق الأفريقي.</p><p>تقدر احتياجات الاستثمار بـ <strong>280-420 مليار فرنك</strong> على 10 سنوات.</p><p>المنهجية قابلة للتكرار في مدن تشادية أخرى وفي أفريقيا الوسطى والغربية.</p>"},
        {"order":13,"slug":"conclusion","title_fr":"7. Conclusion et Recommandations","title_en":"7. Conclusion and Recommendations","title_ar":"7. الخاتمة والتوصيات",
         "content_fr":"<p>Cette étude constitue la <strong>première évaluation cartographique exhaustive et quantitative</strong> des infrastructures routières de N'Djamena.</p><h3>Recommandations stratégiques</h3><ul><li>Institutionnaliser la gestion des actifs routiers via une unité SIG dédiée à la Mairie</li><li>Prioriser les réhabilitations sur critères multicritères (PCI, IRI, trafic, accessibilité)</li><li>Intégrer le drainage dans toute intervention — aucune réhabilitation sans évacuation des eaux pluviales</li><li>Réguler le trafic de poids lourds aux entrées de ville</li><li>Actualiser la base de données par campagnes bisannuelles</li><li>Mobiliser des financements internationaux en s'appuyant sur cette étude</li></ul>",
         "content_en":"<p>This study is the <strong>first exhaustive and quantitative cartographic evaluation</strong> of N'Djamena's road infrastructure.</p><h3>Strategic Recommendations</h3><ul><li>Institutionalize road asset management with a dedicated GIS unit</li><li>Prioritize rehabilitations on multi-criteria (PCI, IRI, traffic, accessibility)</li><li>Integrate drainage in all interventions</li><li>Regulate heavy truck traffic at city entrances</li><li>Update database biannually</li><li>Mobilize international financing using this study as base document</li></ul>",
         "content_ar":"<p>هذه الدراسة هي <strong>أول تقييم خرائطي شامل وكمي</strong> للبنية التحتية للطرق في انجمينا.</p><h3>التوصيات الاستراتيجية</h3><ul><li>إضفاء الطابع المؤسسي على إدارة أصول الطرق</li><li>إعطاء الأولوية لإعادة التأهيل على معايير متعددة</li><li>دمج الصرف في جميع التدخلات</li><li>تنظيم حركة الشاحنات الثقيلة</li><li>تحديث قاعدة البيانات بانتظام</li><li>تعبئة التمويل الدولي</li></ul>"},
    ],
    "author": {
        "first_name": "Hilla Prince",
        "last_name":  "Bambé",
        "title":      "M.",
        "affiliation": "KICEKO CONSULTANT · N'Djamena, Tchad",
        "country":     "Tchad",
        "is_corresponding": True,
    }
}


class Command(BaseCommand):
    help = "Importe automatiquement les données de l'article routier N'Djamena dans la DB"

    def add_arguments(self, parser):
        parser.add_argument('--id',     type=str,  help="UUID de l'article à mettre à jour")
        parser.add_argument('--create', action='store_true', help="Crée un nouvel article si aucun n'existe")
        parser.add_argument('--force',  action='store_true', help="Écrase même si les sections existent déjà")

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=" * 60))
        self.stdout.write(self.style.MIGRATE_HEADING("  IMPORT ARTICLE — Portfolio HPB"))
        self.stdout.write(self.style.MIGRATE_HEADING("=" * 60))

        # ── Trouver ou créer l'article ────────────────────────
        art = None

        if options['id']:
            try:
                art = Article.objects.get(pk=options['id'])
                self.stdout.write(f"  Article ciblé : {art.id}")
            except Article.DoesNotExist:
                raise CommandError(f"Aucun article avec l'id : {options['id']}")

        elif options['create']:
            art = Article.objects.create(
                title_fr="Nouvel article",
                abstract_fr="À compléter",
                status="draft",
                year=2026,
            )
            self.stdout.write(self.style.SUCCESS(f"  ✅ Nouvel article créé : {art.id}"))

        else:
            arts = Article.objects.all()
            if not arts.exists():
                raise CommandError(
                    "Aucun article en base.\n"
                    "Créez d'abord un article dans l'admin ou utilisez --create"
                )
            art = arts.first()
            self.stdout.write(f"  Article trouvé : {art.id}")

        # ── Vérifier si déjà importé ──────────────────────────
        if art.content_sections and not options['force']:
            self.stdout.write(self.style.WARNING(
                f"\n  ⚠️  Cet article a déjà {len(art.content_sections)} sections.\n"
                "  Utilisez --force pour écraser."
            ))
            return

        # ── Mise à jour de tous les champs ────────────────────
        d = ARTICLE_DATA
        art.title_fr    = d['title_fr']
        art.title_en    = d['title_en']
        art.title_ar    = d['title_ar']
        art.subtitle_fr = d['subtitle_fr']
        art.subtitle_en = d['subtitle_en']
        art.subtitle_ar = d['subtitle_ar']
        art.abstract_fr = d['abstract_fr']
        art.abstract_en = d['abstract_en']
        art.abstract_ar = d['abstract_ar']
        art.keywords_fr = d['keywords_fr']
        art.keywords_en = d['keywords_en']
        art.keywords_ar = d['keywords_ar']
        art.journal_name = d['journal_name']
        art.volume       = d['volume']
        art.year         = d['year']
        art.doi          = d['doi']
        art.status       = d['status']
        art.meta_description_fr = d['meta_description_fr']
        art.meta_description_en = d['meta_description_en']
        art.content_sections    = d['content_sections']
        art.references          = d['references']
        art.key_metrics         = d['key_metrics']

        if not art.published_at:
            art.published_at = timezone.now()

        art.save()
        self.stdout.write(self.style.SUCCESS(
            f"\n  ✅ Article mis à jour :\n"
            f"     {len(d['content_sections'])} sections\n"
            f"     {len(d['references'])} références\n"
            f"     {len(d['key_metrics'])} statistiques"
        ))

        # ── Auteur ────────────────────────────────────────────
        a = d['author']
        author, created = Author.objects.get_or_create(
            first_name=a['first_name'], last_name=a['last_name'],
            defaults={
                'title': a['title'], 'affiliation': a['affiliation'],
                'country': a['country'], 'is_corresponding': a['is_corresponding'],
            }
        )
        self.stdout.write(self.style.SUCCESS(
            f"  {'✅ Auteur créé' if created else 'ℹ️  Auteur existant'} : {author}"
        ))

        ArticleAuthor.objects.get_or_create(article=art, author=author, defaults={'order': 1})

        # ── Résumé final ──────────────────────────────────────
        self.stdout.write("")
        self.stdout.write(self.style.MIGRATE_HEADING("=" * 60))
        self.stdout.write(self.style.SUCCESS("  IMPORT TERMINÉ ✅"))
        self.stdout.write(self.style.MIGRATE_HEADING("=" * 60))
        self.stdout.write(f"\n  Frontend : http://localhost:5173/articles/{art.id}")
        self.stdout.write(f"  Admin    : http://localhost:8000/admin/api/article/{art.id}/change/\n")
