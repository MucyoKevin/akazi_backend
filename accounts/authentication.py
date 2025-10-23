from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class BearerTokenAuthentication(TokenAuthentication):
    """
    Custom authentication class that supports both 'Token' and 'Bearer' prefixes
    """
    keyword = 'Bearer'
    
    def authenticate_credentials(self, key):
        """
        Override to support both Token and Bearer keywords
        """
        try:
            # Try with Bearer keyword first
            return super().authenticate_credentials(key)
        except AuthenticationFailed:
            # If Bearer fails, try with Token keyword
            original_keyword = self.keyword
            self.keyword = 'Token'
            try:
                result = super().authenticate_credentials(key)
                return result
            finally:
                # Restore original keyword
                self.keyword = original_keyword



