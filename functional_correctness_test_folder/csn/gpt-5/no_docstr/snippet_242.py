class AWSIdentityCheck:
    def __init__(self, session=None, region_name=None, profile_name=None, connect_timeout=3, read_timeout=10, max_attempts=3):
        self._session = session
        self._region_name = region_name
        self._profile_name = profile_name
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._max_attempts = max_attempts

    def check(self):
        result = {
            "success": False,
            "identity": None,
            "error": None,
            "source": None,
        }

        try:
            import boto3
            from botocore.config import Config as _BotocoreConfig
            from botocore.exceptions import NoCredentialsError, NoRegionError, BotoCoreError, ClientError
        except Exception as e:
            result["error"] = f"boto3_not_available: {e}"
            return result

        try:
            session = self._session
            if session is None:
                if self._profile_name:
                    session = boto3.Session(
                        profile_name=self._profile_name, region_name=self._region_name)
                else:
                    session = boto3.Session(region_name=self._region_name)

            cfg = _BotocoreConfig(
                retries={"max_attempts": self._max_attempts,
                         "mode": "standard"},
                connect_timeout=self._connect_timeout,
                read_timeout=self._read_timeout,
            )

            sts = session.client(
                "sts", region_name=self._region_name or session.region_name, config=cfg)
            resp = sts.get_caller_identity()

            identity = {
                "Account": resp.get("Account"),
                "Arn": resp.get("Arn"),
                "UserId": resp.get("UserId"),
            }

            result.update({
                "success": True,
                "identity": identity,
                "source": "boto3",
                "error": None,
            })
            return result

        except NoCredentialsError:
            result["error"] = "no_credentials_found"
        except NoRegionError:
            result["error"] = "no_region_configured"
        except ClientError as e:
            code = getattr(e, "response", {}).get(
                "Error", {}).get("Code", "ClientError")
            msg = getattr(e, "response", {}).get(
                "Error", {}).get("Message", str(e))
            result["error"] = f"{code}: {msg}"
        except BotoCoreError as e:
            result["error"] = f"boto_core_error: {e}"
        except Exception as e:
            result["error"] = f"unexpected_error: {e}"

        return result
