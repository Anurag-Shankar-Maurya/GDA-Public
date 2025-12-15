from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.content.models import Project
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with Project data (EN & ZH-TW) using LoremFlickr and Kingslish Video'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Projects...')

        # Common video from the Kingslish channel for seeding
        # Note: In a real scenario, you would pick specific video IDs from the channel.
        # Here we point to the channel or a representative video format.
        KINGSLISH_CHANNEL_VIDEO = "https://www.youtube.com/watch?v=example_video_id_from_kingslish" 

        projects_data = [
            {
                # English
                "title_en": "English Teaching in Rural Schools",
                "teaser_en": "Help children in remote villages improve their English skills and open doors to new opportunities.",
                "background_objectives_en": "Many rural schools lack resources. Our objective is to provide native-level conversation practice.",
                "tasks_eligibility_en": "Tasks: conduct classes, organize games. Eligibility: Fluent English, patience.",
                "country_en": "Vietnam",
                "theme_en": "Education",
                
                # Traditional Chinese (ZH-TW)
                "title_zh_tw": "偏遠地區學校英語教學",
                "teaser_zh_tw": "幫助偏遠鄉村的兒童提升英語能力，為他們開啟通往新機遇的大門。",
                "background_objectives_zh_tw": "許多鄉村學校缺乏資源。我們的目標是提供母語級別的會話練習。",
                "tasks_eligibility_zh_tw": "任務：授課、組織遊戲。資格：英語流利、有耐心。",
                "country_zh_tw": "越南",
                "theme_zh_tw": "教育",

                # Metadata & Media
                "kicc_project_id": "EDU-VN-001",
                "duration": 40,
                "difficulty": "Medium",
                "total_headcount": 20,
                
                # Images via Lorem Flickr with specific keywords
                "cover_image_url": "https://loremflickr.com/800/600/classroom,vietnam,students",
                "image_urls": [
                    "https://loremflickr.com/800/600/teacher,blackboard,1",
                    "https://loremflickr.com/800/600/teacher,blackboard,2",
                    "https://loremflickr.com/800/600/school,children,1",
                    "https://loremflickr.com/800/600/school,children,2",
                    "https://loremflickr.com/800/600/book,learning,1",
                    "https://loremflickr.com/800/600/book,learning,2",
                    "https://loremflickr.com/800/600/classroom,teaching,1",
                    "https://loremflickr.com/800/600/classroom,teaching,2",
                    "https://loremflickr.com/800/600/volunteer,teacher,1",
                    "https://loremflickr.com/800/600/volunteer,teacher,2",
                    "https://loremflickr.com/800/600/teaching,materials,1",
                    "https://loremflickr.com/800/600/teaching,materials,2",
                    "https://loremflickr.com/800/600/game,learning,1",
                    "https://loremflickr.com/800/600/game,learning,2",
                    "https://loremflickr.com/800/600/group,learning,1",
                    "https://loremflickr.com/800/600/group,learning,2",
                    "https://loremflickr.com/800/600/chart,education,1",
                    "https://loremflickr.com/800/600/chart,education,2",
                    "https://loremflickr.com/800/600/whiteboard,1",
                    "https://loremflickr.com/800/600/whiteboard,2",
                    "https://loremflickr.com/800/600/exam,help,1",
                    "https://loremflickr.com/800/600/exam,help,2",
                    "https://loremflickr.com/800/600/reading,1",
                    "https://loremflickr.com/800/600/reading,2",
                ],
                
                # Videos from Kingslish App Channel
                "video_urls": [
                    "https://www.youtube.com/watch?v=2026_AHS_Taiwan_Trip", # Placeholder for actual channel video
                    "https://www.youtube.com/@kingslishapp" # Fallback to channel URL
                ],

                "application_deadline": timezone.now() + timedelta(days=30),
                "start_date": timezone.now().date() + timedelta(days=45),
                "end_date": timezone.now().date() + timedelta(days=60),
                "is_featured": True,
            },
            {
                # English
                "title_en": "Community Health & Outreach",
                "teaser_en": "Deliver essential health education and basic screenings to remote communities.",
                "background_objectives_en": "Many remote areas lack basic healthcare. We aim to provide health education and screening campaigns.",
                "tasks_eligibility_en": "Tasks: provide basic screenings, teach hygiene. Eligibility: health background preferred, patient-centered.",
                "country_en": "Cambodia",
                "theme_en": "Health",

                # Traditional Chinese (ZH-TW)
                "title_zh_tw": "社區健康與外展",
                "teaser_zh_tw": "為偏遠社區提供基本健康教育與檢查。",
                "background_objectives_zh_tw": "許多偏遠地區缺乏基本醫療。我們的目標是提供健康教育與篩檢活動。",
                "tasks_eligibility_zh_tw": "任務：提供基礎篩檢、教授衛生教育。資格：具醫療背景優先、耐心。",
                "country_zh_tw": "柬埔寨",
                "theme_zh_tw": "健康",

                # Metadata & Media
                "kicc_project_id": "HLT-KH-003",
                "duration": 30,
                "difficulty": "Medium",
                "total_headcount": 30,

                # Images via Lorem Flickr (24 images)
                "cover_image_url": "https://loremflickr.com/800/600/clinic,health,community",
                "image_urls": [
                    "https://loremflickr.com/800/600/clinic,health,1",
                    "https://loremflickr.com/800/600/clinic,health,2",
                    "https://loremflickr.com/800/600/hygiene,education,1",
                    "https://loremflickr.com/800/600/hygiene,education,2",
                    "https://loremflickr.com/800/600/doctor,nurse,1",
                    "https://loremflickr.com/800/600/doctor,nurse,2",
                    "https://loremflickr.com/800/600/village,clinic,1",
                    "https://loremflickr.com/800/600/village,clinic,2",
                    "https://loremflickr.com/800/600/child,checkup,1",
                    "https://loremflickr.com/800/600/child,checkup,2",
                    "https://loremflickr.com/800/600/medical,kit,1",
                    "https://loremflickr.com/800/600/medical,kit,2",
                    "https://loremflickr.com/800/600/fieldclinic,1",
                    "https://loremflickr.com/800/600/fieldclinic,2",
                    "https://loremflickr.com/800/600/community,workshop,1",
                    "https://loremflickr.com/800/600/community,workshop,2",
                    "https://loremflickr.com/800/600/vaccine,education,1",
                    "https://loremflickr.com/800/600/vaccine,education,2",
                    "https://loremflickr.com/800/600/volunteer,health,1",
                    "https://loremflickr.com/800/600/volunteer,health,2",
                    "https://loremflickr.com/800/600/smiling,children,1",
                    "https://loremflickr.com/800/600/smiling,children,2",
                    "https://loremflickr.com/800/600/hands,washing,1",
                    "https://loremflickr.com/800/600/hands,washing,2",
                ],

                # Videos
                "video_urls": [
                    "https://www.youtube.com/watch?v=kingslish_example_1",
                ],

                "application_deadline": timezone.now() + timedelta(days=18),
                "start_date": timezone.now().date() + timedelta(days=25),
                "end_date": timezone.now().date() + timedelta(days=33),
                "is_featured": False,
            },
            {
                "title_en": "Renewable Energy: Solar Village Electrification",
                "teaser_en": "Help build small solar grids to provide power to remote agricultural villages.",
                "background_objectives_en": "Access to electricity helps extend study hours and improve livelihoods. We will install microgrid solutions and teach maintenance.",
                "tasks_eligibility_en": "Tasks: Solar panel installation, system maintenance. Eligibility: electrical/engineering & good communication.",
                "country_en": "Laos",
                "theme_en": "Energy",

                "title_zh_tw": "再生能源：太陽能村莊電氣化",
                "teaser_zh_tw": "協助打造小型太陽能電網，為偏遠農村提供電力。",
                "background_objectives_zh_tw": "電力可延長讀書時間並改善生計。我們將安裝微電網並教導維護。",
                "tasks_eligibility_zh_tw": "任務：太陽能板安裝、系統維護。資格：電機／工程背景與良好溝通能力。",
                "country_zh_tw": "寮國",
                "theme_zh_tw": "能源",

                "kicc_project_id": "ENE-LA-004",
                "duration": 45,
                "difficulty": "Hard",
                "total_headcount": 12,
                "cover_image_url": "https://loremflickr.com/800/600/solar,panels,village",
                "image_urls": [
                    "https://loremflickr.com/800/600/solar,panels,1",
                    "https://loremflickr.com/800/600/solar,panels,2",
                    "https://loremflickr.com/800/600/solar,installation,1",
                    "https://loremflickr.com/800/600/solar,installation,2",
                    "https://loremflickr.com/800/600/microgrid,1",
                    "https://loremflickr.com/800/600/microgrid,2",
                    "https://loremflickr.com/800/600/village,electricity,1",
                    "https://loremflickr.com/800/600/village,electricity,2",
                    "https://loremflickr.com/800/600/engineer,work,1",
                    "https://loremflickr.com/800/600/engineer,work,2",
                    "https://loremflickr.com/800/600/solar,education,1",
                    "https://loremflickr.com/800/600/solar,education,2",
                    "https://loremflickr.com/800/600/panel,maintenance,1",
                    "https://loremflickr.com/800/600/panel,maintenance,2",
                    "https://loremflickr.com/800/600/solar,community,1",
                    "https://loremflickr.com/800/600/solar,community,2",
                    "https://loremflickr.com/800/600/renewable,energy,1",
                    "https://loremflickr.com/800/600/renewable,energy,2",
                    "https://loremflickr.com/800/600/installation,team,1",
                    "https://loremflickr.com/800/600/installation,team,2",
                    "https://loremflickr.com/800/600/solar,village,1",
                    "https://loremflickr.com/800/600/solar,village,2",
                    "https://loremflickr.com/800/600/panel,testing,1",
                    "https://loremflickr.com/800/600/panel,testing,2",
                ],
                "video_urls": [
                    "https://www.youtube.com/watch?v=kingslish_example_solar",
                ],
                "application_deadline": timezone.now() + timedelta(days=45),
                "start_date": timezone.now().date() + timedelta(days=60),
                "end_date": timezone.now().date() + timedelta(days=90),
                "is_featured": True,
            },
            {
                "title_en": "Cultural Exchange: Arts & Heritage Workshops",
                "teaser_en": "Support local artisans through arts workshops, cultural exchange, and documentation of heritage crafts.",
                "background_objectives_en": "Preserving traditional crafts and supporting artisans drives cultural resilience and livelihood improvements.",
                "tasks_eligibility_en": "Tasks: workshop facilitation, documentation. Eligibility: arts/cultural studies background desirable.",
                "country_en": "Indonesia",
                "theme_en": "Culture",

                "title_zh_tw": "文化交流：藝術與傳統工作坊",
                "teaser_zh_tw": "支持當地工匠，透過藝術工作坊、文化交流與傳統工藝紀錄。",
                "background_objectives_zh_tw": "保護傳統工藝並支持工匠，提升文化韌性與生計。",
                "tasks_eligibility_zh_tw": "任務：主持工作坊、紀錄工藝。資格：藝術或文化研究背景佳。",
                "country_zh_tw": "印尼",
                "theme_zh_tw": "文化",

                "kicc_project_id": "CUL-ID-005",
                "duration": 20,
                "difficulty": "Easy",
                "total_headcount": 20,
                "cover_image_url": "https://loremflickr.com/800/600/arts,crafts,heritage",
                "image_urls": [
                    "https://loremflickr.com/800/600/arts,crafts,1",
                    "https://loremflickr.com/800/600/arts,crafts,2",
                    "https://loremflickr.com/800/600/handicraft,1",
                    "https://loremflickr.com/800/600/handicraft,2",
                    "https://loremflickr.com/800/600/artisan,1",
                    "https://loremflickr.com/800/600/artisan,2",
                    "https://loremflickr.com/800/600/workshop,1",
                    "https://loremflickr.com/800/600/workshop,2",
                    "https://loremflickr.com/800/600/cultural,event,1",
                    "https://loremflickr.com/800/600/cultural,event,2",
                    "https://loremflickr.com/800/600/traditional,craft,1",
                    "https://loremflickr.com/800/600/traditional,craft,2",
                    "https://loremflickr.com/800/600/documentation,1",
                    "https://loremflickr.com/800/600/documentation,2",
                    "https://loremflickr.com/800/600/elderly,master,1",
                    "https://loremflickr.com/800/600/elderly,master,2",
                    "https://loremflickr.com/800/600/children,learn,1",
                    "https://loremflickr.com/800/600/children,learn,2",
                    "https://loremflickr.com/800/600/market,crafts,1",
                    "https://loremflickr.com/800/600/market,crafts,2",
                    "https://loremflickr.com/800/600/gallery,exhibition,1",
                    "https://loremflickr.com/800/600/gallery,exhibition,2",
                    "https://loremflickr.com/800/600/sketching,1",
                    "https://loremflickr.com/800/600/sketching,2",
                ],
                "video_urls": [
                    "https://www.youtube.com/watch?v=kingslish_example_arts",
                ],
                "application_deadline": timezone.now() + timedelta(days=40),
                "start_date": timezone.now().date() + timedelta(days=55),
                "end_date": timezone.now().date() + timedelta(days=65),
                "is_hero_highlight": False,
            },
            {
                "title_en": "Agriculture & Food Security Program",
                "teaser_en": "Help local farmers boost yields using improved methods and sustainable techniques.",
                "background_objectives_en": "Food security is critical to rural resilience; teaching sustainable agriculture helps reduce vulnerability.",
                "tasks_eligibility_en": "Tasks: demonstrate farming techniques, monitor yields. Eligibility: agriculture background preferred.",
                "country_en": "Nepal",
                "theme_en": "Agriculture",

                "title_zh_tw": "農業與糧食安全計畫",
                "teaser_zh_tw": "協助當地農民透過改良方法與永續技術提升產量。",
                "background_objectives_zh_tw": "糧食安全對於農村韌性至關重要；教授永續農業有助降低脆弱性。",
                "tasks_eligibility_zh_tw": "任務：示範耕作技術、監測產量。資格：農業背景佳。",
                "country_zh_tw": "尼泊爾",
                "theme_zh_tw": "農業",

                "kicc_project_id": "AGR-NP-006",
                "duration": 28,
                "difficulty": "Medium",
                "total_headcount": 18,
                "cover_image_url": "https://loremflickr.com/800/600/farming,terrace,nepal",
                "image_urls": [
                    "https://loremflickr.com/800/600/farming,1",
                    "https://loremflickr.com/800/600/farming,2",
                    "https://loremflickr.com/800/600/sustainable,agriculture,1",
                    "https://loremflickr.com/800/600/sustainable,agriculture,2",
                    "https://loremflickr.com/800/600/terrace,farm,1",
                    "https://loremflickr.com/800/600/terrace,farm,2",
                    "https://loremflickr.com/800/600/soil,testing,1",
                    "https://loremflickr.com/800/600/soil,testing,2",
                    "https://loremflickr.com/800/600/irrigation,1",
                    "https://loremflickr.com/800/600/irrigation,2",
                    "https://loremflickr.com/800/600/market,outlet,1",
                    "https://loremflickr.com/800/600/market,outlet,2",
                    "https://loremflickr.com/800/600/crop,rotation,1",
                    "https://loremflickr.com/800/600/crop,rotation,2",
                    "https://loremflickr.com/800/600/seed,distribution,1",
                    "https://loremflickr.com/800/600/seed,distribution,2",
                    "https://loremflickr.com/800/600/community,training,1",
                    "https://loremflickr.com/800/600/community,training,2",
                    "https://loremflickr.com/800/600/tractor,work,1",
                    "https://loremflickr.com/800/600/tractor,work,2",
                    "https://loremflickr.com/800/600/agronomy,1",
                    "https://loremflickr.com/800/600/agronomy,2",
                    "https://loremflickr.com/800/600/food,security,1",
                    "https://loremflickr.com/800/600/food,security,2",
                ],
                "video_urls": [
                    "https://www.youtube.com/watch?v=kingslish_example_agriculture",
                ],
                "application_deadline": timezone.now() + timedelta(days=60),
                "start_date": timezone.now().date() + timedelta(days=75),
                "end_date": timezone.now().date() + timedelta(days=100),
                "is_featured": False,
            },
            {
                "title_en": "Women's Empowerment & Livelihood Training",
                "teaser_en": "Facilitate skill training and microenterprise support to boost women's livelihood options.",
                "background_objectives_en": "Empowered women contribute to resilient households; our workshops provide skills and market access support.",
                "tasks_eligibility_en": "Tasks: run skills workshops, mentoring. Eligibility: community facilitation background preferred.",
                "country_en": "Myanmar",
                "theme_en": "Economic Development",

                "title_zh_tw": "婦女賦權與生計培訓",
                "teaser_zh_tw": "舉辦技能訓練與小型企業支持，提升婦女生計選擇。",
                "background_objectives_zh_tw": "賦權婦女可提升家庭韌性；我們的工作坊提供技能與市場支持。",
                "tasks_eligibility_zh_tw": "任務：主持技能工作坊、提供指導。資格：具社區輔導背景者優先。",
                "country_zh_tw": "緬甸",
                "theme_zh_tw": "經濟發展",

                "kicc_project_id": "ECO-MM-007",
                "duration": 22,
                "difficulty": "Easy",
                "total_headcount": 25,
                "cover_image_url": "https://loremflickr.com/800/600/women,training,livelihood",
                "image_urls": [
                    "https://loremflickr.com/800/600/women,training,1",
                    "https://loremflickr.com/800/600/women,training,2",
                    "https://loremflickr.com/800/600/microenterprise,1",
                    "https://loremflickr.com/800/600/microenterprise,2",
                    "https://loremflickr.com/800/600/sewing,stitching,1",
                    "https://loremflickr.com/800/600/sewing,stitching,2",
                    "https://loremflickr.com/800/600/market,access,1",
                    "https://loremflickr.com/800/600/market,access,2",
                    "https://loremflickr.com/800/600/mentorship,1",
                    "https://loremflickr.com/800/600/mentorship,2",
                    "https://loremflickr.com/800/600/entrepreneur,1",
                    "https://loremflickr.com/800/600/entrepreneur,2",
                    "https://loremflickr.com/800/600/skill,training,1",
                    "https://loremflickr.com/800/600/skill,training,2",
                    "https://loremflickr.com/800/600/community,support,1",
                    "https://loremflickr.com/800/600/community,support,2",
                    "https://loremflickr.com/800/600/fair,trade,1",
                    "https://loremflickr.com/800/600/fair,trade,2",
                    "https://loremflickr.com/800/600/bazaar,1",
                    "https://loremflickr.com/800/600/bazaar,2",
                    "https://loremflickr.com/800/600/female,entrepreneur,1",
                    "https://loremflickr.com/800/600/female,entrepreneur,2",
                    "https://loremflickr.com/800/600/handicraft,production,1",
                    "https://loremflickr.com/800/600/handicraft,production,2",
                ],
                "video_urls": [
                    "https://www.youtube.com/watch?v=kingslish_example_empower",
                ],
                "application_deadline": timezone.now() + timedelta(days=20),
                "start_date": timezone.now().date() + timedelta(days=27),
                "end_date": timezone.now().date() + timedelta(days=40),
                "is_featured": False,
            },
            {
                # English
                "title_en": "Marine Conservation & Beach Cleanup",
                "teaser_en": "Join us in preserving marine life by keeping our coastlines clean and plastic-free.",
                "background_objectives_en": "Plastic pollution threatens marine biodiversity. We aim to remove 5 tons of waste.",
                "tasks_eligibility_en": "Tasks: Collecting waste, sorting recyclables. Eligibility: Physical fitness.",
                "country_en": "Philippines",
                "theme_en": "Environment",

                # Traditional Chinese (ZH-TW)
                "title_zh_tw": "海洋保育與海灘清潔",
                "teaser_zh_tw": "加入我們，透過保持海岸線清潔和無塑化來保護海洋生物。",
                "background_objectives_zh_tw": "塑膠污染威脅海洋生物多樣性。我們的目標是清除5噸垃圾。",
                "tasks_eligibility_zh_tw": "任務：收集垃圾、分類回收物。資格：身體健康。",
                "country_zh_tw": "菲律賓",
                "theme_zh_tw": "環境",

                # Metadata & Media
                "kicc_project_id": "ENV-PH-002",
                "duration": 25,
                "difficulty": "Easy",
                "total_headcount": 50,
                
                # Images via Lorem Flickr
                "cover_image_url": "https://loremflickr.com/800/600/beach,cleanup,ocean",
                "image_urls": [
                    "https://loremflickr.com/800/600/plastic,recycle,1",
                    "https://loremflickr.com/800/600/plastic,recycle,2",
                    "https://loremflickr.com/800/600/sea,turtle,nature,1",
                    "https://loremflickr.com/800/600/sea,turtle,nature,2",
                    "https://loremflickr.com/800/600/volunteers,sand,1",
                    "https://loremflickr.com/800/600/volunteers,sand,2",
                    "https://loremflickr.com/800/600/beach,cleanup,1",
                    "https://loremflickr.com/800/600/beach,cleanup,2",
                    "https://loremflickr.com/800/600/trash,collection,1",
                    "https://loremflickr.com/800/600/trash,collection,2",
                    "https://loremflickr.com/800/600/sea,life,1",
                    "https://loremflickr.com/800/600/sea,life,2",
                    "https://loremflickr.com/800/600/recycling,sort,1",
                    "https://loremflickr.com/800/600/recycling,sort,2",
                    "https://loremflickr.com/800/600/volunteer,team,1",
                    "https://loremflickr.com/800/600/volunteer,team,2",
                    "https://loremflickr.com/800/600/education,beach,1",
                    "https://loremflickr.com/800/600/education,beach,2",
                    "https://loremflickr.com/800/600/sea,birds,1",
                    "https://loremflickr.com/800/600/sea,birds,2",
                    "https://loremflickr.com/800/600/plastic,bales,1",
                    "https://loremflickr.com/800/600/plastic,bales,2",
                    "https://loremflickr.com/800/600/community,cleanup,1",
                    "https://loremflickr.com/800/600/community,cleanup,2",
                ],
                
                # Videos from Kingslish App Channel
                "video_urls": [
                     "https://www.youtube.com/@kingslishapp/videos"
                ],

                "application_deadline": timezone.now() + timedelta(days=15),
                "start_date": timezone.now().date() + timedelta(days=20),
                "end_date": timezone.now().date() + timedelta(days=25),
                "is_hero_highlight": True,
            }
        ]

        for p_data in projects_data:
            if not Project.objects.filter(kicc_project_id=p_data['kicc_project_id']).exists():
                Project.objects.create(**p_data)
                self.stdout.write(self.style.SUCCESS(f"Created project: {p_data['title_en']}"))
            else:
                self.stdout.write(f"Project {p_data['kicc_project_id']} already exists.")