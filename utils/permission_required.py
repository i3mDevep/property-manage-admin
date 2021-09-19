from rest_framework import permissions

class HasRequiredPermissionForMethod(permissions.BasePermission):

    get_permission_required = None
    put_permission_required = None
    post_permission_required = None
    delete_permission_required = None
    patch_permission_required = None

    def has_permission(self, request, view):
        permission_required_name = f'{request.method.lower()}_permission_required'
        if not request.user.is_authenticated:
            return False
        if not hasattr(view, permission_required_name):
            return True

        permission_required = getattr(view, permission_required_name)
        if not request.user.has_perm(permission_required):
            self.message = f'Access denied. You need the {permission_required} permission to access this service with {request.method}.'
            return False

        return True
