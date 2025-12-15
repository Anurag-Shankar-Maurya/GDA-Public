from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.content.models import NewsEvent

class Command(BaseCommand):
    help = 'Seeds the database with News & Event data (EN & ZH-TW)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding News & Events...')

        news_data = [
            {
                "content_type": NewsEvent.Type.EVENT,
                # English
                "title_en": "Global Volunteer Summit 2024",
                "body_en": "We are excited to announce our annual summit. Join volunteers from around the world to share stories and strategies.",
                # Traditional Chinese
                "title_zh_tw": "2024 全球志工高峰會",
                "body_zh_tw": "我們很高興宣佈我們的年度高峰會。加入來自世界各地的志工，分享故事和策略。",
                
                "publish_date": timezone.now(),
                
                # Images via Lorem Flickr (20+ images)
                "cover_image_url": "https://loremflickr.com/800/600/conference,convention,speaker",
                "image_urls": [
                    "https://loremflickr.com/800/600/audience,clapping,1",
                    "https://loremflickr.com/800/600/audience,clapping,2",
                    "https://loremflickr.com/800/600/panel,discussion,1",
                    "https://loremflickr.com/800/600/panel,discussion,2",
                    "https://loremflickr.com/800/600/keynote,speaker,1",
                    "https://loremflickr.com/800/600/keynote,speaker,2",
                    "https://loremflickr.com/800/600/networking,1",
                    "https://loremflickr.com/800/600/networking,2",
                    "https://loremflickr.com/800/600/expo,booth,1",
                    "https://loremflickr.com/800/600/expo,booth,2",
                    "https://loremflickr.com/800/600/award,ceremony,1",
                    "https://loremflickr.com/800/600/award,ceremony,2",
                    "https://loremflickr.com/800/600/delegate,photo,1",
                    "https://loremflickr.com/800/600/delegate,photo,2",
                    "https://loremflickr.com/800/600/workshop,1",
                    "https://loremflickr.com/800/600/workshop,2",
                    "https://loremflickr.com/800/600/volunteer,1",
                    "https://loremflickr.com/800/600/volunteer,2",
                    "https://loremflickr.com/800/600/closing,remarks,1",
                    "https://loremflickr.com/800/600/closing,remarks,2",
                ],
                
                "is_featured": True,
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                # English
                "title_en": "New Partnership with Local NGOs",
                "body_en": "Our organization has officially partnered with 5 new NGOs in Southeast Asia to expand our reach.",
                # Traditional Chinese
                "title_zh_tw": "與當地非政府組織建立新合作夥伴關係",
                "body_zh_tw": "我們的組織已正式與東南亞的 5 個新非政府組織合作，以擴大我們的影響範圍。",

                "publish_date": timezone.now(),
                
                 # Images via Lorem Flickr (20+ images)
                 "cover_image_url": "https://loremflickr.com/800/600/handshake,partnership,team",
                 "image_urls": [
                     "https://loremflickr.com/800/600/signing,contract,1",
                     "https://loremflickr.com/800/600/signing,contract,2",
                     "https://loremflickr.com/800/600/meeting,1",
                     "https://loremflickr.com/800/600/meeting,2",
                     "https://loremflickr.com/800/600/team,1",
                     "https://loremflickr.com/800/600/team,2",
                     "https://loremflickr.com/800/600/celebration,1",
                     "https://loremflickr.com/800/600/celebration,2",
                     "https://loremflickr.com/800/600/press,conference,1",
                     "https://loremflickr.com/800/600/press,conference,2",
                     "https://loremflickr.com/800/600/agreement,1",
                     "https://loremflickr.com/800/600/agreement,2",
                     "https://loremflickr.com/800/600/community,1",
                     "https://loremflickr.com/800/600/community,2",
                     "https://loremflickr.com/800/600/handshake,1",
                     "https://loremflickr.com/800/600/handshake,2",
                     "https://loremflickr.com/800/600/strategy,1",
                     "https://loremflickr.com/800/600/strategy,2",
                     "https://loremflickr.com/800/600/collaboration,1",
                     "https://loremflickr.com/800/600/collaboration,2",
                 ],
                
                "is_hero_highlight": False,
            }
        ]
        # Additional news/events
        news_data += [
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Volunteer of the Year Awards 2024",
                "body_en": "Celebrating outstanding volunteers who made a difference during the year. The awards recognize innovation, leadership, and impact.",
                "title_zh_tw": "2024 年度志工獎",
                "body_zh_tw": "表彰在過去一年中做出重大貢獻的傑出志工，肯定創新、領導與影響力。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/award,volunteer,ceremony",
                "image_urls": [
                    "https://loremflickr.com/800/600/award,volunteer,1",
                    "https://loremflickr.com/800/600/award,volunteer,2",
                    "https://loremflickr.com/800/600/award,volunteer,3",
                    "https://loremflickr.com/800/600/award,volunteer,4",
                    "https://loremflickr.com/800/600/ceremony,1",
                    "https://loremflickr.com/800/600/ceremony,2",
                    "https://loremflickr.com/800/600/recipient,1",
                    "https://loremflickr.com/800/600/recipient,2",
                    "https://loremflickr.com/800/600/group,photo,1",
                    "https://loremflickr.com/800/600/group,photo,2",
                    "https://loremflickr.com/800/600/certificate,1",
                    "https://loremflickr.com/800/600/certificate,2",
                    "https://loremflickr.com/800/600/stage,1",
                    "https://loremflickr.com/800/600/stage,2",
                    "https://loremflickr.com/800/600/host,1",
                    "https://loremflickr.com/800/600/host,2",
                    "https://loremflickr.com/800/600/audience,1",
                    "https://loremflickr.com/800/600/audience,2",
                    "https://loremflickr.com/800/600/speech,1",
                    "https://loremflickr.com/800/600/speech,2",
                ],
                "video_urls": ["https://www.youtube.com/watch?v=awards_example"],
                "is_featured": True,
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Field Report: Coastal Cleanup Reaches Target",
                "body_en": "Our coastal cleanup campaign successfully removed 5.2 tons of waste and engaged volunteer groups across the region.",
                "title_zh_tw": "實地報導：海岸清潔達標",
                "body_zh_tw": "我們的海岸清潔活動成功清除 5.2 噸廢棄物，並吸引來自各地的志工團隊參與。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/beach,cleanup,success",
                "image_urls": [
                    "https://loremflickr.com/800/600/beach,cleanup,1",
                    "https://loremflickr.com/800/600/beach,cleanup,2",
                    "https://loremflickr.com/800/600/volunteer,cleanup,1",
                    "https://loremflickr.com/800/600/volunteer,cleanup,2",
                    "https://loremflickr.com/800/600/plastic,collection,1",
                    "https://loremflickr.com/800/600/plastic,collection,2",
                    "https://loremflickr.com/800/600/sorting,recycling,1",
                    "https://loremflickr.com/800/600/sorting,recycling,2",
                    "https://loremflickr.com/800/600/waste,scale,1",
                    "https://loremflickr.com/800/600/waste,scale,2",
                    "https://loremflickr.com/800/600/sea,turtle,1",
                    "https://loremflickr.com/800/600/sea,turtle,2",
                    "https://loremflickr.com/800/600/boat,cleanup,1",
                    "https://loremflickr.com/800/600/boat,cleanup,2",
                    "https://loremflickr.com/800/600/education,1",
                    "https://loremflickr.com/800/600/education,2",
                    "https://loremflickr.com/800/600/community,volunteers,1",
                    "https://loremflickr.com/800/600/community,volunteers,2",
                    "https://loremflickr.com/800/600/impact,1",
                    "https://loremflickr.com/800/600/impact,2",
                ],
                "video_urls": ["https://www.youtube.com/watch?v=cleanup_report"],
                "is_hero_highlight": True,
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "New Office Opens in Taiwan",
                "body_en": "We're proud to announce the opening of our new regional office in Taipei to better serve partners and volunteers.",
                "title_zh_tw": "台灣新辦公室開幕",
                "body_zh_tw": "我們自豪地宣布我們在台北的新區域辦公室開幕，以更好地服務合作夥伴與志工。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/taipei,office,opening",
                "image_urls": [
                    "https://loremflickr.com/800/600/office,opening,1",
                    "https://loremflickr.com/800/600/office,opening,2",
                    "https://loremflickr.com/800/600/ribbon,cut,1",
                    "https://loremflickr.com/800/600/ribbon,cut,2",
                    "https://loremflickr.com/800/600/staff,team,1",
                    "https://loremflickr.com/800/600/staff,team,2",
                    "https://loremflickr.com/800/600/meeting,room,1",
                    "https://loremflickr.com/800/600/meeting,room,2",
                    "https://loremflickr.com/800/600/partners,1",
                    "https://loremflickr.com/800/600/partners,2",
                    "https://loremflickr.com/800/600/volunteers,1",
                    "https://loremflickr.com/800/600/volunteers,2",
                    "https://loremflickr.com/800/600/signage,1",
                    "https://loremflickr.com/800/600/signage,2",
                    "https://loremflickr.com/800/600/press,1",
                    "https://loremflickr.com/800/600/press,2",
                    "https://loremflickr.com/800/600/urban,taipei,1",
                    "https://loremflickr.com/800/600/urban,taipei,2",
                    "https://loremflickr.com/800/600/office,interior,1",
                    "https://loremflickr.com/800/600/office,interior,2",
                ],
                "video_urls": ["https://www.youtube.com/watch?v=new_office_taipei"],
                "is_featured": True,
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Health Outreach Program Reaches 10,000 Beneficiaries",
                "body_en": "Our community health and outreach program reached a milestone of 10,000 beneficiaries this year — thanks to volunteers and local health partners.",
                "title_zh_tw": "健康外展計畫達到 10,000 受惠人次",
                "body_zh_tw": "我們的社區健康與外展計畫今年達到 10,000 名受惠人次，感謝志工與當地醫療合作夥伴。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/health,outreach,milestone",
                "image_urls": [
                    "https://loremflickr.com/800/600/health,outreach,1",
                    "https://loremflickr.com/800/600/health,outreach,2",
                    "https://loremflickr.com/800/600/clinic,1",
                    "https://loremflickr.com/800/600/clinic,2",
                    "https://loremflickr.com/800/600/beneficiaries,1",
                    "https://loremflickr.com/800/600/beneficiaries,2",
                    "https://loremflickr.com/800/600/medical,team,1",
                    "https://loremflickr.com/800/600/medical,team,2",
                    "https://loremflickr.com/800/600/outreach,training,1",
                    "https://loremflickr.com/800/600/outreach,training,2",
                    "https://loremflickr.com/800/600/education,program,1",
                    "https://loremflickr.com/800/600/education,program,2",
                    "https://loremflickr.com/800/600/volunteer,care,1",
                    "https://loremflickr.com/800/600/volunteer,care,2",
                    "https://loremflickr.com/800/600/awareness,1",
                    "https://loremflickr.com/800/600/awareness,2",
                    "https://loremflickr.com/800/600/community,event,1",
                    "https://loremflickr.com/800/600/community,event,2",
                    "https://loremflickr.com/800/600/clinic,setup,1",
                    "https://loremflickr.com/800/600/clinic,setup,2",
                ],
                "video_urls": ["https://www.youtube.com/watch?v=health_outreach_report"],
                "is_featured": False,
            }
        ]

        for n_data in news_data:
            if not NewsEvent.objects.filter(title=n_data['title_en']).exists():
                NewsEvent.objects.create(**n_data)
                self.stdout.write(self.style.SUCCESS(f"Created news: {n_data['title_en']}"))
            else:
                self.stdout.write(f"News '{n_data['title_en']}' already exists.")