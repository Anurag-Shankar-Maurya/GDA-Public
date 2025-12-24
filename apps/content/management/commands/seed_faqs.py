from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import connection
from apps.content.models import FAQ


class Command(BaseCommand):
    help = 'Seed FAQ data with all 40 FAQs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing FAQ data before seeding',
        )

    def handle(self, *args, **options):
        if options.get('clear'):
            FAQ.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all existing FAQs'))
            
            # Reset auto-increment ID
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='content_faq'")
            
        # Complete FAQ data with all 40 entries
        faq_data = [
            {
                'faq_id': 'faq_id_1',
                'question_en': 'How do I apply for a volunteer project?',
                'answer_en': 'To apply for a volunteer project, browse our projects page, select a project that interests you, and click the "Apply" button. You will need to be logged in to your account to submit an application.',
                'question_zh_tw': '如何申請志工專案？',
                'answer_zh_tw': '若要申請志工專案，請瀏覽我們的專案頁面，選擇您感興趣的專案，然後點擊「申請」按鈕。您需要登入帳戶才能提交申請。',
                'order': 1,
                'is_schema_ready': True,
                'thumbs_up': 87,
                'thumbs_down': 3
            },
            {
                'faq_id': 'faq_id_2',
                'question_en': 'What are the requirements to become a volunteer?',
                'answer_en': 'Requirements vary by project, but generally you need to be at least 18 years old (or 16 with parental consent), have a passion for community service, and be able to commit to the project duration. Specific projects may have additional requirements.',
                'question_zh_tw': '成為志工有什麼要求？',
                'answer_zh_tw': '要求因專案而異，但通常您需要年滿 18 歲（或 16 歲並獲得父母同意），熱衷於社區服務，並能承諾專案期間。特定專案可能有額外要求。',
                'order': 2,
                'is_schema_ready': True,
                'thumbs_up': 92,
                'thumbs_down': 5
            },
            {
                'faq_id': 'faq_id_3',
                'question_en': 'Are there any fees for volunteering?',
                'answer_en': 'Most of our volunteer projects are free to join. However, volunteers are typically responsible for their own travel, accommodation, and personal expenses. Some projects may have a small administrative fee.',
                'question_zh_tw': '志工活動有費用嗎？',
                'answer_zh_tw': '我們的大多數志工專案都是免費參加的。然而，志工通常需要自行負擔交通、住宿和個人費用。有些專案可能會收取少量的行政費用。',
                'order': 3,
                'is_schema_ready': True,
                'thumbs_up': 78,
                'thumbs_down': 8
            },
            {
                'faq_id': 'faq_id_4',
                'question_en': 'Can I volunteer internationally?',
                'answer_en': 'Yes! We offer volunteer opportunities both in Taiwan and internationally. Check the country filter on our projects page to find opportunities that interest you.',
                'question_zh_tw': '我可以參加國際志工嗎？',
                'answer_zh_tw': '是的！我們提供台灣和國際的志工機會。請查看我們專案頁面上的國家篩選器，找到您感興趣的機會。',
                'order': 4,
                'is_schema_ready': True,
                'thumbs_up': 95,
                'thumbs_down': 2
            },
            {
                'faq_id': 'faq_id_5',
                'question_en': 'How long do volunteer projects typically last?',
                'answer_en': 'Project durations vary from a few days to several weeks or months. Each project listing shows the estimated time commitment and duration. You can filter projects by duration on our search page.',
                'question_zh_tw': '志工專案通常持續多久？',
                'answer_zh_tw': '專案持續時間從幾天到幾週或幾個月不等。每個專案列表都會顯示預計的時間投入和持續時間。您可以在我們的搜尋頁面上按持續時間篩選專案。',
                'order': 5,
                'is_schema_ready': True,
                'thumbs_up': 84,
                'thumbs_down': 4
            },
            {
                'faq_id': 'faq_id_6',
                'question_en': 'Will I receive a certificate after completing a project?',
                'answer_en': 'Yes! Upon successful completion of a volunteer project, you will receive a certificate documenting your volunteer hours and contribution. This can be useful for school requirements or job applications.',
                'question_zh_tw': '完成專案後我會收到證書嗎？',
                'answer_zh_tw': '是的！順利完成志工專案後，您將收到一份記錄您的志工時數和貢獻的證書。這對學校要求或求職申請很有用。',
                'order': 6,
                'is_schema_ready': True,
                'thumbs_up': 99,
                'thumbs_down': 1
            },
            {
                'faq_id': 'faq_id_7',
                'question_en': 'What if I need to cancel my application?',
                'answer_en': 'If you need to cancel your application, please contact us as soon as possible through the contact form or email. We understand that circumstances change, and we will work with you to find a solution.',
                'question_zh_tw': '如果我需要取消申請怎麼辦？',
                'answer_zh_tw': '如果您需要取消申請，請盡快透過聯絡表單或電子郵件與我們聯繫。我們了解情況可能會發生變化，我們將與您一起尋找解決方案。',
                'order': 7,
                'is_schema_ready': True,
                'thumbs_up': 76,
                'thumbs_down': 6
            },
            {
                'faq_id': 'faq_id_8',
                'question_en': 'Do I need special skills to volunteer?',
                'answer_en': 'Not necessarily! Many of our projects welcome volunteers with no special skills - just enthusiasm and willingness to help. However, some specialized projects may require specific skills or qualifications, which will be clearly stated in the project description.',
                'question_zh_tw': '志工需要特殊技能嗎？',
                'answer_zh_tw': '不一定！我們的許多專案都歡迎沒有特殊技能的志工——只需要熱情和樂於助人的心。然而，有些專業專案可能需要特定的技能或資格，這將在專案描述中清楚說明。',
                'order': 8,
                'is_schema_ready': True,
                'thumbs_up': 91,
                'thumbs_down': 3
            },
            {
                'faq_id': 'faq_id_9',
                'question_en': 'What happens after I apply?',
                'answer_en': 'After you submit your application, our team will review it. If your profile matches the project requirements, we will contact you within 1-2 weeks to schedule an interview. You can always check the status of your application by logging into your account.',
                'question_zh_tw': '申請後會發生什麼？',
                'answer_zh_tw': '提交申請後，我們的團隊將進行審核。如果您的資格符合專案需求，我們會在 1-2 週內與您聯繫安排面試。您隨時可以登入您的帳戶查看申請狀態。',
                'order': 9,
                'is_schema_ready': True,
                'thumbs_up': 88,
                'thumbs_down': 4
            },
            {
                'faq_id': 'faq_id_10',
                'question_en': 'Can I apply to multiple projects at once?',
                'answer_en': 'Yes, you are welcome to apply to all projects that interest you! However, please be selective based on your interests and availability to ensure you can commit fully. If accepted to multiple projects, you will need to choose one.',
                'question_zh_tw': '我可以同時申請多個專案嗎？',
                'answer_zh_tw': '可以，我們鼓勵您申請所有感興趣的專案！不過，請根據您的興趣和時間仔細選擇，以確保您能全身心投入。如果您被多個專案錄取，您需要從中選擇一個。',
                'order': 10,
                'is_schema_ready': True,
                'thumbs_up': 82,
                'thumbs_down': 5
            },
            {
                'faq_id': 'faq_id_11',
                'question_en': 'What documents do I need to submit with my application?',
                'answer_en': 'Typically, you will need to submit an updated resume and a cover letter explaining your interest in the project. For international projects, you may also need a copy of your passport and visa documentation.',
                'question_zh_tw': '申請需要提交哪些文件？',
                'answer_zh_tw': '通常，您需要提交一份最新的履歷和一封說明您為何對該專案感興趣的求職信。對於國際專案，可能還需要您的護照影本和簽證文件。',
                'order': 11,
                'is_schema_ready': True,
                'thumbs_up': 79,
                'thumbs_down': 6
            },
            {
                'faq_id': 'faq_id_12',
                'question_en': 'Is there an interview process?',
                'answer_en': 'Yes, most projects require a brief online interview. This helps us get to know you better and ensures the project is a good fit. It is also a great opportunity for you to ask questions!',
                'question_zh_tw': '申請流程中會有面試嗎？',
                'answer_zh_tw': '是的，大多數專案都需要進行一次簡短的線上面試。這有助於我們更了解您，並確保專案適合您。這也是您提問的好機會！',
                'order': 12,
                'is_schema_ready': True,
                'thumbs_up': 85,
                'thumbs_down': 4
            },
            {
                'faq_id': 'faq_id_13',
                'question_en': 'Will there be training before the project starts?',
                'answer_en': 'Yes, all volunteers are required to attend a pre-departure orientation session. This session covers important information about project goals, cultural sensitivity, safety protocols, and your role and responsibilities.',
                'question_zh_tw': '專案開始前有提供培訓嗎？',
                'answer_zh_tw': '是的，所有志工都必須參加行前培訓課程。本課程涵蓋專案目標、文化敏感性、安全協議以及您的角色和職責等重要資訊。',
                'order': 13,
                'is_schema_ready': True,
                'thumbs_up': 93,
                'thumbs_down': 2
            },
            {
                'faq_id': 'faq_id_14',
                'question_en': 'What should I pack?',
                'answer_en': 'We will provide a detailed packing list once you are accepted. Generally, bring comfortable clothing suitable for the local climate, personal toiletries, any medications you need, and an open mind!',
                'question_zh_tw': '我應該帶些什麼？',
                'answer_zh_tw': '我們會在您被錄取後提供一份詳細的行李清單。一般來說，請準備適合當地氣候的舒適衣物、個人盥洗用品、任何您需要的藥品以及一顆開放的心！',
                'order': 14,
                'is_schema_ready': True,
                'thumbs_up': 81,
                'thumbs_down': 5
            },
            {
                'faq_id': 'faq_id_15',
                'question_en': 'Do I need travel insurance?',
                'answer_en': 'Yes, comprehensive travel insurance is mandatory for all international volunteers. For local projects, we also strongly recommend it. Your insurance should cover medical emergencies, trip cancellation, and personal belongings.',
                'question_zh_tw': '我需要購買旅遊保險嗎？',
                'answer_zh_tw': '是的，所有國際志工都必須購買全面的旅遊保險。對於本地專案，我們也強烈建議您購買。保險應涵蓋醫療緊急情況、行程取消和個人財物。',
                'order': 15,
                'is_schema_ready': True,
                'thumbs_up': 96,
                'thumbs_down': 1
            },
            {
                'faq_id': 'faq_id_16',
                'question_en': 'Do I need a visa for international volunteering?',
                'answer_en': 'Visa requirements depend on your nationality and the destination country. It is your responsibility to research and apply for the necessary visas. We can provide supporting documents, such as acceptance letters, to assist with your application.',
                'question_zh_tw': '我需要簽證才能參加國際志工活動嗎？',
                'answer_zh_tw': '簽證要求取決於您的國籍和目的地國家。您有責任研究並申請必要的簽證。我們可以提供支持文件，例如錄取通知書，以協助您的申請。',
                'order': 16,
                'is_schema_ready': True,
                'thumbs_up': 89,
                'thumbs_down': 3
            },
            {
                'faq_id': 'faq_id_17',
                'question_en': 'What are the accommodation arrangements?',
                'answer_en': 'Accommodation varies by project. It may include dormitories, host families, or shared apartments. All accommodations are vetted for safety and comfort. Details will be provided in the project description.',
                'question_zh_tw': '住宿安排是怎樣的？',
                'answer_zh_tw': '住宿因專案而異。可能包括宿舍、寄宿家庭或共用公寓。所有住宿都經過安全和舒適度的審查。詳細資訊將在專案說明中提供。',
                'order': 17,
                'is_schema_ready': True,
                'thumbs_up': 86,
                'thumbs_down': 4
            },
            {
                'faq_id': 'faq_id_18',
                'question_en': 'What does a typical day look like?',
                'answer_en': 'Your day will typically include project activities in the morning, workshops or community engagement in the afternoon, and free time in the evening. A detailed schedule will be provided upon your arrival.',
                'question_zh_tw': '典型的一天是怎樣的？',
                'answer_zh_tw': '您的一天通常包括早上參加專案活動，下午可能有工作坊或社區參與，晚上則有自由時間。具體行程將在您抵達時提供。',
                'order': 18,
                'is_schema_ready': True,
                'thumbs_up': 83,
                'thumbs_down': 5
            },
            {
                'faq_id': 'faq_id_19',
                'question_en': 'Will I have free time?',
                'answer_en': 'Yes, volunteers typically have free time in the evenings and on weekends to explore the local area, socialize with other volunteers, or relax. We encourage you to make the most of your cultural experience.',
                'question_zh_tw': '我會有空閒時間嗎？',
                'answer_zh_tw': '是的，志工們通常在晚上和週末有空閒時間可以探索當地地區、與其他志工社交或放鬆。我們鼓勵您充分利用您的文化體驗。',
                'order': 19,
                'is_schema_ready': True,
                'thumbs_up': 90,
                'thumbs_down': 3
            },
            {
                'faq_id': 'faq_id_20',
                'question_en': 'Who should I contact if I have issues?',
                'answer_en': 'Each project has an on-site coordinator who will be your main point of contact throughout the project. They are there to provide support, guidance, and help resolve any issues that may arise.',
                'question_zh_tw': '如果遇到問題，我應該聯繫誰？',
                'answer_zh_tw': '每個專案都有一名現場協調員，他將是您在整個專案期間的主要聯繫人。他們將為您提供支持、指導並協助解決任何問題。',
                'order': 20,
                'is_schema_ready': True,
                'thumbs_up': 94,
                'thumbs_down': 2
            },
            {
                'faq_id': 'faq_id_21',
                'question_en': 'Are meals provided during the project?',
                'answer_en': 'It depends on the project. Some projects include meals, while others require you to prepare your own. Check the project page for specific details. We will also provide information about local dining options.',
                'question_zh_tw': '專案期間提供膳食嗎？',
                'answer_zh_tw': '這取決於專案。有些專案提供膳食，而有些則需要您自行準備。請查看專案頁面以了解具體詳情。我們也會提供有關當地餐飲選擇的資訊。',
                'order': 21,
                'is_schema_ready': True,
                'thumbs_up': 80,
                'thumbs_down': 7
            },
            {
                'faq_id': 'faq_id_22',
                'question_en': 'What safety measures are in place?',
                'answer_en': 'Your safety is our top priority. We provide comprehensive safety briefings, 24/7 emergency contact, and have local staff on the ground. We closely monitor local conditions and have robust emergency protocols.',
                'question_zh_tw': '有哪些安全措施？',
                'answer_zh_tw': '您的安全是我們的首要任務。我們提供全面的安全簡報、24/7 緊急聯繫電話，並在當地設有工作人員。我們密切關注當地情況，並制定了健全的應急預案。',
                'order': 22,
                'is_schema_ready': True,
                'thumbs_up': 97,
                'thumbs_down': 1
            },
            {
                'faq_id': 'faq_id_23',
                'question_en': 'Are there any vaccination requirements?',
                'answer_en': 'For international volunteering, we recommend consulting with your doctor or a travel clinic about recommended and required vaccinations. Make sure your routine vaccinations are up to date as well.',
                'question_zh_tw': '有任何疫苗接種要求嗎？',
                'answer_zh_tw': '對於國際志工，我們建議您諮詢您的醫生或旅遊診所，以了解有關建議和要求的疫苗接種資訊。請確保您的常規疫苗接種也是最新的。',
                'order': 23,
                'is_schema_ready': True,
                'thumbs_up': 88,
                'thumbs_down': 4
            },
            {
                'faq_id': 'faq_id_24',
                'question_en': 'What if there is a medical emergency?',
                'answer_en': 'Our on-site staff are trained in first aid and can assist with minor medical issues. In case of a serious emergency, they will immediately take you to the nearest local medical facility.',
                'question_zh_tw': '如果發生醫療緊急情況怎麼辦？',
                'answer_zh_tw': '我們的現場工作人員接受過急救培訓，並能協助處理輕微的醫療問題。如果發生嚴重的緊急情況，他們將立即將您送往當地最近的醫療機構。',
                'order': 24,
                'is_schema_ready': True,
                'thumbs_up': 91,
                'thumbs_down': 3
            },
            {
                'faq_id': 'faq_id_25',
                'question_en': 'Will I be working with other volunteers?',
                'answer_en': 'Yes, most projects are team-based. You will have the opportunity to work alongside volunteers from diverse backgrounds, share experiences, and build lasting friendships.',
                'question_zh_tw': '我會和其他志工一起工作嗎？',
                'answer_zh_tw': '是的，大多數專案都是團隊合作。您將有機會與來自不同背景的志工合作，分享經驗並建立持久的友誼。',
                'order': 25,
                'is_schema_ready': True,
                'thumbs_up': 92,
                'thumbs_down': 2
            },
            {
                'faq_id': 'faq_id_26',
                'question_en': 'Do I need to speak the local language?',
                'answer_en': 'While not mandatory, learning some basic phrases in the local language is very helpful and shows respect to the local community. Some projects may offer basic language lessons.',
                'question_zh_tw': '我需要會說當地語言嗎？',
                'answer_zh_tw': '雖然不是強制性的，但學習一些當地語言的基本短語會非常有幫助，也能讓當地社區感受到您的尊重。有些專案可能會提供基本的語言課程。',
                'order': 26,
                'is_schema_ready': True,
                'thumbs_up': 85,
                'thumbs_down': 5
            },
            {
                'faq_id': 'faq_id_27',
                'question_en': 'What cultural norms should I be aware of?',
                'answer_en': 'Our pre-departure training will cover important cultural norms and etiquette. It is important to approach the local culture with an open mind and respect. Observe how locals behave and do not hesitate to ask questions!',
                'question_zh_tw': '我應該注意哪些文化規範？',
                'answer_zh_tw': '我們的行前培訓將涵蓋重要的文化規範和禮儀。以開放和尊重的態度對待當地文化非常重要。觀察當地人的行為並隨時提出問題！',
                'order': 27,
                'is_schema_ready': True,
                'thumbs_up': 89,
                'thumbs_down': 3
            },
            {
                'faq_id': 'faq_id_28',
                'question_en': 'How does my work contribute to the community?',
                'answer_en': 'Each of our projects is designed in partnership with local communities to address real needs they have identified. Your contribution, no matter how small, will be part of achieving sustainable, long-term goals.',
                'question_zh_tw': '我的工作如何為社區做出貢獻？',
                'answer_zh_tw': '我們的每個專案都是與當地社區合作設計的，旨在解決他們確定的實際需求。您的貢獻，無論大小，都將成為實現可持續、長期目標的一部分。',
                'order': 28,
                'is_schema_ready': True,
                'thumbs_up': 95,
                'thumbs_down': 1
            },
            {
                'faq_id': 'faq_id_29',
                'question_en': 'Can I stay in touch with the community after the project?',
                'answer_en': 'Absolutely! We encourage you to maintain connections with the communities you serve and fellow volunteers. Many volunteers continue to support their projects through social media or future visits.',
                'question_zh_tw': '專案結束後我可以和社區保持聯繫嗎？',
                'answer_zh_tw': '當然！我們鼓勵您與您所服務的社區以及其他志工保持聯繫。許多志工透過社交媒體或未來的訪問繼續支持他們的專案。',
                'order': 29,
                'is_schema_ready': True,
                'thumbs_up': 93,
                'thumbs_down': 2
            },
            {
                'faq_id': 'faq_id_30',
                'question_en': 'Can I fundraise for my project?',
                'answer_en': 'Yes, we welcome fundraising for your project! We can provide you with fundraising tips and resources. All funds raised will go directly towards project materials and community development.',
                'question_zh_tw': '我可以為我的專案籌款嗎？',
                'answer_zh_tw': '是的，我們歡迎您為您的專案籌款！我們可以為您提供籌款技巧和資源。所有籌集的資金將直接用於專案材料和社區發展。',
                'order': 30,
                'is_schema_ready': True,
                'thumbs_up': 87,
                'thumbs_down': 4
            },
            {
                'faq_id': 'faq_id_31',
                'question_en': 'How do I get my volunteer certificate?',
                'answer_en': 'Your certificate will be emailed to you within 2 weeks after the project ends, once you have successfully completed the project and met all requirements. You can also download it from your profile.',
                'question_zh_tw': '我如何獲得我的志工證書？',
                'answer_zh_tw': '在您成功完成專案並達到所有要求後，您的證書將在專案結束後 2 週內透過電子郵件發送給您。您也可以從您的個人資料中下載。',
                'order': 31,
                'is_schema_ready': True,
                'thumbs_up': 96,
                'thumbs_down': 1
            },
            {
                'faq_id': 'faq_id_32',
                'question_en': 'Is there an alumni network?',
                'answer_en': 'Yes, we have an active alumni network that you can join after your project. It is a great way to stay connected with past volunteers, share stories, and learn about future opportunities worldwide.',
                'question_zh_tw': '有校友網絡嗎？',
                'answer_zh_tw': '是的，我們有一個活躍的校友網絡，您可以在專案結束後加入。這是在全球範圍內與過去的志工保持聯繫、分享故事並了解未來機會的好方法。',
                'order': 32,
                'is_schema_ready': True,
                'thumbs_up': 90,
                'thumbs_down': 3
            },
            {
                'faq_id': 'faq_id_33',
                'question_en': 'Can I request a reference letter?',
                'answer_en': 'Yes, after successfully completing your project, you can request a reference letter from your project coordinator. Please give them advance notice so they have adequate time to write it.',
                'question_zh_tw': '我可以索取推薦信嗎？',
                'answer_zh_tw': '是的，在您成功完成專案後，您可以向您的專案協調員索取推薦信。請提前通知他們，以便他們有足夠的時間為您撰寫。',
                'order': 33,
                'is_schema_ready': True,
                'thumbs_up': 88,
                'thumbs_down': 4
            },
            {
                'faq_id': 'faq_id_34',
                'question_en': 'How do I update my profile?',
                'answer_en': 'You can update your profile anytime by logging into your account. Just navigate to the "My Profile" section, and you can edit your contact information, skills, and preferences there.',
                'question_zh_tw': '如何更新我的個人資料？',
                'answer_zh_tw': '您可以隨時登入您的帳戶來更新您的個人資料。只需導航至「我的個人資料」部分，您就可以在那裡編輯您的聯繫資訊、技能和偏好。',
                'order': 34,
                'is_schema_ready': True,
                'thumbs_up': 84,
                'thumbs_down': 5
            },
            {
                'faq_id': 'faq_id_35',
                'question_en': 'I forgot my password. What should I do?',
                'answer_en': 'No worries! Just click the "Forgot Password" link on the login page. You will receive an email with instructions on how to reset your password. Make sure to check your spam folder.',
                'question_zh_tw': '我忘記密碼了，該怎麼辦？',
                'answer_zh_tw': '別擔心！只需點擊登入頁面上的「忘記密碼」連結即可。您會收到一封電子郵件，其中包含重設密碼的說明。請務必檢查您的垃圾郵件文件夾。',
                'order': 35,
                'is_schema_ready': True,
                'thumbs_up': 82,
                'thumbs_down': 6
            },
            {
                'faq_id': 'faq_id_36',
                'question_en': 'How do I check the status of my application?',
                'answer_en': 'Once logged into your account, there will be a "My Applications" section on your dashboard. You can track the status of all your applications there, from "Submitted" to "Accepted".',
                'question_zh_tw': '如何查看我的申請狀態？',
                'answer_zh_tw': '登入您的帳戶後，儀表板上會有一個「我的申請」部分。您可以在那裡跟踪所有申請的狀態，從「已提交」到「已錄取」。',
                'order': 36,
                'is_schema_ready': True,
                'thumbs_up': 91,
                'thumbs_down': 3
            },
            {
                'faq_id': 'faq_id_37',
                'question_en': 'Can my friend/family member volunteer with me?',
                'answer_en': 'We love hosting groups! You can indicate who you would like to volunteer with in your application. We will do our best to accommodate, but please note this depends on project availability.',
                'question_zh_tw': '我的朋友/家人可以和我一起做志工嗎？',
                'answer_zh_tw': '我們很樂意接待團體！您可以在申請表中註明您希望與誰一起做志工。我們會盡力安排，但請注意，這取決於專案的可用性。',
                'order': 37,
                'is_schema_ready': True,
                'thumbs_up': 86,
                'thumbs_down': 5
            },
            {
                'faq_id': 'faq_id_38',
                'question_en': 'Do you offer corporate volunteering?',
                'answer_en': 'Yes, we offer tailored corporate volunteering programs for companies looking to give back to the community. Please contact us through our partnerships page to discuss possibilities.',
                'question_zh_tw': '你們提供企業志工服務嗎？',
                'answer_zh_tw': '是的，我們為希望為社區做出貢獻的公司提供量身定制的企業志工計畫。請透過我們的合作夥伴頁面與我們聯繫以討論可能性。',
                'order': 38,
                'is_schema_ready': True,
                'thumbs_up': 79,
                'thumbs_down': 7
            },
            {
                'faq_id': 'faq_id_39',
                'question_en': 'Where do project fees (if any) go?',
                'answer_en': 'Project fees (if applicable) go directly towards covering the operational costs of the project, including materials, local staff salaries, accommodation, and training. We are fully transparent about how funds are used.',
                'question_zh_tw': '專案費用（如果有的話）用在哪裡？',
                'answer_zh_tw': '專案費用（如適用）直接用於支付專案運營成本，包括材料、當地員工薪資、住宿和培訓。我們對我們的資金使用方式完全透明。',
                'order': 39,
                'is_schema_ready': True,
                'thumbs_up': 93,
                'thumbs_down': 2
            },
            {
                'faq_id': 'faq_id_40',
                'question_en': 'Are there scholarships or financial aid available?',
                'answer_en': 'We offer a limited number of need-based scholarships. Application information can be found on the "Fees and Funding" section of our website. We also encourage you to seek external funding opportunities.',
                'question_zh_tw': '有獎學金或經濟援助嗎？',
                'answer_zh_tw': '我們提供有限數量的基於需求的獎學金。申請資訊可在我們網站的「費用和資助」部分找到。我們也鼓勵您尋找外部的資助機會。',
                'order': 40,
                'is_schema_ready': True,
                'thumbs_up': 94,
                'thumbs_down': 2
            }
        ]

        if options['clear']:
            self.stdout.write('Clearing existing FAQ data...')
            FAQ.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing FAQ data cleared.'))

        self.stdout.write('Starting FAQ data seeding...')

        for faq_item in faq_data:
            defaults = {
                'question': faq_item['question_en'],
                'answer': faq_item['answer_en'],
                'question_en': faq_item['question_en'],
                'answer_en': faq_item['answer_en'],
                'question_zh_tw': faq_item['question_zh_tw'],
                'answer_zh_tw': faq_item['answer_zh_tw'],
                'order': faq_item['order'],
                'is_schema_ready': faq_item['is_schema_ready'],
                'thumbs_up': faq_item['thumbs_up'],
                'thumbs_down': faq_item['thumbs_down'],
                'created_at': timezone.now(),
                'updated_at': timezone.now(),
            }

            faq, created = FAQ.objects.update_or_create(
                faq_id=faq_item['faq_id'],
                defaults=defaults
            )

            if created:
                self.stdout.write(f'Created FAQ: {faq.question}')
            else:
                self.stdout.write(f'Updated FAQ: {faq.question}')

        self.stdout.write(self.style.SUCCESS(f'FAQ seeding completed successfully! Total FAQs: {len(faq_data)}'))
