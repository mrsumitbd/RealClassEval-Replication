class S2Image:

    def extend(self, source, new_image_name, s2i_args=None):
        import os
        import shutil
        import subprocess

        if not isinstance(source, str) or not source.strip():
            raise ValueError(
                "source must be a non-empty string (local path or git URL)")
        if not isinstance(new_image_name, str) or not new_image_name.strip():
            raise ValueError("new_image_name must be a non-empty string")
        s2i_args = s2i_args or {}

        s2i_bin = shutil.which("s2i") or shutil.which("source-to-image")
        if not s2i_bin:
            raise FileNotFoundError("s2i binary not found in PATH")

        builder_image = s2i_args.get(
            "builder_image") or os.getenv("S2I_BUILDER_IMAGE")
        if not builder_image:
            raise ValueError(
                "builder_image is required in s2i_args or via S2I_BUILDER_IMAGE env var")

        cmd = [s2i_bin, "build", source, builder_image, new_image_name]

        # Optional flags
        if s2i_args.get("incremental") is True:
            cmd.append("--incremental")
        if s2i_args.get("rm") is True:
            cmd.append("--rm")
        if s2i_args.get("loglevel") is not None:
            cmd.extend(["--loglevel", str(s2i_args["loglevel"])])
        if s2i_args.get("scripts_url"):
            cmd.extend(["--scripts-url", str(s2i_args["scripts_url"])])
        if s2i_args.get("ref"):
            cmd.extend(["--ref", str(s2i_args["ref"])])
        if s2i_args.get("context_dir"):
            cmd.extend(["--context-dir", str(s2i_args["context_dir"])])
        if s2i_args.get("image_workdir"):
            cmd.extend(["--image-workdir", str(s2i_args["image_workdir"])])
        if s2i_args.get("assemble_user"):
            cmd.extend(["--assemble-user", str(s2i_args["assemble_user"])])

        # Environment variables passed to the build image
        env_vars = s2i_args.get("env") or {}
        for k, v in env_vars.items():
            if k is None:
                continue
            v = "" if v is None else str(v)
            cmd.extend(["--env", f"{k}={v}"])

        # Labels
        labels = s2i_args.get("labels") or {}
        for k, v in labels.items():
            if k is None:
                continue
            v = "" if v is None else str(v)
            cmd.extend(["--label", f"{k}={v}"])

        # Inject files (path on host:destination in image)
        inject = s2i_args.get("inject") or []
        for spec in inject:
            cmd.extend(["--inject", str(spec)])

        # Additional arbitrary CLI tokens
        additional = s2i_args.get("additional_args") or []
        cmd.extend(map(str, additional))

        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            msg = []
            msg.append("s2i build failed")
            msg.append(f"Command: {' '.join(cmd)}")
            if e.stdout:
                msg.append(f"stdout:\n{e.stdout}")
            if e.stderr:
                msg.append(f"stderr:\n{e.stderr}")
            raise RuntimeError("\n".join(msg)) from e

        return {
            "image": new_image_name,
            "cmd": cmd,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode,
        }

    def usage(self):
        return (
            "S2Image.extend(source, new_image_name, s2i_args=None)\n"
            "- Builds a new container image using Source-to-Image (s2i).\n"
            "- Parameters:\n"
            "  source: Path or Git URL of the source code.\n"
            "  new_image_name: Name:tag for the resulting image.\n"
            "  s2i_args: Optional dict with keys:\n"
            "    builder_image (str, required if S2I_BUILDER_IMAGE env not set)\n"
            "    incremental (bool)\n"
            "    rm (bool)\n"
            "    loglevel (int)\n"
            "    scripts_url (str)\n"
            "    ref (str)  # git ref\n"
            "    context_dir (str)\n"
            "    image_workdir (str)\n"
            "    assemble_user (str)\n"
            "    env (dict[str, str])  # passed as --env KEY=VAL\n"
            "    labels (dict[str, str])  # passed as --label KEY=VAL\n"
            "    inject (list[str])  # items like hostPath:destination\n"
            "    additional_args (list[str])  # extra s2i CLI tokens\n"
            "Returns a dict with keys: image, cmd, stdout, stderr, returncode."
        )
