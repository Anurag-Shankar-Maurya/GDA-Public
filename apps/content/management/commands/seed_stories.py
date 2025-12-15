from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.content.models import SuccessStory, Project
import random

class Command(BaseCommand):
    help = 'Seeds the database with Success Stories (EN & ZH-TW)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding Success Stories...')

        # Try to fetch a project to link to
        projects = Project.objects.all()
        related_proj = projects.first() if projects.exists() else None

        stories_data = [
            {
                # English
                "title_en": "Sarah's Month Teaching in Hanoi",
                "body_en": "Living in Hanoi was a life-changing experience. The students were eager to learn, and despite the language barrier, we connected through games and laughter.",
                # Traditional Chinese
                "title_zh_tw": "莎拉在河內教書的一個月",
                "body_zh_tw": "在河內生活是一次改變人生的經歷。學生們渴望學習，儘管有語言障礙，我們通過遊戲和歡笑建立了聯繫。",

                "beneficiaries": 120,
                "total_hours_contributed": 160,
                "published_at": timezone.now(),
                "related_project": related_proj,
                "is_featured": True,
                
                # Images via Lorem Flickr (20+ images)
                "cover_image_url": "https://loremflickr.com/800/600/hanoi,vietnam,girl",
                "image_urls": [
                    "https://loremflickr.com/800/600/teaching,students,1",
                    "https://loremflickr.com/800/600/teaching,students,2",
                    "https://loremflickr.com/800/600/classroom,1",
                    "https://loremflickr.com/800/600/classroom,2",
                    "https://loremflickr.com/800/600/teacher,1",
                    "https://loremflickr.com/800/600/teacher,2",
                    "https://loremflickr.com/800/600/learning,1",
                    "https://loremflickr.com/800/600/learning,2",
                    "https://loremflickr.com/800/600/games,education,1",
                    "https://loremflickr.com/800/600/games,education,2",
                    "https://loremflickr.com/800/600/smiling,children,1",
                    "https://loremflickr.com/800/600/smiling,children,2",
                    "https://loremflickr.com/800/600/school,playground,1",
                    "https://loremflickr.com/800/600/school,playground,2",
                    "https://loremflickr.com/800/600/storytelling,1",
                    "https://loremflickr.com/800/600/storytelling,2",
                    "https://loremflickr.com/800/600/volunteer,work,1",
                    "https://loremflickr.com/800/600/volunteer,work,2",
                    "https://loremflickr.com/800/600/community,event,1",
                    "https://loremflickr.com/800/600/community,event,2",
                    "https://loremflickr.com/800/600/hanoi,street,1",
                    "https://loremflickr.com/800/600/hanoi,street,2",
                    "https://loremflickr.com/800/600/student,achievement,1",
                    "https://loremflickr.com/800/600/student,achievement,2",
                ],
                
                # Video from Kingslish Channel
                "video_urls": [
                    "https://www.youtube.com/@kingslishapp"
                ],
            },
            {
                # English
                "title_en": "Restoring the Coral Reefs",
                "body_en": "Diving down to plant new coral fragments was hard work, but seeing the fish return to the reef made every minute worth it.",
                # Traditional Chinese
                "title_zh_tw": "修復珊瑚礁",
                "body_zh_tw": "潛入水中種植新的珊瑚碎片是一項艱苦的工作，但看到魚群回到珊瑚礁，每一分鐘都值得。",

                "beneficiaries": 0,
                "total_hours_contributed": 50,
                "published_at": timezone.now(),
                "related_project": None,
                "is_hero_highlight": True,
                
                # Images via Lorem Flickr (20+ images)
                "cover_image_url": "https://loremflickr.com/800/600/coral,reef,diving",
                "image_urls": [
                    "https://loremflickr.com/800/600/coral,reef,1",
                    "https://loremflickr.com/800/600/coral,reef,2",
                    "https://loremflickr.com/800/600/diver,1",
                    "https://loremflickr.com/800/600/diver,2",
                    "https://loremflickr.com/800/600/underwater,1",
                    "https://loremflickr.com/800/600/underwater,2",
                    "https://loremflickr.com/800/600/fish,1",
                    "https://loremflickr.com/800/600/fish,2",
                    "https://loremflickr.com/800/600/frag,planting,1",
                    "https://loremflickr.com/800/600/frag,planting,2",
                    "https://loremflickr.com/800/600/research,1",
                    "https://loremflickr.com/800/600/research,2",
                    "https://loremflickr.com/800/600/boat,work,1",
                    "https://loremflickr.com/800/600/boat,work,2",
                    "https://loremflickr.com/800/600/community,volunteers,1",
                    "https://loremflickr.com/800/600/community,volunteers,2",
                    "https://loremflickr.com/800/600/beach,cleanup,1",
                    "https://loremflickr.com/800/600/beach,cleanup,2",
                    "https://loremflickr.com/800/600/sea,turtle,1",
                    "https://loremflickr.com/800/600/sea,turtle,2",
                    "https://loremflickr.com/800/600/monitoring,1",
                    "https://loremflickr.com/800/600/monitoring,2",
                    "https://loremflickr.com/800/600/ecology,1",
                    "https://loremflickr.com/800/600/ecology,2",
                ],
                
                # Video from Kingslish Channel
                "video_urls": [
                    "https://www.youtube.com/@kingslishapp"
                ],
            }
        ]

        # Add additional success stories
        stories_data += [
            {
                "title_en": "Solar Village: A Day with Volunteers",
                "body_en": "The day started at 6 AM as our team carried solar panels into the fields; by afternoon, lights were bringing smiles to families who had been in the dark for years.",
                "title_zh_tw": "太陽能村落：與志工的一天",
                "body_zh_tw": "一天從清晨開始，我們的團隊把太陽能板搬到田間；午後，燈光為多年處於黑暗的家庭帶來笑容。",
                "beneficiaries": 45,
                "total_hours_contributed": 200,
                "published_at": timezone.now(),
                "related_project": related_proj,
                "is_featured": True,
                "cover_image_url": "https://loremflickr.com/800/600/solar,village,volunteers",
                "image_urls": [
                    "https://loremflickr.com/800/600/solar,install,1",
                    "https://loremflickr.com/800/600/solar,install,2",
                    "https://loremflickr.com/800/600/panel,team,1",
                    "https://loremflickr.com/800/600/panel,team,2",
                    "https://loremflickr.com/800/600/night,light,1",
                    "https://loremflickr.com/800/600/night,light,2",
                    "https://loremflickr.com/800/600/solar,education,1",
                    "https://loremflickr.com/800/600/solar,education,2",
                    "https://loremflickr.com/800/600/maintenance,1",
                    "https://loremflickr.com/800/600/maintenance,2",
                    "https://loremflickr.com/800/600/community,meeting,1",
                    "https://loremflickr.com/800/600/community,meeting,2",
                    "https://loremflickr.com/800/600/children,study,1",
                    "https://loremflickr.com/800/600/children,study,2",
                    "https://loremflickr.com/800/600/engineer,teaching,1",
                    "https://loremflickr.com/800/600/engineer,teaching,2",
                    "https://loremflickr.com/800/600/tools,work,1",
                    "https://loremflickr.com/800/600/tools,work,2",
                    "https://loremflickr.com/800/600/family,happy,1",
                    "https://loremflickr.com/800/600/family,happy,2",
                    "https://loremflickr.com/800/600/remote,village,1",
                    "https://loremflickr.com/800/600/remote,village,2",
                    "https://loremflickr.com/800/600/solar,infrastructure,1",
                    "https://loremflickr.com/800/600/solar,infrastructure,2",
                ],
                "video_urls": ["https://www.youtube.com/watch?v=solar_village_story"],
            },
            {
                "title_en": "Women Entrepreneurs Transforming Their Community",
                "body_en": "Small loans, new skills, and mentorship helped dozens of women launch their microbusinesses — now they provide consistent income to their families.",
                "title_zh_tw": "婦女創業家改變社區",
                "body_zh_tw": "小額貸款、新技能和指導幫助數十名婦女創立微型企業，現在她們為家庭提供穩定收入。",
                "beneficiaries": 200,
                "total_hours_contributed": 300,
                "published_at": timezone.now(),
                "related_project": related_proj,
                "is_featured": False,
                "cover_image_url": "https://loremflickr.com/800/600/women,entrepreneur,workshop",
                "image_urls": [
                    "https://loremflickr.com/800/600/women,entrepreneur,1",
                    "https://loremflickr.com/800/600/women,entrepreneur,2",
                    "https://loremflickr.com/800/600/product,display,1",
                    "https://loremflickr.com/800/600/product,display,2",
                    "https://loremflickr.com/800/600/training,1",
                    "https://loremflickr.com/800/600/training,2",
                    "https://loremflickr.com/800/600/mentorship,1",
                    "https://loremflickr.com/800/600/mentorship,2",
                    "https://loremflickr.com/800/600/sewing,1",
                    "https://loremflickr.com/800/600/sewing,2",
                    "https://loremflickr.com/800/600/market,stand,1",
                    "https://loremflickr.com/800/600/market,stand,2",
                    "https://loremflickr.com/800/600/customer,interaction,1",
                    "https://loremflickr.com/800/600/customer,interaction,2",
                    "https://loremflickr.com/800/600/business,planning,1",
                    "https://loremflickr.com/800/600/business,planning,2",
                    "https://loremflickr.com/800/600/bazaar,1",
                    "https://loremflickr.com/800/600/bazaar,2",
                    "https://loremflickr.com/800/600/networking,1",
                    "https://loremflickr.com/800/600/networking,2",
                    "https://loremflickr.com/800/600/loan,training,1",
                    "https://loremflickr.com/800/600/loan,training,2",
                    "https://loremflickr.com/800/600/community,celebration,1",
                    "https://loremflickr.com/800/600/community,celebration,2",
                ],
                "video_urls": ["https://www.youtube.com/watch?v=women_empowerment"],
            },
            {
                "title_en": "Community Garden Brings New Life to Flood-Prone Area",
                "body_en": "Through raised beds, permaculture techniques, and community seeds, households improved food access and diet diversity in their neighborhoods.",
                "title_zh_tw": "社區花園為易洪水地區帶來新生命",
                "body_zh_tw": "透過高床、永續農法與社區種子，家庭在鄰里中改善了食物取得與飲食多樣性。",
                "beneficiaries": 80,
                "total_hours_contributed": 100,
                "published_at": timezone.now(),
                "related_project": related_proj,
                "is_hero_highlight": False,
                "cover_image_url": "https://loremflickr.com/800/600/community,garden,farm",
                "image_urls": [
                    "https://loremflickr.com/800/600/garden,raisedbed,1",
                    "https://loremflickr.com/800/600/garden,raisedbed,2",
                    "https://loremflickr.com/800/600/permaculture,1",
                    "https://loremflickr.com/800/600/permaculture,2",
                    "https://loremflickr.com/800/600/compost,1",
                    "https://loremflickr.com/800/600/compost,2",
                    "https://loremflickr.com/800/600/community,planting,1",
                    "https://loremflickr.com/800/600/community,planting,2",
                    "https://loremflickr.com/800/600/vegetables,harvest,1",
                    "https://loremflickr.com/800/600/vegetables,harvest,2",
                    "https://loremflickr.com/800/600/farmers,1",
                    "https://loremflickr.com/800/600/farmers,2",
                    "https://loremflickr.com/800/600/seeds,distribution,1",
                    "https://loremflickr.com/800/600/seeds,distribution,2",
                    "https://loremflickr.com/800/600/education,workshop,1",
                    "https://loremflickr.com/800/600/education,workshop,2",
                    "https://loremflickr.com/800/600/kids,garden,1",
                    "https://loremflickr.com/800/600/kids,garden,2",
                    "https://loremflickr.com/800/600/irrigation,setup,1",
                    "https://loremflickr.com/800/600/irrigation,setup,2",
                    "https://loremflickr.com/800/600/soil,improvement,1",
                    "https://loremflickr.com/800/600/soil,improvement,2",
                    "https://loremflickr.com/800/600/community,market,1",
                    "https://loremflickr.com/800/600/community,market,2",
                ],
                "video_urls": ["https://www.youtube.com/watch?v=community_garden_story"],
            }
        ]

        for s_data in stories_data:
            if not SuccessStory.objects.filter(title=s_data['title_en']).exists():
                SuccessStory.objects.create(**s_data)
                self.stdout.write(self.style.SUCCESS(f"Created story: {s_data['title_en']}"))
            else:
                self.stdout.write(f"Story '{s_data['title_en']}' already exists.")