from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
	"""
    Anyone can read SAFE methods (GET) if snippet is NOT private
    Only the author can edit/delete (PUT, PATCH, DELETE).
    """
	def has_object_permission(self,request,view,obj):
		if request.method in permissions.SAFE_METHODS:
			if getattr(obj, 'is_private', False):
				return obj.author == request.user
			return True

		return obj.author == request.user
