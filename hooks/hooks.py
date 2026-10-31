"""
MkDocs 빌드 전 자동 동기화 훅(Hook).
- 저장소 내 단일 원본인 `notebooks/*.ipynb`와 `assets/imgs/*`를
  웹 문서 빌드 시점에 `docs/notebooks/` 및 `docs/assets/imgs/`로 자동 복사하여
  파일 중복 보관 없이 웹에서 모든 노트북과 데모 이미지를 렌더링합니다.
"""
import shutil
from pathlib import Path


def on_pre_build(config):
    project_root = Path(__file__).resolve().parent.parent
    docs_dir = project_root / "docs"

    # 1. notebooks/*.ipynb -> docs/notebooks/ 동기화
    src_nb_dir = project_root / "notebooks"
    dst_nb_dir = docs_dir / "notebooks"
    dst_nb_dir.mkdir(parents=True, exist_ok=True)
    if src_nb_dir.exists():
        for nb_file in src_nb_dir.glob("*.ipynb"):
            shutil.copy2(nb_file, dst_nb_dir / nb_file.name)

    # 2. assets/imgs/* -> docs/assets/imgs/ 동기화
    src_img_dir = project_root / "assets" / "imgs"
    dst_img_dir = docs_dir / "assets" / "imgs"
    if src_img_dir.exists():
        shutil.copytree(src_img_dir, dst_img_dir, dirs_exist_ok=True)

