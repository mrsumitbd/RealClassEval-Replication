from django.conf import settings
from webauthn.helpers.structs import PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity
from hashlib import sha1

class DefaultWebauthnEntitiesFormMixin:
    """
    Mixin to build WebAuthn entities from HttpRequest instances
    """

    @property
    def webauthn_user(self):
        user = self.request.user
        return PublicKeyCredentialUserEntity(id=sha1(str(user.pk).encode('utf-8')).hexdigest().encode('utf-8'), name=user.get_username(), display_name=user.get_full_name() or user.get_username())

    @property
    def webauthn_rp(self):
        rp_id = settings.TWO_FACTOR_WEBAUTHN_RP_ID or self.request.get_host().split(':')[0]
        return PublicKeyCredentialRpEntity(id=rp_id, name=settings.TWO_FACTOR_WEBAUTHN_RP_NAME)

    @property
    def webauthn_origin(self):
        scheme = 'https' if self.request.is_secure() else 'http'
        return '{scheme}://{host}'.format(scheme=scheme, host=self.request.get_host())