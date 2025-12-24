from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import connection
from apps.content.models import NewsEvent

class Command(BaseCommand):
    help = 'Seeds the database with News & Event data (EN & ZH-TW)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing news/events before seeding',
        )

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding News & Events...')

        if kwargs.get('clear'):
            NewsEvent.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all existing news & events'))
            
            # Reset auto-increment ID
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='content_newsevent'")

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
                "video_urls": [
                    "https://www.youtube.com/shorts/3oZNHz3atqY",
                    "https://www.youtube.com/shorts/DVCvwI46Sik"
                ],
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
                 "video_urls": [
                    "https://www.youtube.com/watch?v=us7SMS44FIw",
                    "https://www.youtube.com/watch?v=J_kcp_Owsrk"
                 ],
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
                "video_urls": [
                    "https://www.youtube.com/watch?v=tYANvrEzvKk",
                    "https://www.youtube.com/watch?v=xJl9i6nsmvw"
                ],
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
                "video_urls": [
                    "https://www.youtube.com/watch?v=w1EXAdzDAxA",
                    "https://www.youtube.com/watch?v=DSBcBSdJDaE"
                ],
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
                "video_urls": [
                    "https://www.youtube.com/watch?v=B0iwi5EXFWU",
                    "https://www.youtube.com/watch?v=Kd45fA5pD9I"
                ],
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
                "video_urls": [
                    "https://www.youtube.com/watch?v=BU1TQY-SfkA",
                    "https://www.youtube.com/watch?v=5U9DLtSwNgQ"
                ],
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
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Workshop: Digital Skills for Non-Profits",
                "body_en": "Join our free workshop to learn essential digital skills for fundraising, marketing, and volunteer management.",
                "title_zh_tw": "工作坊：非營利組織的數位技能",
                "body_zh_tw": "參加我們的免費工作坊，學習募款、行銷和志工管理的基本數位技能。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/digital,workshop,nonprofit",
                "video_urls": [
                    "https://www.youtube.com/watch?v=2---xb-BmBw",
                    "https://www.youtube.com/watch?v=KaWQ2Ua9CW8"
                ],
                "image_urls": [
                    "https://loremflickr.com/800/600/workshop,tech,1",
                    "https://loremflickr.com/800/600/workshop,tech,2",
                    "https://loremflickr.com/800/600/computer,lab,1",
                    "https://loremflickr.com/800/600/computer,lab,2"
                ],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Annual Report 2023 Released",
                "body_en": "Our 2023 Annual Report is now available, highlighting our achievements, financial transparency, and future goals.",
                "title_zh_tw": "2023 年度報告發布",
                "body_zh_tw": "我們的 2023 年度報告現已發布，重點介紹我們的成就、財務透明度和未來目標。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/report,data,chart",
                "video_urls": [
                    "https://www.youtube.com/watch?v=4l4UWZGxvoc",
                    "https://www.youtube.com/watch?v=DRIx1pXj0ag"
                ],
                "image_urls": [
                    "https://loremflickr.com/800/600/infographic,1",
                    "https://loremflickr.com/800/600/infographic,2",
                    "https://loremflickr.com/800/600/presentation,1",
                    "https://loremflickr.com/800/600/presentation,2"
                ],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Charity Gala & Fundraiser",
                "body_en": "Join us for an evening of inspiration and fundraising to support our upcoming projects for 2025.",
                "title_zh_tw": "慈善晚會暨募款活動",
                "body_zh_tw": "與我們共度一個充滿啟發的夜晚，為我們 2025 年的計畫籌集資金。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/gala,charity,event",
                "video_urls": [
                    "https://www.youtube.com/watch?v=DFbb4dSzXRk",
                    "https://www.youtube.com/shorts/C5kFh-VtV6s"
                ],
                "image_urls": [
                    "https://loremflickr.com/800/600/gala,event,1",
                    "https://loremflickr.com/800/600/gala,event,2",
                    "https://loremflickr.com/800/600/fundraiser,1",
                    "https://loremflickr.com/800/600/fundraiser,2"
                ],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Youth Ambassador Program Launched",
                "body_en": "We are launching a new Youth Ambassador Program to empower young leaders in community service.",
                "title_zh_tw": "青年大使計畫啟動",
                "body_zh_tw": "我們正在啟動一項新的青年大使計畫，以賦予年輕領袖在社區服務中的能力。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/youth,leadership,community",
                "video_urls": [
                    "https://www.youtube.com/watch?v=7wDTkAiaNyc",
                    "https://www.youtube.com/watch?v=PhJnZnQuuT0"
                ],
                "image_urls": [
                    "https://loremflickr.com/800/600/youth,group,1",
                    "https://loremflickr.com/800/600/youth,group,2",
                    "https://loremflickr.com/800/600/presentation,youth,1",
                    "https://loremflickr.com/800/600/presentation,youth,2"
                ],
                "is_hero_highlight": True
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Documentary Screening: 'The Changemakers'",
                "body_en": "A screening of our new documentary showcasing the impact of volunteers on communities worldwide.",
                "title_zh_tw": "紀錄片放映：《改變者》",
                "body_zh_tw": "放映我們的新紀錄片，展示全球志工對社區的影響。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/documentary,film,screening",
                "video_urls": [
                    "https://www.youtube.com/watch?v=ywVS21j7fE8",
                    "https://www.youtube.com/watch?v=R-FhDcKJFqw"
                ],
                "image_urls": [
                    "https://loremflickr.com/800/600/movie,screen,1",
                    "https://loremflickr.com/800/600/movie,screen,2",
                    "https://loremflickr.com/800/600/audience,watching,1",
                    "https://loremflickr.com/800/600/audience,watching,2"
                ],
                "video_urls": ["https://www.youtube.com/watch?v=changemakers_doc"],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Emergency Response Team Deployed to Flood-Affected Areas",
                "body_en": "Our emergency response team has been deployed to provide aid and support to communities affected by the recent floods.",
                "title_zh_tw": "緊急應變小組已部署至水災災區",
                "body_zh_tw": "我們的緊急應變小組已部署，為受近期水災影響的社區提供援助與支持。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/flood,rescue,aid",
                "video_urls": [
                    "https://www.youtube.com/watch?v=ZpmxwtN4KRA",
                    "https://www.youtube.com/watch?v=Scg3HjVHOBI"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Webinar: The Future of Volunteering",
                "body_en": "A deep dive into the trends, challenges, and opportunities shaping the future of volunteering in a post-pandemic world.",
                "title_zh_tw": "網路研討會：志願服務的未來",
                "body_zh_tw": "深入探討後疫情時代塑造志願服務未來的趨勢、挑戰與機遇。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/webinar,future,volunteer",
                "video_urls": [
                    "https://www.youtube.com/watch?v=0x5N_7d82JY",
                    "https://www.youtube.com/watch?v=Cr7Se5revOk"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Literacy Program Expands to Rural Schools",
                "body_en": "Our literacy program is expanding to 50 new rural schools, providing books and educational resources to thousands of children.",
                "title_zh_tw": "識字計畫擴展至農村學校",
                "body_zh_tw": "我們的識字計畫正擴展至 50 所新的農村學校，為數千名兒童提供書籍和教育資源。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/children,reading,books",
                "video_urls": [
                    "https://www.youtube.com/watch?v=LYowTbsj8Zs",
                    "https://www.youtube.com/watch?v=IlUB5OhXXZM"
                ],
                "image_urls": [],
                "is_hero_highlight": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "GDA Receives Grant for Environmental Conservation",
                "body_en": "We are thrilled to receive a substantial grant to support our ongoing environmental conservation efforts and reforestation projects.",
                "title_zh_tw": "GDA 獲得環境保護補助金",
                "body_zh_tw": "我們很高興獲得一筆可觀的補助金，以支持我們持續的環境保護工作和重新造林計畫。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/forest,conservation,grant",
                "video_urls": [
                    "https://www.youtube.com/watch?v=g3G9dCECYGU",
                    "https://www.youtube.com/watch?v=Nj4O3BazlWk"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Community Tree Planting Day",
                "body_en": "Join us for a day of community action as we plant 1,000 native trees to help restore our local ecosystem.",
                "title_zh_tw": "社區植樹日",
                "body_zh_tw": "加入我們，參與社區行動，種植 1,000 棵原生樹木，幫助恢復當地生態系統。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/tree,planting,community",
                "video_urls": [
                    "https://www.youtube.com/watch?v=iv6052eJ6I8",
                    "https://www.youtube.com/watch?v=a8DueDYaxvE"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Partnership with Tech Company to Develop Volunteer App",
                "body_en": "A new partnership with a leading tech company will help us develop a mobile app to connect volunteers with opportunities more efficiently.",
                "title_zh_tw": "與科技公司合作開發志工 App",
                "body_zh_tw": "與一家領先的科技公司建立新的合作夥伴關係，將幫助我們開發一款行動應用程式，以更有效地將志工與機會聯繫起來。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/tech,app,volunteer",
                "video_urls": [
                    "https://www.youtube.com/watch?v=o7O0Smy3jPo",
                    "https://www.youtube.com/watch?v=PzrEoE8AU3c"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Mental Health Support Program for Volunteers Launched",
                "body_en": "We are launching a new program to provide mental health resources and support for our dedicated volunteers.",
                "title_zh_tw": "為志工推出心理健康支持計畫",
                "body_zh_tw": "我們正在啟動一項新計畫，為我們敬業的志工提供心理健康資源和支持。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/mental,health,support",
                "video_urls": [
                    "https://www.youtube.com/watch?v=_s9JzPWDcIc",
                    "https://www.youtube.com/watch?v=i-lrDYV_piE"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Online Course: Project Management for Social Good",
                "body_en": "Enroll in our new online course designed to equip non-profit leaders with effective project management skills.",
                "title_zh_tw": "線上課程：社會公益專案管理",
                "body_zh_tw": "報名參加我們的新線上課程，旨在為非營利組織領導者提供有效的專案管理技能。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/online,course,management",
                "video_urls": [
                    "https://www.youtube.com/watch?v=xaaiy2KcLkQ",
                    "https://www.youtube.com/watch?v=4ORYxFFs_oU"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Cultural Exchange Program Connects Youth Across Borders",
                "body_en": "Our cultural exchange program has successfully connected 100 young people from 15 different countries this year.",
                "title_zh_tw": "文化交流計畫連結跨國青年",
                "body_zh_tw": "我們的文化交流計畫今年成功地將來自 15 個不同國家的 100 名年輕人聯繫在一起。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/youth,culture,exchange",
                "video_urls": [
                    "https://www.youtube.com/watch?v=RbgBNE_G5pE",
                    "https://www.youtube.com/watch?v=AZfHFDJuVak"
                ],
                "image_urls": [],
                "is_hero_highlight": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Impact Study Shows Long-Term Benefits of Volunteering",
                "body_en": "A new impact study reveals the long-term positive effects of volunteering on both communities and individuals.",
                "title_zh_tw": "影響研究顯示志願服務的長期效益",
                "body_zh_tw": "一項新的影響研究揭示了志願服務對社區和個人的長期正面影響。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/impact,study,research",
                "video_urls": [
                    "https://www.youtube.com/watch?v=ZRQYJucDSXM",
                    "https://www.youtube.com/watch?v=H-aBNHNB_6Y"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Photo Exhibition: 'A Year in Service'",
                "body_en": "Visit our photo exhibition showcasing powerful moments from our volunteer projects over the past year.",
                "title_zh_tw": "攝影展覽：「服務一年」",
                "body_zh_tw": "參觀我們的攝影展，欣賞過去一年我們志工專案中的感人時刻。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/photo,exhibition,volunteer",
                "video_urls": [
                    "https://www.youtube.com/watch?v=uOwNq-Nm-NU",
                    "https://www.youtube.com/watch?v=W8894gV6ArY"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Disaster Preparedness Workshops Held in Coastal Communities",
                "body_en": "We conducted a series of disaster preparedness workshops to help coastal communities build resilience against natural calamities.",
                "title_zh_tw": "在沿海社區舉辦防災工作坊",
                "body_zh_tw": "我們舉辦了一系列防災工作坊，幫助沿海社區建立抵禦自然災害的能力。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/disaster,preparedness,workshop",
                "video_urls": [
                    "https://www.youtube.com/watch?v=sb1_vLijK40",
                    "https://www.youtube.com/watch?v=8CQldQfW_oY"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "New Scholarship for Students in Environmental Science",
                "body_en": "We are proud to launch a new scholarship fund for students pursuing higher education in environmental science.",
                "title_zh_tw": "環境科學學生新獎學金",
                "body_zh_tw": "我們很自豪地為攻讀環境科學高等教育的學生設立了新的獎學金基金。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/scholarship,student,environment",
                "video_urls": [
                    "https://www.youtube.com/watch?v=lTMpt8kjbBQ",
                    "https://www.youtube.com/watch?v=m-QsbfsBjk0"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "International Volunteer Day Celebration",
                "body_en": "Join us as we celebrate International Volunteer Day with stories of impact, awards, and a special live performance.",
                "title_zh_tw": "國際志工日慶祝活動",
                "body_zh_tw": "與我們一起慶祝國際志工日，分享影響力故事、頒獎典禮和特別的現場表演。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/volunteer,day,celebration",
                "video_urls": [
                    "https://www.youtube.com/watch?v=dIk6V68sBm8",
                    "https://www.youtube.com/watch?v=QKs8bqQ-0Ck"
                ],
                "image_urls": [],
                "is_hero_highlight": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Animal Shelter Renovation Project Completed",
                "body_en": "Thanks to our amazing volunteers, the local animal shelter renovation is now complete, providing a better home for rescued animals.",
                "title_zh_tw": "動物收容所翻新計畫完成",
                "body_zh_tw": "感謝我們出色的志工，當地動物收容所的翻新工程現已完成，為獲救的動物提供了更好的家。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/animal,shelter,renovation",
                "video_urls": [
                    "https://www.youtube.com/watch?v=KWaOjypn3Zo",
                    "https://www.youtube.com/watch?v=1pca674L1OA"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Water Sanitation Project Improves Health in Village",
                "body_en": "The completion of our water sanitation project has significantly improved the health and well-being of a rural village community.",
                "title_zh_tw": "水衛生計畫改善村莊健康狀況",
                "body_zh_tw": "我們的水衛生計畫的完成，顯著改善了一個農村社區的健康和福祉。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/water,sanitation,health",
                "video_urls": [
                    "https://www.youtube.com/watch?v=iLN17kZB08U",
                    "https://www.youtube.com/watch?v=rc8W3VHHBE0"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Virtual Career Fair for Non-Profit Jobs",
                "body_en": "Looking for a career with purpose? Join our virtual career fair to connect with leading non-profit organizations.",
                "title_zh_tw": "非營利工作虛擬就業博覽會",
                "body_zh_tw": "正在尋找有意義的職業嗎？參加我們的虛擬就業博覽會，與領先的非營利組織建立聯繫。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/career,fair,nonprofit",
                "video_urls": [
                    "https://www.youtube.com/watch?v=wVwJ1WkhIto",
                    "https://www.youtube.com/watch?v=aI5TYfoE97U"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "GDA Joins Global Alliance for Climate Action",
                "body_en": "We are proud to join a global alliance of organizations committed to taking urgent action on climate change.",
                "title_zh_tw": "GDA 加入全球氣候行動聯盟",
                "body_zh_tw": "我們很自豪能加入一個由致力於對氣候變遷採取緊急行動的組織組成的全球聯盟。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/climate,action,alliance",
                "video_urls": [
                    "https://www.youtube.com/watch?v=s2nbu0u57KM",
                    "https://www.youtube.com/watch?v=PF72XUJpjCA"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Mobile Library Reaches Remote Communities",
                "body_en": "Our new mobile library is bringing the joy of reading to children and adults in remote and underserved communities.",
                "title_zh_tw": "行動圖書館抵達偏遠社區",
                "body_zh_tw": "我們新的行動圖書館為偏遠和服務欠缺社區的兒童和成人帶來閱讀的樂趣。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/mobile,library,reading",
                "video_urls": [
                    "https://www.youtube.com/watch?v=cOA8AKv5v6Y",
                    "https://www.youtube.com/watch?v=YjNDBqbRfT0"
                ],
                "image_urls": [],
                "is_hero_highlight": True
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Fundraising Marathon for Education",
                "body_en": "Run for a cause! Join our annual fundraising marathon to support educational programs for underprivileged children.",
                "title_zh_tw": "為教育而跑的募款馬拉松",
                "body_zh_tw": "為公益而跑！參加我們的年度募款馬拉松，支持弱勢兒童的教育計畫。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/marathon,fundraising,education",
                "video_urls": [
                    "https://www.youtube.com/watch?v=f3vVhcZzZv0",
                    "https://www.youtube.com/watch?v=yNN2igIMpsA"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Solar Panel Installation Project Powers Community Center",
                "body_en": "A new solar panel installation is providing clean, reliable energy to a vital community center, reducing costs and environmental impact.",
                "title_zh_tw": "太陽能板安裝計畫為社區中心供電",
                "body_zh_tw": "新的太陽能板安裝為一個重要的社區中心提供清潔、可靠的能源，降低了成本和環境影響。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/solar,panel,community",
                "video_urls": [
                    "https://www.youtube.com/watch?v=DFXjFwjj4nc",
                    "https://www.youtube.com/watch?v=SpGKK9t28w0"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Women's Empowerment Initiative Trains 500 Entrepreneurs",
                "body_en": "Our women's empowerment initiative has successfully trained 500 women in starting and managing their own small businesses.",
                "title_zh_tw": "婦女賦權倡議培訓 500 名企業家",
                "body_zh_tw": "我們的婦女賦權倡議已成功培訓 500 名婦女創辦和管理自己的小型企業。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/women,empowerment,entrepreneur",
                "video_urls": [
                    "https://www.youtube.com/watch?v=Y2bNOiVmWeE",
                    "https://www.youtube.com/watch?v=SzwSCySBmac"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "TEDxGDA: Ideas Worth Spreading",
                "body_en": "We are hosting our first-ever TEDx event, featuring inspiring talks from leaders in the social impact space.",
                "title_zh_tw": "TEDxGDA：值得傳播的思想",
                "body_zh_tw": "我們正在舉辦有史以來第一次的 TEDx 活動，邀請社會影響力領域的領導者發表鼓舞人心的演講。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/tedx,talk,conference",
                "video_urls": [
                    "https://www.youtube.com/watch?v=5P73ai8zGpg",
                    "https://www.youtube.com/watch?v=o3fRujnTsGE"
                ],
                "image_urls": [],
                "is_hero_highlight": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "New Food Bank Opened in Urban Center",
                "body_en": "In partnership with local businesses, we have opened a new food bank to address food insecurity in the city.",
                "title_zh_tw": "市中心新食物銀行開幕",
                "body_zh_tw": "我們與當地企業合作，開設了一家新的食物銀行，以解決城市中的糧食不安全問題。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/food,bank,community",
                "video_urls": [
                    "https://www.youtube.com/watch?v=lJDD44EzdEw",
                    "https://www.youtube.com/watch?v=UvdrudafRUU"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Research on Volunteer Motivation Published",
                "body_en": "Our latest research paper on the motivations of long-term volunteers has been published in a leading academic journal.",
                "title_zh_tw": "志工動機研究發表",
                "body_zh_tw": "我們關於長期志工動機的最新研究論文已在一家領先的學術期刊上發表。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/research,paper,journal",
                "video_urls": [
                    "https://www.youtube.com/watch?v=lDBS3vkqZf0",
                    "https://www.youtube.com/watch?v=ZyuJckzEBHM"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Art for a Cause: Charity Auction",
                "body_en": "Join us for a charity auction featuring works from local artists to raise funds for our youth programs.",
                "title_zh_tw": "為公益而藝術：慈善拍賣會",
                "body_zh_tw": "參加我們的慈善拍賣會，欣賞當地藝術家的作品，為我們的青年計畫籌集資金。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/art,auction,charity",
                "video_urls": [
                    "https://www.youtube.com/watch?v=HRKy4y2c7Zg",
                    "https://www.youtube.com/watch?v=ZM25iP0DmIo"
                ],
                "image_urls": [],
                "is_featured": True
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "Sports for Development Program Engages At-Risk Youth",
                "body_en": "Our Sports for Development program is using the power of sports to engage and empower at-risk youth in underserved communities.",
                "title_zh_tw": "體育促進發展計畫吸引高風險青年參與",
                "body_zh_tw": "我們的體育促進發展計畫正在利用體育的力量，在服務欠缺的社區中吸引和賦予高風險青年權力。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/sports,youth,development",
                "video_urls": [
                    "https://www.youtube.com/watch?v=VhHvO96qRuM",
                    "https://www.youtube.com/watch?v=LYowTbsj8Zs"
                ],
                "image_urls": [],
                "is_featured": False
            },
            {
                "content_type": NewsEvent.Type.NEWS,
                "title_en": "GDA Expands Operations to Two New Countries",
                "body_en": "We are excited to announce the expansion of our operations into two new countries, furthering our global impact.",
                "title_zh_tw": "GDA 將業務擴展至兩個新國家",
                "body_zh_tw": "我們很高興地宣布將我們的業務擴展到兩個新的國家，進一步擴大我們的全球影響力。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/global,expansion,map",
                "video_urls": [
                    "https://www.youtube.com/watch?v=2---xb-BmBw",
                    "https://www.youtube.com/watch?v=0x5N_7d82JY"
                ],
                "image_urls": [],
                "is_hero_highlight": True
            },
            {
                "content_type": NewsEvent.Type.EVENT,
                "title_en": "Hackathon for Social Innovation",
                "body_en": "Calling all innovators! Join our hackathon to develop creative solutions to pressing social and environmental challenges.",
                "title_zh_tw": "社會創新黑客松",
                "body_zh_tw": "號召所有創新者！參加我們的黑客松，為緊迫的社會和環境挑戰開發創新的解決方案。",
                "publish_date": timezone.now(),
                "cover_image_url": "https://loremflickr.com/800/600/hackathon,social,innovation",
                "video_urls": [
                    "https://www.youtube.com/watch?v=kLLVTueI0y4",
                    "https://www.youtube.com/watch?v=WU4gKwKoOf8"
                ],
                "image_urls": [],
                "is_featured": True
            },
        ]

        for n_data in news_data:
            if not NewsEvent.objects.filter(title=n_data['title_en']).exists():
                NewsEvent.objects.create(**n_data)
                self.stdout.write(self.style.SUCCESS(f"Created news: {n_data['title_en']}"))
            else:
                self.stdout.write(f"News: {n_data['title_en']}' already exists.")
        self.stdout.write(self.style.SUCCESS(f'News & Events seeding completed successfully! Total news/events: {len(news_data)}'))