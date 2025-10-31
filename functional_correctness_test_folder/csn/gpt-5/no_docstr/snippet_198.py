class RSA_PSS_Mechanism:
    def __init__(self, mecha, hashAlg, mgf, sLen):
        if not isinstance(mecha, int):
            raise TypeError("mecha must be int")
        if not isinstance(hashAlg, int):
            raise TypeError("hashAlg must be int")
        if not isinstance(mgf, int):
            raise TypeError("mgf must be int")
        if not isinstance(sLen, int):
            raise TypeError("sLen must be int")
        if sLen < 0:
            raise ValueError("sLen must be >= 0")

        self.mecha = mecha
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.sLen = sLen

        self._native_params = None  # keep reference alive if using ctypes

    def to_native(self):
        # Attempt PyKCS11 first
        try:
            import PyKCS11
            from PyKCS11.LowLevel import CK_MECHANISM, CK_RSA_PKCS_PSS_PARAMS

            params = CK_RSA_PKCS_PSS_PARAMS(self.hashAlg, self.mgf, self.sLen)
            mech = CK_MECHANISM(self.mecha, params)
            # Keep params alive with the object to avoid GC issues
            self._native_params = params
            return mech
        except Exception:
            # Fallback to ctypes representation
            from ctypes import Structure, c_ulong, c_void_p, sizeof, pointer, cast

            class CK_RSA_PKCS_PSS_PARAMS(Structure):
                _fields_ = [
                    ("hashAlg", c_ulong),
                    ("mgf", c_ulong),
                    ("sLen", c_ulong),
                ]

            class CK_MECHANISM(Structure):
                _fields_ = [
                    ("mechanism", c_ulong),
                    ("pParameter", c_void_p),
                    ("ulParameterLen", c_ulong),
                ]

            params = CK_RSA_PKCS_PSS_PARAMS(
                c_ulong(self.hashAlg),
                c_ulong(self.mgf),
                c_ulong(self.sLen),
            )
            # Keep params alive on the instance
            self._native_params = params

            mech = CK_MECHANISM()
            mech.mechanism = c_ulong(self.mecha)
            mech.pParameter = cast(pointer(self._native_params), c_void_p)
            mech.ulParameterLen = c_ulong(sizeof(self._native_params))
            return mech
