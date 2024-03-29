import random
import string

from django.utils import timezone

from faker import Faker

from user.models import User, Profile
from transactions.models import BankInfo, AccountInfo

today = timezone.localdate()
fake = Faker("ko_KR")

# ============================================================ #
# BankInfo dummy
# ============================================================ #

# from: https://docs.tosspayments.com/reference/codes
bank_code_info_list = [
    ["기업 BC, 기업비씨, IBK_BC", "3K"],
    ["광주은행, 광주, GWANGJUBANK", "46"],
    ["롯데카드, 롯데, LOTTE", "71"],
    ["KDB산업은행, 산업, KDBBANK", "30"],
    ["BC카드, -, BC", "B31"],
    ["삼성카드, 삼성, SAMSUNG", "51"],
    ["새마을금고, 새마을, SAEMAUL", "38"],
    ["신한카드, 신한, SHINHAN", "41"],
    ["신협, 신협, SHINHYEOP", "62"],
    ["씨티카드, 씨티, CITI", "36"],
    ["우리BC카드(BC 매입), 우리, WOORI", "33"],
    ["우리카드(우리 매입), 우리, WOORI", "W1"],
    ["저축은행중앙회, 저축, SAVINGBANK", "39"],
    ["전북은행, 전북, JEONBUKBANK", "J35"],
    ["제주은행, 제주, JEJUBANK", "42"],
    ["카카오뱅크, 카카오뱅크, KAKAOBANK", "15"],
    ["케이뱅크, 케이뱅크, KBANK", "3A"],
    ["토스뱅크, 토스뱅크, TOSSBANK", "24"],
    ["하나카드, 하나, HANA", "21"],
    ["현대카드, 현대, HYUNDAI", "61"],
    ["KB국민카드, 국민, KOOKMIN", "11"],
    ["NH농협카드, 농협, NONGHYEOP", "91"],
    ["Sh수협은행, 수협, SUHYEOP", "34"],
    ["다이너스 클럽, 다이너스, DINERS", "6D"],
    ["마스터카드, 마스터, MASTER", "4M"],
    ["유니온페이, 유니온페이, UNIONPAY", "3C"],
    ["아메리칸 익스프레스, -, AMEX", "7A"],
    ["JCB, -, JCB", "4J"],
    ["VISA, 비자, VISA", "4V"],
    ["경남은행, 경남, KYONGNAMBANK", "B39"],
    ["교보증권, 교보증권, KYOBO_SECURITIES", "S8"],
    ["단위농협(지역농축협), 단위농협, LOCALNONGHYEOP", "12"],
    ["대신증권, 대신증권, DAISHIN_SECURITIES", "SE"],
    ["메리츠증권, 메리츠증권, MERITZ_SECURITIES", "SK"],
    ["미래에셋증권, 미래에셋증권, MIRAE_ASSET_SECURITIES", "S5"],
    ["부국증권, 부국, BOOKOOK_SECURITIES", "SM"],
    ["부산은행, 부산, BUSANBANK", "32"],
    ["삼성증권, 삼성증권, SAMSUNG_SECURITIES", "S3"],
    ["새마을금고, 새마을, SAEMAUL", "45"],
    ["산림조합, 산림, SANLIM", "64"],
    ["신영증권, 신영증권, SHINYOUNG_SECURITIES", "SN"],
    ["신한금융투자, 신한금융투자, SHINHAN_INVESTMENT", "S2"],
    ["신한은행, 신한, SHINHAN", "88"],
    ["신협, 신협, SHINHYEOP", "48"],
    ["씨티은행, 씨티, CITI", "27"],
    ["우리은행, 우리, WOORI", "20"],
    ["우체국예금보험, 우체국, POST", "P71"],
    ["유안타증권, 유안타증권, YUANTA_SECURITES", "S0"],
    ["유진투자증권, 유진투자증권, EUGENE_INVESTMENT_AND_SECURITIES", "SJ"],
    ["저축은행중앙회, 저축, SAVINGBANK", "50"],
    ["전북은행, 전북, JEONBUKBANK", "37"],
    ["제주은행, 제주, JEJUBANK", "35"],
    ["카카오뱅크, 카카오, KAKAOBANK", "90"],
    ["카카오페이증권, 카카오페이증권, KAKAOPAY_SECURITIES", "SQ"],
    ["케이뱅크, 케이, KBANK", "89"],
    ["키움증권, 키움증권, KIWOOM", "SB"],
    # ["토스머니, 토스머니, TOSS_MONEY", "-"],
    ["토스뱅크, 토스, TOSSBANK", "92"],
    ["토스증권, 토스증권, TOSS_SECURITIES", "ST"],
    ["펀드온라인코리아(한국포스증권), 펀드온라인코리아, KOREA_FOSS_SECURITIES", "SR"],
    ["하나금융투자, 하나금융투자, HANA_INVESTMENT_AND_SECURITIES", "SH"],
    ["하나은행, 하나, HANA", "81"],
    ["하이투자증권, 하이투자증권, HI_INVESTMENT_AND_SECURITIES", "S9"],
    ["한국투자증권, 한국투자증권, KOREA_INVESTMENT_AND_SECURITIES", "S6"],
    ["한화투자증권, 한화투자증권, HANHWA_INVESTMENT_AND_SECURITIES", "SG"],
    ["현대차증권, 현대차증권, HYUNDAI_MOTOR_SECURITIES", "SA"],
    ["홍콩상하이은행, -, HSBC", "54"],
    ["DB금융투자, DB금융투자, DB_INVESTMENT_AND_SECURITIES", "SI"],
    ["DGB대구은행, 대구, DAEGUBANK", "31"],
    ["IBK기업은행, 기업, IBK", "03"],
    ["KB국민은행, 국민, KOOKMIN", "06"],
    ["KB증권, KB증권, KB_SECURITIES", "S4"],
    ["KDB산업은행, 산업, KDBBANK", "02"],
    ["KTB투자증권(다올투자증권), KTB투자증권, DAOL_INVESTMENT_AND_SECURITIES", "SP"],
    ["LIG투자증권, LIG투자, LIG_INVESTMENT_AND_SECURITIES", "SO"],
    ["NH농협은행, 농협, NONGHYEOP", "N11"],
    ["NH투자증권, NH투자증권, NH_INVESTMENT_AND_SECURITIES", "SL"],
    ["SC제일은행, SC제일, SC", "23"],
    ["Sh수협은행, 수협, SUHYEOP", "07"],
    ["SK증권, SK증권, SK_SECURITIES", "SD"],
    # ["토스페이, 토스페이, TOSSPAY", "-"],
    # ["네이버페이, 네이버페이, NAVERPAY", "-"],
    # ["삼성페이, 삼성페이, SAMSUNGPAY", "-"],
    # ["애플페이, 애플페이, APPLEPAY", "-"],
    # ["엘페이, 엘페이, LPAY", "-"],
    # ["카카오페이, 카카오페이, KAKAOPAY", "-"],
    # ["페이코, 페이코, PAYCO", "-"],
    # ["SSG페이, SSG페이, SSG", "-"],
    # ["KT, KT, KT", "-"],
    # ["LGU, LGU, LG 유플러스", "-"],
    # ["SKT, SKT, SK 텔레콤", "-"],
    # ["HELLO, HELLO, LG 헬로모바일", "-"],
    # ["KCT, KCT, 티플러스", "-"],
    # ["SK7, SK7, SK 세븐모바일", "-"],
]

