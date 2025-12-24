import csv
import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.content.models import FAQ


class Command(BaseCommand):
    help = 'Seed FAQ data from CSV file with Chinese translations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing FAQ data before seeding',
        )

    def handle(self, *args, **options):
        # Define hardcoded translations since they are not in the CSV
        # Map faq_id (e.g. "faq_id_1") or question text to Chinese Q&A
        translations = {
            "faq_id_1": {
                "question_zh_tw": "如何申請志工專案？",
                "answer_zh_tw": "若要申請志工專案，請瀏覽我們的專案頁面，選擇您感興趣的專案，然後點擊「申請」按鈕。您需要登入帳戶才能提交申請。"
            },
            "faq_id_2": {
                "question_zh_tw": "成為志工有什麼要求？",
                "answer_zh_tw": "要求因專案而異，但通常您需要年滿 18 歲（或 16 歲並獲得父母同意），熱衷於社區服務，並能承諾專案期間。特定專案可能有額外要求。"
            },
            "faq_id_3": {
                "question_zh_tw": "志工活動有費用嗎？",
                "answer_zh_tw": "我們的大多數志工專案都是免費參加的。然而，志工通常需要自行負擔交通、住宿和個人費用。有些專案可能會收取少量的行政費用。"
            },
            "faq_id_4": {
                "question_zh_tw": "我可以參加國際志工嗎？",
                "answer_zh_tw": "是的！我們提供台灣和國際的志工機會。請查看我們專案頁面上的國家篩選器，找到您感興趣的機會。"
            },
            "faq_id_5": {
                "question_zh_tw": "志工專案通常持續多久？",
                "answer_zh_tw": "專案持續時間從幾天到幾週或幾個月不等。每個專案列表都會顯示預計的時間投入和持續時間。您可以在我們的搜尋頁面上按持續時間篩選專案。"
            },
            "faq_id_6": {
                "question_zh_tw": "完成專案後我會收到證書嗎？",
                "answer_zh_tw": "是的！順利完成志工專案後，您將收到一份記錄您的志工時數和貢獻的證書。這對學校要求或求職申請很有用。"
            },
            "faq_id_7": {
                "question_zh_tw": "如果我需要取消申請怎麼辦？",
                "answer_zh_tw": "如果您需要取消申請，請盡快透過聯絡表單或電子郵件與我們聯繫。我們了解情況可能會發生變化，我們將與您一起尋找解決方案。"
            },
            "faq_id_8": {
                "question_zh_tw": "志工需要特殊技能嗎？",
                "answer_zh_tw": "不一定！我們的許多專案都歡迎沒有特殊技能的志工——只需要熱情和樂於助人的心。然而，有些專業專案可能需要特定的技能或資格，這將在專案描述中清楚說明。"
            },
            "faq_id_9": {
                "question_zh_tw": "申請後會發生什麼？",
                "answer_zh_tw": "提交申請後，我們的團隊將進行審核。如果您的資格符合專案需求，我們會在 1-2 週內與您聯繫安排面試。您隨時可以登入您的帳戶查看申請狀態。"
            },
            "faq_id_10": {
                "question_zh_tw": "我可以同時申請多個專案嗎？",
                "answer_zh_tw": "可以，我們鼓勵您申請所有感興趣的專案！不過，請根據您的興趣和時間仔細選擇，以確保您能全身心投入。如果您被多個專案錄取，您需要從中選擇一個。"
            },
            "faq_id_11": {
                "question_zh_tw": "申請需要提交哪些文件？",
                "answer_zh_tw": "通常，您需要提交一份最新的履歷和一封說明您為何對該專案感興趣的求職信。對於國際專案，可能還需要您的護照影本和簽證文件。"
            },
            "faq_id_12": {
                "question_zh_tw": "申請流程中會有面試嗎？",
                "answer_zh_tw": "是的，大多數專案都需要進行一次簡短的線上面試。這有助於我們更了解您，並確保專案適合您。這也是您提問的好機會！"
            },
            "faq_id_13": {
                "question_zh_tw": "專案開始前有提供培訓嗎？",
                "answer_zh_tw": "是的，所有志工都必須參加行前培訓課程。本課程涵蓋專案目標、文化敏感性、安全協議以及您的角色和職責等重要資訊。"
            },
            "faq_id_14": {
                "question_zh_tw": "我應該帶些什麼？",
                "answer_zh_tw": "我們會在您被錄取後提供一份詳細的行李清單。一般來說，請準備適合當地氣候的舒適衣物、個人盥洗用品、任何您需要的藥品以及一顆開放的心！"
            },
            "faq_id_15": {
                "question_zh_tw": "我需要購買旅遊保險嗎？",
                "answer_zh_tw": "是的，所有國際志工都必須購買全面的旅遊保險。對於本地專案，我們也強烈建議您購買。保險應涵蓋醫療緊急情況、行程取消和個人財物。"
            },
            "faq_id_16": {
                "question_zh_tw": "我需要簽證才能參加國際志工活動嗎？",
                "answer_zh_tw": "簽證要求取決於您的國籍和目的地國家。您有責任研究並申請必要的簽證。我們可以提供支持文件，例如錄取通知書，以協助您的申請。"
            },
            "faq_id_17": {
                "question_zh_tw": "住宿安排是怎樣的？",
                "answer_zh_tw": "住宿因專案而異。可能包括宿舍、寄宿家庭或共用公寓。所有住宿都經過安全和舒適度的審查。詳細資訊將在專案說明中提供。"
            },
            "faq_id_18": {
                "question_zh_tw": "典型的一天是怎樣的？",
                "answer_zh_tw": "您的一天通常包括早上參加專案活動，下午可能有工作坊或社區參與，晚上則有自由時間。具體行程將在您抵達時提供。"
            },
            "faq_id_19": {
                "question_zh_tw": "我會有空閒時間嗎？",
                "answer_zh_tw": "是的，志工們通常在晚上和週末有空閒時間可以探索當地地區、與其他志工社交或放鬆。我們鼓勵您充分利用您的文化體驗。"
            },
            "faq_id_20": {
                "question_zh_tw": "如果遇到問題，我應該聯繫誰？",
                "answer_zh_tw": "每個專案都有一名現場協調員，他將是您在整個專案期間的主要聯繫人。他們將為您提供支持、指導並協助解決任何問題。"
            },
            "faq_id_21": {
                "question_zh_tw": "專案期間提供膳食嗎？",
                "answer_zh_tw": "這取決於專案。有些專案提供膳食，而有些則需要您自行準備。請查看專案頁面以了解具體詳情。我們也會提供有關當地餐飲選擇的資訊。"
            },
            "faq_id_22": {
                "question_zh_tw": "有哪些安全措施？",
                "answer_zh_tw": "您的安全是我們的首要任務。我們提供全面的安全簡報、24/7 緊急聯繫電話，並在當地設有工作人員。我們密切關注當地情況，並制定了健全的應急預案。"
            },
            "faq_id_23": {
                "question_zh_tw": "有任何疫苗接種要求嗎？",
                "answer_zh_tw": "對於國際志工，我們建議您諮詢您的醫生或旅遊診所，以了解有關建議和要求的疫苗接種資訊。請確保您的常規疫苗接種也是最新的。"
            },
            "faq_id_24": {
                "question_zh_tw": "如果發生醫療緊急情況怎麼辦？",
                "answer_zh_tw": "我們的現場工作人員接受過急救培訓，並能協助處理輕微的醫療問題。如果發生嚴重的緊急情況，他們將立即將您送往當地最近的醫療機構。"
            },
            "faq_id_25": {
                "question_zh_tw": "我會和其他志工一起工作嗎？",
                "answer_zh_tw": "是的，大多數專案都是團隊合作。您將有機會與來自不同背景的志工合作，分享經驗並建立持久的友誼。"
            },
            "faq_id_26": {
                "question_zh_tw": "我需要會說當地語言嗎？",
                "answer_zh_tw": "雖然不是強制性的，但學習一些當地語言的基本短語會非常有幫助，也能讓當地社區感受到您的尊重。有些專案可能會提供基本的語言課程。"
            },
            "faq_id_27": {
                "question_zh_tw": "我應該注意哪些文化規範？",
                "answer_zh_tw": "我們的行前培訓將涵蓋重要的文化規範和禮儀。以開放和尊重的態度對待當地文化非常重要。觀察當地人的行為並隨時提出問題！"
            },
            "faq_id_28": {
                "question_zh_tw": "我的工作如何為社區做出貢獻？",
                "answer_zh_tw": "我們的每個專案都是與當地社區合作設計的，旨在解決他們確定的實際需求。您的貢獻，無論大小，都將成為實現可持續、長期目標的一部分。"
            },
            "faq_id_29": {
                "question_zh_tw": "專案結束後我可以和社區保持聯繫嗎？",
                "answer_zh_tw": "當然！我們鼓勵您與您所服務的社區以及其他志工保持聯繫。許多志工透過社交媒體或未來的訪問繼續支持他們的專案。"
            },
            "faq_id_30": {
                "question_zh_tw": "我可以為我的專案籌款嗎？",
                "answer_zh_tw": "是的，我們歡迎您為您的專案籌款！我們可以為您提供籌款技巧和資源。所有籌集的資金將直接用於專案材料和社區發展。"
            },
            "faq_id_31": {
                "question_zh_tw": "我如何獲得我的志工證書？",
                "answer_zh_tw": "在您成功完成專案並達到所有要求後，您的證書將在專案結束後 2 週內透過電子郵件發送給您。您也可以從您的個人資料中下載。"
            },
            "faq_id_32": {
                "question_zh_tw": "有校友網絡嗎？",
                "answer_zh_tw": "是的，我們有一個活躍的校友網絡，您可以在專案結束後加入。這是在全球範圍內與過去的志工保持聯繫、分享故事並了解未來機會的好方法。"
            },
            "faq_id_33": {
                "question_zh_tw": "我可以索取推薦信嗎？",
                "answer_zh_tw": "是的，在您成功完成專案後，您可以向您的專案協調員索取推薦信。請提前通知他們，以便他們有足夠的時間為您撰寫。"
            },
            "faq_id_34": {
                "question_zh_tw": "如何更新我的個人資料？",
                "answer_zh_tw": "您可以隨時登入您的帳戶來更新您的個人資料。只需導航至「我的個人資料」部分，您就可以在那裡編輯您的聯繫資訊、技能和偏好。"
            },
            "faq_id_35": {
                "question_zh_tw": "我忘記密碼了，該怎麼辦？",
                "answer_zh_tw": "別擔心！只需點擊登入頁面上的「忘記密碼」連結即可。您會收到一封電子郵件，其中包含重設密碼的說明。請務必檢查您的垃圾郵件文件夾。"
            },
            "faq_id_36": {
                "question_zh_tw": "如何查看我的申請狀態？",
                "answer_zh_tw": "登入您的帳戶後，儀表板上會有一個「我的申請」部分。您可以在那裡跟踪所有申請的狀態，從「已提交」到「已錄取」。"
            },
            "faq_id_37": {
                "question_zh_tw": "我的朋友/家人可以和我一起做志工嗎？",
                "answer_zh_tw": "我們很樂意接待團體！您可以在申請表中註明您希望與誰一起做志工。我們會盡力安排，但請注意，這取決於專案的可用性。"
            },
            "faq_id_38": {
                "question_zh_tw": "你們提供企業志工服務嗎？",
                "answer_zh_tw": "是的，我們為希望為社區做出貢獻的公司提供量身定制的企業志工計畫。請透過我們的合作夥伴頁面與我們聯繫以討論可能性。"
            },
            "faq_id_39": {
                "question_zh_tw": "專案費用（如果有的話）用在哪裡？",
                "answer_zh_tw": "專案費用（如適用）直接用於支付專案運營成本，包括材料、當地員工薪資、住宿和培訓。我們對我們的資金使用方式完全透明。"
            },
            "faq_id_40": {
                "question_zh_tw": "有獎學金或經濟援助嗎？",
                "answer_zh_tw": "我們提供有限數量的基於需求的獎學金。申請資訊可在我們網站的「費用和資助」部分找到。我們也鼓勵您尋找外部的資助機會。"
            }
        }

        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        csv_path = os.path.join(data_dir, '4_FAQ.csv')

        if options['clear']:
            self.stdout.write('Clearing existing FAQ data...')
            FAQ.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing FAQ data cleared.'))

        self.stdout.write('Starting FAQ data seeding...')

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.WARNING(f'CSV file not found: {csv_path}'))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse dates
                created_at = self.parse_datetime(row.get('created_at'))
                updated_at = self.parse_datetime(row.get('updated_at'))

                # Parse boolean field
                is_schema_ready = row.get('is_schema_ready', '').lower() == 'true'

                # Parse integers
                order = int(row.get('order', 0)) if row.get('order') else 0
                thumbs_up = int(row.get('thumbs_up', 0)) if row.get('thumbs_up') else 0
                thumbs_down = int(row.get('thumbs_down', 0)) if row.get('thumbs_down') else 0

                faq_id = row.get('faq_id')
                question_en = row.get('question', '')
                answer_en = row.get('answer', '')
                
                # Check for translations in CSV first, then fallback to hardcoded map
                question_zh = row.get('question_zh_tw') or translations.get(faq_id, {}).get('question_zh_tw', '')
                answer_zh = row.get('answer_zh_tw') or translations.get(faq_id, {}).get('answer_zh_tw', '')

                # If still empty, maybe use English as fallback? 
                # Better to leave it empty if we really don't have it, but for this task we want Chinese.
                if not question_zh:
                    question_zh = question_en
                if not answer_zh:
                    answer_zh = answer_en

                defaults = {
                    'question': question_en,       # Default language (usually en)
                    'answer': answer_en,           # Default language (usually en)
                    'question_en': question_en,
                    'answer_en': answer_en,
                    'question_zh_tw': question_zh,
                    'answer_zh_tw': answer_zh,
                    'order': order,
                    'is_schema_ready': is_schema_ready,
                    'thumbs_up': thumbs_up,
                    'thumbs_down': thumbs_down,
                    'created_at': created_at or timezone.now(),
                    'updated_at': updated_at or timezone.now(),
                }

                faq, created = FAQ.objects.update_or_create(
                    faq_id=faq_id,
                    defaults=defaults
                )

                if created:
                    self.stdout.write(f'Created FAQ: {faq.question}')
                else:
                    self.stdout.write(f'Updated FAQ: {faq.question}')

        self.stdout.write(self.style.SUCCESS('FAQ seeding completed successfully!'))

    def parse_datetime(self, date_str):
        """Parse datetime string to datetime object"""
        if not date_str or date_str.lower() == 'null':
            return None
        try:
            # Handle ISO format with Z
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            # Make timezone-naive since USE_TZ=False or handled elsewhere
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        except ValueError:
            self.stdout.write(self.style.WARNING(f'Invalid datetime format: {date_str}'))
            return None
