from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum

from rangefilter.filter import DateRangeFilter

from transactions.models import BankInfo, AccountInfo, Transaction


admin.site.register(BankInfo)
admin.site.register(AccountInfo)


class PayPlatformFilter(admin.SimpleListFilter):
    title = "결제 플랫폼"  # 필터 제목
    parameter_name = "pay_platform"  # URL에서 사용할 파라미터 이름

    def lookups(self, request, model_admin):
        # 필터 옵션 목록을 반환합니다.
        return (
            ("현장결제", "현장결제"),
            ("포장", "포장"),
            ("네이버", "네이버"),
            ("쿠팡", "쿠팡"),
            ("배달의민족", "배달의민족"),
            ("구글", "구글"),
            ("기타", "기타"),
        )

    def queryset(self, request, queryset):
        # 선택된 필터 옵션에 따라 쿼리셋을 필터링합니다.
        if self.value() == "현장결제":
            return queryset.filter(pay_platform="현장결제")
        if self.value() == "포장":
            return queryset.filter(pay_platform="포장")
        if self.value() == "네이버":
            return queryset.filter(pay_platform="네이버")
        if self.value() == "쿠팡":
            return queryset.filter(pay_platform="쿠팡")
        if self.value() == "배달의민족":
            return queryset.filter(pay_platform="배달의민족")
        if self.value() == "구글":
            return queryset.filter(pay_platform="구글")
        if self.value() == "기타":
            return queryset.exclude(
                pay_platform__in=["현장결제", "포장", "네이버", "쿠팡", "배달의민족", "구글"]
            )
        return queryset


class TransactionAdmin(admin.ModelAdmin):
    ordering = ["-id"]  # id 필드를 역순으로 정렬
    list_display = (
        "id",
        "user",
        "tran_date",
        "pay_type",
        "pay_platform",
        "amount_total",
        "amount_fee",
        "amount",
    )
    list_filter = [
        ("tran_date", DateRangeFilter),
        "pay_type",
        PayPlatformFilter,
    ]
    list_select_related = ["user"]
    list_per_page = 100  # 한 페이지당 100 개의 항목을 표시

    # custom admin template
    change_list_template = "admin/transaction_custom_admin.html"

    def changelist_view(self, request, extra_context=None):
        result = (
            Transaction.objects.all()
            .values("pay_type")
            .annotate(
                sum_amount_total=Sum("amount_total"),
                sum_amount_fee=Sum("amount_fee"),
                sum_amount=Sum("amount"),
            )
        )

        context = list()
        for item in result:
            context.append(
                dict(
                    pay_type=item["pay_type"],
                    sum_amount_total=intcomma(item["sum_amount_total"]),
                    sum_amount_fee=intcomma(item["sum_amount_fee"]),
                    sum_amount=intcomma(item["sum_amount"]),
                )
            )

        # 추가 컨텍스트를 포함하여 render
        res = super().changelist_view(request, extra_context=dict(result=context))
        return res


admin.site.register(Transaction, TransactionAdmin)