created_bank_info_cnt = 0
for info in bank_code_info_list:
    new_bank_info, is_created = BankInfo.objects.get_or_create(
        remark=info[0],
        bank_code=info[1],
    )
    if is_created:
        created_bank_info_cnt += 1

print(f"[{today}] {created_bank_info_cnt} 개의 BankInfo bulk create")


# ============================================================ #
# User & Profile dummy
# ============================================================ #
inflow_list = [
    "naver",
    "google",
    "daum",
    "kakao",
    "naver-cafe",
    "daum-cafe",
    "marketing-agency",
    "email",
    "other",
]
created_profile_cnt = 0
created_user_cnt = 0
for _ in range(20):
    new_profile, is_created = Profile.objects.get_or_create(
        nick_name=fake.user_name()[:20],
        profile_img=f"https://picsum.photos/200?random={random.randint(1, 500)}",
        profile_desc=fake.sentence(nb_words=14),
    )
    created_profile_cnt += 1
    phone_number = fake.phone_number()
    while True:
        if phone_number.startswith("010"):
            break
        phone_number = fake.phone_number()

    new_user, is_created = User.objects.get_or_create(
        profile=new_profile,
        name=fake.name(),
        phone=phone_number,
        inflow=random.choice(inflow_list),
    )
    created_user_cnt += 1

print(f"[{today}] {created_profile_cnt} 개의 Profile bulk create")
print(f"[{today}] {created_user_cnt} 개의 User bulk create")


# ============================================================ #
# all User's random bank_info - AccountInfo
# ============================================================ #
def generate_account_number(length) -> str:
    account_number = "".join(random.choice(string.digits) for _ in range(length))
    return account_number


created_account_info_cnt = 0
for target_user in User.objects.all():
    target_bank = BankInfo.objects.all().order_by("?").first()

    how_many_accounts = random.randint(1, 4)
    for _ in range(how_many_accounts):
        new_account_info, is_created = AccountInfo.objects.get_or_create(
            user=target_user,
            bank_info=target_bank,
            account=generate_account_number(16),
        )
        if is_created:
            created_account_info_cnt += 1

print(f"[{today}] {created_account_info_cnt} 개의 AccountInfo bulk create")
