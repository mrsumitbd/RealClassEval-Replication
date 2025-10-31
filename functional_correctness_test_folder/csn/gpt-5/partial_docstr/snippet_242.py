import datetime
from typing import Any, Dict, Optional

import boto3
from botocore.credentials import ReadOnlyCredentials
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError, PartialCredentialsError


class AWSIdentityCheck:
    '''Just a Utility Script that allows people to check which AWS Identity is active'''

    def __init__(self):
        self.session = boto3.session.Session()
        self.profile_name: Optional[str] = getattr(
            self.session, "profile_name", None)
        self.region_name: Optional[str] = self.session.region_name
        self._sts = self.session.client("sts")

    def _mask(self, s: Optional[str], visible: int = 4) -> Optional[str]:
        if not s:
            return s
        if len(s) <= visible:
            return "*" * len(s)
        return "*" * (len(s) - visible) + s[-visible:]

    def _get_ro_credentials(self) -> Optional[ReadOnlyCredentials]:
        try:
            # type: ignore[attr-defined]
            creds = self.session._session.get_credentials()
            return creds.get_frozen_credentials() if creds else None
        except Exception:
            return None

    def _exp_iso(self, creds: Optional[ReadOnlyCredentials]) -> Optional[str]:
        # botocore ReadOnlyCredentials may include 'expiry_time' attribute on the parent credentials
        try:
            # access the non-frozen provider credentials for expiry when available
            # type: ignore[attr-defined]
            provider_creds = self.session._session.get_credentials()
            expiry = getattr(provider_creds, "expiry_time", None)
            if not expiry:
                return None
            if isinstance(expiry, (datetime.datetime, )):
                if expiry.tzinfo is None:
                    expiry = expiry.replace(tzinfo=datetime.timezone.utc)
                return expiry.astimezone(datetime.timezone.utc).isoformat()
            return str(expiry)
        except Exception:
            return None

    def check(self) -> Dict[str, Any]:
        '''Check the AWS Identity'''
        result: Dict[str, Any] = {
            "profile": self.profile_name,
            "region": self.region_name,
            "identity": None,
            "credentials": None,
        }

        creds = self._get_ro_credentials()
        if creds:
            # type: ignore[attr-defined]
            is_session = bool(
                getattr(self.session._session.get_credentials(), "token", None))
            result["credentials"] = {
                "access_key_id": self._mask(creds.access_key),
                "is_session": is_session,
                "has_token": is_session,
                "expiration": self._exp_iso(creds),
                # type: ignore[attr-defined]
                "source": getattr(self.session._session.get_credentials(), "method", None),
            }
        else:
            result["credentials"] = {
                "access_key_id": None,
                "is_session": None,
                "has_token": None,
                "expiration": None,
                "source": None,
            }

        try:
            resp = self._sts.get_caller_identity()
            result["identity"] = {
                "account": resp.get("Account"),
                "arn": resp.get("Arn"),
                "user_id": resp.get("UserId"),
            }
            result["ok"] = True
        except (NoCredentialsError, PartialCredentialsError) as e:
            result["ok"] = False
            result["error"] = "No AWS credentials found or incomplete credentials"
            result["error_detail"] = str(e)
        except ClientError as e:
            result["ok"] = False
            result["error"] = "AWS STS client error"
            result["error_detail"] = str(e)
        except BotoCoreError as e:
            result["ok"] = False
            result["error"] = "AWS SDK error"
            result["error_detail"] = str(e)
        except Exception as e:
            result["ok"] = False
            result["error"] = "Unexpected error"
            result["error_detail"] = str(e)

        return result
