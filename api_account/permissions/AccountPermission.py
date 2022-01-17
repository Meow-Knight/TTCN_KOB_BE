from api_base.permission import MyBasePermission
from api_account.constants import RoleData


class CustomerPermission(MyBasePermission):
    match_any_roles = [RoleData.CUSTOMER]


class StaffPermission(MyBasePermission):
    match_any_roles = [RoleData.STAFF]


class AdminPermission(MyBasePermission):
    match_any_roles = [RoleData.ADMIN]


class StaffOrAdminPermission(MyBasePermission):
    match_any_roles = [RoleData.ADMIN, RoleData.STAFF]
