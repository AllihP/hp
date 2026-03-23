"""
signals.py — Portfolio HPB

Signal post_save sur Article :
→ Dès qu'un article est enregistré dans l'admin avec le bon DOI
  ou le bon titre, ses sections / références / métriques sont
  injectées automatiquement si les champs sont encore vides.

Logique :
  - Si content_sections est vide  → on injecte les données
  - Si content_sections est rempli → on ne touche à rien
  - Fonctionne pour la création ET la mise à jour depuis l'admin
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# ── Import lazy pour éviter les imports circulaires ──────────
def get_article_model():
    from api.models import Article
    return Article

def get_author_models():
    from api.models import Author, ArticleAuthor
    return Author, ArticleAuthor


# ══════════════════════════════════════════════════════════════
#  DONNÉES DE L'ARTICLE ROUTIER N'DJAMENA
#  (identiques au management command import_article)
# ══════════════════════════════════════════════════════════════

NDJAMENA_KEY_METRICS = [
    {"label": "Réseau cartographié",    "value": "1 015", "unit": "km", "icon": "🛣️"},
    {"label": "PCI moyen global",        "value": "46,0",  "unit": "",   "icon": "📊"},
    {"label": "Précision modèle IA",     "value": "91,3",  "unit": "%",  "icon": "🤖"},
    {"label": "Réseau en état critique", "value": "63",    "unit": "%",  "icon": "⚠️"},
]

NDJAMENA_REFERENCES = [
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
]

NDJAMENA_SECTIONS = [
    {
        "order": 1, "slug": "introduction",
        "title_fr": "1. Introduction",
        "title_en": "1. Introduction",
        "title_ar": "1. مقدمة",
        "content_fr": (
            "<p>Les infrastructures routières représentent l'épine dorsale du développement "
            "économique et social de toute agglomération urbaine. Elles conditionnent "
            "l'accessibilité aux services essentiels, la mobilité des personnes et des biens, "
            "l'attractivité économique et la résilience face aux aléas naturels.</p>"
            "<p>N'Djamena, capitale et principal pôle économique de la République du Tchad, "
            "illustre de manière paradigmatique cette problématique. Malgré leur importance "
            "stratégique, les infrastructures routières de N'Djamena ne font l'objet d'aucune "
            "cartographie systématique, exhaustive et quantitative.</p>"
            "<p>Le présent article vise à combler ce vide en proposant une approche "
            "méthodologique intégrée, innovante et reproductible, combinant géomatique avancée, "
            "photogrammétrie par drone et intelligence artificielle.</p>"
        ),
        "content_en": (
            "<p>Road infrastructure represents the backbone of economic and social development "
            "of any urban agglomeration. N'Djamena illustrates this issue paradigmatically — "
            "despite their strategic importance, N'Djamena's road infrastructure has never been "
            "systematically and quantitatively mapped.</p>"
            "<p>This article aims to fill this gap by proposing an integrated, innovative and "
            "reproducible methodological approach, combining advanced geomatics, drone "
            "photogrammetry and artificial intelligence.</p>"
        ),
        "content_ar": (
            "<p>تمثل البنية التحتية للطرق العمود الفقري للتنمية الاقتصادية والاجتماعية. "
            "انجمينا توضح هذه المشكلة بشكل مثالي. تهدف هذه المقالة إلى سد هذه الفجوة من "
            "خلال اقتراح منهجية متكاملة ومبتكرة تجمع الجيوماتيكا والتصوير بالطائرات بدون "
            "طيار والذكاء الاصطناعي.</p>"
        ),
    },
    {
        "order": 2, "slug": "objectifs-recherche",
        "title_fr": "1.1 Objectifs de la recherche",
        "title_en": "1.1 Research Objectives",
        "title_ar": "1.1 أهداف البحث",
        "content_fr": (
            "<ul>"
            "<li>Cartographier de manière exhaustive l'ensemble du réseau routier de N'Djamena "
            "(voies primaires, secondaires, tertiaires et pistes non revêtues)</li>"
            "<li>Établir une nomenclature fonctionnelle en cinq catégories adaptée au contexte tchadien</li>"
            "<li>Évaluer l'état de chaque segment routier via les indices PCI et IRI</li>"
            "<li>Mettre en œuvre une chaîne de traitement deep learning pour la détection automatisée des dégradations</li>"
            "<li>Produire un tableau de bord cartographique interactif pour les décideurs</li>"
            "<li>Formuler des recommandations stratégiques pour la réhabilitation du réseau</li>"
            "</ul>"
        ),
        "content_en": (
            "<ul>"
            "<li>Comprehensively map the entire road network of N'Djamena</li>"
            "<li>Establish a functional nomenclature in five road categories</li>"
            "<li>Evaluate each road segment using PCI and IRI indices</li>"
            "<li>Implement a deep learning processing chain for automated damage detection</li>"
            "<li>Produce an interactive cartographic dashboard for decision-makers</li>"
            "<li>Formulate strategic recommendations for network rehabilitation</li>"
            "</ul>"
        ),
        "content_ar": (
            "<ul>"
            "<li>رسم خرائط شاملة لشبكة الطرق بأكملها في انجمينا</li>"
            "<li>إنشاء تسمية وظيفية في خمس فئات</li>"
            "<li>تقييم كل قطاع من الطرق عبر مؤشرات PCI و IRI</li>"
            "<li>تنفيذ سلسلة معالجة تعلم عميق للكشف الآلي عن الأضرار</li>"
            "<li>إنتاج لوحة قيادة خرائطية تفاعلية</li>"
            "<li>صياغة توصيات استراتيجية لإعادة تأهيل الشبكة</li>"
            "</ul>"
        ),
    },
    {
        "order": 3, "slug": "zone-etude",
        "title_fr": "2. Zone d'étude : N'Djamena",
        "title_en": "2. Study Area: N'Djamena",
        "title_ar": "2. منطقة الدراسة: انجمينا",
        "content_fr": (
            "<p>N'Djamena (12°06'N, 15°02'E) est la capitale de la République du Tchad, "
            "située à la confluence du fleuve Chari et du Logone, à la frontière camerounaise. "
            "La ville est divisée en <strong>dix arrondissements administratifs</strong> "
            "couvrant <strong>294 km²</strong>.</p>"
            "<p>Le réseau routier estimé totalise environ <strong>1 015 km</strong> de voies "
            "toutes catégories. Seuls 15 à 18 % bénéficient d'un revêtement bitumineux ou "
            "bétonné, concentrés dans les arrondissements centraux (1er, 2ème, 6ème).</p>"
            "<p><strong>⚠ Facteurs aggravants :</strong> Inondations saisonnières "
            "(500-600 mm/an), trafic de poids lourds non régulé, absence de drainage sur plus "
            "de 70 % du linéaire, maintenance exclusivement curative.</p>"
        ),
        "content_en": (
            "<p>N'Djamena (12°06'N, 15°02'E) is the capital of Chad, at the confluence of the "
            "Chari and Logone rivers. The city has <strong>ten administrative districts</strong> "
            "covering <strong>294 km²</strong>.</p>"
            "<p>The road network totals approximately <strong>1,015 km</strong>. Only 15-18% "
            "has bituminous or concrete pavement, concentrated in central districts.</p>"
            "<p><strong>⚠ Aggravating factors:</strong> Seasonal flooding, unregulated heavy "
            "traffic, no drainage on 70%+ of the network.</p>"
        ),
        "content_ar": (
            "<p>انجمينا (12°06'N, 15°02'E) هي عاصمة تشاد، عند ملتقى نهر شاري ولوغون. "
            "تنقسم إلى <strong>عشر مقاطعات إدارية</strong> تغطي <strong>294 كم²</strong>.</p>"
            "<p>شبكة الطرق تبلغ حوالي <strong>1015 كم</strong>. فقط 15-18% لديها رصف إسفلتي.</p>"
        ),
    },
    {
        "order": 4, "slug": "revue-litterature",
        "title_fr": "3. Revue de littérature",
        "title_en": "3. Literature Review",
        "title_ar": "3. مراجعة الأدبيات",
        "content_fr": (
            "<p>Le <strong>Pavement Condition Index (PCI)</strong>, normalisé ASTM D6433-20, "
            "constitue la méthode de référence mondiale d'évaluation visuelle des chaussées "
            "sur une échelle de 0 à 100. L'<strong>International Roughness Index (IRI)</strong> "
            "mesure la rugosité longitudinale du profil de chaussée.</p>"
            "<p>L'émergence du deep learning a ouvert de nouvelles perspectives pour "
            "l'automatisation du diagnostic. Les architectures <strong>YOLO, Faster R-CNN "
            "et EfficientDet</strong> permettent la détection automatique des dégradations "
            "avec des niveaux de précision proches de l'expert humain.</p>"
        ),
        "content_en": (
            "<p>The <strong>Pavement Condition Index (PCI)</strong>, standardized ASTM D6433-20, "
            "is the world reference for visual pavement evaluation on a 0-100 scale. The "
            "<strong>International Roughness Index (IRI)</strong> measures longitudinal roughness.</p>"
            "<p>Deep learning architectures such as <strong>YOLO, Faster R-CNN and EfficientDet"
            "</strong> enable automatic damage detection with human-expert-level accuracy.</p>"
        ),
        "content_ar": (
            "<p><strong>مؤشر حالة الرصف (PCI)</strong> المعياري ASTM D6433-20 هو المرجع "
            "العالمي للتقييم البصري على مقياس 0-100.</p>"
            "<p>معماريات التعلم العميق مثل <strong>YOLO و Faster R-CNN</strong> تتيح الكشف "
            "الآلي عن الأضرار بدقة قريبة من الخبير البشري.</p>"
        ),
    },
    {
        "order": 5, "slug": "methodologie",
        "title_fr": "4. Méthodologie",
        "title_en": "4. Methodology",
        "title_ar": "4. المنهجية",
        "content_fr": (
            "<p>La méthodologie se décompose en <strong>cinq phases successives</strong> :</p>"
            "<ol>"
            "<li><strong>Phase 1</strong> — Collecte et préparation des données géospatiales "
            "(OSM, GNSS RTK, drone DJI Mavic 3)</li>"
            "<li><strong>Phase 2</strong> — Cartographie et catégorisation du réseau "
            "(PostgreSQL/PostGIS, 5 catégories V1→V5)</li>"
            "<li><strong>Phase 3</strong> — Évaluation PCI (ASTM D6433-20) et IRI (ISO 8608)</li>"
            "<li><strong>Phase 4</strong> — Détection IA avec YOLOv8 "
            "(8 500 images annotées, 4 classes)</li>"
            "<li><strong>Phase 5</strong> — Tableau de bord OpenLayers/Flask</li>"
            "</ol>"
        ),
        "content_en": (
            "<p>The methodology has <strong>five successive phases</strong>:</p>"
            "<ol>"
            "<li><strong>Phase 1</strong> — Geospatial data collection (OSM, GNSS RTK, DJI Mavic 3 drone)</li>"
            "<li><strong>Phase 2</strong> — Network mapping and categorization (PostgreSQL/PostGIS, 5 categories V1→V5)</li>"
            "<li><strong>Phase 3</strong> — PCI evaluation (ASTM D6433-20) and IRI (ISO 8608)</li>"
            "<li><strong>Phase 4</strong> — AI detection with YOLOv8 (8,500 annotated images, 4 classes)</li>"
            "<li><strong>Phase 5</strong> — OpenLayers/Flask dashboard</li>"
            "</ol>"
        ),
        "content_ar": (
            "<p>تنقسم المنهجية إلى <strong>خمس مراحل متتالية</strong>:</p>"
            "<ol>"
            "<li><strong>المرحلة 1</strong> — جمع البيانات الجغرافية (OSM، GNSS RTK، طائرة بدون طيار)</li>"
            "<li><strong>المرحلة 2</strong> — الرسم الخرائطي والتصنيف (PostgreSQL/PostGIS)</li>"
            "<li><strong>المرحلة 3</strong> — تقييم PCI و IRI</li>"
            "<li><strong>المرحلة 4</strong> — كشف الذكاء الاصطناعي بـ YOLOv8</li>"
            "<li><strong>المرحلة 5</strong> — لوحة القيادة التفاعلية</li>"
            "</ol>"
        ),
    },
    {
        "order": 6, "slug": "resultats",
        "title_fr": "5. Résultats",
        "title_en": "5. Results",
        "title_ar": "5. النتائج",
        "content_fr": (
            "<p>L'inventaire exhaustif a permis de recenser et cartographier "
            "<strong>1 015,3 km</strong> de voies sur les dix arrondissements :</p>"
            "<ul>"
            "<li>Voies primaires V1 : <strong>84,7 km</strong> (8,3 %)</li>"
            "<li>Voies secondaires V2 : <strong>141,2 km</strong> (13,9 %)</li>"
            "<li>Voies tertiaires V3 : <strong>219,8 km</strong> (21,7 %)</li>"
            "<li>Pistes non revêtues V4 : <strong>391,4 km</strong> (38,6 %)</li>"
            "<li>Voies périurbaines V5 : <strong>178,2 km</strong> (17,6 %)</li>"
            "</ul>"
            "<p>Taux de revêtement bitumineux/bétonné : <strong>18,7 %</strong></p>"
            "<p>Le PCI moyen global de <strong>46,0</strong> classe le réseau dans la "
            "catégorie « Médiocre ». Plus de <strong>63 %</strong> du réseau présente un "
            "PCI &lt; 50. L'indice de Moran (I = 0,68 ; p &lt; 0,001) confirme une "
            "auto-corrélation spatiale positive significative.</p>"
        ),
        "content_en": (
            "<p>The exhaustive inventory mapped <strong>1,015.3 km</strong> across ten districts:</p>"
            "<ul>"
            "<li>Primary roads V1: <strong>84.7 km</strong> (8.3%)</li>"
            "<li>Secondary roads V2: <strong>141.2 km</strong> (13.9%)</li>"
            "<li>Tertiary roads V3: <strong>219.8 km</strong> (21.7%)</li>"
            "<li>Unpaved tracks V4: <strong>391.4 km</strong> (38.6%)</li>"
            "<li>Peri-urban roads V5: <strong>178.2 km</strong> (17.6%)</li>"
            "</ul>"
            "<p>Pavement rate: <strong>18.7%</strong></p>"
            "<p>Overall average PCI of <strong>46.0</strong> classifies the network as 'Poor'. "
            "More than <strong>63%</strong> has PCI &lt; 50. Moran's index (I = 0.68; "
            "p &lt; 0.001) confirms significant positive spatial autocorrelation.</p>"
        ),
        "content_ar": (
            "<p>تم رسم خرائط <strong>1015.3 كم</strong> عبر المقاطعات العشر:</p>"
            "<ul>"
            "<li>V1: <strong>84.7 كم</strong> (8.3%)</li>"
            "<li>V2: <strong>141.2 كم</strong> (13.9%)</li>"
            "<li>V3: <strong>219.8 كم</strong> (21.7%)</li>"
            "<li>V4: <strong>391.4 كم</strong> (38.6%)</li>"
            "<li>V5: <strong>178.2 كم</strong> (17.6%)</li>"
            "</ul>"
            "<p>متوسط PCI <strong>46.0</strong> — أكثر من <strong>63%</strong> بمؤشر PCI &lt; 50.</p>"
        ),
    },
    {
        "order": 7, "slug": "performance-ia",
        "title_fr": "5.1 Performance du modèle IA",
        "title_en": "5.1 AI Model Performance",
        "title_ar": "5.1 أداء نموذج الذكاء الاصطناعي",
        "content_fr": (
            "<p><strong>127 400</strong> images drone traitées automatiquement<br>"
            "<strong>342 800</strong> dégradations géoréférencées détectées</p>"
            "<p>Répartition par type :</p>"
            "<ul>"
            "<li>Faïençage : <strong>41,2 %</strong></li>"
            "<li>Nids-de-poule : <strong>28,7 %</strong></li>"
            "<li>Fissures longitudinales : <strong>19,4 %</strong></li>"
            "<li>Orniérage : <strong>10,7 %</strong></li>"
            "</ul>"
            "<p>Accord de <strong>87,3 %</strong> entre le diagnostic automatisé et l'évaluation visuelle expert.</p>"
        ),
        "content_en": (
            "<p><strong>127,400</strong> drone images automatically processed<br>"
            "<strong>342,800</strong> georeferenced damages detected</p>"
            "<p>Distribution: cracking <strong>41.2%</strong> — potholes <strong>28.7%</strong> "
            "— longitudinal cracks <strong>19.4%</strong> — rutting <strong>10.7%</strong></p>"
            "<p><strong>87.3%</strong> agreement between automated and expert evaluation.</p>"
        ),
        "content_ar": (
            "<p><strong>127,400</strong> صورة معالجة تلقائياً | <strong>342,800</strong> ضرر مكتشف</p>"
            "<p>التشقق <strong>41.2%</strong> — الحفر <strong>28.7%</strong> — "
            "الشقوق الطولية <strong>19.4%</strong> — الأخاديد <strong>10.7%</strong></p>"
        ),
    },
    {
        "order": 8, "slug": "discussion",
        "title_fr": "6. Discussion et Implications",
        "title_en": "6. Discussion and Implications",
        "title_ar": "6. المناقشة والآثار",
        "content_fr": (
            "<p>Les résultats démontrent la faisabilité d'une approche géomatique intégrée "
            "à coût maîtrisé en contexte africain à ressources limitées.</p>"
            "<p>Les besoins d'investissement sont estimés entre <strong>280 et 420 milliards "
            "FCFA</strong> sur 10 ans — base de plaidoyer structurée pour la Banque mondiale, "
            "la BAD et l'Union européenne.</p>"
            "<p>La méthodologie est reproductible dans d'autres villes tchadiennes "
            "(Moundou, Sarh, Abéché) et dans des contextes comparables en Afrique centrale "
            "et de l'Ouest. La documentation complète sera disponible en open source sur GitHub.</p>"
        ),
        "content_en": (
            "<p>Results demonstrate the feasibility of an integrated geomatic approach at "
            "controlled cost in resource-limited African context.</p>"
            "<p>Investment needs estimated at <strong>280-420 billion FCFA</strong> over 10 "
            "years — structured advocacy base for the World Bank, AfDB and EU.</p>"
            "<p>The methodology is reproducible in other Chadian cities and comparable African "
            "urban contexts. Complete documentation will be open source on GitHub.</p>"
        ),
        "content_ar": (
            "<p>تُظهر النتائج جدوى نهج جيوماتيكي متكامل في السياق الأفريقي.</p>"
            "<p>احتياجات الاستثمار: <strong>280-420 مليار فرنك</strong> على 10 سنوات.</p>"
            "<p>المنهجية قابلة للتكرار في مدن تشادية أخرى وفي أفريقيا الوسطى والغربية.</p>"
        ),
    },
    {
        "order": 9, "slug": "conclusion",
        "title_fr": "7. Conclusion et Recommandations",
        "title_en": "7. Conclusion and Recommendations",
        "title_ar": "7. الخاتمة والتوصيات",
        "content_fr": (
            "<p>Cette étude constitue la <strong>première évaluation cartographique exhaustive "
            "et quantitative</strong> des infrastructures routières de N'Djamena. Elle démontre "
            "la faisabilité d'une approche géomatique intégrée pour produire, à coût maîtrisé, "
            "une information géospatiale fiable en contexte à ressources limitées.</p>"
            "<h3>Recommandations stratégiques</h3>"
            "<ul>"
            "<li>Institutionnaliser la gestion des actifs routiers via une unité SIG dédiée à la Mairie</li>"
            "<li>Prioriser les réhabilitations sur critères multicritères (PCI, IRI, trafic, accessibilité)</li>"
            "<li>Intégrer le drainage dans toute intervention — aucune réhabilitation sans évacuation des eaux pluviales</li>"
            "<li>Réguler le trafic de poids lourds aux entrées de ville (contrôle de charge à l'essieu)</li>"
            "<li>Actualiser la base de données par campagnes bisannuelles</li>"
            "<li>Mobiliser des financements internationaux en s'appuyant sur cette étude comme document de base</li>"
            "</ul>"
        ),
        "content_en": (
            "<p>This study is the <strong>first exhaustive and quantitative cartographic "
            "evaluation</strong> of N'Djamena's road infrastructure.</p>"
            "<h3>Strategic Recommendations</h3>"
            "<ul>"
            "<li>Institutionalize road asset management with a dedicated GIS unit in City Hall</li>"
            "<li>Prioritize rehabilitations on multi-criteria (PCI, IRI, traffic, accessibility)</li>"
            "<li>Integrate drainage in all interventions — no rehabilitation without stormwater system</li>"
            "<li>Regulate heavy truck traffic at city entrances (axle load control)</li>"
            "<li>Update database biannually</li>"
            "<li>Mobilize international financing using this study as base document</li>"
            "</ul>"
        ),
        "content_ar": (
            "<p>هذه الدراسة هي <strong>أول تقييم خرائطي شامل وكمي</strong> للبنية التحتية للطرق في انجمينا.</p>"
            "<h3>التوصيات الاستراتيجية</h3>"
            "<ul>"
            "<li>إضفاء الطابع المؤسسي على إدارة أصول الطرق</li>"
            "<li>إعطاء الأولوية لإعادة التأهيل على معايير متعددة</li>"
            "<li>دمج الصرف في جميع التدخلات</li>"
            "<li>تنظيم حركة الشاحنات الثقيلة عند مداخل المدينة</li>"
            "<li>تحديث قاعدة البيانات بانتظام</li>"
            "<li>تعبئة التمويل الدولي</li>"
            "</ul>"
        ),
    },
]

# Mots-clés indiquant que c'est l'article routier N'Djamena
NDJAMENA_KEYWORDS = [
    "ndjamena", "n'djamena", "routier", "road", "pci", "iri", "yolov8",
    "géomatique", "geomatique", "infrastructure", "cartographie",
]


def _is_ndjamena_article(art):
    """Détecte si un article correspond à l'article routier N'Djamena."""
    text = " ".join([
        (art.title_fr or ""),
        (art.doi or ""),
        (art.keywords_fr or ""),
        (art.abstract_fr or ""),
    ]).lower()
    return any(kw in text for kw in NDJAMENA_KEYWORDS)


def _inject_ndjamena_data(art):
    """Injecte les données dans l'article et le sauvegarde."""
    Author, ArticleAuthor = get_author_models()

    art.title_fr    = "Évaluation et Cartographie des Infrastructures Routières Urbaines de N'Djamena"
    art.title_en    = "Evaluation and Mapping of Urban Road Infrastructure in N'Djamena"
    art.title_ar    = "تقييم ورسم خرائط البنية التحتية للطرق الحضرية في انجمينا"
    art.subtitle_fr = "Approche Multi-Source par SIG, Télédétection et Intelligence Artificielle Appliquée à la Ville de N'Djamena, Tchad"
    art.subtitle_en = "Multi-Source Approach using GIS, Remote Sensing and Artificial Intelligence Applied to N'Djamena, Chad"
    art.subtitle_ar = "نهج متعدد المصادر باستخدام نظم المعلومات الجغرافية والاستشعار عن بعد والذكاء الاصطناعي"
    art.abstract_fr = (
        "L'état des infrastructures routières constitue un indicateur clé du développement "
        "urbain et de la qualité de vie des populations. N'Djamena, capitale du Tchad, illustre "
        "cette problématique avec un réseau routier de plus de 1 000 km dont la majorité est en "
        "état médiocre à critique. Cette étude propose une approche méthodologique intégrée "
        "combinant SIG, photogrammétrie drone GNSS RTK et deep learning (YOLOv8). Les résultats "
        "révèlent que 63 % du réseau présente un PCI inférieur à 50. Le modèle IA atteint une "
        "précision mAP@0.5 de 91,3 %."
    )
    art.abstract_en = (
        "The condition of road infrastructure is a key indicator of urban development and quality "
        "of life. N'Djamena illustrates this issue with a road network of over 1,000 km, mostly "
        "in poor to critical condition. This study proposes an integrated methodological approach "
        "combining GIS, drone GNSS RTK photogrammetry and deep learning (YOLOv8). Results reveal "
        "63% of the network has PCI below 50. The AI model achieves 91.3% mAP@0.5 accuracy."
    )
    art.abstract_ar = (
        "يُعد حالة البنية التحتية للطرق مؤشراً رئيسياً للتنمية الحضرية. تجسد نجامينا هذه "
        "المشكلة بشبكة طرق تزيد عن 1000 كم معظمها في حالة سيئة. النتائج: 63% بمؤشر PCI أقل "
        "من 50، ودقة نموذج الذكاء الاصطناعي 91.3%."
    )
    art.keywords_fr  = "GIS, PCI, IRI, Télédétection, Intelligence Artificielle, N'Djamena, Géomatique urbaine"
    art.keywords_en  = "GIS, PCI, IRI, Remote Sensing, Artificial Intelligence, N'Djamena, Urban Geomatics"
    art.keywords_ar  = "GIS, PCI, IRI, استشعار عن بعد, ذكاء اصطناعي, انجمينا, جيوماتيكا حضرية"
    art.journal_name = "Revue de Géomatique & d'Ingénierie Urbaine"
    art.volume       = "Vol. 1"
    art.year         = 2026
    art.content_sections = NDJAMENA_SECTIONS
    art.references       = NDJAMENA_REFERENCES
    art.key_metrics      = NDJAMENA_KEY_METRICS

    if not art.published_at:
        art.published_at = timezone.now()

    # Sauvegarder sans déclencher le signal à nouveau
    Article = get_article_model()
    Article.objects.filter(pk=art.pk).update(
        title_fr=art.title_fr,
        title_en=art.title_en,
        title_ar=art.title_ar,
        subtitle_fr=art.subtitle_fr,
        subtitle_en=art.subtitle_en,
        subtitle_ar=art.subtitle_ar,
        abstract_fr=art.abstract_fr,
        abstract_en=art.abstract_en,
        abstract_ar=art.abstract_ar,
        keywords_fr=art.keywords_fr,
        keywords_en=art.keywords_en,
        keywords_ar=art.keywords_ar,
        journal_name=art.journal_name,
        volume=art.volume,
        year=art.year,
        content_sections=art.content_sections,
        references=art.references,
        key_metrics=art.key_metrics,
        published_at=art.published_at,
    )

    # Auteur
    author, _ = Author.objects.get_or_create(
        first_name="Hilla Prince", last_name="Bambé",
        defaults={
            "title": "M.",
            "affiliation": "KICEKO CONSULTANT · N'Djamena, Tchad",
            "country": "Tchad",
            "is_corresponding": True,
        }
    )
    ArticleAuthor.objects.get_or_create(
        article=art, author=author, defaults={"order": 1}
    )

    print(f"[signal] ✅ Article routier N'Djamena : données injectées automatiquement ({len(NDJAMENA_SECTIONS)} sections)")


# ══════════════════════════════════════════════════════════════
#  SIGNAL POST_SAVE
# ══════════════════════════════════════════════════════════════

@receiver(post_save, sender='api.Article')
def auto_populate_article(sender, instance, created, **kwargs):
    """
    Déclenché à chaque save() sur Article.
    Conditions d'injection :
      1. content_sections est vide ([] ou None)
      2. Le titre/DOI/keywords correspondent à l'article routier N'Djamena
    """
    # Ne rien faire si les sections sont déjà remplies
    if instance.content_sections:
        return

    # Détecter si c'est l'article routier N'Djamena
    if _is_ndjamena_article(instance):
        _inject_ndjamena_data(instance)
