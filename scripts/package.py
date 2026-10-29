#!/usr/bin/env python3
"""生成可重复构建的 .skill 安装包和附使用说明的 .zip 包，仅依赖 Python 标准库。"""

from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "repo-docs"
DIST = ROOT / "dist"
EXCLUDED = {".DS_Store", "__pycache__", "node_modules"}


def build_archive(destination: Path, files: list[Path]) -> None:
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            info = ZipInfo(path.relative_to(ROOT).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

    payload = buffer.getvalue()
    with ZipFile(BytesIO(payload)) as archive:
        damaged = archive.testzip()
        if damaged:
            raise RuntimeError(f"安装包校验失败: {damaged}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists() or destination.read_bytes() != payload:
        destination.write_bytes(payload)
    print(f"{destination.relative_to(ROOT)}: {len(payload)} bytes")


def main() -> None:
    if not (SKILL / "SKILL.md").is_file():
        raise SystemExit("未找到 repo-docs/SKILL.md")

    files = sorted(
        path
        for path in SKILL.rglob("*")
        if path.is_file()
        and not EXCLUDED.intersection(path.relative_to(SKILL).parts)
        and path.suffix not in {".pyc", ".pyo"}
    )
    build_archive(DIST / "repo-docs.skill", files)
    build_archive(DIST / "repo-docs.zip", [ROOT / "README.md", *files])


if __name__ == "__main__":
    main()
