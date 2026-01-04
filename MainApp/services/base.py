from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from copy import deepcopy

class BaseService:
    model = None
    allowed_roles = None
    user_field_name = None
    confidential_fields = []

    @classmethod
    def _check_role(cls, user):
        if cls.allowed_roles is None:
            return
        if user.role not in cls.allowed_roles:
            raise PermissionDenied(f"Роль '{user.role}' не имеет доступа к этому сервису.")

    @classmethod
    def _check_ownership(cls, user, obj):
        if user.role == "student":
            if cls.user_field_name and hasattr(obj, cls.user_field_name):
                owner = getattr(obj, cls.user_field_name)
                if hasattr(owner, "user"):
                    owner_id = owner.user_id
                else:
                    owner_id = getattr(owner, "id", None)
                if owner_id != user.id:
                    raise PermissionDenied("Студент может изменять только свои данные.")
        elif user.role == "mentor":
            if cls.user_field_name and hasattr(obj, cls.user_field_name):
                owner = getattr(obj, cls.user_field_name)
                if hasattr(owner, "group") and owner.group_id != user.mentor_profile.department_id:
                    raise PermissionDenied("Ментор может изменять только своих студентов.")

    @classmethod
    def _hide_confidential(cls, user, obj):
        if user.role in ["teacher", "mentor"]:
            obj_copy = deepcopy(obj.__dict__)
            for field in cls.confidential_fields:
                if field in obj_copy:
                    obj_copy[field] = None
            return obj_copy
        return obj

    @classmethod
    def get(cls, user, obj_id):
        cls._check_role(user)
        try:
            obj = cls.model.objects.get(id=obj_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"{cls.model.__name__} с id={obj_id} не найден.")
        cls._check_ownership(user, obj)
        return cls._hide_confidential(user, obj)

    @classmethod
    def list(cls, user, filters=None):
        cls._check_role(user)
        queryset = cls.model.objects.all()
        if filters:
            queryset = queryset.filter(**filters)
        if user.role == "student" and cls.user_field_name:
            kwargs = {f"{cls.user_field_name}__user_id": user.id}
            queryset = queryset.filter(**kwargs)
        elif user.role == "mentor" and cls.user_field_name:
            if hasattr(user, "mentor_profile") and user.mentor_profile:
                queryset = queryset.filter(**{f"{cls.user_field_name}__group": user.mentor_profile.department})
        return [cls._hide_confidential(user, obj) for obj in queryset]

    @classmethod
    def create(cls, user, **data):
        cls._check_role(user)
        if user.role == "student" and cls.user_field_name:
            data[cls.user_field_name] = user.studentprofile
        obj = cls.model(**data)
        cls._check_ownership(user, obj)
        obj.save()
        return cls._hide_confidential(user, obj)

    @classmethod
    def update(cls, user, obj_id, **data):
        obj = cls.model.objects.get(id=obj_id)
        cls._check_ownership(user, obj)
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
        return cls._hide_confidential(user, obj)

    @classmethod
    def delete(cls, user, obj_id):
        obj = cls.model.objects.get(id=obj_id)
        cls._check_ownership(user, obj)
        obj.delete()
        return True
        