class MultiDBRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to orders.
        """
        return "read"

    def db_for_write(self, model, **hints):
        # "insert", "update", "delete" 작업은 "default" 데이터베이스로 라우팅
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        # 관계 허용
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # 마이그레이션 허용
        return True
