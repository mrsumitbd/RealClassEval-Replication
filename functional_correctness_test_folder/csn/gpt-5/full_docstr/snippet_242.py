class AWSIdentityCheck:
    '''Just a Utility Script that allows people to check which AWS Identity is active'''

    def __init__(self):
        '''AWSIdentityCheck Initialization'''
        # Lazy import to avoid hard dependency at import time
        try:
            import boto3  # noqa: F401
            import botocore  # noqa: F401
        except Exception as e:
            raise RuntimeError(
                "boto3 and botocore are required to use AWSIdentityCheck") from e

        self._boto3 = boto3
        self._botocore = botocore

        # Capture environment hints
        import os
        self._env = {
            "AWS_PROFILE": os.environ.get("AWS_PROFILE"),
            "AWS_DEFAULT_REGION": os.environ.get("AWS_DEFAULT_REGION"),
            "AWS_REGION": os.environ.get("AWS_REGION"),
            "AWS_ROLE_ARN": os.environ.get("AWS_ROLE_ARN"),
            "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
        }

        # Create a session using the environment or default configuration
        profile = self._env["AWS_PROFILE"]
        try:
            if profile:
                self._session = self._boto3.Session(profile_name=profile)
            else:
                self._session = self._boto3.Session()
        except Exception as e:
            # If profile is set but invalid, surface a clear error
            raise RuntimeError(
                f"Failed to create boto3 session (profile={profile!r}): {e}") from e

    def _parse_arn(self, arn):
        # arn:partition:service:region:account-id:resource
        out = {
            "partition": None,
            "service": None,
            "region": None,
            "account": None,
            "resource": None,
            "principal_type": None,
            "principal_name": None,
        }
        try:
            parts = arn.split(":", 5)
            if len(parts) >= 6:
                _, partition, service, region, account, resource = parts
                out["partition"] = partition or None
                out["service"] = service or None
                out["region"] = region or None
                out["account"] = account or None
                out["resource"] = resource or None

                # resource often looks like: user/NAME or role/NAME or root
                res = resource or ""
                if res == "root":
                    out["principal_type"] = "root"
                    out["principal_name"] = "root"
                else:
                    segs = res.split("/", 1)
                    if segs:
                        out["principal_type"] = segs[0]
                        out["principal_name"] = segs[1] if len(
                            segs) > 1 else None
        except Exception:
            pass
        return out

    def _get_account_aliases(self):
        try:
            iam = self._session.client("iam")
            aliases = []
            marker = None
            while True:
                if marker:
                    resp = iam.list_account_aliases(Marker=marker)
                else:
                    resp = iam.list_account_aliases()
                aliases.extend(resp.get("AccountAliases", []))
                if resp.get("IsTruncated"):
                    marker = resp.get("Marker")
                else:
                    break
            return aliases
        except self._botocore.exceptions.ClientError as e:
            # Access denied or iam disabled is fine; return empty
            return []
        except Exception:
            return []

    def check(self):
        '''Check the AWS Identity'''
        sts = self._session.client("sts")
        region = (
            self._env["AWS_REGION"]
            or self._env["AWS_DEFAULT_REGION"]
            or self._session.region_name
        )

        # Determine credential source/method if possible
        cred_method = None
        try:
            creds = self._session.get_credentials()
            if creds is not None:
                # botocore credentials expose .method (e.g., env, shared-credentials-file, assume-role, sso, iam-role, container-role)
                cred_method = getattr(creds, "method", None)
        except Exception:
            pass

        result = {
            "ok": False,
            "error": None,
            "account": None,
            "arn": None,
            "user_id": None,
            "principal_type": None,
            "principal_name": None,
            "partition": None,
            "profile": self._env["AWS_PROFILE"] or self._session.profile_name,
            "region": region,
            "credential_method": cred_method,
            "account_aliases": [],
            "environment": {
                "AWS_PROFILE": self._env["AWS_PROFILE"],
                "AWS_REGION": self._env["AWS_REGION"],
                "AWS_DEFAULT_REGION": self._env["AWS_DEFAULT_REGION"],
                "AWS_ROLE_ARN": self._env["AWS_ROLE_ARN"],
                "AWS_ACCESS_KEY_ID_present": bool(self._env["AWS_ACCESS_KEY_ID"]),
            },
        }

        try:
            identity = sts.get_caller_identity()
            result["ok"] = True
            result["account"] = identity.get("Account")
            result["arn"] = identity.get("Arn")
            result["user_id"] = identity.get("UserId")

            arn_meta = self._parse_arn(result["arn"] or "")
            result["principal_type"] = arn_meta.get("principal_type")
            result["principal_name"] = arn_meta.get("principal_name")
            result["partition"] = arn_meta.get("partition")

            result["account_aliases"] = self._get_account_aliases()
            return result
        except self._botocore.exceptions.NoCredentialsError as e:
            result["error"] = "No AWS credentials found"
            return result
        except self._botocore.exceptions.ClientError as e:
            result["error"] = f"ClientError: {e.response.get('Error', {}).get('Code')}: {e.response.get('Error', {}).get('Message')}"
            return result
        except self._botocore.exceptions.BotoCoreError as e:
            result["error"] = f"BotoCoreError: {str(e)}"
            return result
        except Exception as e:
            result["error"] = f"UnexpectedError: {str(e)}"
            return result
